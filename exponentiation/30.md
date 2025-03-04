_[Exponentiation](https://en.wikipedia.org/wiki/Exponentiation)_ is an operation involving two numbers, the 
_[Exponentiation](https://en.wikipedia.org/wiki/Exponentiation)_ is an operation involving two numbers, the base and the exponent or power. Exponentiation is written as ***b<sup>n</sup>***, where ***b*** is the base and ***n*** is the power.

{% include list.liquid all=true %}

Exponentiation zones allows _[multiplication zones](https://www.eq19.com/multiplication/)_ on representing [recursive residues](https://arxiv.org/pdf/1801.07561) by virtualizing _[addition zones](https://www.eq19.com/addition/)_ on top of the original.

## The Root System 

The first appearance of ***e*** in a printed publication was in Euler's [Mechanica](https://en.m.wikipedia.org/wiki/Mechanica) (1736). It is unknown why Euler chose [the letter e](https://youtu.be/R0oUeLQIbIk). 

```note
[Leonhard Euler](https://en.m.wikipedia.org/wiki/Leonhard_Euler) started to use ***the letter e*** for the constant in 1727 or 1728, in an unpublished paper on explosive forces in cannons, and in a letter to [Christian Goldbach](https://en.m.wikipedia.org/wiki/Christian_Goldbach) on 25 November 1731. _([Wikipedia](https://en.wikipedia.org/wiki/E_(mathematical_constant)))_
```

[![Letter e](https://user-images.githubusercontent.com/36441664/262249679-b5d6fc1a-6e42-4775-b09d-965ddd046171.png)](https://en.wikipedia.org/wiki/E_(mathematical_constant))

This exponentiation takes important roles since by the _[multiplication zones](https://www.eq19.com/multiplication/#parsering-structure)_ the MEC30 forms a matrix of  `8 x 8 = 64 = 8²` where the power of 2 stands as exponent

```note
We present a method to increase the dynamical range of a ***Residue Number System (RNS)*** by adding virtual RNS layers on top of the original RNS, where the required modular arithmetic for a modulus on any non-bottom layer is implemented by means of an [RNS Montgomery multiplication algorithm](https://www.google.com/search?q=RNS+Montgomery+multiplication) that uses the RNS on the layer.
- As a result, the actual arithmetic is deferred to the bottom layer. We have presented an improved Bajard-Imbert-type full RNS algorithm that can also operate on inputs represented by pseudo-residues.
- Using this algorithm, we have developed a multi-layer RNS that is ***capable of implementing modular addition, subtraction and multiplication for very large moduli*** by only using actual arithmetic for a fixed set of moduli. If the moduli of this fixed set are sufficiently small, the method allows for a fully table-based implementation.
- In contrast to digit-based implementations of modular operations for large moduli, our method allows for a massively parallel implementation and is completely carry- free, thus thwarting potential attacks exploiting such carries, e.g., with side-channel analysis or in a white-box cryptography context.
- Our system may be considered as a method to provide a given, fixed RNS with a very large dynamical range. To illustrate the method, we have described a 2-layer RNS system that can be used to implement an RSA ***exponentiation by adding the desired RSA modulus on top in a third layer***.
- The system employs 19 moduli of 8-bits each in the bottom layer and can be used to implement an RSA exponentiation for 2048-bits RSA moduli with all the required arithmetic done by table look-up, using 19 modular addition tables and 19 modular multiplication tables, each of these 38 tables having size 2⁸ × 2⁸ × 8 bits, with one modular multiplication taking approximately 160,000 table look-ups.

We further observed that in order to change the RSA modulus, only some constants for computing on the top layer with moduli on the middle layer need to be updated. This update need not be computed in a secure manner and hence can be done quickly. _([Recursive Residues - pdf](https://arxiv.org/pdf/1801.07561))_
```

***π(π(30+37)) = π(π(67)) = π(19) = 8***

```bash
#!/usr/bin/env bash

edit_file () {

  NUM=$(($2 + 0))
  
  while IFS=' ' read -ra SPIN; do
    T+=("${SPIN[0]}")
    R+=("${SPIN[1]}")
    A+=("${SPIN[2]}")
    C+=("${SPIN[3]}")
    K+=("${SPIN[4]}")
    I+=("${SPIN[5]}")
    N+=("${SPIN[6]}")
    G+=("${SPIN[7]}")
  done < /tmp/spin.txt

  FRONT="---\n"
  FRONT+="sort: ${K[$NUM]}\n"
  FRONT+="span: ${I[$NUM]}\n"
  FRONT+="spin: ${N[$NUM]}\n"
  FRONT+="suit: ${G[$NUM]}\n"
  FRONT+="---\n"

  IFS=$'\n' read -d '' -r -a LINE < _Sidebar.md
  TEXT="${LINE[$NUM]}" && TITLE=${TEXT%|*}
  FRONT+="# $TITLE\n\n"

  [[ $NUM -le 9 ]] && sed -i "1s|^|$FRONT|" $1
  if [[ $NUM -lt 2 || $NUM == 9 ]]; then
    mv -f $1 ${1%/*}/README.md
    sed '1,6!d' ${1%/*}/README.md
  fi
}

FILE=${1##*/} && SORT=${FILE%.*}
[[ $SORT =~ ^-?[0-9]+$ ]] && edit_file $1 $SORT
```

These representations are a curious finding. They relate particles to antiparticles by using only the complex conjugate ***i → −i***, they fill these as of _[Euler's Identity](https://www.eq19.com/#identition-zones)_.

```note
Euler's identity is a special case of Euler's formula ***e^ix = cos x + i sin x*** when evaluated for ***x = π***, In addition, it is directly used in a proof that ***π is transcendental***, which implies the impossibility of squaring the circle. _([Wikipedia](https://en.wikipedia.org/wiki/Euler%27s_identity))_
```

[![Euler's identity](https://user-images.githubusercontent.com/8466209/219020102-60b526fd-273d-4c6d-8997-06254bdc5625.png)](https://en.wikipedia.org/wiki/Euler%27s_identity)

Euler angles specify the rotation of the X, Y, and Z rotation axes. The Euler angle is the culprit of the singularities in _[matrix algebra](https://github.com/user-attachments/files/16897487/COmpendium.of.RElations.pdf)_.

```note
In this work we present a matrix generalization of the Euler identity about exponential representation of a complex number. The concept of matrix exponential is used in a fundamental way. We define a notion of matrix imaginary unit which generalizes the usual complex imaginary unit. The Euler-like identity so obtained is compatible with the classical one. Also, we derive some exponential representation for matrix real and imaginary unit, and for the first [Pauli matrix](https://github.com/eq19/maps/files/13818844/math0703448.pdf)
```

[![Spin](https://github.com/eq19/maps/assets/8466209/1addf803-99bf-4af3-914b-3a1116f6bf7a)
](https://www.lancaster.ac.uk/staff/schomeru/lecturenotes/Quantum%20Mechanics/S16.html)

Euler identity present a matrix generalization of the about ***exponential representation*** for matrix real and imaginary unit which compatible with the [Pauli matrix](https://github.com/eq19/maps/files/13818844/math0703448.pdf)

```note
Gell–Mann matrices are to SU(3) what the Pauli matrices are to SU(2). Gell–Mann -matrices are a complete set of Hermitian 3 ⊗ 3 noncommuting trace-orthogonal matrices. They are at the heart of Quantum Chromodynamics (QCD), an integral part of the Standard Model. They are also used in quantum information theory to represent qutrits. _([Wolfram](https://demonstrations.wolfram.com/EverythingAboutGellMannMatricesPart1UnaryOperations/))_
```

[![Everything About Gell Mann Matrices Unary Operations](https://github.com/eq19/maps/assets/8466209/a92606c8-0fc1-4690-be88-7e85a5bc77b5)](https://demonstrations.wolfram.com/EverythingAboutGellMannMatricesPart1UnaryOperations/)

This imaginary unit is particularly important in both mathematics and physics. For example, those [matrices](https://mathworld.wolfram.com/Matrix.html) (and their generalizations) are important in [Lie Theory](https://en.wikipedia.org/wiki/Lie_theory).

```note
As usual, the images ***on the left are snapshots of the particles at different times. Those times correspond to the grey slices in the space-time diagram on the right***. You can see the specific interaction points in the space-time diagram, where the blue particle is emitted and then absorbed by the red particles. _([Slimy.com](http://www.slimy.com/~steuard/research/StringIntro/slide13.html))_
```

[![Feynman diagrams](https://github.com/eq19/maps/assets/8466209/1f5fba0d-4951-4be9-a232-23a1b00b9843)](https://www.eq19.com/multiplication/#physical-movements)

So it will need a gap between each identities to proceed the thing. Let's discuss how it goes by the _[seven (7) hidden dimensions](https://www.eq19.com/identition/#hidden-dimensions)_.

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

In [this paper](https://github.com/eq19/maps/files/13628325/Gellmann.pdf), you may find a way to apply the Gell-Mann transformations made by the λi matrices using Geometric Algebra Cl3,0.

```note
The action of C⊗O on itself can be seen to generate a ***64-complex-dimensional algebra***, wherein we are able to identify two sets of generators for SU(3)c.
- Furthermore, we show that ***these three-generation results can be extended, so as to include all 48 fermionic U(1)em charges***.
- The 64-dimensional octonionic chain algebra splits into ***two sets of SU (3) generators of the form iΛν and −iΛ * ν * , six SU (3) singlets j , six triplets q k , and their complex conjugates***.
- These objects are sectioned off above into four quadrants according to their forms: νaν, ν * aν, νaν * and ν * aν * for a in the chain algebra.
```

![ezgif-4-95200c65b5](https://github.com/eq19/maps/assets/8466209/0d535588-49f7-428c-b119-0f696220253e)

We apply these generators to the rest of the space, and find that it breaks down into the SU(3)c representations of ***exactly three generations of quarks and leptons***.

```note
They are at the heart of Quantum Chromodynamics (QCD), an integral part of the Standard Model. They are also used in ***quantum information*** theory to represent qutrits. _[Gell–Mann matrices](https://github.com/search?q=Gellmann+language%3APython&type=code&l=Python)_ are to SU(3) what the _[Pauli matrices](https://github.com/search?q=Pauli+language%3APython&type=code&l=Python)_ are to SU(2). _([Wolfram](https://demonstrations.wolfram.com/EverythingAboutGellMannMatricesPart1UnaryOperations/))_
```

![Gell-Mann transformations](https://github.com/eq19/maps/assets/8466209/4082d67f-9c41-407c-b0cb-030dbf57765d)

These unifying principles of both mathematics and physics might come in the form of grand unified theories, supersymmetry, string theory, or perhaps something else.

```note
Standard heuristic mathematical models of population dynamics are often constructed using ordinary differential equations (ODEs). These deterministic models yield pre-dictable results which allow researchers to make informed recommendations on public policy. A common immigration, natural death, and fission ODE model is derived from a quantum mechanics view. _([A Quantum Mechanics Approach.pdf](https://github.com/eq19/maps/files/14953912/Coarse_Medium_or_Fine_A_Quantum_Mechanics_Approach.pdf))_
```

[![I15-53-electroweak](https://github.com/eq19/maps/assets/8466209/3c8b96e8-e5fe-47af-8c19-97224d3c918f)](https://www.researchgate.net/publication/343201245_Coarse_Medium_or_Fine_A_Quantum_Mechanics_Approach_to_Single_Species_Population_Dynamics)

Although, at the moment evidence do not have a complete model. However, it becomes a little more clear ***that this unlikely algebra is not going away***.

## Extra Dimensions

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
- ***It has eight (8) supersymmetries***, which is the most any gravitational theory can have, since there are eight half-steps between spin 2 and spin −2. (The spin 2 graviton is the particle with the highest spin in this theory.)

- More supersymmetries would mean the particles would have [superpartners](https://en.wikipedia.org/wiki/Superpartner) with spins higher than 2.
- The only theories with ***spins higher than 2 which are consistent*** involve an infinite number of particles (such as String Theory and Higher-Spin Theories).
- _[Stephen Hawking](https://en.wikipedia.org/wiki/Stephen_Hawking) in his [Brief History of Time](https://en.wikipedia.org/wiki/Brief_History_of_Time) speculated that this theory could be the [Theory of Everything](https://en.wikipedia.org/wiki/Theory_of_Everything)_.
- However, in later years this was abandoned in favour of _[string theory](https://en.wikipedia.org/wiki/String_theory)_.
- The theory contains 1 [graviton](https://en.wikipedia.org/wiki/Graviton) (spin 2), 8 [gravitinos](https://en.wikipedia.org/wiki/Gravitinos) (spin 3/2), 28 [vector bosons](https://en.wikipedia.org/wiki/Vector_boson) (spin 1), 56 [fermions](https://en.wikipedia.org/wiki/Fermions) (spin 1/2), 70 [scalar fields](https://en.wikipedia.org/wiki/Scalar_fields) (spin 0) where we don't distinguish particles with negative spin.
- These numbers are simple combinatorial numbers that come from [Pascal's Triangle](https://en.wikipedia.org/wiki/Pascal%27s_Triangle) and also the number of ways of writing n as a sum of 8 nonnegative cubes [A173681](https://oeis.org/A173681).
- One reason why the theory was abandoned was that the 28 vector bosons which form an ***O(8) gauge group is too small*** to contain the standard model U(1) x SU(2) x SU(3) gauge group, which can only fit within the [orthogonal group](https://en.wikipedia.org/wiki/Orthogonal_group) O(10).

There has been renewed interest in the 21st century, with the possibility that string theory may be finite. _([Wikipedia](https://en.wikipedia.org/wiki/N_%3D_8_supergravity))_
```

[![eight (8) supersymmetries](https://github.com/eq19/maps/assets/8466209/3796ffd2-465f-44d7-b750-95a092537939)](https://github.com/eq19/maps/files/14229967/0109010.pdf)

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

## Standard Model

There is a proof that it is [impossible](https://en.wikipedia.org/wiki/An_Exceptionally_Simple_Theory_of_Everything) to embed all the three generations  in E8 without the presence of additional particles that do not exist in the physical world.

```note
This is a somewhat arbitrary choice, selected for leaving W3 and color invariant. Once the first generation of fermions, with correct charges and spins, are assigned to elements of e8, this T rotates them to the second and third generations.
- The second and third generations only have the correct spins and charges when considered as equivalent under this T. ***When considered as independent fields with E8 quantum numbers, irrespective of this triality relationship, the second and third generation of fields do not have correct charges and spins.***
- The W3 and color charges are invariant under our choice of T but the spins and hypercharges are only correct through triality equivalence. This relationship between fermion generations and triality is the least understood aspect of this theory.
- It is conceivable that there is a more complicated way of assigning three generations of fermions to the E8 roots to get standard model quantum numbers for all three generations without triality equivalence.

There is such an assignment known to the author that gives the correct hypercharges for all three generations, but it is not a triality rotation and it produces unusual spins. A correct description of the relationship between triality and generations, if it exists, awaits a better understanding. _([An Exceptionally  Simple Theory of Everything - pdf](https://github.com/eq19/maps/files/14151110/0711.0770.pdf))_
```

[![An Exceptionally Simple Theory of Everything](https://github.com/eq19/maps/assets/8466209/0e0db7cf-9b02-4719-8521-26bb8973709a)](https://www.researchgate.net/publication/2217412_An_Exceptionally_Simple_Theory_of_Everything)

```note
The matter representations come in three copies (generations) of the 16 representation. The [Yukawa coupling](https://en.wikipedia.org/wiki/Yukawa_coupling) is 10H 16f 16f. ***This includes a right-handed neutrino**". One may either include three copies of [singlet](https://en.wikipedia.org/wiki/Singlet_state) representations φ and a Yukawa coupling (the "double seesaw mechanism"); or else, add the Yukawa interaction or add the [nonrenormalizable](https://en.wikipedia.org/wiki/Nonrenormalizable) coupling. _([Wikipedia](https://en.wikipedia.org/wiki/SO(10)))_
```

[![12648_2023_2718_Figa_HTML](https://github.com/eq19/maps/assets/8466209/b5cbabf1-60f4-4a43-b45e-f005e1460ed4)](https://github.com/eq19/maps/files/14548332/2304.07559.pdf)

Beyond leading approx. we define mGUT as the mass of the heavy 24 gauge bosons, while mT = mHT is the mass of the triplet Higgs.

```note
The cleanest signature for a Higgs sector with triplet fields would be the discovery of [doubly charged](https://www.researchgate.net/publication/13276480_Higgs_triplets_in_the_standard_model) Higgs Bosons. Like Pauli’s bold prediction of the neutrino and GIM’s bold prediction of the charm quark, the equally bold speculation of Kobayashi and Maskawa was proved absolutely correct, when the ***fermions of the third generation*** began to be discovered one by one. First came the tau lepton in 1975, closely followed by the bottom quark in 1977. There followed a 17-year hiatus till the 1994 discovery of the top quark, and another 6 years wait till the existence of the tau neutrino νwas confirmed in 2000.
```

[![24 matriks](https://github.com/eq19/maps/assets/8466209/f37dc9db-2d96-4a1b-884f-83299590cf75)](https://github.com/eq19/maps/files/14414508/kitgut_s_12.pdf)

Is the fermion red? green? blue? Does the fermion have isospin up? down? These five questions can be represented by an exterior algebra of 2⁵ or _[32-complex dimensional](https://github.com/eq19/maps/files/14387513/Standard_model_physics_from_an_algebra.pdf)_.

```note
This thesis constitutes a first attempt to derive aspects of standard model particle physics from little more than an algebra.
-  Here, we argue that physical concepts such as particles, causality, and irreversible time may result from ***the algebra acting on itself***.
- We then focus on a special case by considering the algebra R ⊗ C ⊗ H ⊗ O, the tensor product of the only four normed division algebras over the real numbers.
- ***Using nothing more than R ⊗ C ⊗ H ⊗ O acting on itself***, we set out to find standard model particle representations: a task which occupies the remainder of this text.
- From the C ⊗ H portion of the algebra, we find generalized ideals, and show that ***they describe concisely all of the Lorentz representations of the standard model***.
- From just the C ⊗ O portion of the algebra, we find minimal left ideals, and show that ***they mirror the behaviour of a generation of quarks and leptons under su(3)c and u(1)em***.
- These unbroken symmetries, su(3)c and u(1)em, appear uniquely in this model as particular symmetries of the ***algebra’s ladder operators***. Electric charge, here, is seen to be simply a number operator for the system.
- We then combine the C ⊗ H and C ⊗ O portions of R ⊗ C ⊗ H ⊗ O, and focus on a leptonic subspace, so as to ***demonstrate a rudimentary electroweak model***. Here, the underlying ladder operators are found to have a symmetry generated uniquely by su(2)L and u(1)Y.
- Furthermore, we find that this model yields a straight forward explanation as to why SU(2)L acts only on ***left-handed states***.
- We then make progress towards a three-generation model. The action of C ⊗ O on itself can be seen to generate ***a 64-complex-dimensional*** algebra, wherein we are ***able to identify two sets of generators for SU(3)c***.
- We apply these generators to the rest of the space, and find that it breaks down into the SU(3)c representations of ***exactly three generations of quarks and leptons***.

Furthermore, we show that these three-generation results can be extended, so as to include ***all 48 fermionic U(1)em charges***. _([Standard Model from an algebra - pdf](https://github.com/eq19/maps/files/14387513/Standard_model_physics_from_an_algebra.pdf))_
```

[![The-64-dimensional-octonionic-chain-algebra-splits-into-two-sets-of-SU-3-generators](https://github.com/eq19/maps/assets/8466209/b6fffa01-8eda-46c9-b093-0488336135d2)](https://github.com/eq19/maps/files/14387513/Standard_model_physics_from_an_algebra.pdf)

Subatomic particles such as protons or neutrons, which contain two or more elementary particles, are known as composite particles. 

```note
The Standard Model of Particle Physics, describes for us all know fundamental interaction in nature till date, with the exception of Gravity (work on this front is going on). Here is a summary of the fundamental content of the standard model
- There are three families of particle, the Quarks, the Leptons and the Gauge Bosons. The Quarks in groups of three forms the composite particles such as the Protons, along with the electron this forms ordinary matter.
- The Gauge Bosons are the ones those are responsible for interactions. The Quarks interact among themselves by the exchange of a Gluon these are responsible for the strong nuclear force.
- The newly discovered Higgs Boson interacts with all the Quarks and the first group of Leptons (electron, muon and tau) providing them with their mass. The neutrinos which are the other Leptons originally were thought to have zero mass, but recent discoveries argue that this is not the case.
- The Weak bosons interact with both Leptons and Quarks, these are responsible for the Weak nuclear forces. The exchange of photon is responsible for the Electromagnetic Force.

They interact, they transfer energy and momentum and angular momentum; excitations are created and destroyed. Every excitation that’s possible has a reverse excitation. _([Quora](https://qr.ae/pK4Nd7))_
```

[![fundamental interaction in nature](https://github.com/eq19/maps/assets/8466209/1837fed2-6beb-4ea2-888a-5a2cfbfef311)](https://en.wikipedia.org/wiki/Talk:Standard_Model/Archive_2)

It is hypothesized that gravitational interactions are mediated by an as yet undiscovered elementary particle, dubbed the graviton.

## How many quarks?

Elementary particles and their interactions are considered by a theoretical framework called the [Standard Model (SM) of Particle Physics](https://en.wikipedia.org/wiki/Standard_Model).

```note
The Standard Model presently recognizes ***seventeen distinct particles (twelve fermions and five bosons)***. As a consequence of flavor and color combinations and antimatter, the fermions and bosons are known to have ***48 and 13 variations***, respectively. Among ***the 61 elementary particles*** embraced by the Standard Model number electrons and other leptons, quarks, and the fundamental bosons. _([Wikipedia](https://en.wikipedia.org/wiki/Elementary_particle))_
```

***17 distinct particles = 12 fermions + 5 bosons = 48 + 13 = 61 variations***

[![Standard_Model_of_Elementary_Particles](https://user-images.githubusercontent.com/36441664/274339509-913c39a3-9fdf-4a02-91da-7bc7b746db27.png)](https://www.eq19.com/multiplication/#elementary-structure)

```txt
Answer-1: 3 generation x 3 color x 2 types x 2 each = 36 quarks
```

[![How many types of quarks are there and what are their names?](https://github.com/eq19/maps/assets/8466209/97c8458b-9967-492d-9f68-33b658d30fef)](https://www.toppr.com/ask/en-ch/question/how-many-types-of-quarks-are-there-and-what-are-their-names-404930-1/)

```txt
Answer-2: 6 flavour x 3 colors x 2 types = 36 quarks
```

[![image](https://github.com/eq19/maps/assets/8466209/4842a867-cc3e-425f-9ca6-d1fd497d49f8)](https://www.quora.com/How-many-kinds-of-quarks-are-there-Is-there-anything-smaller-than-a-quark/answer/Arohan-Sharma?ch=15&oid=9122535&share=6f2c7b70&srid=hI1GZ&target_type=answer)

```txt
Answer-3: 6 flavour x 3 colour x 4 bispinor = 72 quarks
```

## There are 72 quarks

```note
In order to be ***[four-spinors](https://en.wikipedia.org/wiki/Dirac_spinor#Four-spinor_for_particles)*** like the electron and other [lepton](https://en.wikipedia.org/wiki/Lepton) components, there must be one quark component for every combination of [flavour](https://en.wikipedia.org/wiki/Flavor_(particle_physics)) and [colour](https://en.wikipedia.org/wiki/Color_charge), ***bringing the total to 24 (3 for charged leptons, 3 for neutrinos, and 2·3·3 = 18 for quarks). Each of these is a four (4) component [bispinor](https://en.wikipedia.org/wiki/Bispinor), for a total of [96 complex-valued components](https://github.com/eq19/maps/files/13796986/NEUTRINOS_Mysterious_Particles_with_Fascinating_Fe.pdf) for the fermion field***. _([Wikipedia](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model))_
```

[![IMG_20240108_045902](https://github.com/eq19/maps/assets/8466209/1ded3458-09fa-4121-95af-9e380cc50392)
](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model)

It is stated that each of the 24 components is a four component bispinor. A bispinor is constructed out 2 simpler component spinor so there are ***eight (8) spinors in total***.

```note
Bispinors are so called because ***they are constructed out of two (2) simpler component spinors, the Weyl spinors***. Each of the two (2) component spinors transform differently under the two (2) distinct complex-conjugate spin-1/2 representations of the Lorentz group. This pairing is of fundamental importance, as it allows the represented particle to have a mass, carry a charge, and represent the flow of charge as a current, and perhaps most importantly, to carry angular momentum. _([Wikipedia](https://en.wikipedia.org/wiki/Bispinor))_
```

***((3+3) + 2x(3x3)) x 4 = (3 + 3 + 18) x 4 = 24 x 4 = 96 components***

```txt
  Fermion  | spinors | charged | neutrinos |   quark   | components
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q)
===========+=========+=========+===========+===========+============
bispinor-1 |    2    |    3    |     3     |    18     |     24
-----------+---------+---------+-----------+-----------+------------ } 48
bispinor-2 |    2    |    3    |     3     |    18     |     24
===========+=========+=========+===========+===========+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24
-----------+---------+---------+-----------+-----------+------------ } 48
bispinor-4 |    2    |    3    |     3     |    18     |     24
===========+=========+=========+===========+===========+============
     Total |    8    |   12    |    12     |    72     |     96
```

Thus fermion is constructed out of eight (8) spinors that brings the total of 96 components consist of ***12 charged leptons, 12 neutrinos and 72 quarks***.

## Free Parameters

The physical evolution of neutrino parameters with respect to energy scale may help elucidate the mechanism for their mass generation.

```note
The most general Lagrangian with massless neutrinos, one finds that the dynamics depend on ***19 parameters***, whose numerical values are established by experiment.

- The 19 certain parameters are summarized below:
[![IMG_20231230_232603](https://github.com/eq19/maps/assets/8466209/2b4f5d82-d000-46f0-91ee-618ff55f01a4)](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model#Free_parameters)
- The neutrino parameter values are still uncertain.
- The value of the [vacuum energy](https://en.wikipedia.org/wiki/Vacuum_energy) (or more precisely, the [renormalization](https://en.wikipedia.org/wiki/Renormalization) scale used to calculate this energy) may also be treated as an additional free parameter.

The renormalization scale may be identified with the [Planck scale](https://en.wikipedia.org/wiki/Planck_scale) or fine-tuned to match the observed [cosmological constant](https://en.wikipedia.org/wiki/Cosmological_constant). However, both options [are problematic](https://en.wikipedia.org/wiki/Cosmological_constant_problem). _([Wikipedia](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model))_
```

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
      |      |     |  6  |                          11s ‹-- ∆28 = (71-43)
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |‹-- ∆9 + ∆18 = ∆27         |
  2   +------|  5* +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) --------------------- ∆32
      |      |  6  +-----+            ‹------------------------------ 15 {0}
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s ‹-- ∆24 = (43-19)
  3*  +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19) ‹-- parameters ✔️    |
      |      |  9  +-----+                           |
      |      |     |  18 | -------------------------- ∆68 - ∆18 = ∆50
------|------|-----+-----+-----  ‹----------------------------------- 30 {+1/2}
```

The Standard Model with massive neutrinos need ***7 more parameters*** (3 masses and 4 [PMNS matrix](https://en.wikipedia.org/wiki/PMNS_matrix) parameters) for a total of _[26 parameters](https://www.eq19.com/multiplication/15.html#parity-order)_.

```note
In principle, there is one further parameter in the Standard Model; the Lagrangian
of QCD can contain a phase that would lead to CP violation in the strong interac-
tion.
- Experimentally, this strong CP phase is known to be extremely small,
 θCP ≃ 0, and is usually taken to be zero.
- If θCP is counted, then the Standard Model has ***26 free parameters***.
- The relatively large number of free parameters is symptomatic of the StandardModel being just that; a model where the parameters are chosen to match the observations, rather than coming from a higher theoretical principle.
- Putting aside θCP, of the 25 SM parameters, 14 are associated with the Higgs field, eight with the
flavour sector and only three with the gauge interactions.

Likewise, ***the coupling constants of the three gauge interactions*** are of a similar order of magnitude, hinting that they might be different low-energy manifestations of a Grand Unified Theory (GUT) of the forces. These patterns provide hints for, as yet unknown, physics beyond the Standard Model. _([Modern Particle Physics - pdf](https://github.com/eq19/maps/files/13800674/Modern-Particle-Physics.pdf))_
```

***(24-5) + (24-17) = 19 + 7 = 26***

```txt
  Fermion  | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19+i5 ✔️
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-2 |    2    |    3    |     3     |    18     |     24     |   17+i7 ✔️
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |     ❓
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-4 |    2    |    3    |     3     |    18     |     24     |     ❓
===========+=========+=========+===========+===========+============+===========
     Total |    8    |   12    |    12     |    72     |     96     |     ❓
```

The first diagram corresponds to the ***first term*** at _[right hand side of equality](https://www.sciencedirect.com/science/article/pii/S0550321321002340#fm1770)_, while the other two diagrams with back-moving lines combine to produce the ***second term***.

```note
We study the anomalous scale [symmetry breaking](https://www.sciencedirect.com/topics/physics-and-astronomy/broken-symmetry) effects on the proton mass in [QCD](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-chromodynamics) due to [quantum fluctuations](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-fluctuation) at ultraviolet scales.
- We confirm that a novel contribution naturally arises as a part of the proton mass, which we call the quantum anomalous energy (QAE). We discuss the QAE origins in both [lattice](https://www.sciencedirect.com/topics/mathematics/lattices) and dimensional [regularizations](https://www.sciencedirect.com/topics/mathematics/regularization) and demonstrate its role as a scheme-and-scale independent component in the mass decomposition.
- We further argue that QAE role in the proton mass resembles a dynamical [Higgs mechanism](https://www.sciencedirect.com/topics/mathematics/higgs-mechanism), in which the anomalous scale symmetry breaking field generates mass scales through its vacuum condensate, as well as its [static](https://www.sciencedirect.com/topics/physics-and-astronomy/statics) and dynamical responses to the valence quarks.
- We demonstrate some of our points in two simpler but closely related [quantum field theories](https://www.sciencedirect.com/topics/mathematics/quantum-field-theory), namely the 1+1 dimensional non-linear sigma model in which QAE is non-perturbative and scheme-independent, and [QED](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-electrodynamics) where the anomalous energy effect is perturbative calculable. 

Dynamical response of the scalar Hamiltonian HS in the presence of the fermion , generating a contribution to the fermion mass _([Scale symmetry breaking - pdf](https://github.com/eq19/maps/files/14183267/1-s2.0-S0550321321002340-main.pdf))_
```

[![1-s2 0-S0550321321002340-gr008_lrg](https://github.com/eq19/maps/assets/8466209/636313e9-fdc9-4555-b704-38ad21fba3a8)](https://www.sciencedirect.com/science/article/pii/S0550321321002340)

The dotted line represents the dynamical Higgs particles h and the crossed circle denotes the scalar Hamiltonian linear in h.

```note
Now we show the interplay of the finite system of prime positions with the ***15 finite even positions*** in the cyclic convolution. Consequently, we only need ***to fold a 30's cycle*** as so that we can identify the opposite prime positions that form their specific pairs in a specific convolution.
```

***13+17 = 11+19 = 30***

```txt
  Fermion  | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19+i5 
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-2 |    2    |    3    |     3     |    18     |     24     |   17+i7
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |   11+i13 ✔️
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-4 |    2    |    3    |     3     |    18     |     24     |     ❓
===========+=========+=========+===========+===========+============+===========
     Total |    8    |   12    |    12     |    72     |     96     |     ❓
```

The coupling g between the Higgs field and the fermion is proportional to fermion mass. 

## The Seven (7) Groups

Let's consider a prime spin theory of compactifying the 7-dimensional manifold on the 3-sphere of a fixed radius and study its [dimensional reduction](https://en.wikipedia.org/wiki/Dimensional_reduction
) to 4D.

```note
We now place integers sequentially into the lattice with a simple rule: ***Each time a prime number is encountered, the spin or ‘wall preference’ is switched***.

[![19 abuts 2](https://github.com/eq19/maps/assets/8466209/b9cef585-fcef-4090-ad5e-e820ecb29ceb)](https://www.hexspin.com/defining-the-prime-hexagon/)

So, from the first cell, exit from 2’s left side. This sets the spin to left and the next cell is 3, a prime, so switches to right. 4 is not prime and continues right. 5 is prime, so switch to left and so on. ***There are twists and turns until 19 abuts 2***. _([HexSpin](https://www.hexspin.com/defining-the-prime-hexagon/))_
```

[![Defining the Prime Hexagon](https://github.com/eq19/maps/assets/8466209/36aeac77-ecb2-4c94-b2ea-fe0f8b7e391c)](https://www.hexspin.com/defining-the-prime-hexagon/)

In our approach a 3-form is not an object that exist in addition to the metric, it is the only object that exist and in particular ***[the 4D metric, is defined by the 3-form](https://www.eq19.com/identition/span12/#three-3-layers)***.

```note
We would like to say that our present use of G2 structures (3-forms in 7D) is different from what
one can find in the literature on Kaluza–Klein compactifications of supergravity.
- We show that the resulting 4D theory is (Riemannian) [General Relativity](https://www.sciencedirect.com/topics/physics-and-astronomy/general-relativity) (GR) in Plebanski formulation, modulo corrections that are negligible for curvatures smaller than Planckian.
- Possibly the most interesting point of this construction is that the dimensionally reduced theory is GR with a non-zero cosmological constant, and the value of the cosmological constant is directly related to the size of . Realistic values of Λ correspond to of Planck size.

Also, in the supergravity context a 7D manifold with a G2 structure is used for compactifying the 11D supergravity down to 4D. In contrast, we compactify from 7D to 4D. _([General relativity from three-forms in seven dimensions - pdf](https://github.com/eq19/maps/files/14064088/1-s2.0-S0370269317304926-main.pdf))_
```

![Standard Spin](https://github.com/eq19/maps/assets/8466209/705213d6-00e3-4130-9b06-adfb8d06c110)

The complete theory was obtained by [dimensional reduction](https://en.wikipedia.org/wiki/Dimensional_reduction
) of the 11D supergravity on a seven (7) torus and realizing the exceptional symmetry group E7(7)

```note
In particular, these theories include the compactification of eleven-dimensional supergravity on the seven-sphere S7, which gives rise to a ***[four-dimensional theory](https://www.eq19.com/identition/span12/#the-four-4-dimensions)*** with compact non-abelian gauge group SO(8) _([11D Supergravity and Hidden Symmetries - pdf](https://github.com/eq19/maps/files/14126154/2303.12682.pdf))_
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f
------+------+-----+---------
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
      |      |     |  6  |                          11s ✔️
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
      |      |  6  +-----+        <----------------  strip
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s ✔️
  3   +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | --------------------------
------|------|-----+-----+------
```

The most general Lagrangian with massless neutrinos, one finds that the dynamics depend on ***19 parameters***, whose numerical values are established by experiment.

```note
Straight forward extensions of the Standard Model with massive neutrinos need 7 more parameters (3 masses and 4 PMNS matrix parameters) for a total of [26 parameters](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model#cite_note-Thomson499-15). The neutrino parameter values are still uncertain. The 19 certain parameters are summarized here:

[![IMG_20231230_232603](https://github.com/eq19/maps/assets/8466209/2b4f5d82-d000-46f0-91ee-618ff55f01a4)](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model#Free_parameters)

- The choice of free parameters is somewhat arbitrary. In the table above, gauge couplings are listed as free parameters, therefore with this choice the Weinberg angle is not a free parameter.
- Instead of fermion masses, dimensionless Yukawa couplings can be chosen as free parameters. For example, the electron mass depends on the Yukawa coupling of the electron to the Higgs field.
- The value of the [vacuum energy](https://en.wikipedia.org/wiki/Vacuum_energy) (or more precisely, the [renormalization](https://en.wikipedia.org/wiki/Renormalization) scale used to calculate this energy) may also be treated as ***an additional free parameter***.
- The renormalization scale may be identified with the [Planck scale](https://en.wikipedia.org/wiki/Planck_scale) or fine-tuned to match the observed [cosmological constant](https://en.wikipedia.org/wiki/Cosmological_constant). However, both options [are problematic](https://en.wikipedia.org/wiki/Cosmological_constant_problem).

As these theories tend to reproduce the entirety of current phenomena, the question of which theory is the right one, or at least the "best step" towards a [Theory of Everything](https://en.wikipedia.org/wiki/Theory_of_Everything), can only be settled via experiments _([Wikipedia](https://en.wikipedia.org/wiki/Mathematical_formulation_of_the_Standard_Model))_
```

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
      |      |  6  +-----+        <----------------  strip
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |       extra
      |      |     |  15 |                           7s  <-- parameters ✔️
  3   +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+           certain         |
      |  6   |     |  17 | (19)  <-- parameters ✔️   |
      |      |  9  +-----+                           |
      |      |     |  18 | --------------------------
------|------|-----+-----+------
```

Please note that we are not talking about the number 19 which is the ***8th-prime***. Here we are talking about 19th as sequence follow backward position of the 18th.

```tip
The same number of 7 vs 11 dimensions as we have discussed are hold by 7 primes vs 11 natural numbers in every first term of the prime spin. Consider the following:
- the prime 19 is not counted on the first term since it is taking the position of number 1 which is not prime, this prime takes it place only on the second term,
- assume the number 1 is still in its position then the 18 would be the quantity of all numbers so it is eligible as the origin position of zero,
- thus there are π(17) or ***7 primes*** with red color plus ***11 natural*** numbers (including the number 1) with black color and consequently 18 is the sum of 7 and 11,
- so by the concept of prime identity, this 7 vs 11 scheme of dimensions is originated from the behaviour of both 19 and 18,
- the prime is fewer than the natural so the 7 prime cycle is always happen in every first term followed by 11 composite cycle (see our side menu).

The further terms will only have their specific meaning when they are formed in the favor of _[True Prime Pairs](https://www.eq19.com/addition/2.html)_ which we called as ***Δ(19 vs 18) Scenario***
```

![Δ(19 vs 18) Scenario](https://user-images.githubusercontent.com/36441664/274093531-0878e3e5-6be3-448e-9ad4-3b34523c1e9c.jpg)

Symmetry breaking in Quantum Field Theory (QFT) applies to the scalar field, at first so that it can have an impact and give mass to gauge bosons and fermions.

```note
In QFT this is currently done by manually adding an extra term to the field's self-interaction, creating the famous ***Mexican Hat*** potential well.
- In QFT the scalar field generates _[four (4) Goldstone bosons](https://en.wikipedia.org/wiki/Goldstone_boson)_.
- ***One (1) of the 4 turns into the Higgs boson***. Unlike popularized, the Higgs itself does not give mass to particles, but represents the symmetry broken scalar field.
- The other three (3) Goldstone bosons are "absorbed" by the ***three (3) intermediate, electroweak bosons (W+, W-, Z), giving them an extra spin***.

This (otherwise) plain and featureless "absorbtion" of the Goldstone modes in the EW field could be a reason why a complex, synergy-creating quality of the scalar field is largely unnoticed in QFT. Obviously this has the potential to become a new research challenge in physics. _([TGMResearch](http://science.trigunamedia.com/geometry-and-topology/index.htm))_
```

![sterile_neutrino_does_not_exist](https://github.com/eq19/maps/assets/8466209/116182d5-aca1-4e84-bb34-6e80d1a7d06a)

The greatest problem in theoretical physics is combining the general relativity with quantum mechanics. Actually it is related to a non-standard renormalization. 

```note
A lot number of positive color-charges move from the positive charged particle toward the negative charged particles, and negative color-charges move from negative charged particle toward the positive charged particle and they combine in each other.
- According to CPH Theory, gravity is a currency among the objects. Consider the interaction between the earth and the moon: when a graviton reaches the earth, the other one moves toward the moon and pushes the earth toward the moon.
- Because as to maintain equality times - positive and negative color-charges, there is a fixed ratio between the mass and the number of gravitons surrounding.
- Also when a graviton reaches the moon, the other one moves toward the earth and  pushes the moon toward the earth.
-So earth (In fact everything) is bombarded by gravitons continuously.

Due to the fact that everything is made up of sub quantum energy, the classical concept of acceleration and relativistic Newton's second law needs to be reviewed. _([Gravity in Time space - pdf](https://github.com/eq19/maps/files/13950511/Descriptiongravityinteractwithspace-timeatthequantumlevel.pdf))_
```

[![A-lot-number-of-positive-color-charges-move-from-the-positive-charged-particle-toward-the](https://github.com/eq19/maps/assets/8466209/cab50da0-531b-4e00-a18b-89f5151fcfe4)](https://www.linkedin.com/pulse/mechanism-transform-energy-from-strong-weak-nuclear-force-javadi)

Renormalization was first developed in [quantum electrodynamics](https://en.wikipedia.org/wiki/Quantum_electrodynamics) (QED) to make sense of [infinite](https://en.wikipedia.org/wiki/Infinity) integrals in [perturbation theory](https://en.wikipedia.org/wiki/Perturbation_theory_(quantum_mechanics)).

```note
Renormalization is a collection of techniques in [quantum field theory](https://en.wikipedia.org/wiki/Quantum_field_theory), [statistical field theory](https://en.wikipedia.org/wiki/Statistical_field_theory), and the theory of [self-similar](https://en.wikipedia.org/wiki/Self-similarity) geometric structures, that are used to treat [infinities](https://en.wikipedia.org/wiki/Infinity) arising in calculated quantities by altering values of these quantities to compensate for effects of their self-interactions. _([Wikipedia](https://en.wikipedia.org/wiki/Renormalization))_
```

![0_5540_t3k8UUhCxaU](https://github.com/eq19/maps/assets/8466209/360ca110-8e3c-4a6b-b86e-54a1b51b7727)

The problem is raised when the non-standard renormalization _[hides](https://www.sciencedirect.com/science/article/pii/S0550321321002340)_ the scheme and scale-independent quantum anomalous energy (QAE) contribution in the mass.

```note
In this paper we have studied the renormalization of the QCD trace anomaly separately for the quark and gluon parts of the energy momentum tensor.
- While the renormalization of the total anomaly T = Tq + Tg is well understood in the literature [10], our analysis at ***the quark and gluon level has revealed some interesting new features***. The bare and renormalized (Tq,g)α differ by finite operators, and this difference can be systematically computed order by order in αs.
- It is interesting to notice that, at one loop, the renormalized Tq gives the nf part of the beta function. However, ***this property no longer holds at two-loop***, see (5.19).
- Besides, the partition of ***the total anomaly can be different*** if one uses other regularization schemes (see, e.g., the ‘gradient flow’ regularization [25]), and it is interesting to study their mutual relations.

We have also found that C¯q,g(µ) ***does not go to zero as µ → ∞ even in the chiral limit, contrary to what one would naively expect*** from the one-loop calculation (3.16). _([Quark and gluon contributions to the QCD trace anomaly - pdf](https://github.com/eq19/maps/files/14226905/JHEP12.2018.008.pdf))_
```

***(24-5) + (24-17) = 19 + 7 = 26***

```txt
The True Prime Pairs:
(5,7), (11,13), (17,19)

|--------------- 7¤ ---------------|👈
|-------------- {89} --------------|
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|  5 |  7 | 11 |{13}| 17 | 19 | 17 |{12}| 11 | 19 |{18}| 18 | 12 |{13}|
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
                         |---- {48} ----|---- {48} ----|---- {43} ----|
                         |----- 3¤ -----|----- 3¤ -----|----- 3¤ -----|
                         |-------------------- 9¤ --------------------|👈

  Fermion  | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19+i5
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-2 |    2    |    3    |     3     |    18     |     24     | 👉17+i7
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |   11+i13👈
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-4 |    2    |    3    |     3     |    18     |     24     |   19+i5
===========+=========+=========+===========+===========+============+===========
     Total |    8    |   12    |    12     |    72     |     96     |   66+i30
```

In order to explain the generation process of gravitational energy between two identical sign charged particles, it is necessary to explain the process of the generated ***electromagnetic energy*** by the interaction of their electrical repulsion.

```note
In quantum mechanics, the graviton is a hypothetical elementary particle that mediates the force of gravitation in the framework of quantum field theory. If it exists, the graviton must be  massless and must have a spin of 2. This is because the source of gravitation is the stress-energy tensor, a second-rank tensor. This definition of graviton is not able to describe gravitational phenomena, so we need a new definition of graviton. _([What is CPH Theory - pdf](https://www.researchgate.net/publication/309153372_What_is_CPH_Theory))_
```

![A-schematic-illustration-of-how-quantum-gravity-emerges-in-an-information-based-theory-of](https://github.com/eq19/maps/assets/8466209/9ab1b0c8-ca84-49c5-8780-89c083c1b6cd)

The physical evolution of neutrino parameters with respect to energy scale may help elucidate the mechanism for their mass generation.

```note
We study the anomalous scale [symmetry breaking](https://www.sciencedirect.com/topics/physics-and-astronomy/broken-symmetry) effects on the proton mass in [QCD](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-chromodynamics) due to [quantum fluctuations](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-fluctuation) at ultraviolet scales.
- We confirm that a novel contribution naturally arises as a part of the proton mass, which we call the quantum anomalous energy (QAE). We discuss the QAE origins in both [lattice](https://www.sciencedirect.com/topics/mathematics/lattices) and dimensional [regularizations](https://www.sciencedirect.com/topics/mathematics/regularization) and demonstrate its role as a scheme-and-scale independent component in the mass decomposition.
- We further argue that QAE role in the proton mass resembles a dynamical [Higgs mechanism](https://www.sciencedirect.com/topics/mathematics/higgs-mechanism), in which the anomalous scale symmetry breaking field generates mass scales through its vacuum condensate, as well as its [static](https://www.sciencedirect.com/topics/physics-and-astronomy/statics) and dynamical responses to the valence quarks.
- We demonstrate some of our points in two simpler but closely related [quantum field theories](https://www.sciencedirect.com/topics/mathematics/quantum-field-theory), namely the 1+1 dimensional non-linear sigma model in which QAE is non-perturbative and scheme-independent, and [QED](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-electrodynamics) where the anomalous energy effect is perturbative calculable. 

Dynamical response of the scalar Hamiltonian HS in the presence of the fermion , generating a contribution
to the fermion mass The dotted line represents the dynamical Higgs particles h and the crossed circle denotes the scalar Hamiltonian linear in h. The coupling g between the Higgs field and the fermion is proportional to fermion mass. _([Scale symmetry breaking - pdf](https://github.com/eq19/maps/files/14183267/1-s2.0-S0550321321002340-main.pdf))_
```

[![1-s2 0-S0550321321002340-gr008_lrg](https://github.com/eq19/maps/assets/8466209/636313e9-fdc9-4555-b704-38ad21fba3a8)](https://www.sciencedirect.com/science/article/pii/S0550321321002340)

The first diagram corresponds to the ***first term*** at _[right hand side of equality](https://www.sciencedirect.com/science/article/pii/S0550321321002340#fm1770)_, while the other two diagrams with back-moving lines combine to produce the ***second term***.

## The Quantum Gravity

By [True Prime Pars](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#true-prime-pairs) we shall take **36 nodes** to conjugate partitions. So the most possible way is taking the 3rd layer which hold the sum 36 of prime pair 19 and 17.

```note
A chiral phenomenon is one that is not identical to its [mirror image](https://en.wikipedia.org/wiki/Mirror_image) (see the article on [mathematical chirality](https://en.wikipedia.org/wiki/Chirality_(mathematics))). The [spin](https://en.wikipedia.org/wiki/Spin_(physics)) of a [particle](https://en.wikipedia.org/wiki/Elementary_particle) may be used to define a handedness, or helicity, for that particle, which, in the case of a massless particle, is the same as chirality. A [symmetry transformation](https://en.wikipedia.org/wiki/Symmetry_transformation) between the two is called [parity](https://en.wikipedia.org/wiki/Parity_(physics)) transformation. Invariance under parity transformation by a [Dirac fermion](https://en.wikipedia.org/wiki/Dirac_fermion) is called chiral symmetry.
- For massless particles – photons, gluons, and (hypothetical) gravitons – chirality is the same as helicity; a given massless particle appears to [spin](https://en.wikipedia.org/wiki/Spin_(physics)) in the same direction along its axis of motion regardless of point of view of the observer.
- For massive particles – such as electrons, quarks, and neutrinos – chirality and helicity must be distinguished: In the case of these particles, it is possible for an observer to change to a reference frame moving faster than the spinning particle, in which case the particle will then appear to move backwards, and its helicity (which may be thought of as "apparent chirality") will be reversed. That is, helicity is a constant of motion, but it is not Lorentz invariant. Chirality is Lorentz invariant, but is not a constant of motion: a massive left-handed spinor, when propagating, will evolve into a right handed spinor over time, and vice versa.
- A massless particle moves with the speed of light, so no real observer (who must always travel at less than the speed of light) can be in any reference frame where the particle appears to reverse its relative direction of spin, meaning that all real observers see the same helicity. Because of this, the direction of spin of massless particles is not affected by a change of inertial reference frame (a Lorentz boost) in the direction of motion of the particle, and the sign of the projection (helicity) is fixed for all reference frames: The helicity of massless particles is a relativistic invariant (a quantity whose value is the same in all inertial reference frames) which always matches the massless particle's chirality.

The discovery of neutrino oscillation implies that neutrinos have mass, so the photon is the only confirmed massless particle; gluons are expected to also be massless, although this has not been conclusively tested.[b] Hence, these are the only two particles now known for which helicity could be identical to chirality, and only the photon has been confirmed by measurement. All other observed particles.
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

+----+----+----+----+----+-👇-+
|  5 |  7 | 11 |{13}| 17 | 19 |
+----+----+----+----+----+----+
|------------ {72} -----------|
|------------- 6¤ ------------|

The Fermion Fields
(19,17,i12), (11,19,i18), (18,12,i13)

+-👇-+----+----+----+----+----+----+----+----+
| 19 | 17 |{12}| 11 | 19 |{18}| 18 | 12 |{13}|
+----+----+----+----+----+----+----+----+----+
|---- {48} ----|---- {48} ----|---- {43} ----|
|------------ {96} -----------|----- 3¤ -----|

Spontaneous Symmetry Breaking:
(5,7), (11,13,17) , (19,17,12), (11,19,18), (18,12,13)

|--------------- 7¤ ---------------|
|-------------- {89} --------------|
+----+----+----+----+----+-👇-+-👇-+----+----+----+----+----+----+----+
|  5 |  7 | 11 |{13}| 17 | 19 | 17 |{12}| 11 | 19 |{18}| 18 | 12 |{13}|
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
                         |-- {36} -|------ {60} -------|---- {43} ----|
                         |--- 2¤ --|------- 4¤ --------|----- 3¤ -----|
                         |-------------------- 9¤ --------------------|
```

The ***first term*** will directly be identified as a forward moving diagram for external mψψ¯ insertion, while the ***second term*** corresponds to the combination of [two backward](https://www.sciencedirect.com/science/article/pii/S0550321321002340) moving diagrams using the relation in energy denominators.

```note
The helicity of a particle is positive ("right-handed") if the direction of its [spin](https://en.wikipedia.org/wiki/Spin_(physics)) is the same as the direction of its motion. It is negative ("left-handed") if the directions of spin and motion are opposite. So a standard [clock](https://en.wikipedia.org/wiki/Clock), with its spin vector defined by the rotation of its hands, has left-handed helicity if tossed with its face directed forwards.
- Mathematically, helicity is the sign of the projection of the [spin](https://en.wikipedia.org/wiki/Spin_(physics)) [vector](https://en.wikipedia.org/wiki/Vector_(geometric)) onto the [momentum](https://en.wikipedia.org/wiki/Momentum) [vector](https://en.wikipedia.org/wiki/Vector_(geometric)): ***"left" is negative, "right" is positive.
have mass and thus may have different helicities in different reference frames***.
- Chiral theories: Particle physicists have only observed or inferred left-chiral fermions and right-chiral antifermions engaging in the charged weak interaction.[1] In the case of the weak interaction, which can in principle engage with both left- and right-chiral fermions, only two left-handed fermions interact. Interactions involving right-handed or opposite-handed fermions have not been shown to occur, ***implying that the universe has a preference for left-handed chirality***. This preferential treatment of one chiral realization over another violates parity, as first noted by Chien Shiung Wu in her famous experiment known as the Wu experiment. This is a striking observation, since parity is a symmetry that holds for all other fundamental interactions.
- Chirality for a Dirac fermion ψ is defined through the operator γ5, which has eigenvalues ±1; the eigenvalue's sign is equal to the particle's chirality: +1 for right-handed, −1 for left-handed. Any Dirac field can thus be projected into its ***left- or right-handed*** component by acting with the projection operators.[![Right_left_helicity svg](https://github.com/eq19/maps/assets/8466209/6a9a0f44-a1ed-41e5-878f-62948c19d9de)](https://en.wikipedia.org/wiki/Left-right_model)
- The coupling of the charged weak interaction to fermions is proportional to the first projection operator, which is responsible for this interaction's parity symmetry violation.
- A common source of confusion is due to conflating the γ5, chirality operator with the helicity operator. Since the helicity of massive particles is frame-dependent, it might seem that the same particle would interact with the weak force according to one frame of reference, but not another. The resolution to this paradox is that the chirality operator is equivalent to helicity for massless fields only, for which helicity is not frame-dependent. By contrast, for massive particles, chirality is not the same as helicity, or, alternatively, helicity is not Lorentz invariant, so there is no frame dependence of the weak interaction: a particle that couples to the weak force in one frame does so in every frame.
- A theory that is asymmetric with respect to chiralities is called a chiral theory, while a non-chiral (i.e., parity-symmetric) theory is sometimes called a vector theory. Many pieces of the Standard Model of physics are non-chiral, which is traceable to anomaly cancellation in chiral theories. Quantum chromodynamics is an example of a vector theory, since both chiralities of all quarks appear in the theory, and couple to gluons in the same way.
- ***The electroweak theory, developed in the mid 20th century, is an example of a chiral theory***. Originally, it assumed that neutrinos were massless, and assumed the existence of only left-handed neutrinos and right-handed antineutrinos. After the observation of neutrino oscillations, which imply that neutrinos are massive (like all other fermions) the revised theories of the electroweak interaction now include both right- and left-handed neutrinos. However, it is still a chiral theory, as it does not respect parity symmetry.
- The exact nature of the neutrino is still unsettled and so the electroweak theories that have been proposed are somewhat different, but most accommodate the chirality of neutrinos in the same way as was already done for all other fermions.

By Chiral symmetry the Vector gauge theories with massless Dirac fermion fields ψ exhibit chiral symmetry, i.e., rotating the left-handed and the right-handed components independently makes no difference to the theory. We can write this as the action of rotation on the fields:
```

![Symmetry State](https://github.com/eq19/maps/assets/8466209/70cb2eb0-0955-4d18-8400-e05ac1b9d325)

The Standard Model with massive neutrinos need ***7 more parameters*** (3 [CKM](https://en.wikipedia.org/wiki/Cabibbo%E2%80%93Kobayashi%E2%80%93Maskawa_matrix) and 4 [PMNS matrix](https://en.wikipedia.org/wiki/PMNS_matrix) parameters) for a total of _[26 parameters](https://www.eq19.com/multiplication/15.html#parity-order)_. By our concept these 7 parameters correspond to ***π(17) = 7 prime identities*** of _[additional zones](https://www.eq19.com/addition)_.

```note
Massive fermions do not exhibit chiral symmetry, as the mass term in the [Lagrangian](https://en.wikipedia.org/wiki/Lagrangian_(field_theory)), mψψ, breaks chiral symmetry explicitly.
- [Spontaneous chiral symmetry breaking](https://en.wikipedia.org/wiki/Chiral_symmetry_breaking) may also occur in some theories, as it most notably does in [quantum chromodynamics](https://en.wikipedia.org/wiki/Quantum_chromodynamics).
- The chiral symmetry transformation can be divided into a component that treats the left-handed and the right-handed parts equally, known as vector symmetry, and a component that actually treats them differently, known as axial symmetry.[[2]](https://en.wikipedia.org/wiki/Chirality_(physics)#cite_note-5) (cf. [Current algebra](https://en.wikipedia.org/wiki/Current_algebra).) A scalar field model encoding chiral symmetry and its [breaking](https://en.wikipedia.org/wiki/Chiral_symmetry_breaking) is the [chiral model](https://en.wikipedia.org/wiki/Chiral_model).
- The most common application is expressed as equal treatment of clockwise and counter-clockwise rotations from a fixed frame of reference.

The general principle is often referred to by the name chiral symmetry. The rule is absolutely valid in the [classical mechanics](https://en.wikipedia.org/wiki/Classical_mechanics) of [Newton](https://en.wikipedia.org/wiki/Isaac_Newton) and [Einstein](https://en.wikipedia.org/wiki/Albert_Einstein), but results from [quantum mechanical](https://en.wikipedia.org/wiki/Quantum_mechanics) experiments show a difference in the behavior of left-chiral versus right-chiral [subatomic particles](https://en.wikipedia.org/wiki/Subatomic_particles). _([Wikipedia](https://en.wikipedia.org/wiki/Left-right_model))_
```

***1 + 77 = 78 = 3 copies of 26-dimensions***

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

+----+----+----+----+----+-👇-+
|  5 |  7 | 11 |{13}| 17 | 19 |
+----+----+----+----+----+----+
|------------ {72} -----------|
|------------- 6¤ ------------|

Spontaneous Symmetry Breaking:
(5,7), (11,13,17) , (19,17,12), (11,19,18), (18,12,13)

|--------------- 7¤ ---------------|
|-------------- {89} --------------|
+----+----+----+----+----+-👇-+-👇-+----+----+----+----+----+----+----+
|  5 |  7 | 11 |{13}| 17 | 19 | 17 |{12}| 11 | 19 |{18}| 18 | 12 |{13}|
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
                         |-- {36} -|------ {60} -------|---- {43} ----|
                         |--- 2¤ --|------- 4¤ --------|----- 3¤ -----|
                         |-------------------- 9¤ --------------------|

|--------------- 7¤ ---------------|
|-------------- {89} --------------|
+----+----+----+----+----+-💢-+----+----+----+----+----+----+----+----+
|  5 |  7 | 11 |{13}| 17 | 19 | 17 |{12}| 11 | 19 |{18}| 18 | 12 |{13}|
+----+----+----+----+----+----+----+----+-👇-+----+----+----+----+----+
                         |-👇-|--------- {77} ---------|---- {43} ----|✔️
                         |-1¤ |---------- 5¤ ----------|----- 3¤ -----|
                         |-------------------- 9¤ --------------------|
```

The first term forms the photonic contribution while the second term is the fermionic contribution (two backward). The first backward is correspond to the three (3) known neutrino flavors: the electron-, muon- and tau-neutrino which are left-handed.

```note
Summary of various critical points in the context of superpotential observed in this paper first : Gauge symmetry, supersymmetry, vacuum expectation value of field, superpotential and cosmological constants.
- For SO(3)+ × SO(5)+ case, one can check it by the change of variable of SO(5)+×SO(3)+ case, s → −3s/5 that corresponding potential of SO(3)+×SO(5)+ is obtained while by change of variable, s → −s/7, the potential of SO(1)+ × SO(7)+ can be found from SO(7)+ × SO(1)+ case.
- Although the corresponding superpotential of these two cases may be different from the original ones, the scalar potentials are the same.
- It is natural to ask whether 11-dimensional embedding of various vacua we have considered of
 non-compact and non-semi-simple gauged supergravity can be obtained.
- In a recent paper [46],
 the metric on the 7-dimensional internal space and domain wall in 11-dimensions was found.
 However, they did not provide an ansatz for an 11-dimensional three-form gauge field.
-It would
 be interesting to study the geometric superpotential, 11-dimensional analog of superpotential
we have obtained.

We expect that the nontrivial r-dependence of vevs makes Einstein-Maxwell
 equations consistent not only at the critical points but also along the supersymmetric RG flow
 connecting two critical points. _([N = 8 Supergravity: Part I - pdf](https://github.com/eq19/maps/files/14229967/0109010.pdf))_
```

[![Symmetry Breaking](https://github.com/eq19/maps/assets/8466209/80bb1b09-e1d4-479a-b570-815786058b04)](https://www.eq19.com/multiplication/20.html#strand-partition)

Taking 19 as a certain parameter we can see that the left handed cycles are happen on ***5th-spin*** (forms 4th hexagon, purple) and ***6th-spin*** (forms 5th hexagon, cyan). Both have different rotation with other spin below 9th spin (forms 6th hexagon, yellow).

```note
Proceeding, the number line begins to coil upon itself; 20 lands on 2’s cell, 21 on 3’s cell. Prime number 23 sends the number line left to form the fourth (4th) hexagon, purple. As it is not a twin, the clockwise progression (rotation) reverses itself. Twin primes ***29 and 31 define the fifth (5th) hexagon***, cyan. Finally, 37, again not a twin, reverses the rotation of the system, so 47 can define the yellow hexagon _([HexSpin](https://www.hexspin.com/defining-the-prime-hexagon/))_.
```

***7th spin - 4th spin = (168 - 102)s = 66s = 6 x 11s = 30s + 36s***

![IMG_20231221_074421](https://github.com/eq19/maps/assets/8466209/1e7dc443-b7d8-44d9-8da0-5fe50dd7ee70)

Thus it appears that the [cosmological models](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7897631/#RSPA20200786C24)] derived from compactification of 11d supergravity on a manifold with [G2 holonomy](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7897631/) have some ***[hidden E7 symmetry](https://www.eq19.com/identition/span12/#the-seven-7-groups).***

```note
There are `14 + 7 × 16 = 126` integral octonions. It was [shown](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7897631/#RSPA20200786C33) that the set of transformations which preserve the octonion algebra of [the root system of E7](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7897631/#RSPA20200786M5x4) is the adjoint Chevalley group G2(2). It is possible to decompose these 126 imaginary octonions into ***eighteen (18) sets of seven (7) imaginary octonionic units*** that can be transformed to each other by the finite subgroup of matrices. These lead to 18 sets of 7, which we see in figures [​figure-77](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7897631/figure/RSPA20200786F7/) and [​figure-88](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7897631/figure/RSPA20200786F8/). _([M-theory, Black Holes and Cosmology - pdf](https://github.com/eq19/maps/files/14207670/2009.11339.pdf))_
```

```txt
  Fermion  | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19
-----------+---------+---------+-----------+-----------+------------+-- 17💢36
bispinor-2 |    2    |    3    |     3     |    18     |     24     |   i12 ✔️
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |   11
-----------+---------+---------+-----------+-----------+------------+-- 19💢30
bispinor-4 |    2    |    3    |     3     |    18     |     24     |   i18 ✔️
===========+=========+=========+===========+===========+============+===========
  SubTotal |    8    |   12    |    12     |    72     |     96     |   66+i30
===========+=========+=========+===========+===========+============+===========
```

By the _[Δ(19 vs 18) Scenario](https://www.eq19.com/identition/span12/#the-seven-7-groups)_ those three are exactly landed in the ***0's cell*** out of Δ18. See that the sum of 30 and 36 is 66 while the difference between 36 and 102 is also 66.

```note
You likely noticed I began with 2 rather than 1 or 0 when I first constructed the hexagon. Why? Because they do not fit inside — they stick off the hexagon like a tail. Perhaps that’s where they belong. However, if one makes a significant and interesting assumption, then 1 and 0 fall in their logical locations – in the 1 and 0 cells, respectively. _([HexSpin](https://www.hexspin.com/0-1-and-negative-numbers/))
```

***0 + 30 + 36 + 102 = 168 = π(1000)***

[![0, 1 and negative numbers](https://github.com/eq19/maps/assets/8466209/19f68eca-c0e1-48fc-9c9a-60d01cf26057)](https://www.hexspin.com/0-1-and-negative-numbers/)

By defining the pattern on each individual numbers against _[homogeneous sorting](https://gist.github.com/eq19/c9bdc2bbe55f2d162535023c8d321831#interpolation)_. Using this method then out of bilateral way the _[∆(19 vs 18) Scenario](https://www.eq19.com/identition/span12/#the-seven-7-groups)_ we could get in to _[Scheme-33](https://gist.github.com/eq19/c9bdc2bbe55f2d162535023c8d321831#file-entrance-md)_. 

```note
The [electroweak force](https://en.wikipedia.org/wiki/Electroweak_interaction) is believed to have separated into the electromagnetic and weak forces during the [quark epoch](https://en.wikipedia.org/wiki/Quark_epoch) of the [early universe](https://en.wikipedia.org/wiki/Chronology_of_the_universe#Early_universe).
- In [physical cosmology](https://en.wikipedia.org/wiki/Physical_cosmology), the quark epoch was the period in the evolution of the [early universe](https://en.wikipedia.org/wiki/Chronology_of_the_universe#Early_universe) when the [fundamental interactions](https://en.wikipedia.org/wiki/Fundamental_interaction) of [gravitation](https://en.wikipedia.org/wiki/Gravitation), [electromagnetism](https://en.wikipedia.org/wiki/Electromagnetism), the [strong interaction](https://en.wikipedia.org/wiki/Strong_interaction) and the [weak interaction](https://en.wikipedia.org/wiki/Weak_interaction) had taken their present forms, but the temperature of the universe was still too high to allow [quarks](https://en.wikipedia.org/wiki/Quark) to bind together to form [hadrons](https://en.wikipedia.org/wiki/Hadron).
- The quark epoch began approximately [10−¹² seconds](https://en.wikipedia.org/wiki/Picosecond) after the [Big Bang](https://en.wikipedia.org/wiki/Big_Bang), when the preceding [electroweak epoch](https://en.wikipedia.org/wiki/Electroweak_epoch) ended as the [electroweak interaction](https://en.wikipedia.org/wiki/Electroweak_interaction) separated into the weak interaction and electromagnetism.
- During the quark epoch, the universe was filled with a dense, hot [quark–gluon plasma](https://en.wikipedia.org/wiki/Quark%E2%80%93gluon_plasma), containing quarks, [leptons](https://en.wikipedia.org/wiki/Lepton) and their [antiparticles](https://en.wikipedia.org/wiki/Antiparticle).
- Collisions between particles were too energetic to allow quarks to combine into [mesons](https://en.wikipedia.org/wiki/Meson) or [baryons](https://en.wikipedia.org/wiki/Baryon).

[![Elementary Particle](https://github.com/eq19/maps/assets/8466209/b6b6ea3c-cbbc-431c-b767-ecabf1cba933)](https://en.wikipedia.org/wiki/Fundamental_interaction)

The quark epoch ended when the universe was about 10−⁶ seconds old, when the average energy of particle interactions had fallen below the [binding energy](https://en.wikipedia.org/wiki/Binding_energy) of hadrons. The following period, when quarks became confined within hadrons, is known as the [hadron epoch](https://en.wikipedia.org/wiki/Hadron_epoch). _([Wikipedia](https://en.wikipedia.org/wiki/Quark_epoch))_
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

Prime Loops:
π(10) = 4 (node)
π(100) = 25 (partition)
π(1000) - 29 = 139 (section)
π(10000) - 29th - 29 = 1091 (segment)
π(100000) - 109th - 109 = 8884 (texture)
Sum: 4 + 25 + 139 + 1091 + 8884 = 10143 (object)

     |    168    |    618    |
-----+-👇--+-👇--+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"              |
-----+-----+-----+-----+-----+                                              |
 17¨ | {5¨}| {3¨}|  2¨ |  7¨👈 4¤  ----->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  6¨ |  6¨ |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-----+-----+-----+                                                   96¨
 11¨ |  3¨ | {3¨}| {5¨}| 3¤        ----->  assigned to "id:33"              |
-----+-----+-----+-----+-----+                                              |
 19¨ |  4¨ |  4¨ |  5¨ |  6¨ | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  5¨ |  5¨ |  8¨ | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
 43¨ | {3¨}| {5¨}|  5¨ | {5¨}| {3¨}|  7¨ | {5¨}| {3¨}|  7¨ | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |-----  13¨  -----|------ 15¨ ------|------ 15¨ ------|
     |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ
                  Mod 30            Mod 60            Mod 90
```

In terms of [Feynman diagrams](https://en.wikipedia.org/wiki/Feynman_diagrams) it has shown that the expansion of N = 8 supergravity is in [some ways](https://en.wikipedia.org/wiki/N_%3D_8_supergravity#cite_note-1) a product of two [N = 4 super Yang–Mills](https://en.wikipedia.org/wiki/N_%3D_4_super_Yang%E2%80%93Mills) theories.

```note
The number 28, aside from being triangular wave of perfect pyramid, is the sum of the ***first 5 primes*** and the sum of the ***first 7 natural numbers***.

[![Base of TOE](https://user-images.githubusercontent.com/8466209/249753163-6cfbcecf-3713-409b-8d8b-5fa5cf8489ac.png)](https://www.hexspin.com/finding-a-number-in-the-hexagon/)

The intervention of the Golden Ratio can be seen as a way to enter the quantum world, the world of subtle vibrations, in which we observe increasing energy levels as we move to smaller and smaller scales. El Nachie has proposed a way of calculating the fractal dimension of quantum space-time. The resulting value (Figure 7) suggests that the quantum world is composed of an infinite number or scaled copies of our ordinary 4-dimensional space-time.

[![PHI_Quantum_SpaceTime](https://github.com/eq19/maps/assets/8466209/6d91e9b8-9fc7-4ab9-9ec9-6e87a6f70c99)](https://www.sacred-geometry.es/?q=en/content/phi-particle-physics)

Setting k=0 one obtains the classical dimensions of ***heterotic superstring theory***, namely 26, 16, 10, 6 and 4, as well as the constant of super-symmetric (αgs=26) and ***non super-symmetric (αg=42) unification of all fundamental forces***. As we have seen in section 2, the above is a Fibonacci-like sequence with a very concise geometrical interpetation related to numbers ***5, 11 and φ***. _([Phi in Particle Physics](https://www.sacred-geometry.es/?q=en/content/phi-particle-physics))_
```

***d(43,71,114) = d(7,8,6) » 786***

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f           
------+------+-----+-----+------
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
      |      |     |  6  |                          11s ‹-- ∆28 = (71-43) ✔️
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |                           |
  2   +------|  5* +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) --------------------- 
      |      |  6  +-----+        <--------------  strip of the id: 37 (TOE)
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s ‹-- ∆24 = (43-19) ✔️
  3*  +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | -------------------------- 
------|------|-----+-----+-----
```

We can use simplexes to [triangulate a surface](https://github.com/eq19/maps/files/14252849/TerryPilling_-_2002.pdf) and compute the Euler characteristic and other topological properties in this fashion.

```note
Several aspects of torsion in string-inspired cosmologies are reviewed. In particular, its connection with fundamental, string-model independent, axion fields associated with the massless gravitational multiplet of the string are discussed.
- It is argued in favour of the role of primordial gravitational anomalies coupled to such axions in inducing inflation of a type encountered in the ***Running-Vacuum-Model (RVM)*** cosmological framework, without fundamental inflaton fields.[![15-Figure1-1](https://github.com/eq19/maps/assets/8466209/3733ba04-0bad-4651-90ee-01afbe319a5f)](https://github.com/eq19/maps/files/14229964/0209128.pdf)
- The gravitational-anomaly terms owe their existence to the Green–Schwarz mechanism for the (extra-dimensional) anomaly cancellation, and may be non-trivial in such theories in ***the presence of (primordial) gravitational waves at early stages of the four (4) dimensional string universe (after compactification)***.[![Torsion in String Cosmologies](https://github.com/eq19/maps/assets/8466209/a1cb4596-ff53-46bc-9da3-af9420603b35)
](https://github.com/eq19/maps/files/14230039/Torsion_in_String-Inspired_Cosmologies_and_the_Uni.pdf)
- The paper also discusses how the torsion-induced stringy axions can acquire a mass in the post inflationary era, due to non-perturbative effects, thus having the potential to play the role of (a component of) dark matter in such models.[![triangular wave](https://user-images.githubusercontent.com/8466209/225824209-ba2b9fe0-1a29-4208-940e-3351243ab0ba.png)](https://www.primesdemystified.com/First1000Primes.html)

Finally, the current-era phenomenology of this model is briefly described with emphasis placed on the possibility of alleviating tensions observed in the current-era cosmological data. A brief phenomenological comparison with other cosmological models in contorted geometries is also made. _([Torsion in String Cosmologies - pdf](https://github.com/eq19/maps/files/14230039/Torsion_in_String-Inspired_Cosmologies_and_the_Uni.pdf))_
```

***114 = 102 + 66 - 29 - 25 = 6 + (6x6) + 6 x (6+6) = 6 x (6+6) + 6 + (6x6) = 25 + 89***

[![28+Octonion](https://github.com/eq19/maps/assets/8466209/727945dd-a7fc-4f6e-8f89-0c843341a671)](https://theoryofeverything.org/theToE/)

The value of the [vacuum energy](https://en.wikipedia.org/wiki/Vacuum_energy) (or more precisely, the [renormalization](https://en.wikipedia.org/wiki/Renormalization) scale used to calculate this energy) may also be treated as an additional free parameter.

```note
In Fuller's synergetic geometry, symmetry breaking is modeled as 4 sub-tetra's, of which 3 form a tetrahelix and the 4th. "gets lost".
- In the present approach, intermediate (symmetry broken) states are proposed to be latent in the allready extended cube-octahedral matrix, and are actualized or mapped through the trefoil operator. In terms of tetra-logic, it is the invisible, confining icosa-dodeca matrix, acting upon the visible, deconfined cube-octahedral matrix.
- Further, the author proposes a more natural and versatile QFT symmetry breaking mechanism, based on well determined scalar field excitations.
- In QFT, the potential well is based on excitation modes, not on actual excitations, which is a reason why the proposed synergetic action gets obscured.
- A new type of symmetry breaking is proposed, based on a synchronized path integral.

The latter solves into a Goldstone oscillation and a vacuum expectation value (VEV), among other unique properties. The scalar field's self-interaction is a _[Golden Ratio scale-invariant group effect](https://www.eq19.com/multiplication/11.html#fibonacci-retracement)_, such as geometrically registered by the icosa-dodeca matrix. _([TGMResearch](http://science.trigunamedia.com/geometry-and-topology/index.htm))_
```

```txt
$True Prime Pairs:
(5,7$True Prime Pairs:
(5,7), (11,13), (17,19)
 
layer | node | sub |  i  |  f           
------+------+-----+-----+------
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
      |      |     |  6  |                          11s ‹-- ∆28 = (71-43)
------+------+-----+-----+------      } (36)         |
      |      |     |  7  |                           |
      |      |  4  +-----+                           |
      |  3   |     |  8  | (11)                      |
      |      +-----+-----+                           |
      |      |     |  9  |                           |
  2   +------|  5* +-----+-----                      |
      |      |     |  10 |                           |
      |      |-----+-----+                           |
      |  4   |     |  11 | (13) --------------------- 
      |      |  6  +-----+        <-----vacuum energy <--- ∆60 = (131-71) ✔️
      |      |     |  12 |---------------------------
------+------+-----+-----+------------               |
      |      |     |  13 |                           |
      |      |  7  +-----+                           |
      |  5   |     |  14 | (17)                      |
      |      |-----+-----+                           |
      |      |     |  15 |                           7s ‹-- ∆24 = (43-19)
  3*  +------+  8  +-----+-----       } (36)         |
      |      |     |  16 |                           |
      |      |-----+-----+                           |
      |  6   |     |  17 | (19)                      |
      |      |  9  +-----+                           |
      |      |     |  18 | -------------------------- 
------|------|-----+-----+-----
```

The second backward of second term will return to the right handed. Since this second term is the fermionic contribution then it will correspond to the right handed neutrinos.

```note
If right-handed neutrinos exist but do not have a Majorana mass, the neutrinos would instead behave as _[three (3) Dirac fermions](https://en.wikipedia.org/wiki/Dirac_fermion)_ and their antiparticles with masses coming directly from the Higgs interaction, like the other Standard Model fermions.
- The seesaw mechanism is appealing because it would naturally explain why the observed neutrino masses are so small. However, if the neutrinos are Majorana then they violate the conservation of [lepton number](https://en.wikipedia.org/wiki/Lepton_number) and even of [B − L](https://en.wikipedia.org/wiki/B_%E2%88%92_L).
- [Neutrinoless double beta decay](https://en.wikipedia.org/wiki/Double_beta_decay#Neutrinoless_double_beta_decay) has not (yet) been observed,[[3]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-3) but if it does exist, it can be viewed as two ordinary [beta decay](https://en.wikipedia.org/wiki/Beta_decay) events whose resultant antineutrinos immediately annihilate each other, and is only possible if neutrinos are their own antiparticles.[[4]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-4)
- The high-energy analog of the neutrinoless double beta decay process is the production of same-sign charged lepton pairs in [hadron colliders](https://en.wikipedia.org/wiki/Hadron_collider);[[5]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-5) it is being searched for by both the [ATLAS](https://en.wikipedia.org/wiki/ATLAS_experiment) and [CMS](https://en.wikipedia.org/wiki/Compact_Muon_Solenoid) experiments at the [Large Hadron Collider](https://en.wikipedia.org/wiki/Large_Hadron_Collider).
- In theories based on [left–right symmetry](https://en.wikipedia.org/wiki/Left%E2%80%93right_symmetry), there is a deep connection between these processes.[[6]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-6) In the currently most-favored explanation of the smallness of [neutrino mass](https://en.wikipedia.org/wiki/Neutrino_mass), the [seesaw mechanism](https://en.wikipedia.org/wiki/Seesaw_mechanism), the neutrino is “naturally” a Majorana fermion.

Majorana fermions cannot possess intrinsic electric or magnetic moments, only [toroidal moments](https://en.wikipedia.org/wiki/Toroidal_moment).[[7]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-7)[[8]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-8)[[9]](https://en.wikipedia.org/wiki/Majorana_fermion#cite_note-9) Such minimal interaction with electromagnetic fields makes them potential candidates for [cold dark matter](https://en.wikipedia.org/wiki/Cold_dark_matter). _([Wikipedia](https://en.wikipedia.org/wiki/Majorana_fermion))_
```

![Renormalization](https://github.com/eq19/maps/assets/8466209/d0b14d1d-6d11-42af-9309-7a98a7e1f07b)

In other words, the synchronized path integral represents a deterministic approach to ***scalar field's self-excitation***, and thus to the confined state in quentum physics

```note
Beside the operator proof, here we also provide a diagrammatic argument of the above derivation, using the QED in background field in Sec. 5 as an example.
- We show that: taking mass derivatives in one-loop Feynman diagrams Fig. 4 for δEN will exactly produce the one-loop Feynman diagrams for insertion of 4HS.
- ***The mass derivative has four (4) origins***: the explicit mass dependency of the electron propagator, the implicit mass dependency in the energy level EN, the mass dependencies in renormalization constants δm and Z3 − 1, and the implicit mass dependency in the wave function uN.
- The mass derivative of the fermion propagator 1iγ·D−m simply reduces to mψψ¯ operator insertion in the internal electron line as shown in Fig. 7.
- The mass dependency in EN will lead to ***the wave function renormalization in external legs***. The mass dependencies in renormalization constants δm and Z3 −1 will exactly lead to the anomalous energy contribution.

Finally, the mass derivative of the external wave function uN is more complicated, which is shown the remaining diagrams where the mψψ¯ are inserted at external legs. _([Scale symmetry breaking - pdf](https://github.com/eq19/maps/files/14183267/1-s2.0-S0550321321002340-main.pdf))_
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

Prime Loops:
π(10) = 4 (node)
π(100) = 25 (partition)
π(1000) - 29 = 139 (section)
π(10000) - 29th - 29 = 1091 (segment)
π(100000) - 109th - 109 = 8884 (texture)
Sum: 4 + 25 + 139 + 1091 + 8884 = 10143 (object)

     |    168    |    618    |
-----+-----+-----+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"             19¨
-----+-👇--+-👇--+-----+-----+                                             ---
 17¨ | {5¨}| {3¨}|  2¨ |  7¨ | 4¤  ----->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  6¨ |  6¨ |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-----+-----+-----+                                                    |
 11¨ |  3¨ | {3¨}| {5¨}| 3¤  --->  Np(33)  assigned to "id:33"   ----->    77¨
-----+-----+-----+-----+-----+                                              |
 19¨ |  4¨ |  4¨ |  5¨ |  6¨ | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  5¨ |  5¨ |  8¨ | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-👇--+-👇--+-----+-👇--+-👇--+-----+               ---
 43¨ | {3¨}| {5¨}|  5¨ | {5¨}| {3¨}|  7¨ | {5¨}| {3¨}|  7¨ | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |-----  13¨  -----|------ 15¨ ------|------ 15¨ ------|
     |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ
                  Mod 30            Mod 60            Mod 90
```

Let us make some concluding remarks with the help of the Fritzsch-Xing “pizza" plot. It offers a summary of _[28 free parameters](https://github.com/eq19/maps/files/14159651/1411.2713.pdf)_ associated with the SM itself and neutrino masses, lepton flavor mixing angles and CP-violating phases. 

```note
The reduction of pure gravity from eleven dimensions down to D = 4 dimensions yields a gravitational theory with ***seven (7) abelian vector fields*** Aµn, `n = 1,...,7`, and `1+27=28` scalar fields, parametrizing the coset space GL(7)/SO(7). The dimensional reduction of the antisymmetric 3-form to D = 4 dimensions gives rise to one 3-form field, seven 2-form fields. _([11D Supergravity and Hidden Symmetries - pdf](https://github.com/eq19/maps/files/14126154/2303.12682.pdf))_
```

[![28 free parameters](https://github.com/eq19/maps/assets/8466209/1c3bcda6-bfc6-464b-a738-5afd2488546b)](https://github.com/eq19/maps/files/14159651/1411.2713.pdf)

Those results, compared with those for the nucleon, indicate quite different pattern, revealed as a new aspect by exploiting the quark/gluon decomposition of the QCD trace anomaly.

```note
The matrix elements of this quark/gluon decomposition of the QCD trace anomaly allow us to derive the QCD constraints on the hadron’s gravitational form factors, in particular, on the twist-four gravitational form factor, Cq,g.
- Using the three-loop quark/gluon [trace anomaly formulas](https://github.com/eq19/maps/files/14223125/dis23_3_28_v2_tanaka.pdf), we calculate the forward (zero momentum transfer) value of the twist-four gravitational form factor C¯q,g at the next-to-next-to-leading-order (NNLO) accuracy.
- We present quantitative results for nucleon as well as for pion, leading to a model-independent determination of the forward value of C¯q,g.

We find quite different pattern in the obtained results between the nucleon and the pion. _([Twist-four gravitational - pdf](https://github.com/eq19/maps/files/14182160/JHEP03.2023.013.pdf))_
```

***2+7 = 3×3 lepton vs quarks***

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

Prime Loops:
π(10) = 4 (node)
π(100) = 25 (partition)
π(1000) - 29 = 139 (section)
π(10000) - 29th - 29 = 1091 (segment)
π(100000) - 109th - 109 = 8884 (texture)
Sum: 4 + 25 + 139 + 1091 + 8884 = 10143 (object)

     |    168    |    618    |
-----+-----+-----+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"             19¨
-----+-----+-----+-👇--+-👇--+                                             ---
 17¨ | {5¨}| {3¨}|  2¨ |  7¨ | 4¤  ----->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  6¨ |  6¨ |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-👇--+-👇--+-----+                                                    |
 11¨ |  3¨ | {3¨}| {5¨}| 3¤  --->  Np(33)  assigned to "id:33"   ----->    77¨
-----+-----+-----+-----+-----+                                              |
 19¨ |  4¨ |  4¨ |  5¨ |  6¨ | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  5¨ |  5¨ |  8¨ | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
 43¨ | {3¨}| {5¨}|  5¨ | {5¨}| {3¨}|  7¨ | {5¨}| {3¨}|  7¨ | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |-----  13¨  -----|------ 15¨ ------|------ 15¨ ------|
     |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ
                  Mod 30            Mod 60            Mod 90
````

This fact may also provide a possible explanation for why almost all of the particle interactions we see are describable by renormalizable theories.

```note
The [Standard Model](https://en.wikipedia.org/wiki/Standard_Model) of particle physics contains only renormalizable operators, but the interactions of [general relativity](https://en.wikipedia.org/wiki/General_relativity) become nonrenormalizable operators if one attempts to construct a field theory of [quantum gravity](https://en.wikipedia.org/wiki/Quantum_gravity) in the most straightforward manner (treating the metric in the [Einstein–Hilbert Lagrangian](https://en.wikipedia.org/wiki/Einstein%E2%80%93Hilbert_Lagrangian) as a perturbation about the [Minkowski metric](https://en.wikipedia.org/wiki/Minkowski_metric)), suggesting that [perturbation theory](https://en.wikipedia.org/wiki/Perturbation_theory_(quantum_mechanics)) is not satisfactory in application to quantum gravity.
- However, in an [effective field theory](https://en.wikipedia.org/wiki/Effective_field_theory), "renormalizability" is, strictly speaking, a [misnomer](https://en.wikipedia.org/wiki/Misnomer). In nonrenormalizable effective field theory, terms in the Lagrangian do multiply to infinity, but have coefficients suppressed by ever-more-extreme inverse powers of the energy cutoff.![169-over-109-blood-pressure](https://github.com/eq19/maps/assets/8466209/a702ea20-2ef3-424f-804e-c73a6c873692)
- If the cutoff is a real, physical quantity—that is, if the theory is only an effective description of physics up to some maximum energy or minimum distance scale—then these additional terms could represent real physical interactions.
- Assuming that the dimensionless constants in the theory do not get too large, one can group calculations by inverse powers of the cutoff, and extract approximate predictions to finite order in the cutoff that still have a finite number of free parameters. It can even be useful to renormalize these "nonrenormalizable" interactions.[![multiplication zones](https://user-images.githubusercontent.com/8466209/195963923-0796217c-7a87-4b2d-ba93-f47465304c03.png)](https://www.eq19.com/multiplication/)
- Nonrenormalizable interactions in effective field theories rapidly become weaker as the energy scale becomes much smaller than the cutoff. The classic example is the [Fermi theory](https://en.wikipedia.org/wiki/Fermi%27s_interaction) of the [weak nuclear force](https://en.wikipedia.org/wiki/Weak_nuclear_force), a nonrenormalizable effective theory whose cutoff is comparable to the mass of the [W particle](https://en.wikipedia.org/wiki/W_particle).

It may be that any others that may exist at the [GUT](https://en.wikipedia.org/wiki/Grand_Unified_Theory) or Planck scale simply become too weak to detect in the realm we can observe, with one exception: [gravity](https://en.wikipedia.org/wiki/Gravity), whose exceedingly weak interaction is magnified by the presence of the enormous masses of [stars](https://en.wikipedia.org/wiki/Star) and [planets](https://en.wikipedia.org/wiki/Planet). _([Wikipedia](https://en.wikipedia.org/wiki/Renormalization))_
```

![Mod 60](https://github.com/eq19/maps/assets/8466209/dc478428-f7aa-4845-869a-f04383b19873)

For the renormalization mixing at twist four, the Feynman diagram calculation of ZF and ZC is available to the two-loop order. 

```note
Moreover, it is shown that the constraints imposed by the RG invariance of (1.1) allow to determine the power series in αs for ZF as well as ZC in the MS-like schemes, completely from the perturbative expansions of β(g) and γm(g), which are now known to five-loop order [43–48] in the literature.
- Therefore, ***six renormalization constants ZT,ZL, Zψ, ZQ, ZF and ZC among ten constants arising in (2.3) (2.6) are available to a certain accuracy beyond two-loop order inthe MS-like schemes***, and they take the form, (2.8) in the d = 4 − 2 spacetime dimensions with X = T, L, ψ, Q, F, and C; here, aX, bX, cX.…, are the constants given as the power series in αs, and δX,X0 denotes the Kronecker symbol. ***However, ZM, ZS, ZK and ZB still remain unknown***.
- It is shown [8] that these four renormalization constants can be determined to the accuracy same as the renormalization constants (2.8), by invoking that they should also obey the form (2.8) with X = M, S, K, B,  and that the r.h.s. of the formulas (2.3), (2.4) are, in total, UV-finite.

Thus, all the renormalization constants in (2.3)–(2.6) are determined up to the ***three-loop accuracy***. _([Twist-four gravitational - pdf](https://github.com/eq19/maps/files/14182160/JHEP03.2023.013.pdf))_
```

[![IMG_20240211_101224](https://github.com/eq19/maps/assets/8466209/ca8870e2-b74e-48a6-9540-7122e9522440)](https://github.com/eq19/maps/files/14231180/1012.4409.pdf)

A gauge colour rotation is [a spacetime-dependent SU(3)](https://en.m.wikipedia.org/wiki/Special_unitary_group#The_group_SU(3)) group element. They span the [Lie algebra](https://github.com/lkpetrich/Semisimple-Lie-Algebras) of the SU(3) group in the defining representation.

```note
The Gell-Mann matrices, developed by [Murray Gell-Mann](https://en.m.wikipedia.org/wiki/Murray_Gell-Mann), are a set of eight [linearly independent](https://en.m.wikipedia.org/wiki/Linear_independence) 3×3 [traceless](https://en.m.wikipedia.org/wiki/Matrix_trace) [Hermitian matrices](https://en.wikipedia.org/wiki/Hermitian_matrices) used in the study of the [strong interaction](https://en.wikipedia.org/wiki/Strong_interaction) in [particle physics](https://en.wikipedia.org/wiki/Particle_physics). They span the [Lie algebra](https://en.wikipedia.org/wiki/Lie_group#The_Lie_algebra_associated_with_a_Lie_group) of the [SU(3)](https://en.wikipedia.org/wiki/Special_unitary_group#SU(3)) group in the defining representation.
```

![QED vs QCD](https://github.com/eq19/maps/assets/8466209/5852976f-4e7e-45df-87a5-1fe5dfe6b63b)

Indeed, a particularly well-chosen cellular automaton on [II(9,1) or II(25,1)](https://cp4space.hatsya.com/2013/09/12/leech-lattice/) would be a discretised version of ***10- or 26-dimensional*** string theory.


```note
The [Lie algebra](https://www.valdostamuseum.com/hamsmith/Lie.html) E6 of the [D4-D5-E6-E7-E8 VoDou Physics model](https://www.valdostamuseum.com/hamsmith/d4d5e6hist.html) can be represented in terms of 3 copies of the 26-dimensional traceless subalgebra J3(O)o of the 27-dimensional [Jordan algebra](https://www.valdostamuseum.com/hamsmith/Jordan.html) J3(O) by using the [fibration E6 / F4](https://www.valdostamuseum.com/hamsmith/Jordan.html#E6F4fib) of 78-dimensional E6 over 52-dimensional F4 and the structure of [F4 as doubled J3(O)o](https://www.valdostamuseum.com/hamsmith/Jordan.html#F4J3Oo) based on the 26-dimensional representation of [F4](https://www.valdostamuseum.com/hamsmith/Lie.html#Liexceptional). _([Tony's Home](https://www.valdostamuseum.com/hamsmith/Rzeta.html))_
```

[![Quantum Chromodynamics](https://github.com/eq19/maps/assets/8466209/62c106bd-7950-4b63-9e64-4f758473b48e)](https://www.eq19.com/exponentiation/span15/)

The fact that quarks of the same electric charge possess a mass hierarchy is a big puzzle. It must be highly correlated with the hierarchy of quark flavor mixing.

```note
This chapter is intended to provide a brief description of some important issues regarding quark masses, flavor mixing and CP-violation. A comparison between the salient features of quark and lepton flavor mixing structures is also made.
- The SM contains thirteen free flavor parameters in its electroweak sector: three charged-lepton masses,
six quark masses, three quark flavor mixing angles and one CP-violating phase.
- Since the three neutrinos must be massive beyond the SM, one has to introduce seven (or nine) extra free parameters to describe their flavor properties: three neutrino masses, three lepton flavor mixing angles and one (or three) CP-violating phase(s), corresponding to their Dirac (or Majorana) nature a
- The ***3x3 lepton vs quark mixing matrices*** appearing in the weak charged-current interactions are referred to, respectively, as the ***Pontecorvo-Maki-Nakagawa-Sakata (PMNS)*** matrix Uand the ***Cabibbo-Kobayashi-Maskawa (CKM)*** matrix V which all the fermion fields are the mass eigenstates.
- By convention, U and V are defined to be associated with W− and W+, respectively. Note that V is unitary as dictated by the SM itself, but whether U is unitary or not depends on the mechanism responsible for the origin of neutrino masses.
- The charged leptons and quarks with the same electriccharges all have the normal mass hierarchies (namely, me ≪ mµ ≪ mτ, mu ≪ mc ≪ mt and md ≪ ms ≪ m. Yet it remains unclear whether the three neutrinos also have a normal mass ordering (m1 < m2 < m3) or not. Now that m1 < m2 has been fixed from the solar neutrino oscillations, ***the only likely “abnormal” mass ordering is m3 < m1 < m2***
- The neutrino mass ordering is one of the central concerns in flavor physics, and it will be determined in the foreseeable future with the help of either an accelerator-based neutrino oscillation experiment or a reactor-based antineutrino oscillation experiment, or both of them. Up to now the moduli of nine elements of the CKM matrix V have been determined from current experimental data to a good degree of accuracy.

Here our focus is on the ***five (5) parameters*** of strong and weak CP violation. In the quark sector, the strong CP-violating phase θ remains unknown, but the weak CP-violating phase δq has been determined to a good degree of accuracy. In the lepton sector, however, none of the CP-violating phases has been measured.  _([Quark Mass Hierarchy and Flavor Mixing Puzzles - pdf](https://github.com/eq19/maps/files/14159651/1411.2713.pdf))_
```

[![CKM vs PMNS](https://github.com/eq19/maps/assets/8466209/44758746-c069-4fb6-a2e9-8574d2d63b29)](https://www.semanticscholar.org/paper/Quark-Mass-Hierarchy-and-Flavor-Mixing-Puzzles-Xing/3719fec87f5e50c70eada23057b4b48fb5de4f18)

The ***3x3 lepton vs quark*** mixing matrices appearing in the weak charged-current interactions are referred to, respectively, as the ***PMNS matrix U***, and the ***CKM matrix V***, which all the fermion fields are the mass eigenstates.

```note
Muons are about ***200 times heavier*** than the electron. The larger mass makes them unstable. Muons exist for only about two microseconds—or two-millionths of a second—before they decay. Electrons live forever. The tau; elementary subatomic particle is similar to the electron but 3,477 times heavier. Like the electron and the muon, the tau is an electrically charged member of the lepton family of subatomic particles; the tau is negatively charged, while its antiparticle is positively charged. _([ResearchGate](https://www.researchgate.net/post/Why-do-fermions-exist-in-three-generations-electron-like-muon-like-and-tau-like))_ 
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

Prime Loops:
π(10) = 4 (node)
π(100) = 25 (partition)
π(1000) - 29 = 139 (section)
π(10000) - 29th - 29 = 1091 (segment)
π(100000) - 109th - 109 = 8884 (texture)
Sum: 4 + 25 + 139 + 1091 + 8884 = 10143 (object)

     |    168    |    618    |
-----+-----+-----+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"             19¨
-----+-----+-----+-----+-----+                                             ---
 17¨ | {5¨}| {3¨}|  2¨ |  7¨ | 4¤  ----->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  6¨ |  6¨ |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-👇--+-👇--+-----+                                                    |
 11¨ |  3¨ | {3¨}| {5¨}| 3¤  --->  Np(33)  assigned to "id:33"   ----->    77¨
-----+-----+-----+-----+-----+                                              |
 19¨ |  4¨ |  4¨ |  5¨ |  6¨ | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  5¨ |  5¨ |  8¨ | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
 43¨ | {3¨}| {5¨}|  5¨ | {5¨}| {3¨}|  7¨ | {5¨}| {3¨}|  7¨ | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |-----  13¨  -----|------ 15¨ ------|------ 15¨ ------|
     |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ
                  Mod 30            Mod 60            Mod 90
```

[Bound state corrections](https://github.com/eq19/maps/files/14178591/hennessy.pdf)
 to the semileptonic width and measured by a number moments analyses have permitted the extraction to a level of a few %.

```note
In principle, there is one further parameter in the Standard Model; the Lagrangian of QCD can contain a phase that would lead to CP violation in the strong interaction.
- Experimentally, this strong CP phase is known to be extremely small, θCP ≃ 0, and is usually taken to be zero.
- The [theoretical and experimental pillars](https://github.com/eq19/maps/files/14173324/1924367859.pdf) of the Standard Model:
  - the ***twelve (12) fermions*** (or perhaps more correctly the twelve Yukawa couplings to the Higgs field), mν1, mν2, mν3, me, mµ, mτ, md, ms, mb, mu, mc, and mt ;
  - the ***three (3) coupling constants*** describing the strengths of the gauge interactions, α, GF and αS, or equivalently g′, gW and gS;
  - the ***two (2) Higgs parameters*** describing the Higgs potential, µ and λ, or equivalently its vacuum expectation value and the mass of the Higgs boson, v and mH; and
  - the ***eight (8) mixing angles*** of the PMNS and CKM matrices, which can be parameterised by θ12, θ13, θ23, δ, and λ, A, ρ, η.[![neutrino-mixing-the-pmns-matrix-l](https://github.com/eq19/maps/assets/8466209/9b2c1114-c94e-4a4d-91c4-196dc625b844)](https://www.slideserve.com/misha/recent-results-from-the-minos-experiment)
  - in principle, there is ***one (1) further*** parameter in the Standard Model; the Lagrangian of QCD can contain a phase that would lead to CP violation in the strong interaction. Experimentally, this strong CP phase is known to be extremely small, θCP ≃ 0, and is usually taken to be zero. 
- If θCP is counted, then the Standard Model has ***`12+3+2+8+1=26` free parameters***.
- The relatively large number of free parameters is symptomatic of the Standard Model being just that; a model where the parameters are chosen to match the observations, rather than coming from a higher theoretical principle.
- Putting aside θCP, of the ***25 SM parameters: 14 are associated with the Higgs field, eight (8) with the
flavour sector and only three (3) with the gauge interactions***.

Likewise, ***the coupling constants of the three gauge interactions*** are of a similar order of magnitude, hinting that they might be different low-energy manifestations of a Grand Unified Theory (GUT) of the forces. These patterns provide hints for, as yet unknown, physics beyond the Standard Model. _([Modern Particle Physics P.500 - pdf](https://github.com/eq19/maps/files/13800674/Modern-Particle-Physics.pdf))_
```

[![slide_40](https://github.com/eq19/maps/assets/8466209/87da7032-06f2-4d44-8b30-a6a26b569b04)](https://slideplayer.com/slide/5347869/)

## The 11 Dimensions

Below is a model of E11 (shown by 11 dimensions). Its absolute dimensions represent all related key knowledges of modern physics. 

```note
Moreover this model represents [Quark-Gluon Plasma](https://en.wikipedia.org/wiki/Quark%E2%80%93gluon_plasma), with all of the [fundamental forces](https://www.eq19.com/exponentiation/#fundamental-forces) in the early stage after [Big Bang](https://youtu.be/7VgoECW06-s?si=_l-Pu42gwtnxzzT2). _([Youtube](https://www.youtube.com/watch?v=dEoMeHi-6kM))_
```

[![default](https://user-images.githubusercontent.com/8466209/242000067-6d2ac164-06d6-4546-a118-10642982ce52.png)](https://www.youtube.com/watch?v=dEoMeHi-6kM)

Classically, we have only one 11-dimensional supergravity theory: 7D hyperspace + 4 common dimensions. 

```note
The four (4) faces of our pyramid additively cascade ***32 four-times triangular numbers***
- These include Fibo1-3 equivalent 112 (rooted in `T7 = 28; 28 x 4 = 112`),
- which creates a pyramidion or capstone in our model, and 2112 (rooted in `T32 = 528; 528 x 4 = 2112`),
- which is the index number of ***the 1000th prime*** within our domain,
- and equals the total number of 'elements' used to construct the pyramid.

Note that `4 x 32 = 128` is the perimeter of the square base which has an area of `32^2 = 1024 = 2^10`). _([PrimesDemystified](https://www.primesdemystified.com/First1000Primes.html))_
```

[![](https://user-images.githubusercontent.com/8466209/225830554-007fbd06-9d7d-44e8-867d-c7b0188bf488.png)](https://www.primesdemystified.com/First1000Primes.html)

The above 11 stands as the central point which is correlated to 77 sequencial processes of sun vs moon orbits starting with the _[symmetri breaking](https://www.eq19.com/multiplication/10.html#spontaneous-symmetry-breaking)_ that involving 9 and 7.

```note
Back in 1982, a very nice paper by Kugo and Townsend, [Supersymmetry and the Division Algebras](http://linkinghub.elsevier.com/retrieve/pii/0550321383905849), explained some of this, ending up with some comments on the ***relation of octonions to d=10 super Yang-Mills and d=11 super-gravity***.
- Baez and Huerta in 2009 wrote the very clear [Division Algebras and Supersymmetry I](http://arxiv.org/abs/0909.0551), which explains how the existence of supersymmetry relies on algebraic identities that follow from the existence of the division algebras. Kugo-Townsend don’t mention string theory at all, and Baez-Huerta refers to superstrings just in passing, only really discussing supersymmetric QFT.
- There’s also [Division Algebras and Supersymmetry II](http://arxiv.org/abs/1003.3436) by Baez and Huerta from last year, with intriguing speculation about Lie n-algebras and what these might have to do with relations between octonions and 10 and 11 dimensional supergravity. For a nice expository paper about this stuff, see their [An Invitation to Higher Gauge Theory](http://arxiv.org/abs/1003.4485).

The headline argument is that octonions are important and interesting because they’re [The Strangest Numbers in String Theory](http://www.nature.com/scientificamerican/journal/v304/n5/pdf/scientificamerican0511-60.pdf), even though they play only a minor role in the subject. _([math.columbia.edu](https://www.math.columbia.edu/~woit/wordpress/?p=3665))_
```

```txt
 8§8  |------- 5® --------|------------ 7® --------------|
      |QED|------------------- QCD ----------------------|👈
      | 1 |-------------- 77 = 4² + 5² + 6² -------------|
------+---|---+---+---+---+---+---+---+---+----+----+----+
 repo |{1}|{2}| 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |{12}| 1,77
------+---|---+---+---+---+---+---+---+---+----+----+----+
 user | 7 | - | - | - | - | 7 | 8 | - | - |  8 |  8 |  3 |
------+---|👇-+👇-+---+---+---+---+---+---+----+----+----+ 7,78
 main | - | 9 | 7 | 9 | 6 | - | - | 8 | 5 |  - |  - |  - |
------+---|---+---+---+---+---+---+---+---+----+----+----+
        Δ | Δ             |                      Δ  |   Δ
       Φ17|Φ29            |                    96-99|  100 - 123 ({24})
          |--- A,T,G,C ---|                         |  └── 100 - 103 (4x) » 100
          Δ    2x2 = 4x   |-------  2x3 = 6x -------|  └── 104 - 109 (6x) » 30
         {98}                                       |  └── 110 - 123 (14x)» 70
```

A number of other GUT models are based upon subgroups of SO(10). ***They are the minimal [left-right model](https://www.eq19.com/identition/span12/#the-quantum-gravity), [SU(5)](https://en.wikipedia.org/wiki/SU(5)), [flipped SU(5)](https://en.wikipedia.org/wiki/Flipped_SU(5)) and the Pati–Salam model***.

```note
SU(5) fermions of standard model in 5+10 representations. The sterile neutrino singlet's 1 representation is omitted. Neutral bosons are omitted, but would occupy diagonal entries in complex superpositions. X and Y bosons as shown are the opposite of the conventional definition
```

[![SO(10)](https://github.com/eq19/maps/assets/8466209/b1d3bccd-a423-4ebb-a397-e973b2cc8e6e)
](https://en.wikipedia.org/wiki/Grand_Unified_Theory)

[![SU(5)_representation_of_fermions](https://github.com/eq19/maps/assets/8466209/2b1aa8f5-0028-4549-a091-eee291ed4890)
](https://en.wikipedia.org/wiki/Grand_Unified_Theory)

The simplest theory describing the above is the SU(3) one with the gluons as the basis states of the Lie algebra. That is, gluons transform in the adjoint representation of SU(3), which is 8-dimensional.

## The pairwise disjoint

The Cartan–Weyl basis of the Lie algebra of SU(3) is obtained by another change of basis, where one defines _[The Root System](https://en.wikipedia.org/wiki/Root_system)_ for SU(3).

```note
The Lie group structure of the Lorentz group is explored. Its generators and its Lie algebra are exhibited, via the study of infinitesimal Lorentz transformations.
- The exponential map is introduced and it is shown that the study of the Lorentz group can be reduced to that of its Lie algebra.
- Finally, the link between the restricted Lorentz group and the special linear group  is established via the spinor map. 

The Lie algebras of these two groups are shown to be identical (up to some isomorphism).
```

![270355_1_En_7_Fig1_HTML](https://github.com/eq19/maps/assets/8466209/5e3fd958-f39a-48b3-b747-6e05ac700572)

***19 + i(13+5) = 19 + i18***

```txt
  Fermion  | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19+i5
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-2 |    2    |    3    |     3     |    18     |     24     |   17+i7
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |   11+i13
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-4 |    2    |    3    |     3     |    18     |     24     |   19+i5
===========+=========+=========+===========+===========+============+===========
     Total |    8    |   12    |    12     |    72     |     96     |   66+i30 ✔️
```

A bispinor is more or less "the same thing" as a ***[Dirac spinor](https://en.wikipedia.org/wiki/Dirac_spinor)***. The convention used here is that the article on the Dirac spinor presents [plane-wave](https://en.wikipedia.org/wiki/Plane-wave) solutions to the Dirac equation.

```note
The four pairwise disjoint and non-compact connected components of the Lorentzgroup L = O(1, 3) and corresponding subgroups:
- the proper Lorentz group L+ = SO(1, 3),
- the orthochronous Lorentz group L↑,
- the orthochronous Lorentz group Lo = L↑ + ∪ TL↑+ (see below) and
- the proper orthochronous Lorentz group L↑+ = SO+(1, 3), which contains the identity element. 

Of course, the sets L↓−, L↑− and L↓+ do not represent groups due to the missing identity element. _([The-four-pairwise-disjoint](https://github.com/eq19/maps/files/13810691/weyl_majorana_dirac_aste.pdf))_
```

***19 + 7 = 26***

[![The-four-pairwise-disjoint-and-non-compact-connected-components-of-the-Lorentz-group-L](https://github.com/eq19/maps/assets/8466209/f322446f-8726-4e51-bc5c-be1276c459c4)](https://github.com/eq19/maps/files/13810691/weyl_majorana_dirac_aste.pdf)

```note
Fermion particles are described by [Fermi–Dirac statistics](https://en.m.wikipedia.org/wiki/Fermi%E2%80%93Dirac_statistics) and have [quantum numbers](https://en.m.wikipedia.org/wiki/Quantum_numbers) described by the [Pauli exclusion principle](https://en.m.wikipedia.org/wiki/Pauli_exclusion_principle). They include the [quarks](https://en.m.wikipedia.org/wiki/Quarks) and [leptons](https://en.m.wikipedia.org/wiki/Leptons), as well as any [composite particles](https://en.m.wikipedia.org/wiki/Composite_particles) consisting of an odd number of these, such as all [baryons](https://en.m.wikipedia.org/wiki/Baryons) and many atoms and nuclei. Fermions have half-integer spin; for all known elementary fermions this is 1⁄2. In the Standard Model, there are 12 types of elementary fermions: six [quarks](https://en.m.wikipedia.org/wiki/Quark) and six [leptons](https://en.m.wikipedia.org/wiki/Lepton).
- Leptons do not interact via the strong interaction. Their respective antiparticles are the antileptons, which are identical, except that they carry the opposite electric charge and lepton number. The antiparticle of an electron is an antielectron, which is almost always called a "positron" for historical reasons.[![IMG_20240108_032736](https://github.com/eq19/maps/assets/8466209/d0593a3f-0411-4ae9-94a6-7bba9e97391c)](https://en.wikipedia.org/wiki/List_of_particles)
  - There are six leptons in total; the three charged leptons are called "electron-like leptons", while the neutral leptons are called "neutrinos".
  - Neutrinos are known to oscillate, so that neutrinos of definite flavor do not have definite mass, rather they exist in a superposition of mass eigenstates.
  - The hypothetical heavy right-handed neutrino, called a ***sterile neutrino***, has been omitted.
- [Quarks](https://en.m.wikipedia.org/wiki/Quark) are the fundamental constituents of [hadrons](https://en.m.wikipedia.org/wiki/Hadron) and interact via the [strong force](https://en.m.wikipedia.org/wiki/Strong_force). Quarks are the only known carriers of [fractional charge](https://en.m.wikipedia.org/wiki/Fractional_charge), but because they combine in groups of three quarks (baryons) or in pairs of one quark and one [antiquark](https://en.m.wikipedia.org/wiki/Antiquark) (mesons), only integer charge is observed in nature.[![IMG_20240108_033012](https://github.com/eq19/maps/assets/8466209/7427eccf-647c-4409-8f64-a144742b2fa3)](https://en.wikipedia.org/wiki/List_of_particles)
  - Their respective [antiparticles](https://en.m.wikipedia.org/wiki/Antiparticle) are the [antiquarks](https://en.m.wikipedia.org/wiki/Antiquark), which are identical except that they carry the opposite electric charge (for example the up quark carries charge +2⁄3, while the up antiquark carries charge −2⁄3), color charge, and baryon number.
  - There are six [flavors](https://en.m.wikipedia.org/wiki/Flavor_(particle_physics)) of quarks; the three positively charged quarks are called ***up-type quarks*** while the three negatively charged quarks are called ***down-type quarks***.

All known fermions except [neutrinos](https://en.m.wikipedia.org/wiki/Neutrinos), are also [Dirac fermions](https://en.m.wikipedia.org/wiki/Dirac_fermion); that is, each known fermion has its own distinct [antiparticle](https://en.m.wikipedia.org/wiki/Antiparticle). It is not known whether the [neutrino](https://en.m.wikipedia.org/wiki/Neutrino) is a [Dirac fermion](https://en.m.wikipedia.org/wiki/Dirac_fermion) or a [Majorana fermion](https://en.m.wikipedia.org/wiki/Majorana_fermion).[[4]](https://en.m.wikipedia.org/wiki/List_of_particles#cite_note-4) Fermions are the basic building blocks of all [matter](https://en.m.wikipedia.org/wiki/Matter). They are classified according to whether they interact via the [strong interaction](https://en.m.wikipedia.org/wiki/Strong_interaction) or not.
```

[![Electrodynamics](https://github.com/eq19/maps/assets/8466209/b8629985-8996-4819-9e19-a106b98eed48)](https://github.com/eq19/maps/files/13930310/Mexican_nu_Lecture_1_2009.pdf)

```note
In [physics](https://en.wikipedia.org/wiki/Physics), a subatomic particle is a [particle](https://en.wikipedia.org/wiki/Particle) smaller than an [atom](https://en.wikipedia.org/wiki/Atom).[[1]](https://en.wikipedia.org/wiki/Subatomic_particle#cite_note-1)
- According to the [Standard Model of particle physics](https://en.wikipedia.org/wiki/Standard_Model), a subatomic particle can be either a [composite particle](https://en.wikipedia.org/wiki/Composite_particle), which is composed of other particles (for example, a [baryon](https://en.wikipedia.org/wiki/Baryon), like a [proton](https://en.wikipedia.org/wiki/Proton) or a [neutron](https://en.wikipedia.org/wiki/Neutron), composed of three [quarks](https://en.wikipedia.org/wiki/Quarks); or a [meson](https://en.wikipedia.org/wiki/Meson), composed of two quarks), or an [elementary particle](https://en.wikipedia.org/wiki/Elementary_particle), which is not composed of other particles (for example, [quarks](https://en.wikipedia.org/wiki/Quarks); or [electrons](https://en.wikipedia.org/wiki/Electrons), [muons](https://en.wikipedia.org/wiki/Muons), and [tau](https://en.wikipedia.org/wiki/Tau) particles, which are called [leptons](https://en.wikipedia.org/wiki/Leptons)).[[2]](https://en.wikipedia.org/wiki/Subatomic_particle#cite_note-2)
- [Particle physics](https://en.wikipedia.org/wiki/Particle_physics) and [nuclear physics](https://en.wikipedia.org/wiki/Nuclear_physics) study these particles and how they interact.[[3]](https://en.wikipedia.org/wiki/Subatomic_particle#cite_note-3)
- Most force carrying particles like [photons](https://en.wikipedia.org/wiki/Photons) or [gluons](https://en.wikipedia.org/wiki/Gluons) are called [bosons](https://en.wikipedia.org/wiki/Bosons) and, although they have discrete quanta of energy, do not have rest mass or discrete diameters (other than pure energy wavelength) and are unlike the former particles that have rest mass and cannot overlap or combine which are called [fermions](https://en.wikipedia.org/wiki/Fermions).

[![subatomic particles](https://github.com/eq19/maps/assets/8466209/d54d3cd4-ee66-400b-a9cc-d7e0b888b468)](https://en.wikipedia.org/wiki/Subatomic_particle)

Experiments show that light could behave like a [stream of particles](https://en.wikipedia.org/wiki/Stream_of_particles) (called [photons](https://en.wikipedia.org/wiki/Photon)) as well as exhibiting wave-like properties. This led to the concept of [wave–particle duality](https://en.wikipedia.org/wiki/Wave%E2%80%93particle_duality) to reflect that quantum-scale particles behave both like particles and like [waves](https://en.wikipedia.org/wiki/Wave); they are sometimes called wavicles to reflect this. _([Wikipedia](https://en.wikipedia.org/wiki/Subatomic_particle))_
```

```txt
 Bispinors | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19
-----------+---------+---------+-----------+-----------+------------+-- 17
bispinor-2 |    2    |    3    |     3     |    18     |     24     |   i5+i7 ✔️
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |   11
-----------+---------+---------+-----------+-----------+------------+-- 19
bispinor-4 |    2    |    3    |     3     |    18     |     24     |   i13+i5 ✔️
===========+=========+=========+===========+===========+============+===========
     Total |    8    |   12    |    12     |    72     |     96     |   66+i30
```

## Parsering Structure

This scheme goes to the unification of 11s with 7s to 18s meanwhile the 11th it self behave as residual by the 5th minor hexagon between the ***[30 to 36' cells](https://www.eq19.com/exponentiation/#fundamental-forces)***.

```note
The interaction of any pair of fermions in perturbation theory can be modelled as:

***Two fermions go in → interaction by boson exchange → Two changed fermions go out.***

The exchange of bosons always carries energy and momentum between the fermions, thereby ***changing their speed and direction***. The exchange may also transport a charge between the fermions, changing the charges of the fermions in the process (e.g., turn them from one type of fermion to another). Since bosons carry one unit of angular momentum, ***the fermion's spin direction will flip from +1⁄2 to −1⁄2 (or vice versa)*** during such an exchange (in units of the reduced Planck's constant). _([Wikipedia](https://en.wikipedia.org/wiki/Fundamental_interaction))_
```

***36th prime - 30th prime = 151 - 113 = 1 + 37***

[![Defining the Prime Hexagon](https://user-images.githubusercontent.com/8466209/282279534-a448cd09-3d5e-4006-a84d-2574f7ed85c3.png)](https://www.hexspin.com/defining-the-prime-hexagon/)

The boson, photon and gravity forces are assigned to ***30, 31 and 32***. Gluon force and exchange are assigned to ***33 and 34*** which are then standing as the ***[lexer](https://www.eq19.com/multiplication/#assigning-a-lexer)*** and ***[parser](https://www.eq19.com/exponentiation/#parsering-structure)***.

```note
Below we will demonstrate how factorization algorithms and twin prime dyad cycling at the digital root level rotate the vertices of ***equilateral triangles within {9/3}*** star polygons like the one pictured above. These rotations are ***encoded in 3 x 3 matrices generated by period-24 digital root dyad tri-level cycling***. We will also reveal the Latin Square reflecting {3,6,9} hidden in plain sight betwixt and between the twin prime distribution channels; ***all of its rows, columns and principal diagonals summing to 18***. _[PrimesDemystified](https://www.primesdemystified.com/twinprimes.html)_
```

***19 + 18 + 102 = 37 + 102 = 139 = 34th prime = (40 - 6)the prime***

[![exponentiation zones](https://user-images.githubusercontent.com/8466209/200024664-afc433a0-5f7f-4ec1-9bfc-77d672817fed.png)](https://github.com/eq19)

This lead to a consequence of _[SU(5) grand unification](https://github.com/eq19/maps/files/14394752/MWmassShiftTalk.pdf)_ ***(assigned to 35)*** showing a complex scalar Higgs boson of 24 gauge groups _[observe mass of W boson](https://www.sciencedirect.com/science/article/pii/S0370269322004403)_ ***(assigned to 36)***.

```tip
An overview of the various families of elementary and composite particles, and their interactions. Fermions are on the left, and Bosons are on the right.

[![Elementary Particle](https://github.com/eq19/maps/assets/8466209/b6b6ea3c-cbbc-431c-b767-ecabf1cba933)](https://en.wikipedia.org/wiki/Fundamental_interaction)

According to the [Standard Model](https://en.wikipedia.org/wiki/Standard_Model_of_Particle_Physics) ***there are five (5) elementary bosons with thirteen (13) variations***. These 5 and 13 will be assigned to the "5xid's of **31~35** (sequenced)" and "13xid's of **36~68** (unsequenced)", respectively (see the sidebar menu).
- One (1) [scalar boson](https://en.wikipedia.org/wiki/Scalar_boson) (***spin = 0***) [Higgs boson](https://en.wikipedia.org/wiki/Higgs_boson) – the particle that contributes to the phenomenon of [mass](https://en.wikipedia.org/wiki/Mass) via the [Higgs mechanism](https://en.wikipedia.org/wiki/Higgs_mechanism) (assigned to "19xid's of **2~30**").
- Four (4) [vector bosons](https://en.wikipedia.org/wiki/Vector_boson) (***spin = 1***) that act as [force carriers](https://en.wikipedia.org/wiki/Force_carriers). These four are the [gauge bosons](https://en.wikipedia.org/wiki/Gauge_boson), they have ***twelve (12) different types*** originated from the interaction on _[bispinor-2 and -3](https://www.eq19.com/multiplication/12.html#free-parameters)_ to the _twelve (12) spinors of majorana_:
  - [γ](https://en.wikipedia.org/wiki/Photon) [Photon](https://en.wikipedia.org/wiki/Photon) – the force carrier of the [electromagnetic field](https://en.wikipedia.org/wiki/Electromagnetic_field) (**id:31**).
  - [g](https://en.wikipedia.org/wiki/Gluon) [Gluons](https://en.wikipedia.org/wiki/Gluon) (***eight (8) different types***) – force carriers originated from the _eight (8) spinors of bispinor-1 to -4_ that mediate the [strong force](https://en.wikipedia.org/wiki/Strong_interaction) (**id:33**)
  - [Z](https://en.wikipedia.org/wiki/Z_boson) [Neutral weak boson](https://en.wikipedia.org/wiki/W_and_Z_bosons) – the force carrier that mediates the [weak force](https://en.wikipedia.org/wiki/Weak_interaction) and
  - [W±](https://en.wikipedia.org/wiki/W_boson) [Charged weak bosons](https://en.wikipedia.org/wiki/W_and_Z_bosons) (***two (2) types***) – force carriers that mediate the weak force (**id:34**).
- A second order tensor boson (***spin = 2***) called the [graviton](https://en.wikipedia.org/wiki/Graviton) (G). It has been hypothesised as the force carrier for [gravity](https://en.wikipedia.org/wiki/Gravitational_force) (**id:32**).
```

[![The exchange of virtual pions](https://user-images.githubusercontent.com/8466209/282278731-ac8438f7-afd4-41f8-8c6a-a41c0d740825.png)](https://www.eq19.com/identition/#partition-function)

So the 36 should behave as a central. Therefore the total files that inherited from this scheme will be `1 + 7 + 29 = 37` including [one (1) main page](https://www.eq19.com). 

***109 = 29th prime = (10th prime)th prime***

[![self repetition](https://github.com/eq19/maps/assets/8466209/bde2248a-2feb-4c4b-85fe-f75de640775d)](https://www.eq19.com/exponentiation/#self-repetition)

This behaviour finaly brings us to a suggestion that the dimension in string theory are linked with ***the prime distribution level*** as indicated by the _[self repetition](https://www.eq19.com/exponentiation/#self-repetition)_ on MEC30.

```note
***There are 7 hidden dimensions in 11-d Supergravity, which is the low energy approximation to M theory, which also has 7 hidden dimensions***. _([Prime Curios!](https://t5k.org/curios/page.php?curio_id=20686))_
```

***π(1000) - loop(1,30) - loop(31,36) = 168 - 29 - 25 = 114***

[![IMG_20240114_014704](https://user-images.githubusercontent.com/36441664/262341222-6c71005e-2f44-45d9-ac42-b1464c045a45.png)](https://www.eq19.com/multiplication/#77s-structure)

By the _[identition zones](https://www.eq19.com/identition/)_ we are going to discuss in detail how this reversal behaviour of 8-dimensions is converting the 11 dimensions to `7 x 11 = 77` partitions.

## Grand Unification

When recombination is occur then the prime **13 is forced to → 12** where the impact (Δ1) goes to 18+13+12=43 on the last 7th row. 

[![tensors_flowing](https://github.com/user-attachments/assets/19d09186-a8e7-40af-83d3-516954da49bd)](https://github.com/search?q=%5Bubuntu-latest%2C+macos-latest%2C+windows-latest%5D+path%3A*.yml+path%3A.github%2Fworkflows+language%3AYAML&type=Code&ref=advsearch&l=YAML&l=)

Let's say you have a defaut configuration of π(10)=2,3,5,7. How do you present your html page in order that all of the page elements are represented by the primes without any missing parts?

```html
      <html> → (29=10th prime) → next favicon
        Δ     <head> ← (10)
        |          <style>  - 5 ‹----
        |                     Δ      |
        3(29=10+19)‹------ favicon - 2,3,5=π(5)
                   </style>          |
             </head>               (89²)
              <body> ← (19)          |
                   <script> - 7 ‹----
                   </script>
             </body
      </html>
```

Ploting ***40th prime scheme*** of the three (3) layers with all the features of 3rd prime identity as explained above then they would form their recycing through the three (3) times bilateral 9 sums as shown below.

***89^2 - 1 = 7920 = 22 x 360 = 66 x 120 = (168 - 102) x 120***

```
$True Prime Pairs:
(5,$True Prime Pairs:
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
  
layer | node | sub |  i  |  f                               
------+------+-----+---------- 
      |      |     |  1  | -------------------- _site ---  71 = 72-1
      |      |  1  +-----+                        |
      |  1   |     |  2  | (5)                  _saas
      |      |-----+-----+                        |
      |      |     |  3  | ---------            _data
  1   +------+  2  +-----+----      |             |
      |      |     |  4  |         5x ---       _posts
      |      +-----+-----+          |     |       |
      |  2   |     |  5  | (7) -----      |     _drafts
      |      |  3  +-----+                |       |
289+11=300   |     |  6  |                |     _plugins
------+------+-----+-----+----- 72 x 6   7x ------------ 11x = 77 (rational)◄--
      |      |     |  7  |                |     _includes                      |
      |      |  4  +-----+                |       |                            |
      |  3   |     |  8  | (11)  ---      |     _layouts                       |
      |      +-----+-----+          |     |       |                            |
      |      |     |  9  |         2x ---        assets  (69 = 72-3)           |
  2   +------|  5  +-----+-----     |             |                            |
      |      |     |  10 | ---------            _saas                          |
      |      |-----+-----+                        |                            |
      |  4   |     |  11 | (13) ----------------_site --  71 = 72-1            |
      |      |  6  +-----+                                                     |
329+71=400   |     |  12 |------------------------------  70 = 72-2            |
------+------+-----+-----+                                                    11x
      |      |     |  13 |                                                     |
      |      |  7  +-----+                                                     |
      |  5   |     |  14 | (17) ◄------------------------------------------- (17)
      |      |-----+-----+                                                     |
      |      |     |  15 | ◄-- 42 x 6 partitions of 13 (irrational)            |
  3   +------+  8  +-----+-----                                                +
      |      |     |  16 |                                                     |  
      |      |-----+-----+                                                     |
      |  6   |     |  17 | (19) ◄------------------------------------------- (19)
      |      |  9  +-----+                                                     |
168+32=200   |  |  |  18 |------------------------------  68 = 72-4            |
------|------|--|--+-----+                                                     |
       900 -----                                                               |
                                                                               |
```

Going deeper there are many things raised up as questions. So in this project we are going to analyze it using a javascript library called _[Chevrotain](https://dev.to/codingwithadam/introduction-to-lexers-parsers-and-interpreters-with-chevrotain-5c7b)_.

```note
There are 3 primary concepts in the diagram. We will start with an intro to lexers (tokenization), parsers, grammars and much more. Then build a simple calculator that uses all these concepts.
- The lexer which takes input as a string and converts the input into a set of tokens.
- The Parser which takes the tokens from the lexer and returns a syntax tree based on a grammar. The grammar is often expressed in a meta language such as Backus-Naur Form (BNF). The grammar is the language of languages and provides the rules and syntax.
- The interpreter which takes in the syntax tree and evaluates the result. In this case we return the result of calculator input.

Other than building a simple calculator using chevrotain the concepts that we will learn here are those that are used to build programming languages like javascript, .net, SQL and much more. Perhaps one day you will make your own language. _[Chevrotain](https://dev.to/codingwithadam/introduction-to-lexers-parsers-and-interpreters-with-chevrotain-5c7b)_
```

[![Lexers, Parsers and Interpreters with Chevrotain](https://user-images.githubusercontent.com/8466209/241206698-b4128e07-81ea-4eab-a14a-5d881836b924.png)](https://dev.to/codingwithadam/introduction-to-lexers-parsers-and-interpreters-with-chevrotain-5c7b)

Since the _modulo 6_ is occured all over the spin then we have defined that this 4 zones should stand as ***default configuration*** as you can see on the left sidebar. 

```tip
In order to maintain the 18's structure between each of repositories to correlate with the above density then we could use a hierarchical database that stores low-level settings for the operating system such as _[windows registry](https://en.wikipedia.org/wiki/Windows_Registry)_.
```

[![windows registry](https://user-images.githubusercontent.com/8466209/230746478-0146e88e-22ba-4f1b-abf2-c5226c1a56ca.png)](https://www.eq19.com/exponentiation/)

Using the javascript library from _[Chevotrain](https://www.eq19.com/addition/#structure-minor-hexagons)_ and data parser from _[Jekyll/Liquid](https://jekyllrb.com/docs/datafiles/)_ finally we found the correlation between the lexer and parser trough _[the powers of pi](https://www.eq19.com/identition/#the-powers-of-pi)_.

```note
In this example, the content from a Markdown document `document.md` that specifies `layout: docs` gets pushed into the `{% raw %}{{ content }}{% endraw %}` tag of the layout file `docs.html`. Because the docs layout itself specifies `layout: page`, the content from `docs.html` gets pushed into the `{% raw %}{{ content }}{% endraw %}` tag in the layout file `page.html`. Finally because the page layout specifies `layout: default`, the content from `page.html` gets pushed into the `{% raw %}{{ content }}{% endraw %}` tag of the layout file `default.html`. _([JekyllRb](https://jekyllrb.com/tutorials/convert-site-to-jekyll/#how-layouts-work))_
```

[![Parsering](https://github-production-user-asset-6210df.s3.amazonaws.com/8466209/260864973-50fbc0a0-7441-4800-97aa-265b0dfd2ac2.png)](https://hub.docker.com/layers/jekyll/jekyll/latest/images/sha256-400b8d1569f118bca8a3a09a25f32803b00a55d1ea241feaf5f904d66ca9c625)

It is going to setup **[CI/CD](https://en.wikipedia.org/wiki/CI/CD)** for up to _[1000 public repositories](https://gist.github.com/eq19/b32915925d9d365e2e9351f0c4ed786e)_ out of millions that available on GitHub. You may visit our _[mapping scheme](https://www.eq19.com/maps/exponentiation/span17/)_ for more detail.

```note
This is the partial of [the whole scheme](https://github.com/chetabahana/chetabahana.github.io/wiki/Skema#Implementasi) from our [Quantum Project](https://github.com/eq19) based on the algorithm of **DNA Recombination: [M+F](https://github.com/chetabahana/chetabahana.github.io/blob/Chetabahana/_layouts/feed.rb) to [C1+C2](https://github.com/chetabahana/chetabahana.github.io/blob/workflows/_includes/data/roots.rb):**

[![Quantum Project - The Concept of Primes Algorithm by DNA Recombination](https://user-images.githubusercontent.com/36441664/88602920-fd84c080-d09d-11ea-970d-dd63c12221fc.png)](https://github.com/eq19/maps)

The _M+F_ symbols will stand as: [Project Maps (M)](https://github.com/eq19/maps) + [Project Feed (F)](https://github.com/eq19/feed) while<br>
_C1+C2_ as implementations, see sample: [Project Base (C1)](https://chetabahana.github.io/) + [Project Core (C2)](https://chetabahana.com/).

[![Lexers vs Parsers](https://user-images.githubusercontent.com/36441664/70385860-e5074f00-19c3-11ea-92f3-ec6f33bf9774.png)](https://stackoverflow.com/questions/2842809/lexers-vs-parsers)

The final result of this Q(19,10) would form π(10)=(2,3,5,7) as the [1st row of 19](https://github.com/eq19/quantum#1st-step-q10-30).
```

[![mapping scheme](https://user-images.githubusercontent.com/36441664/162069734-fc8036a1-fd2d-4fc9-bcad-f677388b76fa.jpg)](https://www.eq19.com/maps/exponentiation/span17/)

Such of method is used to generate a _[basic grammar](https://github.com/chetabahana)_ which algorithm is adaptable for any kind of implementations or applications.

## Default Configuration

The 619 is the **114th prime**. By the _[True Prime Pairs](#true-prime-pairs)_ it is laid on the last index of 6 with prime 19 where as **6x19** is also 114. Let's put 19 hexagons within the 3 layers. 

***168+618 - 19x6x6 = 786 - 684 = 102***

[![entry and exit point](https://user-images.githubusercontent.com/8466209/225589915-8f7690c8-4c17-4232-be51-63e79efb2c51.png)](https://www.eq19.com/exponentiation/#parsering-structure)

This sequence is [simulated](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#the-implementation) by a flowchart having 12 arrows flowing on 10 (ten) shapes of prime 31 up to 71 (**40 nodes**).

***6+6 + 6/\6 = 6+6 + 15 = 27-day month***

[![flowchart](https://user-images.githubusercontent.com/36441664/128732737-81762604-0ae0-4a90-b5a8-30921cf46efb.png)](https://gist.github.com/eq19/b32915925d9d365e2e9351f0c4ed786e#assigning-repositories)

By this project the above would be [deployed](https://www.moncefbelyamani.com/making-github-pages-work-with-latest-jekyll/) as **default layout**. It is set to be avalaible throughout the whole platform via [a single page](https://github.com/eq19/parser/blob/eQ19/_layouts/default.liquid) within a parser repository which is acting as _[prime 13](https://gist.github.com/eq19/d2336e28e79702acf38edd182003d5e0#primes-mapping)_. Their [interface](https://eq19.github.io/sitemap/scheme.html) will be in _[json](https://www.eq19.com/feed.json)_ and _[xml](https://www.eq19.com/grammar/feeds.xml)_ format. 

Here is for the sample:

```json
{
  "title":"Mapping System",
  "content":"<p>Hello, <strong>world</strong>.\nI am here.</p>\n",
  "links": [
    {"title":"Introduction","url":"https://www.eq19.com/intro/"},
    {"title":"Go tour on Mapping System ","url":"https://www.eq19.com/maps/"},
    {"title":"A backed pretty display for markdown","url":"https://www.eq19.com/gistio/"},
    {"title":"Gist.io for programmers","url":"https://gist.io/@eq19/d2336e28e79702acf38edd182003d5e0"}
  ]
}
```

Using a kind of [interface](https://gist.github.com/MichaelCurrin/6777b91e6374cdb5662b64b8249070ea) such as _[docker](https://docs.docker.com/ci-cd/github-actions/)_ then it could be developed cross platform. Evenso. Let assume that all alpabethic letter in [the sequence](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#primes-platform) is representing a local disk so you may build _[your own pattern](https://gist.github.com/eq19/b32915925d9d365e2e9351f0c4ed786e)_ in your PC such as shown below:

```note
Still far from production but at least it has a minimum error. You may check the running code starting with [Sequence Diagram](https://chetabahana.github.io/#chetabahana-skema?pad=2) shown below which is developed as [the initial step](https://github.com/eq19/quantum#tabulate-prime-by-the-power-of-168) on building the **[10143 Grammars](https://github.com/eq19/quantum#7th-step-q19-10)**.

[![Sequence Diagram](https://user-images.githubusercontent.com/36441664/107134254-ee22e180-6922-11eb-9465-3dd64ebf7dca.png)](https://chetabahana.github.io/#chetabahana-skema?pad=2)

This sample was developed by converting [eQuantum](https://github.com/eq19) to [eCommerce](https://github.com/MarketLeader) using the cyclic algorithm of **[168](https://github.com/eq19/quantum#tabulate-prime-by-the-power-of-168) vs [618](https://github.com/eq19/quantum#next-target-tabulate-prime-by-618)** that act as [Lexer and Parser](https://stackoverflow.com/questions/2842809/lexers-vs-parsers).

![](https://user-images.githubusercontent.com/36441664/69475449-ce77ca00-0dff-11ea-964e-cc959db0740a.png)

Although the code is already running but however it is not yet user friendly as it could run only in _[GitHub API Platform](https://docs.github.com/en/developers)_.

![](https://user-images.githubusercontent.com/36441664/86481184-b72b9280-bd79-11ea-899b-51db929fc3d2.png)

Mapping the quantum way within a huge of primes objects (5 to 19) by lexering (11) the ungrammared feed (7) and parsering (13) across syntax (17) _([₠Quantum](https://github.com/eq19))_.
```

[![default](https://github.com/user-attachments/assets/fdcf5ccd-3f08-454e-8f6c-cad1a8aae35d)](https://github.com/iree-org/iree?tab=readme-ov-file)

This also introduces a _[lower bound](https://www.primesdemystified.com/Factorization.html)_ of Mod 90 originated from the 4th coupling of MEC30 which is holded by ***five (5) cells between 13 and 17***.

```note
The Minimal Supersymmetric Standard Model (MSSM) contains two Higgs doublets, leading to _five (5) physical [Higgs bosons](https://www.sciencedirect.com/topics/physics-and-astronomy/higgs-bosons)_:
- one (1) neutral CP-odd (A) 👈 ***degenerated with (h or H)*** 
- two (2) charged states ***(H+ and H−)***,
- Two (2) neutral CP-even states ***(h and H)***.

_At tree-level, the masses are [governed](https://github.com/eq19/maps/files/14066329/76104_ANGELESCU_2017_diffusion.pdf)
 by two parameters, often taken to be mA and tan β [3]. When tan β >> 1, A is nearly [degenerated](https://github.com/eq19/maps/files/14066343/epjconf_qfthep2019_04006.pdf)
 with one of the CP-even states (denoted ϕ)_. _([ScienceDirect](https://www.sciencedirect.com/topics/mathematics/higgs-mechanism))_
```

[![the 5 cells](https://github.com/eq19/maps/assets/8466209/d3c8e7cb-2239-4b93-a4be-97e3ddbc8c94)](https://www.eq19.com/multiplication/18.html#higgs-mechanism)

By [The GitHub Runner](https://github.com/actions/runner) you can [connect](https://github.com/tcardonne/docker-github-runner) to the [Google COS Instance](https://gist.github.com/eq19/e9832026b5b78f694e4ad22c3eb6c3ef#container-optimized-os). For self-hosted runners defined at the organization level, configure [runs-on.group](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners-in-a-workflow#about-self-hosted-runner-groups) in your workflow file to target a [runner groups](https://docs.github.com/en/actions/using-jobs/choosing-the-runner-for-a-job#choosing-runners-in-a-group) or [combine groups and labels](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners-in-a-workflow#using-default-labels-to-route-jobs).

```note
Why collaborating with physicists?
- Contribute to the understanding of the Universe.
- Open methodological challenges.
- Test bed for developing ambitious ML/AI methods, as enabled by the precise mechanistic understanding of physical processes.
- Core problems in particle physics transfer to other fields of science (likelihood-free inference, domain adaptation, optimization, etc).
- A high-level summary of various aspects of [machine learning in LHC](https://github.com/eq19/maps/files/14396836/Pata.slides.pdf) data reconstruction, mostly based on CMS examples. A short summary of a particular use case: ML for combining signals across detector subsystems with particle flow. This talk is in personal capacity (not representing CMS or CERN), representing my biased views.

You can find a great and fairly complete overview of [ML papers in HEP](https://iml-wg.github.io/HEPML-LivingReview/). _([Pata Slides](https://github.com/eq19/maps/files/14396836/Pata.slides.pdf))_
```

***π(10) = 2,3,5,7***

[![SO(10)](https://github.com/eq19/maps/assets/8466209/b1d3bccd-a423-4ebb-a397-e973b2cc8e6e)
](https://en.wikipedia.org/wiki/Grand_Unified_Theory)

[![teaching-machines-glouppe_compressed.pdf](https://user-images.githubusercontent.com/8466209/222966425-9da703ef-9189-44e6-8fc1-8b766cf9f7bb.png)](https://www.eq19.com/identition/)

This way will also be our approach to [Euler's identity](https://gist.github.com/eq19/e9832026b5b78f694e4ad22c3eb6c3ef#eulers-identity). By taking the correlation between ***f(π) as P*** vs ***f(i) as NP*** where ***e<sup>iπ</sup> + 1 = 0*** then [theoretically](https://github.com/eq19/maps/files/13765788/teaching-machines-glouppe_compressed.pdf) they shall be correlated to get an expression of the prime distribution similar to _[MEC30](https://gist.github.com/eq19/e9832026b5b78f694e4ad22c3eb6c3ef#eulers-identity)_.
