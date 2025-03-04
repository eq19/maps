{% include list.liquid all=true %}

![image](https://github.com/eq19/maps/assets/8466209/a4e57e16-8334-4270-bce7-9739e30df21a)

***(10 - 2) th prime = 8th prime = 19***

[![default](https://user-images.githubusercontent.com/8466209/200228711-996e52bf-887c-445d-ad4b-46da2eabc30e.png)](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#the-implementation)

The subclasses of partitions systemically develops characters similar to the distribution of prime numbers. 

[![Rank of a partition](https://user-images.githubusercontent.com/8466209/227838045-3ddd5238-7beb-4023-affa-c61a054afd2b.png)](https://en.wikipedia.org/wiki/Rank_of_a_partition)

tps://gist.github.com/eq19/e9832026b5b78f694e4ad22c3eb6c3ef#partition-function) represents the number of possible partitions of a non-negative integer n.

***f(8 twins) = 60 - 23 = 37 inner partitions***

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 -29 = 61 - 1 = 60 ✔️
5 5 2 1 0 5 👉 f(37) = f(8 twins) ✔️
6 7 3 1 0 7 ◄--- #23
7 11 4 1 0 11 ◄--- #19
8 13 5 1 0 13 ◄--- # 17 ◄--- #49
9 17 0 1 1 17 ◄--- 7th prime 👉 7s
10 19 1 1 1 ∆1 ◄--- 0th ∆prime ◄--- Fibonacci Index #18
-----
11 23 2 1 1 ∆2 ◄--- 1st ∆prime ◄--- Fibonacci Index #19 ◄--- #43
..
..
40 163 5 1 0 ∆31 ◄- 11th ∆prime ◄-- Fibonacci Index #29 👉 11
-----
41 167 0 1 1 ∆0
42 173 0 -1 1 ∆1
43 179 0 1 1 ∆2 ◄--- ∆∆1
44 181 1 1 1 ∆3 ◄--- ∆∆2 ◄--- 1st ∆∆prime ◄--- Fibonacci Index #30
..
..
100 521 0 -1 2 ∆59 ◄--- ∆∆17 ◄--- 7th ∆∆prime ◄--- Fibonacci Index #36  👉 7s
-----
```

***7 + 13 + 19 + 25 = 64 = 8 × 8 = 8²***

![](https://user-images.githubusercontent.com/36441664/83051968-e2cfa480-a078-11ea-8ff2-316a809a8fad.jpg)

## Subclasses of Partitions

```note
Let weighted points be given in the plane . For each point a radius is given which is the expected ideal distance from this point to a new facility. We want to find the location of a new facility such that the sum of the weighted errors between the existing points and this new facility is minimized. This is in fact a nonconvex optimization problem. We show that the optimal solution lies in an extended rectangular hull of the existing points. Based on this finding then an efficient big square small square (BSSS) procedure is proposed.
```

[![A_BSSS_Algorithm_for_the_Location_Problem_with_Min.pdf](https://github.com/eq19/maps/assets/8466209/44b32796-e66b-4364-b20c-2a7305c53802)](https://github.com/eq19/maps/files/13764148/A_BSSS_Algorithm_for_the_Location_Problem_with_Min.pdf)

Integers can be considered either in themselves or as solutions to equations ([Diophantine geometry](https://en.wikipedia.org/wiki/Diophantine_geometry)).

```note
[Young diagrams](https://commons.wikimedia.org/wiki/Category:Young_diagrams) associated to the partitions of the positive integers ***1 through 8***. They are arranged so that images under the reflection about the main diagonal of the square are conjugate partitions _([Wikipedia](https://en.wikipedia.org/wiki/Partition_(number_theory)))_.
```

***f(8🪟8) = 1 + 7 + 29 = 37 inner partitions***

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 -29 = 61 - 1 = 60
5 5 2 1 0 5 👉 f(37) = f(8🪟8) ✔️
6 7 3 1 0 7 ◄--- #23
7 11 4 1 0 11 ◄--- #19
8 13 5 1 0 13 ◄--- # 17 ◄--- #49
9 17 0 1 1 17 ◄--- 7th prime 👉 7s
10 19 1 1 1 ∆1 ◄--- 0th ∆prime ◄--- Fibonacci Index #18
-----
11 23 2 1 1 ∆2 ◄--- 1st ∆prime ◄--- Fibonacci Index #19 ◄--- #43
..
..
40 163 5 1 0 ∆31 ◄- 11th ∆prime ◄-- Fibonacci Index #29 👉 11
-----
41 167 0 1 1 ∆0
42 173 0 -1 1 ∆1
43 179 0 1 1 ∆2 ◄--- ∆∆1
44 181 1 1 1 ∆3 ◄--- ∆∆2 ◄--- 1st ∆∆prime ◄--- Fibonacci Index #30
..
..
100 521 0 -1 2 ∆59 ◄--- ∆∆17 ◄--- 7th ∆∆prime ◄--- Fibonacci Index #36  👉 7s
-----
```

When these subclasses of partitions are flatten out into a matrix, you want to take the Jacobian of each of a stack of targets with respect to a stack of sources, where the Jacobians for each target-source pair are independent .

```note
It's possible to build a _[Hessian matrix](https://en.wikipedia.org/wiki/Hessian_matrix)_ for a _[Newton's method](https://en.wikipedia.org/wiki/Newton%27s_method_in_optimization)_ step using the Jacobian method. You would first flatten out its axes into a matrix, and flatten out the gradient into a vector _([Tensorflow](https://www.tensorflow.org/guide/advanced_autodiff#batch_jacobian))_. 
```

[![Partitioned-matrices-of-the-numbers-60-62-and-64-as-examples](https://github.com/eq19/maps/assets/8466209/2009c4a4-49f8-4653-b0ea-b928ecad3240)](https://github.com/eq19/maps/files/13722898/Partitions_of_even_numbers.pdf)

```note
***In summary, it has been shown that partitions into an even number of distinct parts and an odd number of distinct parts exactly cancel each other, producing null terms 0x^n, except if n is a generalized [pentagonal number](https://www.eq19.com/identition/#hidden-dimensions) n=g_{k}=k(3k-1)/2}***, in which case there is exactly one Ferrers diagram left over, producing a term (−1)kxn. But this is precisely what the right side of the identity says should happen, so we are finished. _([Wikipedia](https://en.wikipedia.org/wiki/Pentagonal_number_theorem))_
```

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 -29 = 61 - 1 = 60
5 5 2 1 0 5 👉 f(37) = f(29🪟23) ✔️
6 7 3 1 0 7 ◄--- #23
7 11 4 1 0 11 ◄--- #19
8 13 5 1 0 13 ◄--- # 17 ◄--- #49
9 17 0 1 1 17 ◄--- 7th prime 👉 7s
10 19 1 1 1 ∆1 ◄--- 0th ∆prime ◄--- Fibonacci Index #18
-----
11 23 2 1 1 ∆2 ◄--- 1st ∆prime ◄--- Fibonacci Index #19 ◄--- #43
..
..
40 163 5 1 0 ∆31 ◄- 11th ∆prime ◄-- Fibonacci Index #29 👉 11
-----
41 167 0 1 1 ∆0
42 173 0 -1 1 ∆1
43 179 0 1 1 ∆2 ◄--- ∆∆1
44 181 1 1 1 ∆3 ◄--- ∆∆2 ◄--- 1st ∆∆prime ◄--- Fibonacci Index #30
..
..
100 521 0 -1 2 ∆59 ◄--- ∆∆17 ◄--- 7th ∆∆prime ◄--- Fibonacci Index #36  👉 7s
-----
```

The code is interspersed with python, shell, perl, also demonstrates how multiple languages can be integrated seamlessly. 

[![extended branes](https://github.com/eq19/maps/assets/8466209/deb0e309-2178-4dc5-a1d6-30c81c4a8305)](https://www.eq19.com/identition/#partition-function)

These include generating variants of their abundance profile, assigning taxonomy and finally generating a rooted [phylogenetic tree](https://en.wikipedia.org/wiki/Phylogenetic_tree).

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 f(37) = ❓ 👈 Composite ✔️
6 7 3 1 0 7 ◄--- #23
7 11 4 1 0 11 ◄--- #19
8 13 5 1 0 13 ◄--- # 17 ◄--- #49
9 17 0 1 1 17 ◄--- 7th prime 👉 7s 👈 Composite ✔️
10 19 1 1 1 ∆1 ◄--- 0th ∆prime ◄--- Fibonacci Index #18
-----
11 23 2 1 1 ∆2 ◄--- 1st ∆prime ◄--- Fibonacci Index #19 ◄--- #43
..
..
40 163 5 1 0 ∆31 ◄- 11th ∆prime ◄-- Fibonacci Index #29 👉 11
-----
41 167 0 1 1 ∆0
42 173 0 -1 1 ∆1
43 179 0 1 1 ∆2 ◄--- ∆∆1
44 181 1 1 1 ∆3 ◄--- ∆∆2 ◄--- 1st ∆∆prime ◄--- Fibonacci Index #30
..
..
100 521 0 -1 2 ∆59 ◄--- ∆∆17 ◄--- 7th ∆∆prime ◄--- Fibonacci Index #36  👉 7s
-----
```

This behaviour in a fundamental causal relation to the primes when the products are entered into the  _[partitions](https://en.wikipedia.org/wiki/Partition_(number_theory))_ system. 

## Composite behaviour

The subclasses of partitions systemically develops characters similar to the distribution of prime numbers. It would mean that there should be some undiscovered things hidden within the residual of the decimal values. 

[![integer partition](https://github.com/eq19/maps/assets/8466209/814079f5-a06f-436f-9dc3-a41dbc0c120b)](https://blogs.iiit.ac.in/sumit-jha/)

***168 + 2 = 170 = (10+30)+60+70 = 40+60+70 = 40 + 60 + ∆(2~71)***

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 f(37) ✔️
          6 👉 11s Composite Partition ✔️
6 7 3 1 0 7 ◄--- #23
7 11 4 1 0 11 ◄--- #19
8 13 5 1 0 13 ◄--- # 17 ◄--- #49
9 17 0 1 1 17 ◄--- 7th prime
           18 👉 7s Composite Partition ✔️
10 19 1 1 1 ∆1 ◄--- 0th ∆prime ◄--- Fibonacci Index #18
-----
11 23 2 1 1 ∆2 ◄--- 1st ∆prime ◄--- Fibonacci Index #19 ◄--- #43
..
..
40 163 5 1 0 ∆31 ◄- 11th ∆prime ◄-- Fibonacci Index #29 👉 11
-----
41 167 0 1 1 ∆0
42 173 0 -1 1 ∆1
43 179 0 1 1 ∆2 ◄--- ∆∆1
44 181 1 1 1 ∆3 ◄--- ∆∆2 ◄--- 1st ∆∆prime ◄--- Fibonacci Index #30
..
..
100 521 0 -1 2 ∆59 ◄--- ∆∆17 ◄--- 7th ∆∆prime ◄--- Fibonacci Index #36  👉 7s
-----
```

```note
The initial concept of this work was the Partitioned Matrix of an even number w≥ 4:
- It was shown that ***for every even number w≥ 4*** it is possible to establish a corresponding Partitioned Matrix with a determined number of lines.
- It was demonstrated that, fundamentally, ***the sum of the partitions is equal to the number of lines*** in the matrix: Lw = Cw + Gw + Mw.
- It was also shown that for each and every Partitioned Matrix of an even number w ≥ 4 it is observed that
 Gw = π(w) − (Lw − Cw), which means that the number of Goldbach partitions or ***partitions of prime numbers of an even number w ≥ 4 is given by the number of prime numbers up to w minus the number of available lines*** (Lwd) calculated as follows: Lwd = Lw − Cw.

To analyze the adequacy of the proposed formulas, probabilistically calculated reference values were adopted. _([Partitions of even numbers - pdf](https://github.com/eq19/maps/files/13722898/Partitions_of_even_numbers.pdf))_
```

[![Batch Jacobian](https://user-images.githubusercontent.com/8466209/229297019-4583e9a7-273d-4489-ab87-37c88be16adb.png)](https://www.tensorflow.org/guide/advanced_autodiff#batch_jacobian)

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 11 + 29 = 37 + 3 = 40 ✔️
          6 👉 11s Composite Partition ◄--- 2+60+40 = 102 ✔️
6 7 3 1 0 7 ◄--- #23
7 11 4 1 0 11 ◄--- #19
8 13 5 1 0 13 ◄--- # 17 ◄--- #49
9 17 0 1 1 17 ◄--- 7th prime 
           18 👉 7s Composite Partition 
10 19 1 1 1 ∆1 ◄--- 0th ∆prime ◄--- Fibonacci Index #18
-----
11 23 2 1 1 ∆2 ◄--- 1st ∆prime ◄--- Fibonacci Index #19 ◄--- #43
..
..
40 163 5 1 0 ∆31 ◄- 11th ∆prime ◄-- Fibonacci Index #29 👉 11
-----
41 167 0 1 1 ∆0
42 173 0 -1 1 ∆1
43 179 0 1 1 ∆2 ◄--- ∆∆1
44 181 1 1 1 ∆3 ◄--- ∆∆2 ◄--- 1st ∆∆prime ◄--- Fibonacci Index #30
..
..
100 521 0 -1 2 ∆59 ◄--- ∆∆17 ◄--- 7th ∆∆prime ◄--- Fibonacci Index #36  👉 7s
-----
```

***(11x7) + (29+11) + (25+6) + (11+7) + 4 = 77+40+31+18+4 = 170***

[![16S rRNA amplicons study](https://user-images.githubusercontent.com/36441664/71659208-5515b480-2d79-11ea-859f-a20dea0cf680.jpg)](https://colab.research.google.com/drive/17Up0gSGF9euhqQ8Ext_2GtSptiPdt4HP)
