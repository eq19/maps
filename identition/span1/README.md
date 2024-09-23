---
sort: 39
spin: 68
span: 
suit: 
description: 
---
# Wormhole Theory (span 1)

This section serve to study the internal (color) rotations of the [gluon fields](https://en.m.wikipedia.org/wiki/Gluon_field) associated with the coloured quarks in [quantum chromodynamics](https://en.m.wikipedia.org/wiki/Quantum_chromodynamics) of [colours of the gluon](https://en.m.wikipedia.org/wiki/Gluon#Eight_gluon_colours). 

{% include list.liquid all=true %}

A gauge colour rotation is _[a spacetime-dependent SU(3)](https://en.m.wikipedia.org/wiki/Special_unitary_group#The_group_SU(3))_ group element. They span the [Lie algebra](https://github.com/lkpetrich/Semisimple-Lie-Algebras) of the SU(3) group in the defining representation.

## Three (3) Layers

Our scenario of [prime identity](https://www.eq19.com/#prime-identity) is layering three (3) prime pairs out of the symmetrical behaviour of 36 as the smallest number (greater than 1) which is not a prime.

```tip
By our project this prime layering is called _[The True Prime Pairs](https://www.eq19.com/addition/2.html)_ and to be intrepeted as: Mapping the quantum way within a huge of primes objects (5 to 19) by lexering (11) the ungrammared feed (7) and parsering (13) across syntax (17).
```

```txt
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

The (3) layers represents generation in the [Standard Model](https://en.wikipedia.org/wiki/Standard_Model) of flavor that counts ***six (6) flavours of [quarks](https://en.wikipedia.org/wiki/Quark)*** and ***six (6) flavours of [leptons](https://en.wikipedia.org/wiki/Lepton)***.

```note
Leptons may be assigned the six flavour quantum numbers: electron number, muon number, tau number, and corresponding numbers for the neutrinos.
- These are conserved in strong and electromagnetic interactions, but violated by weak interactions. 
- Therefore, such flavour quantum numbers are not of great use. A separate quantum number for each [generation](https://en.wikipedia.org/wiki/Generation_(particle_physics)) is more useful: electronic lepton number (+1 for electrons and electron neutrinos), muonic lepton number (+1 for muons and muon neutrinos), and tauonic lepton number (+1 for tau leptons and tau neutrinos).
- However, even these numbers are not absolutely conserved, as neutrinos of different generations can [mix](https://en.wikipedia.org/wiki/Quantum_superposition); that is, a neutrino of one flavour can [transform into another flavour](https://en.wikipedia.org/wiki/Neutrino_oscillation).

[![PMNS Matriks](https://github.com/eq19/maps/assets/8466209/da339619-8e78-4453-9eac-f1b5eebe547d)](https://en.wikipedia.org/wiki/Pontecorvo%E2%80%93Maki%E2%80%93Nakagawa%E2%80%93Sakata_matrix)

The strength of such mixings is specified by a matrix called the [Pontecorvo–Maki–Nakagawa–Sakata matrix](https://en.wikipedia.org/wiki/Pontecorvo%E2%80%93Maki%E2%80%93Nakagawa%E2%80%93Sakata_matrix) (PMNS matrix). _([Wikipedia](https://en.wikipedia.org/wiki/Flavour_(particle_physics)))_
```

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
------+------+-----+-----+------  } (36) » 6®
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
  3   +------+  8  +-----+-----  } (36) » 6®
      |      |     |  16 |
      |      |-----+-----+
      |  6   |     |  17 | (19)
      |      |  9  +-----+
      |      |     |  18 |
------|------|-----+-----+------
```

While there are ***nine (9) possible*** combinations of color/anti-color pairs, due to symmetry considerations one of these combinations is eliminated. A gluon can effectively carry one of ***eight (8) possible*** color/anti-color combinations.

[![color charge and confinement](https://github.com/eq19/maps/assets/8466209/5c0f29a2-b3ac-4f93-90bf-1b5bd7bf9558)](https://fafnir.phyast.pitt.edu/particles/color.html)

These [matrices](https://mathworld.wolfram.com/Matrix.html) are particularly important in both mathematics and physics. For example, these matrices (and their generalizations) are important in Lie theory.

```note
_[Gell-mann matrices](https://en.m.wikipedia.org/wiki/Gell-Mann_matrices)_ are a complete set of Hermitian  noncommuting trace-orthogonal matrices. In addition, they also play an important role in physics where they can be thought to model ***the eight gluons*** that mediate the strong force quantum chromodynamics, an analogue of the _[Pauli matrices](https://mathworld.wolfram.com/PauliMatrices.html)_ well-adapted to applications in the realm of quantum mechanics. _([Wolfram](https://mathworld.wolfram.com/Gell-MannMatrix.html))_
```

```python
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

We apply these generators to the rest of the space, and find that it breaks down into the SU(3)c representations of ***exactly three generations of quarks and leptons***.

```note
The action of C⊗O on itself can be seen to generate a ***64-complex-dimensional algebra***, wherein we are able to identify two sets of generators for SU(3)c.
- Furthermore, we show that ***these three-generation results can be extended, so as to include all 48 fermionic U(1)em charges***.
- The 64-dimensional octonionic chain algebra splits into ***two sets of SU (3) generators of the form iΛν and −iΛ * ν * , six SU (3) singlets j , six triplets q k , and their complex conjugates***.
- These objects are sectioned off above into four quadrants according to their forms: νaν, ν * aν, νaν * and ν * aν * for a in the chain algebra.

Transforming particles into anti-particles, and vice versa, requires only the complex conjugate ***i → −i*** in our formalism. _([Standard Model from an algebra - pdf](https://github.com/eq19/maps/files/14387513/Standard_model_physics_from_an_algebra.pdf))_
```

[![The-64-dimensional-octonionic-chain-algebra-splits-into-two-sets-of-SU-3-generators](https://github.com/eq19/maps/assets/8466209/9fb5e061-0e82-4c0d-980d-528932ff1f3f)](https://github.com/eq19/maps/files/14387513/Standard_model_physics_from_an_algebra.pdf)

This quark model underlies [flavor SU(3)](https://en.wikipedia.org/wiki/Flavour_(particle_physics)), or [Eightfold Way](https://en.wikipedia.org/wiki/Eightfold_way_(physics)), the successful classification scheme organizing the large number of lighter [hadrons](https://en.wikipedia.org/wiki/Hadron)

```note
The [pseudoscalar](https://en.wikipedia.org/wiki/pseudoscalar) [meson](https://en.wikipedia.org/wiki/meson) nonet. Members of the original meson "octet (8)" are shown in green, the singlet in magenta.
- Although these mesons ***are now grouped into a nonet (9)***, the [Eightfold Way](https://en.wikipedia.org/wiki/Eightfold_way_(physics)) name derives from the patterns of eight for the mesons and baryons in the original classification scheme.
- The Eightfold Way classification is named after the following fact:
  - If we take three flavors of quarks, then the quarks lie in the [fundamental representation](https://en.wikipedia.org/wiki/Fundamental_representation), 3 (called the triplet) of [flavor](https://en.wikipedia.org/wiki/Flavour_(particle_physics)) [SU(3)](https://en.wikipedia.org/wiki/SU(3)).
  - The antiquarks lie in the complex conjugate representation 3.
- The nine states (nonet) made out of a pair can be decomposed into the [trivial representation](https://en.wikipedia.org/wiki/Trivial_representation), 1 (called the singlet), and the [adjoint representation](https://en.wikipedia.org/wiki/Adjoint_representation_of_a_Lie_group), 8 (called the octet). 
- The notation for this decomposition is ***3⊗3=8⊕1***.

Figure below shows the application of this decomposition to the mesons. _([Wikipedia](https://en.wikipedia.org/wiki/Quark_model))_
```

[![8foldway svg](https://github.com/eq19/maps/assets/8466209/5c3e5114-e89b-40ad-b550-62b39a2963dd)](https://en.wikipedia.org/wiki/Quark_model)

The symmetrical states can couple to a pair of pseudoscalar mesons in a wave, and hence their widths and masses are strongly influenced by these couplings.

```note
In order to be _[four-spinors](https://en.wikipedia.org/wiki/Dirac_spinor#Four-spinor_for_particles)_ like the electron and other [lepton](https://en.wikipedia.org/wiki/Lepton) components, there must be one quark component for every combination of [flavour](https://en.wikipedia.org/wiki/Flavor_(particle_physics)) and [colour](https://en.wikipedia.org/wiki/Color_charge), _bringing the total to 24 (3 for charged leptons, 3 for neutrinos, and 2·3·3 = 18 for quarks). Each of these is a four (4) component [bispinor](https://en.wikipedia.org/wiki/Bispinor), for a total of [96 complex-valued components](https://github.com/eq19/maps/files/13796986/NEUTRINOS_Mysterious_Particles_with_Fascinating_Fe.pdf) for the fermion field_. _([Wikipedia](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model))_
```

***Eightfold Way = 8 × (6®+6®) = 96®***

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
------+------+-----+-----+------  } (36) » 6® -------------
      |      |     |  7  |                                 |
      |      |  4  +-----+                                 |
      |  3   |     |  8  | (11)                            |
      |      +-----+-----+                                 |
      |      |     |  9  | <--------  Eightfold Way = 8 × (6®+6®) = 96®
  2   +------|  5  +-----+-----                               |
      |      |     |  10 |                                    |
      |      |-----+-----+                                    |
      |  4   |     |  11 | (13)                               |
      |      |  6  +-----+                                    |
      |      |     |  12 |                                    |
------+------+-----+-----+------------------                  |
      |      |     |  13 |                                    |
      |      |  7  +-----+                                    |
      |  5   |     |  14 | (17)                               |
      |      |-----+-----+                                    |
      |      |     |  15 |                                    |
  3   +------+  8  +-----+-----  } (36) » 6® -----------------
      |      |     |  16 |
      |      |-----+-----+
      |  6   |     |  17 | (19)
      |      |  9  +-----+
      |      |     |  18 |
------|------|-----+-----+------
```

In fact this particular count of three (3) as the _[Eightfold Way Generation](https://youtu.be/cCsxSjSv-bk)_ of ***6 by 6 flavors*** is the major case of every theories in physics to get in to the TOE.

```note
The origin of multiple generations of fermions, and the particular count of 3, is an _[unsolved problem of physics](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_physics)_.
- [Generations of matter](https://en.wikipedia.org/wiki/Generation_(particle_physics)): Why are there three generations of [quarks](https://en.wikipedia.org/wiki/Quark) and [leptons](https://en.wikipedia.org/wiki/Lepton)? Is there a theory that can explain the masses of particular quarks and leptons in particular generations from first principles (a theory of [Yukawa couplings](https://en.wikipedia.org/wiki/Yukawa_coupling))?
- [String theory](https://en.wikipedia.org/wiki/String_theory) provides a cause for multiple generations, but the particular number depends on the details of the [compactification](https://en.wikipedia.org/wiki/Compactification_(physics)) of the [D-brane](https://en.wikipedia.org/wiki/D-brane) intersections.
- Additionally, [E8](https://en.wikipedia.org/wiki/E8_(mathematics)) [grand unified theories](https://en.wikipedia.org/wiki/Grand_Unified_Theory) in 10 dimensions [compactified](https://en.wikipedia.org/wiki/Compactification_(physics)) on certain [orbifolds](https://en.wikipedia.org/wiki/Orbifold) down to 4‑D naturally contain 3 generations of matter.
- This includes many [heterotic string theory](https://en.wikipedia.org/wiki/Heterotic_string_theory) models.

In standard quantum field theory, under certain assumptions, a single fermion field can give rise to multiple fermion poles with mass ratios of around eπ≈23 and e2π≈535 potentially explaining the large ratios of fermion masses between successive generations and their origin. _([Wikipedia](https://en.wikipedia.org/wiki/Generation_(particle_physics)))_
```

***6 x 114 - 30 - 30 - 5 = 619 = 6 x 19 = 114th prime***

[![](https://user-images.githubusercontent.com/8466209/90985852-ca542500-e5a8-11ea-9027-9bfdcbe37966.jpg)](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#file-1_prime-md)

The quark model for baryons has been very successful in describing them as qqq states,  including those with nonzero internal orbital angular momentum. However, final meson-baryon states (and thus states of qq¯+qqq) play an important role as well.

```note
Why do we see certain types of strongly interacting elementary particles and not others? This question was posed over 50 years ago in the context of the quark model.
- M. Gell-Mann and G. Zweig proposed that the known mesons were qq¯ and baryons qqq, with quarks known at the time u (“up”), d (“down”), and s (“strange”) having charges (2/3,–1/3,–1/3).
- Mesons and baryons would then have integral charges. Mesons such as qqq¯q¯ and baryons such as qqqqq¯ would also have integral charges. Why weren’t they seen?
- They have now been seen, but only with additional heavy quarks and under conditions which tell us a lot about the strong interactions and how they manifest themselves.

[![Beyond the standard model](https://github.com/eq19/maps/assets/8466209/0d5cee08-92b4-48e8-9b50-e55312a5736f)](https://github.com/eq19/maps/files/13793234/the-physics-of-the-standard-model-and-beyond.pdf)

The present article describes recent progress in our understanding of such “exotic” mesons and baryons. _([Multiquark States - pdf](https://github.com/eq19/maps/files/14322719/1711.10626.pdf))_
```

[![structure-of-composite-particles-l](https://github.com/eq19/maps/assets/8466209/2966004c-0c0d-4bca-85a9-1217d6b0237b)](https://github.com/eq19/maps/files/14322719/1711.10626.pdf)

There are higher dimensional numbers besides complex numbers. The classical octet [meson](https://en.wikipedia.org/wiki/meson) is now nonet. Thus consequently it would go higher than E8.

```note
These are called hypercomplex numbers, such as, quaternions (4D), octonions (8D), sedenions (16D), pathions (32D), chingons (64D), routons (128D), and voudons (256D).  These names were coined by Robert P.C. de Marrais and Tony Smith.  It is an alternate naming system providing relief from the difficult Latin names, such as: trigintaduonions (32D), sexagintaquattuornions (64D), centumduodetrigintanions (128D), and ducentiquinquagintasexions (256D). _([Wordpress.com](https://nitinuchil.wordpress.com/2020/09/09/hypercomplex-math/))_ 
```

[![4 types of numbers](https://github.com/eq19/maps/assets/8466209/5b6d06cf-e7b3-442c-b5d8-0818a2eb470c)](https://nitinuchil.wordpress.com/2020/09/09/hypercomplex-math/)

The _[three (3) layers](https://www.eq19.com/identition/span12/#three-3-layers)_ as explained above is in the 1st-term of our discussed structure. So the next step is the 2nd-term which ***goes to the four (4)*** dimensional space-time.

## The Four (4) Dimensions

4D-dimensional space-time is much more complex due to the extra degree of freedom. Almost all of the rest of [unsolved problems](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_physics) in physics are correlated with.

```note
The set of points in Euclidean 4-space having the same distance R from a fixed point P0 forms a hypersurface known as a 3-sphere where R is substituted by function R(t) with t meaning the cosmological age of the universe. Growing or shrinking R with time means expanding or collapsing universe, depending on the mass density inside _([Wikipedia](https://en.wikipedia.org/wiki/Four-dimensional_space#Hypersphere))_.
```

![](https://user-images.githubusercontent.com/8466209/226084191-fbdb2d57-08bc-4d18-adea-4e165aee19a8.gif)

The main reason is that the [general relativity](https://en.wikipedia.org/wiki/General_relativity) not consistent with [quantum mechanics](https://en.wikipedia.org/wiki/Quantum_mechanics). It is even a sign that Einstein's equations are somehow incomplete.

```note
Throughout his life, Einstein published hundreds of books and articles. He published more than 300 scientific papers and 150 non-scientific ones. On 5 December 2014, universities and archives announced the release of Einstein's papers, comprising more than 30,000 unique documents _([Wikipedia](https://en.wikipedia.org/wiki/Albert_Einstein#Scientific_career))_.
```

![default](https://user-images.githubusercontent.com/8466209/227863531-b8b9a02a-148c-4048-b7cb-1d1ff820b6be.png)

Comparatively, four-dimensional space has an extra coordinate axis, orthogonal to the other three, which is usually labeled w to describe the two additional cardinal directions of ***up toward*** and ***down from***, respectively. 

```note
On the other hand, one does not yet have a mathematically complete example of a quantum gauge theory in [4D Space vs Time](https://en.wikipedia.org/wiki/Yang%E2%80%93Mills_existence_and_mass_gap#Background), nor even a precise definition of quantum gauge theory in four dimensions. Will this change in the 21st century? We hope so! _([Clay Institute's - Yang Mills Official problem description](https://github.com/eq19/maps/files/14056642/yangmills.pdf))_.
```

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
------+------+-----+-----+------  } (36) » 6® 👈 up toward ✔️
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
  3   +------+  8  +-----+-----  } (36) » 6® 👈 down from ✔️
      |      |     |  16 |
      |      |-----+-----+
      |  6   |     |  17 | (19)
      |      |  9  +-----+
      |      |     |  18 |
------|------|-----+-----+------
```

The Lorentz group consists, unsurprisingly, of the Lorentz transformations, which are the linear transformations preserving the Minkowski dot product.

```note
Equivalently, they are the linear transformations fixing that hyperboloid of two sheets. If we discard one of the sheets, we obtain the orthochronous (time-preserving) subgroup.
- From the perspective of the centre of the cone, the hyperboloid looks like an open disc. The orthochronous Lorentz transformations precisely correspond to distance-preserving transformations of the hyperbolic plane. These are themselves determined uniquely by a conformal (or anticonformal) transformation of the ‘circle at infinity’.
- Adding an extra dimension, the orthochronous Lorentz group O^{+}(3,1) is isomorphic to the group of distance-preserving transformations of hyperbolic 3-space, which is again isomorphic to the group of (anti-)conformal transformations of the ‘sphere at infinity’, namely our index-2 supergroup of the Möbius group.
- Moreover, this nicely generalises: the group generated by geometric inversions on the n-sphere is abstractly isomorphic to the orthochronous Lorentz group O^{+}(n+1,1).

***And when n = 24, we get a very beautiful discrete subgroup, namely the automorphism group of the II(25,1)*** lattice intimately related to the [Leech lattice](http://cp4space.wordpress.com/2013/09/12/leech-lattice/). _([Complex Projective 4-Space](https://cp4space.hatsya.com/2013/10/10/what-should-this-group-be-called/))_
```

[![spacetime](https://github.com/eq19/maps/assets/8466209/ff442f14-c1c4-4e87-a3e5-8bc157d20e46)](https://cp4space.hatsya.com/2013/10/10/what-should-this-group-be-called/)

This diagram is representing groupings (leptons, quarks, weak-force bosons) with 6 quarks in a way that parallels the 6 leptons.

```note
***There are 8 different types of tiny particles, or 'states', that we can find in a special kind of space that has 6 dimensions*** and involves both real and imaginary numbers. These particles include:
- ***The Higgs field***, which doesn't spin and is represented by 0.
- ***Fermions***, which are particles like electrons, having a spin of plus or minus a half.
- ***Bosons***, like photons, which have a spin of plus or minus 1.
- ***Anti-fermions***, which are like fermions but have a spin of plus or minus two-thirds.
- ***The graviton***, believed to be responsible for gravity, with a spin of 2.

***In a diagram at the top left, this 6-dimensional space is shown to be curved***. In another diagram at the bottom right, we see two waves that are perpendicular to each other, representing the motion of a particle in a 'Dirac harmonic oscillator' – a concept in quantum mechanics. _([Physics In History](https://twitter.com/PhysInHistory/status/1739158977089274165))_
```

[![Dirac_bispinor_6D](https://github.com/eq19/maps/assets/8466209/093efd9e-85ab-4caf-87e5-8987436fa049)](https://github.com/eq19/maps/files/13791680/Zitterbewegung_in_Quantum_Mechanics_a_re.pdf)

While the Dirac CP-violating phase δℓ can be determined in the future, how to probe or constrain ***the Majorana CP-violating phases ρ and σ is still an open question***

```note
Four of the dimensions are the usual four of spacetime. The six (or perhaps seven) extra dimensions are rolled up to be almost unobservable.
- First, let's see why they exist at all. If [N=8 Supersymmetry](https://en.wikipedia.org/wiki/N=8_Supergravity) is correct the universe must be 10 or 11 dimensional.![extra dimensions](https://github.com/eq19/maps/assets/8466209/dc2fca4c-26be-4e52-b8e4-bf8b9ac46835)
- Let D be the actual dimensionality of space time. Let d be the apparent dimensionality. (We know d = 4, but let's think generally.) Then there is a nice relation between D, d and N.[![Dimensional-reduction-of-supergravity-from-11D-to-4D-over-a-space-like-or-time-like](https://github.com/eq19/maps/assets/8466209/9fb715b2-6ab2-45e6-9ae2-7ccd1e1cf38e)
](https://www.researchgate.net/publication/273788549_10D_to_4D_Euclidean_Supergravity_over_a_Calabi-Yau_three-fold)
- It follows from the number of spinor dimensions required by the Dirac equation, which is  The s mean round down to the nearest whole number. So plugging in d=4 and N=8 (which is the highest value N can have) we get D = 10 or 11. String theory has D=10, M-theory has D=11.[![Dirac, Weyl, and Majorana in 4D](https://github.com/eq19/maps/assets/8466209/544aefc2-7ba5-4623-9d99-51febf61efb0)](https://www.mdpi.com/2218-1997/6/8/111)
- One dimension is reserved for time, leaving space with 9 or 10 dimensions.

We don't see 6 (or 7) of these extra dimensions because - we assume - they are [rolled up ](https://en.m.wikipedia.org/wiki/Compactification_(physics))a la [Kaluza–Klein theory](https://en.wikipedia.org/wiki/Kaluza%E2%80%93Klein_theory) into a 6 dimensional [Calabi–Yau space](https://en.m.wikipedia.org/wiki/Calabi%E2%80%93Yau_manifold)
```

![main-qimg-f8cd59c3b8504bdaab0977ee2704ce0e-ezgif com-webp-to-png-converter](https://github.com/eq19/maps/assets/8466209/a55d8ed9-af8c-48ae-ae82-d9f83a5c92f7)

The most promising candidate is [SO(10)](https://en.wikipedia.org/wiki/SO(10)) but it does not contain any [exotic fermions](https://en.wikipedia.org/Exotic_fermion) (i.e. additional fermions besides the Standard Model and the right-handed neutrino), and it unifies each generation into a single [irreducible representation](https://en.wikipedia.org/wiki/Irreducible_representation).

```note
In [particle physics](https://en.wikipedia.org/wiki/Particle_physics), SO(10) refers to a [grand unified theory](https://en.wikipedia.org/wiki/Grand_unified_theory) (GUT) based on the [spin group](https://en.wikipedia.org/wiki/Spin_group) Spin(10). The shortened name SO(10) is conventional[[1]](https://en.wikipedia.org/wiki/SO(10)#cite_note-1) among physicists, and derives from the [Lie algebra](https://en.wikipedia.org/wiki/Lie_algebra) or less precisely the [Lie group](https://en.wikipedia.org/wiki/Lie_group) of SO(10), which is a [special orthogonal group](https://en.wikipedia.org/wiki/Special_orthogonal_group) that is [double covered](https://en.wikipedia.org/wiki/Double_covering_group) by Spin(10).

SO(10) subsumes the [Georgi–Glashow](https://en.wikipedia.org/wiki/Georgi%E2%80%93Glashow_model) and [Pati–Salam models](https://en.wikipedia.org/wiki/Pati%E2%80%93Salam_model), and unifies all [fermions](https://en.wikipedia.org/wiki/Fermion) in a [generation](https://en.wikipedia.org/wiki/Generation_(particle_physics)) into a single field. This requires 12 new [gauge bosons](https://en.wikipedia.org/wiki/Gauge_boson), in addition to the 12 of [SU(5)](https://en.wikipedia.org/wiki/Georgi%E2%80%93Glashow_model) and 9 of [SU(4)×SU(2)×SU(2)](https://en.wikipedia.org/wiki/Pati%E2%80%93Salam_model).
- Left: The pattern of [weak isospin](https://en.wikipedia.org/wiki/Weak_isospin), W, weaker isospin, W', strong g3 and g8, and baryon minus lepton, B, charges for particles in the SO(10) model, rotated to show the embedding of the [Georgi–Glashow model](https://en.wikipedia.org/wiki/Georgi%E2%80%93Glashow_model) and [Standard Model](https://en.wikipedia.org/wiki/Standard_Model), with electric charge roughly along the vertical. In addition to Standard Model particles, the theory includes 30 colored X bosons, responsible for [proton decay](https://en.wikipedia.org/wiki/Proton_decay), and two W' bosons.
- Right: The pattern of charges for particles in the SO(10) model, rotated to show the embedding in [E6](https://en.wikipedia.org/wiki/E6_(mathematics)).
- The matter representations come in three copies (generations) of the 16 representation. The Yukawa coupling is 10H 16f 16f. This includes a right-handed neutrino.

It has been long known that the SO(10) model is free from all perturbative local anomalies, computable by Feynman diagrams. However, it only became clear in 2018 that the SO(10) model is also free from all [nonperturbative global anomalies](https://en.wikipedia.org/wiki/Anomaly_(physics)#Witten_anomaly_and_Wang-Wen-Witten_anomaly) on [non-spin manifolds](https://en.wikipedia.org/wiki/Spin_structure) --- an important rule for confirming the consistency of SO(10) grand unified theory, with a Spin(10) gauge group and chiral fermions in the 16-dimensional spinor representations, defined on non-spin manifolds. _([Wikipedia](https://en.wikipedia.org/wiki/SO(10)))_
```

| Syntax | Description | Last |
| ----------- | ----------- | ---- |
| ![download (3)](https://github.com/eq19/maps/assets/8466209/69668b65-0dae-41c1-b9a4-f4ff5dd67aa4) | ![download (4)](https://github.com/eq19/maps/assets/8466209/b15fab38-3ac0-4f11-9824-d995ab9aa5fe) | ![download (2)](https://github.com/eq19/maps/assets/8466209/a4c1a97b-6580-4889-bd37-abe72ce5a294) |

In the spin-foam formalism, the [Barrett–Crane model](https://en.wikipedia.org/wiki/Barrett%E2%80%93Crane_model), which was for a while the most promising state-sum model of 4D Lorentzian quantum gravity

```note
It was [based on representations](https://www.eq19.com/addition/5.html#power-of-magnitude) of the noncompact groups SO(3,1) or SL(2,C), so the spin foam faces (and hence the spin network edges) were labelled by positive real numbers as opposed to the half-integer labels of SU(2) spin networks. _([Wikipedia](https://en.wikipedia.org/wiki/Lorentz_invariance_in_loop_quantum_gravity))_
```

[![41114_2016_3_Equ168](https://github.com/eq19/maps/assets/8466209/561fe8cb-65f6-4050-ab54-3b45392ac897)](https://link.springer.com/article/10.12942/lrr-2013-3)

![41114_2016_3_Equ115](https://github.com/eq19/maps/assets/8466209/db04e836-0f19-48a1-8f1f-cc48c9a52a1b)

The field content of this theory is the massless N = 8 supergravity which comprises the graviton, 8 gravitinos, _[28 vector fields](https://en.wikipedia.org/wiki/N_%3D_8_supergravity)_.

```note
In four spacetime dimensions, N = 8 supergravity, speculated by [Stephen Hawking](https://en.wikipedia.org/wiki/Stephen_Hawking), is the most [symmetric](https://en.wikipedia.org/wiki/Symmetric) quantum field theory which ***involves gravity*** and a finite number of fields.
- It can be found from a [dimensional reduction](https://www.eq19.com/identition/span12/#the-seven-7-groups) of 11D supergravity ***by making the size of seven (7) of the dimensions go to zero***.
- ***It has eight (8) supersymmetries***, which is the most any gravitational theory can have, since there are eight half-steps between spin 2 and spin −2. (The spin 2 graviton is the particle with the highest spin in this theory.)[![eight (8) supersymmetries](https://github.com/eq19/maps/assets/8466209/3796ffd2-465f-44d7-b750-95a092537939)](https://github.com/eq19/maps/files/14229967/0109010.pdf)

- More supersymmetries would mean the particles would have [superpartners](https://en.wikipedia.org/wiki/Superpartner) with spins higher than 2.
- The only theories with ***spins higher than 2 which are consistent*** involve an infinite number of particles (such as String Theory and Higher-Spin Theories).
- _[Stephen Hawking](https://en.wikipedia.org/wiki/Stephen_Hawking) in his [Brief History of Time](https://en.wikipedia.org/wiki/Brief_History_of_Time) speculated that this theory could be the [Theory of Everything](https://en.wikipedia.org/wiki/Theory_of_Everything)_.
- However, in later years this was abandoned in favour of _[string theory](https://en.wikipedia.org/wiki/String_theory)_.
- The theory contains 1 [graviton](https://en.wikipedia.org/wiki/Graviton) (spin 2), 8 [gravitinos](https://en.wikipedia.org/wiki/Gravitinos) (spin 3/2), 28 [vector bosons](https://en.wikipedia.org/wiki/Vector_boson) (spin 1), 56 [fermions](https://en.wikipedia.org/wiki/Fermions) (spin 1/2), 70 [scalar fields](https://en.wikipedia.org/wiki/Scalar_fields) (spin 0) where we don't distinguish particles with negative spin.
- These numbers are simple combinatorial numbers that come from [Pascal's Triangle](https://en.wikipedia.org/wiki/Pascal%27s_Triangle) and also the number of ways of writing n as a sum of 8 nonnegative cubes [A173681](https://oeis.org/A173681).
- One reason why the theory was abandoned was that the 28 vector bosons which form an ***O(8) gauge group is too small*** to contain the standard model U(1) x SU(2) x SU(3) gauge group, which can only fit within the [orthogonal group](https://en.wikipedia.org/wiki/Orthogonal_group) O(10).

There has been renewed interest in the 21st century, with the possibility that string theory may be finite. _([Wikipedia](https://en.wikipedia.org/wiki/N_%3D_8_supergravity))_
```

[![15-Figure1-1](https://github.com/eq19/maps/assets/8466209/3733ba04-0bad-4651-90ee-01afbe319a5f)](https://github.com/eq19/maps/files/14229964/0209128.pdf)

One remarkable property of both [string](https://en.wikipedia.org/wiki/String_theory) and [M-theory](https://en.wikipedia.org/wiki/M-theory) is that ***seven (7) extra dimensions*** are required for the theory's consistency, on top of the four dimensions in our universe.

```note
There exist scenarios in which there could actually be more than [4D of spacetime](https://en.wikipedia.org/wiki/PMNS_matrix). String theories require extra dimensions of spacetime for their mathematical consistency. These are situations where theories in two or three spacetime dimensions are no more useful.

In string theory, spacetime is _[26-dimensional](https://github.com/eq19/maps/files/13904636/0102042.pdf)_, while in superstring theory it is 10-dimensional, and in M-theory it is 11-dimensional.

This classification theorem identifies several infinite families of groups as well as ***26 additional groups*** which do not fit into any family. _([Wikipedia](https://en.wikipedia.org/wiki/String_theory))_
```

![M-Theory](https://github.com/eq19/maps/assets/8466209/30099ac7-71e9-47db-9a57-e00176ddb191)

So the last “Superstring revolution” was impressive but it was close to 30 years ago now - and we still don’t seem to be adopting it as “The Truth”.

```note
M Theory and/or Loop Quantum Gravity hold the promise of ***resolving the conflict between general relativity and quantum mechanics*** but lack experimental connections to predictability in physics.
- A connection is made to these and other theories vying for the title of a “Theory of Everything” by questioning the value of the traditional Planck unit reference point for the scales at which they operate.
- It also suggests a cosmological model which has acceleration as being fundamental.
- It provides for an intuitive understanding of the Standard Model and its relationship to particle masses and the structure of the atom.

The prediction of particle mass and lifetimes is a good indicator for its validity. _([TOE - pdf](https://github.com/eq19/maps/files/14378301/ToE.pdf))_
```

[![string-theory-dimensions](https://github.com/eq19/maps/assets/8466209/ca05f8c9-d90a-4206-9b8b-37454f897fc8)](https://qr.ae/pKBEhD)

We suspect that using that Lorentz, all four have the same complexified Lie algebra. In loop quantum gravity it makes matters [even more](https://en.wikipedia.org/wiki/Lorentz_invariance_in_loop_quantum_gravity) confusing.
