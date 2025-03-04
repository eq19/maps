{% include list.liquid all=true %}

## The Position Pairs

[![Pauli_matrices](https://github.com/eq19/maps/assets/8466209/a5d16633-09b6-48e2-ad9f-cd55e4a8a181)](https://en.wikipedia.org/wiki/Pauli_matrices)

***36 + 36 - 6 partitions = 72 - 6 = 66 = 30+36 = 6x11***

```
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

[![spinnors in physics](https://github.com/eq19/maps/assets/8466209/231e8377-6d0b-43ec-b0c1-432c2daf24bb)](https://youtu.be/j5soqexrwqY?t=7m32s)

```py
#!/usr/bin/env python

import numpy as np
from scipy import linalg

class SU3(np.matrix):
	GELLMANN_MATRICES = np.array([
		np.matrix([ #lambda_1
			[0, 1, 0],
			[1, 0, 0],
			[0, 0, 0],
		], dtype=np.complex),
		np.matrix([ #lambda_2
			[0,-1j,0],
			[1j,0, 0],
			[0, 0, 0],
		], dtype=np.complex),
		np.matrix([ #lambda_3
			[1, 0, 0],
			[0,-1, 0],
			[0, 0, 0],
		], dtype=np.complex),
		np.matrix([ #lambda_4
			[0, 0, 1],
			[0, 0, 0],
			[1, 0, 0],
		], dtype=np.complex),
		np.matrix([ #lambda_5
			[0, 0,-1j],
			[0, 0, 0 ],
			[1j,0, 0 ],
		], dtype=np.complex),
		np.matrix([ #lambda_6
			[0, 0, 0],
			[0, 0, 1],
			[0, 1, 0],
		], dtype=np.complex),
		np.matrix([ #lambda_7
			[0, 0,  0 ],
			[0, 0, -1j],
			[0, 1j, 0 ],
		], dtype=np.complex),
		np.matrix([ #lambda_8
			[1, 0, 0],
			[0, 1, 0],
			[0, 0,-2],
		], dtype=np.complex) / np.sqrt(3),
	])


	def computeLocalAction(self):
		pass

	@classmethod
	def getMeasure(self):
		pass
```

![](https://user-images.githubusercontent.com/36441664/84902333-e6ce6f80-b0d6-11ea-8289-aac5e1961cd6.gif)

Now the following results: Due to the convolution and starting from the desired value of the prime position pairs, the product templates and prime numbers templates of _the prime number 7 lie in the numerical Double strand parallel opposite_.

## The Fourth Root

In number theory, the [partition functionp(n)](https://gist.github.com/eq19/e9832026b5b78f694e4ad22c3eb6c3ef#partition-function) represents the number of possible partitions of a non-negative integer n.

![image](https://github.com/eq19/maps/assets/8466209/47eb16ae-0e78-4ec8-8351-e76d59511aa0)

Integers can be considered either in themselves or as solutions to equations ([Diophantine geometry](https://en.wikipedia.org/wiki/Diophantine_geometry)).

```note
[Young diagrams](https://commons.wikimedia.org/wiki/Category:Young_diagrams) associated to the partitions of the positive integers 1 through 8. They are arranged so that images under the reflection about the main diagonal of the square are conjugate partitions _([Wikipedia](https://en.wikipedia.org/wiki/Partition_(number_theory)))_.
```

[![integer partition](https://github.com/eq19/maps/assets/8466209/1a979f09-4592-4139-92fd-73472a54c60c)](https://commons.wikimedia.org/wiki/Category:Young_diagrams)

```note
By parsering [π(1000)=168 primes](https://www.eq19.com/sitemap.xml) of the 1000 id's across **π(π(10000))-1=200** of this syntax then the (Δ1) would be _[initiated](https://eq19.github.io/init.js)_. Based on Assigning Sitemap [priority values](https://www.microsystools.com/products/sitemap-generator/help/xml-sitemaps-creator-importance/) You may see them are set 0.75 – 1.0 on the [sitemap's index](https://www.eq19.com/sitemap.xml):
```

```
Priority	Page Name
1	        Homepage
0.9	        Main landing pages
0.85	        Other landing pages
0.8	        Main links on navigation bar
0.75	        Other pages on site
0.8	        Top articles/blog posts
0.75	        Blog tag/category pages
0.4 – 0.7	Articles, blog posts, FAQs, etc.
0.0 – 0.3	Outdated information or old news that has become less relevant
```

By this object orientation then the _[reinjected primes](https://github.com/actions/cache#cache-version)_ from the π(π(10000))-1=200 will be **(168-114)+(160-114)=54+46=100**. Here are our layout that is provided using _[Jekyll/Liquid](https://jekyllrb.com/docs/liquid/)_ to facilitate the cycle:

***100 + 68 + 32 = 200***

```
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f.                                      MEC 30 / 2
------+------+-----+-----+------      ‹--------------------------- 30 {+1/2} √
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
      |      |     |  9  |‹--                        |
  2   +------|  5* +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) --------------------- 32 √
      |      |  6  +-----+            ‹------------------------------ 15 {0} √
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s = f(1000)
  3*  +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | -------------------------- 68 √
------|------|-----+-----+-----                            ‹------  0 {-1/2} √
```

[![Diagram-of-the-statistical-principle-for-the-constitution-of-partitions-of-prime-numbers](https://github.com/eq19/maps/assets/8466209/e0e8d25c-01a4-4c87-9f3a-6f3fcfab3679)](https://github.com/eq19/maps/files/13722898/Partitions_of_even_numbers.pdf)

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61 👈 1st spin
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 11 + 29 = 37 + 3 = 40 
          6 👉 11s Composite Partition ◄--- 102 👈 4th spin
6 7 3 1 0 7 ◄--- #23 👈 7+23 = 30 ✔️
7 11 4 1 0 11 ◄--- #19 👈 11+19 = 30 ✔️
8 13 5 1 0 13 ◄--- #17 ◄--- #49 👈 13+17 = 30 ✔️
9 17 0 1 1 17 ◄--- 7th prime👈 17+7 != 30❓
           18 👉 7s Composite Partition ◄--- 168 👈 7th spin
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

## Composite System

By taking a distinc function between f(π) as P vs f(i) as NP where e<sup>iπ</sup> + 1 = 0 then theoretically they shall be correlated to get an expression of the prime platform similar to the _Mathematical Elementary Cell 30 ([MEC30](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#true-prime-pairs))_.

![](https://user-images.githubusercontent.com/36441664/74591945-2b75cb80-504f-11ea-85dd-14d0a803ee6b.png)

***∆17 + ∆49 = ∆66***

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61 👈 1st spin
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 11 + 29 = 37 + 3 = 40 
          6 👉 11s Composite Partition ◄--- 102 👈 4th spin
6 7 3 1 0 7 ◄--- #23 👈 part of MEC30 ✔️
7 11 4 1 0 11 ◄--- #19 👈 part of MEC30 ✔️
8 13 5 1 0 13 ◄--- #17 ◄--- #49 👈 part of MEC30 ✔️
9 17 0 1 1 17 ◄--- 7th prime👈 not part of MEC30 ❓
           18 👉 7s Composite Partition ◄--- 168 👈 7th spin
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

![a-Example-of-trellis-tone-modulation-generated-by-referring-to-the-trellis-diagram-in](https://github.com/eq19/maps/assets/8466209/12f9a1d4-07c5-40ad-a5e8-e98933b4956d)

***∆102 - ∆2 - ∆60 = ∆40***

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61 👈 1st spin
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 11 + 29 = 37 + 3 = 40 
          6 👉 11s Composite Partition ◄--- 102 👈 4th spin
6 7 3 1 0 7 ◄--- #23 👈 30 ◄--- break MEC30 symmetry ✔️
7 11 4 1 0 11 ◄--- #19 👈 30 ✔️
8 13 5 1 0 13 ◄--- #17 ◄--- #49 👈 30 ✔️
9 17 0 1 1 17 ◄--- 7th prime👈 not part of MEC30 ❓
           18 👉 7s Composite Partition ◄--- 168 👈 7th spin
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
***The partitions of odd composite numbers (Cw) are as important as the partitions of prime numbers or Goldbach partitions (Gw)***. The number of partitions Cw is fundamental for defining the available lines (Lwd) in a Partitioned Matrix that explain the existence of partitions Gw or Goldbach partitions. _([Partitions of even numbers - pdf](https://github.com/eq19/maps/files/13722898/Partitions_of_even_numbers.pdf))_
```

[![Trellis_Tone_Modulation_Multiple-Access_for_Peer_D](https://github.com/eq19/maps/assets/8466209/58a42b62-7c61-404f-a3a0-e4850dd17875)](https://github.com/eq19/maps/files/13734648/Trellis_Tone_Modulation_Multiple-Access_for_Peer_D.pdf)

***30s + 36s (addition) = 6 x 11s (multiplication) = 66s***

```txt
p r i m e s
1 0 0 0 0 0
2 1 0 0 0 1 ◄--- #29 ◄--- #61 👈 1st spin
3 2 0 1 0 2 👉 2
4 3 1 1 0 3 👉 89 - 29 = 61 - 1 = 60
5 5 2 1 0 5 👉 11 + 29 = 37 + 3 = 40 
          6 👉 11s Composite Partition ◄--- 102 👈 4th spin
6 7 3 1 0 7 ◄--- #23 👈 f(#30) ◄--- break MEC30 symmetry
7 11 4 1 0 11 ◄--- #19 👈 30
8 13 5 1 0 13 ◄--- #17 ◄--- #49 👈 30
9 17 0 1 1 17 ◄--- 7th prime 👈 f(#36) ◄--- antisymmetric state ✔️
           18 👉 7s Composite Partition ◄--- 168 👈 7th spin
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

![](https://user-images.githubusercontent.com/36441664/84674358-09387f80-af55-11ea-9fe2-954f020edb21.jpg)
