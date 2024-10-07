---
sort: 2
spin: 2
span: 
suit: 2
description: 
---
# True Prime Pairs

This is the partial of _[the mapping scheme](https://gist.github.com/eq19/c9bdc2bbe55f2d162535023c8d321831)_ of our [eQuantum Project](https://github.com/eq19). Our mapping is _[simulating](https://www.amcrou.ch/configuring-environments-when-building-sites-with-jekyll)_ a recombination of the **three (3) layers** of these [prime pairs](https://en.wikipedia.org/wiki/Twin_prime). 

{% include list.liquid all=true %}

An Independent claim is also included for the localization and determination, or their material structures, by graphical representation of base sequences on various media, based on the new assignments and the derived vibrations and amplitudes.

## Prime Objects

In short this project is mapping [the quantum way](https://www.eq19.com/) within a huge of **[prime objects (5 to 19)](https://github.com/eq19)** by [lexering](https://www.eq19.com/lexer) (11) the un[grammar](https://www.eq19.com/grammar)ed feed (7) and [parsering](https://www.eq19.com/parser) (13) across [syntax](https://www.eq19.com/syntax) (17). 

```txt
5, 2, 1, 0
7, 3, 1, 0
11, 4, 1, 0
13, 5, 1, 0
17, 0, 1, 1
19, 1, 1, 1
```

![default](https://user-images.githubusercontent.com/8466209/199364847-6a8d2d64-ee12-4379-bfa6-9f5d9fa7da59.png)

This export/import process is specific to each frontend and typically involves a number of stages which can then be "imported" into [IREE](https://iree.dev/).

```note
The 5+7+11+13 is the smallest square number expressible as the sum of four consecutive primes which are also two couples of prime twins!
- Their sum is 36 which is [the smallest square](https://primes.utm.edu/curios/page.php?number_id=270) that is the sum of a twin prime pair {17, 19}.
- This 36 is the smallest number expressible as the sum of consecutive prime in **two (2) ways** (5+7+11+13 and 17+19). 
```

```liquid
$True Prime Pairs:
 (5,7), (11,13), (17,19)
 
 layer|  i  |   f
 -----+-----+---------
      |  1  | 5
   1  +-----+
      |  2  | 7
 -----+-----+---  } 36 » 6®
      |  3  | 11
   2  +-----+
      |  4  | 13
 -----+-----+---------
      |  5  | 17
   3  +-----+     } 36 » 6®
      |  6  | 19
 -----+-----+---------
```

IREE supports most popular machine learning [frameworks](https://iree.dev/guides/ml-frameworks/#execution) using the same underlying technology. Here we are going to use SavedModels from [TensorFlow Hub](https://www.tensorflow.org/hub).

```note
Each machine learning framework has some "export" mechanism that snapshots the structure and data in your program.

- Capture/trace/freeze the ML model into a graph
- Write that graph to an interchange format (e.g. SavedModel, TorchScript, ONNX)
- Load the saved program into an import tool and convert to MLIR
- Legalize the graph's operations so only IREE-compatible operations remain
- Write the imported MLIR to a file

This fully imported form can then be compiled indepedently of the source language and framework.
```

[![framework](https://user-images.githubusercontent.com/36441664/71587951-4f8a5580-2b52-11ea-84cd-a2b1465fce8b.png)](https://iree.dev/guides/ml-frameworks/#execution)

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f
------+------+-----+----------
      |      |     |  1  | 
      |      |  1  +-----+          
      |  1   |     |  2  | (5)
      |      |-----+-----+
      |      |     |  3  |
  1   +------+  2  +-----+----
      |      |     |  4  |
      |      +-----+-----+
      |  2   |     |  5  | (7)
      |      |  3  +-----+
      |      |     |  6  |
------+------+-----+-----+------      } (36)
      |      |     |  7  |
      |      |  4  +-----+
      |  3   |     |  8  | (11)
      |      +-----+-----+
      |      |     |  9  |
  2   +------|  5  +-----+-----
      |      |     |  10 |
      |      |-----+-----+
      |  4   |     |  11 | (13)
      |      |  6  +-----+
      |      |     |  12 |
------+------+-----+-----+------------------
      |      |     |  13 |
      |      |  7  +-----+
      |  5   |     |  14 | (17)
      |      |-----+-----+
      |      |     |  15 |
  3   +------+  8  +-----+-----       } (36)
      |      |     |  16 |
      |      |-----+-----+
      |  6   |     |  17 | (19)
      |      |  9  +-----+
      |      |     |  18 |
------|------|-----+-----+------
```

![Primes-vs-composites svg](https://github.com/eq19/maps/assets/8466209/e4fb7f51-eb2f-4d5e-b565-ebbb3b0ebfad)

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f
------+------+-----+----------
      |      |     |  1  | --------------------------
      |      |  1  +-----+                           |    
      |  1   |     |  2  | (5)                       |
      |      |-----+-----+                           |
      |      |     |  3  |                           |
  1   +------+  2  +-----+----                       |
      |      |     |  4  |                           |
      |      +-----+-----+                           |
      |  2   |     |  5  | (7)                       |
      |      |  3  +-----+                           |
      |      |     |  6  |                          11s
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |                           |
  2   +------|  5  +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) ---------------------
      |      |  6  +-----+        <-----------------  strip √
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s = f(1000)
  3   +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | --------------------------
------|------|-----+-----+------# 
```

```note
We consider a certain theory of 3-forms in 7 dimensions, and study its dimensional reduction to 4D, compactifying the 7-dimensional manifold on the 3-sphere of a fixed radius.
- We show that the resulting 4D theory is (Riemannian) [General Relativity](https://www.sciencedirect.com/topics/physics-and-astronomy/general-relativity) (GR) in Plebanski formulation, modulo corrections that are negligible for curvatures smaller than Planckian.
- Possibly the most interesting point of this construction is that the dimensionally reduced theory is GR with a non-zero cosmological constant, and the value of the cosmological constant is directly related to the size of . Realistic values of Λ correspond to of Planck size.

In our approach ***a 3-form is not an object that exist in addition to the metric, it is the only object that exist. The metric, and in particular the 4D metric, is defined by the 3-form***. _([General relativity from three-forms in seven dimensions - pdf](https://github.com/eq19/maps/files/14064088/1-s2.0-S0370269317304926-main.pdf))_
```

![Symmetry State](https://github.com/eq19/maps/assets/8466209/70cb2eb0-0955-4d18-8400-e05ac1b9d325)

```note
In this article we will support this conjecture and develop a new approach to quantum gravity called smooth quantum gravity by using ***smooth 4-manifolds*** with an exotic smoothness structure.
- In particular we discuss the appearance of a wildly embedded 3-manifold which we identify with a quantum state.
- Furthermore, we analyze this quantum state by using foliation theory and relate it to an element in an operator algebra.
- Then we describe a set of geometric, non-commutative operators, the skein algebra, which can be ***used to determine the geometry of a 3-manifold***.
- This operator algebra can be understood as a deformation quantization of the classical Poisson algebra of observables given by [holonomies](https://en.wikipedia.org/wiki/Holonomy).
- The structure of this operator algebra induces an action by using the quantized calculus of Connes. 

The scaling behavior of this action is analyzed to obtain the classical theory of _General Relativity (GRT)_ for large scales. _([Smooth quantum gravity - pdf](https://github.com/eq19/maps/files/14132472/1601.06436.pdf))_
```

[![addition zones](https://github.com/eq19/maps/assets/8466209/4945cbd3-57ff-42ee-a363-7b27ed693a0e)](https://www.eq19.com/addition/)

The holonomy tells you how to propagate MEC30. A spin network state assigns an amplitude to a set of ***spin half particles*** tracing out a path in space, merging and splitting. 

![](https://user-images.githubusercontent.com/36441664/74366957-992db780-4e03-11ea-8f26-cca32bd26003.png)

This kind of approach has some obvious properties: there are non-linear gravitons, a connection to lattice gauge field theory and a ***dimensional reduction from 4D to 2D***.

## Construction of a State

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f
------+------+-----+----------    <----------------- Mobius strip √
      |      |     |  1  | --------------------------
      |      |  1  +-----+                           |
      |  1   |     |  2  | (5)                       |
      |      |-----+-----+                           |
      |      |     |  3  |                           |
  1   +------+  2  +-----+----                       |
      |      |     |  4  |                           |
      |      +-----+-----+                           |
      |  2   |     |  5  | (7)                       |
      |      |  3  +-----+                           |
      |      |     |  6  |                          11s
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |                           |
  2   +------|  5  +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) ---------------------
      |      |  6  +-----+        <----------------- Mobius strip
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s = f(1000)
  3   +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | --------------------------
------|------|-----+-----+------  <----------------- Möbius strip √
```

```note
The funny looking ***Möbius strip***, which was also independently discovered in 1858 by the unlucky Listing whose name left the history of mathematics untouched.
- It is a surface with only one side and only one boundary, often used to puzzle young math students. You can easily create it by taking a strip of paper, twisting it and then joining the ends of the strip.
- Being the first example of a surface without orientation it did not shake the grounds of mathematics as much as the other discoveries of this list did, yet it provided a lot of practical applications, such as a resistant belt, and inspired mathematicians to come up with unorientable surfaces, like the ***Klein bottle***.

- The name of this surface possibly comes from a double coincidence: Klein, its conceptor, originally named it Fläche, which means surface in German and sounds similar to Flasche, which means bottle. The fact that it also looked like a bottle seems to have sealed the renaming.

Mathematical fields were created, we got the ***Turing Machine***, fancy looking surfaces and, most importantly, the ability to re-examine our perceptions and adapt our tools accordingly. _([freeCodeCamp](https://www.freecodecamp.org/news/10-awkward-moments-in-math-history-d364706d902d/))_
```

[![mobius strip](https://github.com/eq19/maps/assets/8466209/d9dd8d68-3821-43a6-87f2-b04def942296)](https://www.freecodecamp.org/news/10-awkward-moments-in-math-history-d364706d902d/)

These items are elementary parts possessing familiar properties but they never exist as free particles. Instead they join together by the strong force into bound states.

***f(18) = f(7) + f(11) = (1+7+29) + 11th prime = 37 + 31 = 36 + 32 = 68***

![](https://github-production-user-asset-6210df.s3.amazonaws.com/8466209/260269050-deb0e309-2178-4dc5-a1d6-30c81c4a8305.png)

## Bilateral 9 Sums

```note
Eigennvalue curves (right) showing a triple eigenvalue at zero for τ = 1 and double eigenvalues at 1 ± √2i for τ = √43. On the left the graph of 1/|Q(λ)| with the same eigenvalue curves plotted in the ground plane. Green stars indicate the eigenvalues of A, blue stars the roots of puv(λ) and triangles the zeroes of Q0
(λ)
```

***10 + 10th prime + 10th prime = 10 + 29 + 29 = 68***

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f
------+------+-----+----------    <----------------- Mobius strip
      |      |     |  1  | --------------------------
      |      |  1  +-----+                           |
      |  1   |     |  2  | (5)                       |
      |      |-----+-----+                           |
      |      |     |  3  |                           |
  1   +------+  2  +-----+----                       |
      |      |     |  4  |                           |
      |      +-----+-----+                           |
      |  2   |     |  5  | (7)                       |
      |      |  3  +-----+                           |
      |      |     |  6  |                          11s ‹-- (71) √
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |                           |
  2   +------|  5  +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) ---------------------
      |      |  6  +-----+        <----------------- Mobius strip
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s ‹-- (43) √
  3   +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | --------------------------
------|------|-----+-----+------  <----------------- Möbius strip
```

This pattern is raised up ***per six (6) cycles*** on the ***[19](https://gist.github.com/eq19/c9bdc2bbe55f2d162535023c8d321831#file-instance-md)***, ***[43](https://gist.github.com/eq19/c9bdc2bbe55f2d162535023c8d321831#file-runner-md)*** and ***[71](https://gist.github.com/eq19/c9bdc2bbe55f2d162535023c8d321831#file-grammar-md)***. Since the members are limited to the sum of ***43+71=114***.

[![Polarity](https://user-images.githubusercontent.com/8466209/212487102-2f080804-9078-45c9-85ee-9977a36a5dbf.jpg)](http://www.hexspin.com/minor-hexagons/)

So here the bilateral way of 19 that originated by the (Δ1) is clearly the one that controls the scheme.

```note
In the matrix pictured below, we list the first 24 elements of our domain, take their squares, calculate the modulo 90 congruence and digital roots of each square, and display the digital root factorization dyad for each square (and map their ***collective bilateral 9 sum symmetry***). _([PrimesDemystified](https://primesdemystified.com/))_
```

***7 x π(89) = 7 x 24 = 168 = π(1000)***

[![collective bilateral 9 sum symmetry](https://user-images.githubusercontent.com/8466209/200229388-03811f48-2492-4845-b15f-85259cd93717.png)](https://www.eq19.com/multiplication/#elementary-structure)

## Supersymmetric Multiplet

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f.                                       MEC 30 / 2
------+------+-----+-----+------      ‹------------------------------ 0 {-1/2}
      |      |     |  1  | --------------------------
      |      |  1  +-----+                           |    
      |  1   |     |  2  | (5)                       |
      |      |-----+-----+                           |
      |      |     |  3  |                           |
  1   +------+  2  +-----+----                       |
      |      |     |  4  |                           |
      |      +-----+-----+                           |
      |  2   |     |  5  | (7)                       |
      |      |  3  +-----+                           |
      |      |     |  6  |                          11s ‹-- ∆28 = (71-43) √
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |‹-- ∆9 = (89-71) / 2 √     |
  2   +------|  5* +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) --------------------- 
      |      |  6  +-----+            ‹------------------------------ 15 {0}
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s ‹-- ∆24 = (43-19) √
  3*  +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | -------------------------- 
------|------|-----+-----+-----  ‹----------------------------------- 30 {+1/2}
```

```note
Given our domain is limited to numbers ≌ {1,7,11,13,17,19,23,29} modulo 30, only ϕ(m)/m = 8/30 or 26.66% of natural numbers N = {0, 1, 2, 3, ...} need be sieved.
- For example, to illustrate the proportionality of this ratio, we find that 25% of the first 100 natural numbers are prime, while 72% of numbers not divisible by 2, 3, or 5 are prime (and, curiously, if we count 2, 3, and 5 in after the fact, we get 75%, or exactly 3 x 25%).
- Also note that if you plug the number 30 into [Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function), phi(n): phi(30)= 8, with the 8 integers (known as [totatives](https://mathworld.wolfram.com/Totative.html)) smaller than and having no factors in common with 30 being: 1, 7, 11, 13, 17, 19, 23 and 29, i.e., what are called "prime roots" above. Thirty is the largest integer with this property.]
- The integer 30, product of the first three prime numbers (2, 3 and 5), and thus a primorial, plays a powerful role organizing the array's perfect symmetry, viz., in the case of the 8 prime roots:

1+29=30; 7+23=30; 11+19=30; and 13+17=30.

- In The Number Mysteries well-known mathematician Marcus Du Sautoy writes: "In the world of mathematics, the numbers 2, 3, and 5 are like hydrogen, helium, and lithium. That's what makes them the most important numbers in mathematics."
- Although 2, 3 and 5 are the only prime numbers not included in the domain under discussion, they are nonetheless integral to it: First of all, they sieve out roughly 73% of all natural numbers, leaving only those nominally necessary to construct a geometry within which prime numbers can be optimally arrayed.
- The remaining 26.66% (to be a bit more precise) constituting the array can be constructed with an elegantly simple interchangeable expression (or power series, if you prefer) that incorporates the first three primes. It's conjectured that this manifold series ultimately consists of all (and only) the numbers not divisible by 2, 3, or 5 (and their negatives), which inclues all prime numbers >5 (more below under the heading "Conjectures and Facts Relating to the Prime Spiral Sieve").

What is critical to understand, is that the invisible hand of 2, 3 and 5, and their factorial 30, create the structure within which the balance of the prime numbers, i.e., all those greater than 5, are arrayed algorithmically–as we shall demonstrate. Primes 2, 3 and 5 play out in modulo 30-60-90 cycles (decomposing to {3,6,9} sequencing at the digital root level). Once the role of 2, 3 and 5 is properly understood, all else falls beautifully into place. _([PrimesDemystified](https://primesdemystified.com/#Distribution_of_Perfect_Squares))_
```

[![One_Grand_Pyramid_Teaser](https://github.com/eq19/maps/assets/8466209/31cec66a-566f-466d-9ea6-f924e7499f01)](https://www.primesdemystified.com/First1000Primes.html)

