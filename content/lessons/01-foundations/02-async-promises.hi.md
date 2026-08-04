---
title: "Promises, Async/Await Aur Event Loop Hinglish Guide"
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

# Promises & Async/Await Hinglish Masterclass

JavaScript **single-threaded** language hai, matlab ek time pe ek hi line of code execute hota hai. Jab hum API call ya heavy task karte hain, toh browser block na ho uske liye hum **Promises** aur **Async/Await** use karte hain.

::concept-callout{type="hinglish" title="Promise Ki 3 States Samjho"}
Promise ek real-world waade ki tarah hai:
1. **Pending**: Waada chal raha hai (Result abhi aana baki hai).
2. **Fulfilled**: Waada pura ho gaya! (`resolve()` call hua).
3. **Rejected**: Waada toot gaya! (`reject()` error ke sath call hua).
::

### Async/Await Ka Easy Pattern

Old `.then()` aur `.catch()` se better pattern hai Modern `async/await`:

```js
async function getUserData() {
  try {
    const user = await fetchUserData(1); // Wait karega resolve hone tak
    console.log("Success: User mil gaya -", user.name);
  } catch (err) {
    console.error("Error aa gaya:", err);
  }
}
```

::js-playground{title="Live Hinglish Async Simulator"}
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function startWork() {
  console.log("Processing Data Start hua...");
  await delay(1000);
  console.log("1 Second ke baad Response aaya!");
  return "Sab badhiya hai!";
}

startWork();
::

### Interactive Quiz

::practice-quiz{question="Microtask Queue (Promises) aur Macrotask Queue (setTimeout) me se kiska priority Event Loop me pehle hota hai?" options='["Microtask Queue (Promises) ka priority pehle hota hai","Macrotask Queue (setTimeout) pehle run hota hai","Dono randomly execute hote hain","Browser decide karta hai background me"]' answer=0 explanation="Event Loop Call Stack khali hote hi pehle saare Microtasks (Promises) ko finish karta hai, uske baad hi Macrotasks (setTimeout) execute hote hain!"}
::
