---
title: "Prototype Chain & Prototypal Inheritance"
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

# Prototype Chain & Inheritance

In JavaScript, objects inherit properties and methods directly from other objects through the **Prototype Chain**. Unlike class-based languages (like Java or C++), JavaScript uses **Prototypal Inheritance**.

::concept-callout{type="info" title="The __proto__ Property"}
Every object in JavaScript has an internal link to another object called its prototype (`[[Prototype]]` or `__proto__`). When accessing a property, JS walks up this chain until it finds the property or hits `null`.
::

### Prototypal Delegation Example

```js
const animal = {
  eats: true,
  walk() {
    console.log("Animal walking...");
  }
};

const rabbit = Object.create(animal);
rabbit.jumps = true;

console.log(rabbit.jumps); // true (own property)
console.log(rabbit.eats);  // true (inherited from animal prototype)
```

::js-playground{title="Interactive Prototype Playground"}
const parent = { familyName: "Developer" };
const child = Object.create(parent);
child.firstName = "ScriptCraft";

console.log(child.firstName + " " + child.familyName);
console.log("Is parent prototype?", Object.getPrototypeOf(child) === parent);
::

### Concept Quiz

::practice-quiz{question="What is at the top of the JavaScript Prototype Chain?" options='["Object.prototype (whose prototype is null)","Function.prototype","Array.prototype","Undefined"]' answer=0 explanation="Object.prototype sits at the root of the prototype chain. Object.prototype.__proto__ is null, marking the end of lookup."}
::
