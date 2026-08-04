---
title: "Async JavaScript, Promises & Event Loop"
module: "01-foundations"
lesson: "02-async-promises"
duration: 20
xp: 60
starterCode: |
  function fetchUserData(userId) {
    return new Promise((resolve, reject) => {
      if (userId > 0) {
        resolve({ id: userId, name: "Alice Developer", status: "Active" });
      } else {
        reject("Invalid User ID");
      }
    });
  }

  fetchUserData(1)
    .then(user => console.log("User fetched:", user.name))
    .catch(err => console.error(err));
testSpecs:
  - id: "test-promise-1"
    name: "fetchUserData resolves valid user object for positive ID"
    code: |
      const res = await fetchUserData(5);
      if (!res || res.name !== "Alice Developer") throw new Error("Expected valid user object");
  - id: "test-promise-2"
    name: "fetchUserData rejects for non-positive ID"
    code: |
      try {
        await fetchUserData(0);
        throw new Error("Should have rejected!");
      } catch (err) {
        if (err === "Should have rejected!") throw err;
      }
---

# Promises & Asynchronous Execution

JavaScript is a single-threaded language. To execute long-running operations like network requests or database queries without blocking the UI, JavaScript relies on **Promises** and the **Event Loop**.

::concept-callout{type="tip" title="Promise States"}
A Promise represents an eventual completion (or failure) of an asynchronous operation. It exists in one of three states:
1. **Pending**: Initial state, neither fulfilled nor rejected.
2. **Fulfilled**: Operation completed successfully.
3. **Rejected**: Operation failed with an error.
::

### Async/Await Syntax

The modern way to handle promises is using `async` and `await`:

```js
async function getUser() {
  try {
    const user = await fetchUserData(1);
    console.log("Found user:", user.name);
  } catch (error) {
    console.error("Fetch failed:", error);
  }
}
```

::js-playground{title="Interactive Promise Simulator"}
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runTask() {
  console.log("Task Started...");
  await delay(1000);
  console.log("Task Finished after 1000ms!");
  return "DONE";
}

runTask();
::

### Concept Quiz

::practice-quiz{question="Which mechanism in JavaScript processes microtasks like Promise callbacks before microtasks?" options='["The Event Loop Microtask Queue","The Main Call Stack Synchronous Execution","Web Worker Thread","SetTimeout Timer API"]' answer=0 explanation="Promise resolution callbacks (.then/async await) are queued in the Microtask Queue, which takes priority over standard Macrotasks (like setTimeout)." }
::
