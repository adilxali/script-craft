---
title: "Prototype Chain Aur Inheritance Ki Hinglish Guide"
module: "02-prototypes"
lesson: "01-prototype-chain"
duration: 20
xp: 60
starterCode: |
  function Person(name) {
    this.name = name;
  }

  Person.prototype.greet = function() {
    return "Hello, I am " + this.name;
  };

  const dev = new Person("Adil");
  console.log(dev.greet());
testSpecs:
  - id: "test-proto-1"
    name: "Person.prototype defines greet method shared across instances"
    code: |
      const p = new Person("Test");
      if (typeof p.greet !== 'function') throw new Error("greet method missing");
      if (p.greet() !== "Hello, I am Test") throw new Error("Incorrect greeting text");
---

# Prototype Chain Aur Inheritance

JavaScript traditional Class-based languages (jaise Java ya C++) se alag hai. Yahan **Prototypal Inheritance** kaam karta hai. Har object ka ek internal reference hota hai apne **Prototype** object ka.

::concept-callout{type="hinglish" title="Prototype Chain Ka Rule"}
Jab bhi aap kisi object par property access karte ho (e.g. `obj.name`), JavaScript sabse pehle dekhta hai ki kya woh property object par khud maujood hai. Agar nahi, toh woh uske prototype chain me upar search karta hai tab tak jab tak `null` nahi mil jata!
::

### Prototypal Inheritance Code Example

```js
const parentObj = {
  surname: "Sharma",
  sayHello() {
    console.log("Namaste!");
  }
};

const childObj = Object.create(parentObj);
childObj.name = "Rahul";

console.log(childObj.name);    // "Rahul" (khud ka property)
console.log(childObj.surname); // "Sharma" (parent prototype se inherit hua)
```

::js-playground{title="Live Hinglish Prototype Sandbox"}
const vehicle = { wheels: 4, drive() { return "Vroom!"; } };
const car = Object.create(vehicle);
car.brand = "Tesla";

console.log("Car Brand:", car.brand);
console.log("Inherited Wheels:", car.wheels);
console.log("Drive Sound:", car.drive());
::

### Quick Quiz

::practice-quiz{question="JavaScript prototype chain ke sabse top root level par kaun sa object hota hai jiska prototype null hota hai?" options='["Object.prototype","Array.prototype","Function.prototype","String.prototype"]' answer=0 explanation="Object.prototype sabse top root level par hota hai. Iske aage Object.prototype.__proto__ null hota hai, jo prototype chain ka end mark karta hai."}
::
