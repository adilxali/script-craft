export interface LogEntry {
  id: string
  level: 'log' | 'warn' | 'error' | 'info'
  args: any[]
  timestamp: string
}

export interface TestSpec {
  id: string
  name: string
  code: string // JavaScript assertion block e.g. "assert(createCounter()(1) === 1)"
}

export interface TestResult {
  id: string
  name: string
  passed: boolean
  error?: string
}

export interface ExecutionResult {
  logs: LogEntry[]
  returnValue: any
  runtimeMs: number
  tests: TestResult[]
  error?: string
}

export function executeJSCode(
  userCode: string,
  testSpecs: TestSpec[] = [],
  timeoutMs: number = 3000
): Promise<ExecutionResult> {
  return new Promise((resolve) => {
    const logs: LogEntry[] = []
    const tests: TestResult[] = []
    const startTime = performance.now()

    // Inline worker script template
    const workerScript = `
      self.onmessage = async function(e) {
        const { userCode, testSpecs } = e.data;
        const logs = [];

        function formatArg(arg) {
          if (typeof arg === 'undefined') return 'undefined';
          if (arg === null) return 'null';
          if (typeof arg === 'function') return arg.toString();
          if (typeof arg === 'object') {
            try {
              return JSON.stringify(arg, null, 2);
            } catch (err) {
              return String(arg);
            }
          }
          return String(arg);
        }

        // Intercept console
        const originalConsole = {
          log: console.log,
          warn: console.warn,
          error: console.error,
          info: console.info
        };

        ['log', 'warn', 'error', 'info'].forEach(level => {
          console[level] = (...args) => {
            const formatted = args.map(formatArg);
            logs.push({
              level,
              args: formatted,
              timestamp: new Date().toLocaleTimeString()
            });
            self.postMessage({ type: 'log', entry: logs[logs.length - 1] });
          };
        });

        let returnValue;
        let execError = null;

        try {
          // Execute user code
          const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
          const userFn = new AsyncFunction(userCode);
          returnValue = await userFn();
        } catch (err) {
          execError = err.message || String(err);
          console.error(execError);
        }

        // Execute test specs if user code executed without fatal syntax error
        const testResults = [];
        if (testSpecs && testSpecs.length > 0) {
          for (const spec of testSpecs) {
            try {
              // Wrap spec code along with userCode in execution context
              const testFn = new AsyncFunction(userCode + '\\n\\n' + spec.code);
              await testFn();
              testResults.push({ id: spec.id, name: spec.name, passed: true });
            } catch (testErr) {
              testResults.push({
                id: spec.id,
                name: spec.name,
                passed: false,
                error: testErr.message || String(testErr)
              });
            }
          }
        }

        self.postMessage({
          type: 'complete',
          returnValue: formatArg(returnValue),
          logs,
          tests: testResults,
          error: execError
        });
      };
    `

    const blob = new Blob([workerScript], { type: 'application/javascript' })
    const workerUrl = URL.createObjectURL(blob)
    const worker = new Worker(workerUrl)

    let isCompleted = false

    const timer = setTimeout(() => {
      if (!isCompleted) {
        isCompleted = true
        worker.terminate()
        URL.revokeObjectURL(workerUrl)
        const endTime = performance.now()
        resolve({
          logs: [
            ...logs,
            {
              id: Math.random().toString(36).substr(2, 9),
              level: 'error',
              args: ['Execution timed out (Limit: 3000ms). Check for infinite loops!'],
              timestamp: new Date().toLocaleTimeString()
            }
          ],
          returnValue: undefined,
          runtimeMs: Math.round(endTime - startTime),
          tests: testSpecs.map((t) => ({
            id: t.id,
            name: t.name,
            passed: false,
            error: 'Timeout exceeded'
          })),
          error: 'Execution Timed Out'
        })
      }
    }, timeoutMs)

    worker.onmessage = (e) => {
      const { type, entry, returnValue, tests: workerTests, error } = e.data

      if (type === 'log') {
        logs.push({
          ...entry,
          id: Math.random().toString(36).substr(2, 9)
        })
      } else if (type === 'complete') {
        if (!isCompleted) {
          isCompleted = true
          clearTimeout(timer)
          worker.terminate()
          URL.revokeObjectURL(workerUrl)
          const endTime = performance.now()
          resolve({
            logs,
            returnValue,
            runtimeMs: Math.round(endTime - startTime),
            tests: workerTests || [],
            error: error || undefined
          })
        }
      }
    }

    worker.onerror = (err) => {
      if (!isCompleted) {
        isCompleted = true
        clearTimeout(timer)
        worker.terminate()
        URL.revokeObjectURL(workerUrl)
        const endTime = performance.now()
        resolve({
          logs: [
            ...logs,
            {
              id: Math.random().toString(36).substr(2, 9),
              level: 'error',
              args: [err.message || 'Worker Script Error'],
              timestamp: new Date().toLocaleTimeString()
            }
          ],
          returnValue: undefined,
          runtimeMs: Math.round(endTime - startTime),
          tests: [],
          error: err.message
        })
      }
    }

    worker.postMessage({ userCode, testSpecs })
  })
}
