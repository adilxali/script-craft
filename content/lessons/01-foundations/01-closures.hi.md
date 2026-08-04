---
title: "Closures Aur Lexical Scope Ki Detail Guide"
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

# Closures Aur Lexical Scope

**Closure** JavaScript ka ek bohot hi powerful concept hai. Simply put, **Closure ek aisa inner function hota hai jo apne parent function ke scope aur variables ko access kar sakta hai**, even after the outer function execution full complete ho chuki ho.

::concept-callout{type="hinglish" title="Hinglish Rule of Closure"}
Jab bhi koi function Dusre function ke andar return hota hai, woh apne sath parent scope ki ek "backpack" leke aata hai. Is backpack ko hum **Lexical Scope** ya Closure kehte hain!
::

### Real World Code Example

Niche diye gaye example ko dhyan se dekho:

```js
function createCounter() {
  let count = 0; // Outer private variable

  return function increment() {
    count += 1; // Parent scope variable ko access aur update kar raha hai
    return count;
  };
}

const myCounter = createCounter();
console.log(myCounter()); // Output: 1
console.log(myCounter()); // Output: 2
```

Dhyan do: `createCounter()` run ho ke return kar chuka hai, par `count` variable memory me destroy nahi hua kyunki `increment` function ke pas `count` ka live reference (Closure) maujood hai!

::js-playground{title="Apna Code Run Karo: Live Closure Playground"}
function createGreeting(greetingMessage) {
  return function(name) {
    console.log(greetingMessage + ", " + name + "! Kaise ho?");
  };
}

const sayNamaste = createGreeting("Namaste");
sayNamaste("Adil");
sayNamaste("JavaScript Developer");
::

### Quick Hinglish Quiz

::practice-quiz{question="Agar parent function execution khatam ho jaye, toh kya inner closure function outer variable ki new value access kar sakta hai?" options='["Haan, closure me variable ka live reference hota hai","Nahi, closure snapshot value copy karta hai","Error aayega ReferenceError naam se","Undefined return hoga"]' answer=0 explanation="Closure outer variables ka live memory reference retain karta hai! Toh jab bhi outer variable change hoga, inner function uski latest updated value dekhega."}
::
