---
title: "Understanding Closures & Lexical Scope"
module: "01-foundations"
lesson: "01-closures"
duration: 15
xp: 50
starterCode: |
  function createCounter() {
    let count = 0;
    return function() {
      count++;
      return count;
    };
  }

  const counter = createCounter();
  console.log(counter()); // Expected: 1
  console.log(counter()); // Expected: 2
testSpecs:
  - id: "test-1"
    name: "createCounter returns a function that increments count"
    code: |
      const c = createCounter();
      if (c() !== 1) throw new Error("First invocation must return 1");
      if (c() !== 2) throw new Error("Second invocation must return 2");
  - id: "test-2"
    name: "Multiple counter instances maintain independent state"
    code: |
      const c1 = createCounter();
      const c2 = createCounter();
      c1(); c1();
      if (c1() !== 3) throw new Error("Counter 1 should be 3");
      if (c2() !== 1) throw new Error("Counter 2 state was mutated!");
---

# Closures & Lexical Scope

A **Closure** is one of the most powerful and fundamental concepts in JavaScript. A closure is created when an inner function retains access to its parent lexical scope, even after the parent function has finished executing.

::concept-callout{type="info" title="Definition"}
In JavaScript, functions enclose their surrounding lexical environment. This means inner functions remember the variables defined in their outer function's scope.
::

### Practical Example

Consider the following counter function:

```js
function createCounter() {
  let count = 0; // Private scope variable
  return function increment() {
    count += 1;
    return count;
  };
}

const myCounter = createCounter();
console.log(myCounter()); // Output: 1
console.log(myCounter()); // Output: 2
```

Notice how `count` is preserved across multiple calls to `myCounter()`!

::js-playground{title="Try It Yourself: Interactive Closure"}
function createGreeting(salutation) {
  return function(name) {
    console.log(salutation + ", " + name + "!");
  };
}

const sayHello = createGreeting("Hello");
sayHello("Developer");
sayHello("ScriptCraft Student");
::

### Interactive Quiz

::practice-quiz{question="What will be the output of calling a closure function that accesses an outer variable modified after function creation?" options='["It reads the updated variable value","It throws a ReferenceError","It uses the initial value at function creation","It returns undefined"]' answer=0 explanation="Functions retain a live reference to outer variables, not a static copy. Any mutation to the variable in the outer scope is reflected when the closure is executed."}
::
