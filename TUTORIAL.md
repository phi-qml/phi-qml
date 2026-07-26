# Φ‑QML Tutorial

Welcome to Φ‑QML, a quantum programming language built around the
holographic nature of the Φ field. This tutorial will guide you through
the basics — from your first program to quantum circuits and holographic
memory.

## Getting Started

Install Φ‑QML using pip:

```
pip install phi-qml
```

Create a file named `hello.phi` with the following content:

```phi
fn main() {
    println("Hello, Substrate*!");
}
```

Run it from the command line:

```
phi run hello.phi
```

You should see the greeting printed to the console. The main function
is the entry point of every Φ‑QML program.

Variables and Arithmetic

Variables are declared with let. You can optionally specify a type
after a colon. Arithmetic works as you would expect.

```phi
fn main() {
    let x = 42;
    let y: Int = 7;
    let sum = x + y;
    let product = x * y;
    let quotient = x / y;
    println("Sum: " + sum);
    println("Product: " + product);
    println("Quotient: " + quotient);
}
```

Use let mut for variables that you intend to change later.

```phi
fn main() {
    let mut counter = 0;
    counter = counter + 1;
    counter += 1;  // shorthand
    println("Counter: " + counter);
}
```

Substrate* Modulo

The heart of Φ‑QML is Substrate* Modulo. It computes the remainder of a
division instantly — with zero computational cost.

```phi
fn main() {
    let a = 2^256 + 123456789;
    let n = 997;
    let r = mod(a, n);
    println("mod(2^256 + 123456789, 997) = " + r);
}
```

The result is not calculated; it is revealed by collapsing the holographic
field at the address (a, n). This is why it has Φ = ∞.

Functions

Define functions with fn. Parameters need type annotations. The return
type goes after an arrow.

```phi
fn add(a: Int, b: Int) -> Int {
    return a + b;
}

fn main() {
    let result = add(5, 3);
    println("5 + 3 = " + result);
}
```

The last expression in a function body is implicitly returned, so you
can omit return:

```phi
fn add(a: Int, b: Int) -> Int {
    a + b
}
```

Conditionals

Use if and else for branching.

```phi
fn main() {
    let temperature = 25;
    if temperature > 30 {
        println("It's hot outside.");
    } else if temperature > 20 {
        println("It's pleasant outside.");
    } else {
        println("It's cold outside.");
    }
}
```

For a more elegant conditional, use when. It evaluates both branches
and picks the one with the higher Φ score.

```phi
fn main() {
    let x = 42;
    let y = 13;
    let result = when x > y {
        x - y,  // more elegant (fewer operations)
        y - x   // less elegant
    };
    println("Result: " + result);
}
```

Loops

Use while for classical loops.

```phi
fn main() {
    let mut i = 0;
    while i < 5 {
        println("i = " + i);
        i = i + 1;
    }
}
```

For quantum‑elegant loops, use until convergence. It repeats while
the Φ score of the body increases, and stops when it no longer does.

```phi
fn main() {
    let mut x = 16.0;
    until convergence {
        x = x / 2.0;
    }
    println("x converged to " + x);
}
```

Arrays

Create arrays with square brackets and access elements by index.

```phi
fn main() {
    let numbers = [10, 20, 30, 40, 50];
    let first = numbers[0];
    let third = numbers[2];
    println("First: " + first);
    println("Third: " + third);
}
```

Quantum Circuits

Φ‑QML can work with qubits directly. Create a qubit, apply gates, and
measure.

```phi
fn main() {
    let q: qubit = |0>;
    let h = H(q);
    let result = measure(h);
    println("Measured: " + result);
}
```

Create an entangled pair with CNOT.

```phi
fn main() {
    let q0: qubit = |0>;
    let q1: qubit = |0>;
    let h = H(q0);
    let (eq0, eq1) = CNOT(h, q1);
    let m0 = measure(eq0);
    let m1 = measure(eq1);
    println("Qubit 0: " + m0);
    println("Qubit 1: " + m1);
}
```

Holographic Memory

Use a holographic field for O(1) memory storage. Write, read, and
define lazy projections between addresses.

```phi
fn main() {
    let f: field<256> = init_field();

    f.write(42, 100);
    println("Address 42: " + f.read(42));

    f.project(43, 42, fn(x) { x * 2 });
    println("Address 43: " + f.read(43));

    f.write(42, 200);
    println("Address 43 after update: " + f.read(43));
}
```

When you update the source address, all projections that depend on it
are automatically recomputed.

Measuring Elegance

Every expression in Φ‑QML has a Φ score. Use phi_score to measure it.

```phi
fn main() {
    let s1 = phi_score(5 + 3, 1);
    println("Φ of addition: " + s1);

    let s2 = phi_score(mod(42, 13), 0);
    println("Φ of Substrate* Modulo: " + s2);
}
```

The linter will warn you when your code could be more elegant. Listen
to it — it is guiding you toward Substrate*.

Next Steps

Read the full specification in SPECIFICATION.md. Explore the example
programs in the examples/ directory. Run the tests with phi test.
And remember: every line of code you write should strive for Φ = ∞.

Φ.
