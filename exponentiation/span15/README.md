---
sort: 24
spin: 33
span: 
suit: 131
description: 
---
# Chromodynamics (lexer)

Quantum Chromodynamics ([QCD](https://en.wikipedia.org/wiki/Quantum_chromodynamics)) is the theory of the strong interactions that glue together quarks inside protons and neutrons, the constituents of ordinary matter.

{% include list.liquid all=true %}

Is QCD a confining theory ? This is one of the fundamental questions and constitutes one of the famous [Millennium Prize problems](http://www.claymath.org/millennium-problems).

## Feynman diagram

This section serve to study the internal (color) rotations of the [gluon fields](https://en.m.wikipedia.org/wiki/Gluon_field) associated with the coloured quarks in [quantum chromodynamics](https://en.m.wikipedia.org/wiki/Quantum_chromodynamics) of [colours of the gluon](https://en.m.wikipedia.org/wiki/Gluon#Eight_gluon_colours). 

```note
In this Feynman diagram, an electron (e−) and a positron (e+) annihilate, producing a photon (γ, represented by the blue sine wave) that becomes a quark–antiquark pair (quark q, antiquark q̄), after which the antiquark radiates a gluon (g, represented by the green helix).
```

[![default](https://user-images.githubusercontent.com/8466209/224185881-0d1c448e-ee04-4ad2-87e2-1da3c864643c.png)](https://en.wikipedia.org/wiki/Feynman_diagram)

Like electromagnetism ([QED](https://eq19.github.io/maps/exponentiation/span17/)), it is a gauge theory, where the force between charged particles originates in the exchange of intermediate massless vector bosons: _one photon in the case of QED and eight gluons in the case of QCD_.

```note
QCD is extremely predictive:
- One gauge coupling constant, six quark masses and the so-called theta vacuum angle are the only free parameters from which a plethora of phenomena can in principle be predicted, such as the spectrum of hadrons and their interactions.
- The famous theta vacuum angle is the only source of CP violation (asymmetry between matter and antimatter) of the strong interactions, but has been constrained from the measurement of the neutron electric dipole moment to be unnaturally small.

The fact that this parameter is so small is the so-called strong CP problem.
```

![quark-quark_scattering](https://github.com/eq19/maps/assets/8466209/06a2f256-191f-438b-aa24-0c8d75bb254e)

This exponentiation takes important roles since by the _[multiplication zones](https://eq19.github.io/multiplication/#parsering-structure)_ the MEC30 forms a matrix of  `8 x 8 = 64 = 8²` where the power of 2 stands as exponent

```note
During the last few years of the 12th century, ***Fibonacci*** undertook a series of travels around the Mediterranean. At this time, the world’s most prominent mathematicians were Arabs, and he spent much time studying with them. His work, whose title translates as the Book of Calculation, was extremely influential in that ***it popularized the use of the Arabic numerals in Europe***, thereby revolutionizing arithmetic and allowing scientific experiment and discovery to progress more quickly. _([Famous Mathematicians](https://famous-mathematicians.org/leonardo-pisano-bigollo/))_
```

[![MEC30 Square](https://user-images.githubusercontent.com/36441664/262213707-63aa0a64-cf7d-4fb7-9f1a-f3d1ba805643.png)](https://eq19.github.io/multiplication/#parsering-structure)

The gauge symmetry of QCD is based on the special unitary group, SU(3), and the associated charge is called color. Quarks carry three basic charges or colors: red, blue and green.

```note
In spite of the simplicity of the QCD Lagrangian, quantitative predictions are highly non trivial.
- Indeed the colored quarks or gluons have not been observed in isolation.
- This fact is referred to as confinement, an essential property of QCD which implies that only states that carry no color charge can propagate freely.

The neutral composites that we observe in nature are the hadrons: mesons composed of a quark and an antiquark, or baryons composed of three quarks.
```

![SmallBookPile](https://github.com/eq19/maps/assets/8466209/0971f647-c8f7-4fc7-8ec6-0a11e1767773)

Since the first member is 30 then the form is initiated by a matrix of `5 x 6 = 30` which has to be transformed first to `6 x 6 = 36 = 6²` prior to the above MEC30's square. 

```note
A square system of coupled nonlinear equations can be solved iteratively by Newton's method. This method uses the Jacobian matrix of the system of equations. _([Wikipedia](https://en.wikipedia.org/Jacobian_matrix_and_determinant))_
```

[![gradien](https://user-images.githubusercontent.com/36441664/128025898-187ba576-795f-4578-af71-ff02a8b682b1.png)](https://eq19.github.io/multiplication/#transformation-to-exponentiation)

By the paper of _[Standard Model Physics from an Algebra](https://arxiv.org/abs/1611.09182)_ the Complex octonions have been used to describe the generations of [quarks](https://en.wikipedia.org/wiki/Quark) and [leptons](https://en.wikipedia.org/wiki/Lepton)

```txt
Decoded Complex Numbers:

[01] (r1.0 + i1.0j)  ‹--- quark-1
[02] (r2.0 + i2.0j)  ‹--- quark-2
[03] (r3.0 + i3.0j)  ‹--- quark-3
[04] (r4.0 + i4.0j)  ‹--- quark-4
[05] (r5.0 + i5.0j)  ‹--- quark-5
[06] (r6.0 + i6.0j)  ‹--- quark-6
[07] (r7.0 + i7.0j) 👈 Center of Metatron ✔️
[08] (r8.0 + i8.0j)    ‹--- lepton-1
[09] (r9.0 + i9.0j)    ‹--- lepton-2
[10] (r10.0 + i10.0j)  ‹--- lepton-3
[11] (r11.0 + i11.0j)  ‹--- lepton-4
[12] (r12.0 + i12.0j)  ‹--- lepton-5
[13] (r13.0 + i13.0j)  ‹--- lepton-6
```

Given a Model, _[MARTY](https://gitHub.com/eq19/lexer)_ may compute symbolically and automatically theoretical quantities. First, Feynman rules are derived.

[![A Modern ARtificial Theoritical phYsicist (MARTY)](https://github.com/user-attachments/assets/9080b501-65ac-4eb7-b4d9-477e4f8bb4ad)](https://gitHub.com/eq19/lexer)

A gauge colour rotation is _[a spacetime-dependent SU(3)](https://en.m.wikipedia.org/wiki/Special_unitary_group#The_group_SU(3))_ group element. They span the [Lie algebra](https://github.com/lkpetrich/Semisimple-Lie-Algebras) of the SU(3) group in the defining representation.

```note
One of the more mature applications of LQCD simulations is precisely the study of confinement and asymptotic freedom. Simulations have demonstrated that the energy between a quark and antiquark pair increases linearly with their separation.
- The running of the QCD gauge coupling has been also studied beyond perturbation theory confirming the property of asymptotic freedom and providing the most accurate determination of the QCD coupling strength, as can be seen from the upper-right figure.
- Nevertheless, there are still important limitations in lattice simulations. One of the major difficulties has to do with the treatment of the quark degrees of freedom. It is very difficult to maintain the chiral properties of the continuum action, which is mandatory to simulate the light quarks. Very important progress has been made in the last decade on this problem. Fermion discretizations that can maintain chiral properties have been found (domain wall fermions and overlap fermions), and variants of the most cost-effective Wilson fermions with improved chiral behaviour, the so-called twisted-mass Wilson fermions, have made the simulation of the chiral regime feasible.
- Furthermore important algorithmic improvements (like Schwarz preconditioning, deflation acceleration, trivializing maps and the Wilson flow and open boundary conditions and twisted-mass reweighting) have been necessary to incorporate efficiently the contribution of quarks to the path integral, which represents the quantum effects of virtual quark-antiquark pairs. State-of-the-art simulations nowadays include the most relevant quark effects: those of the two lightest u and d quarks (Nf=2 simulations), those plus the strange quark (Nf=2+1 simulations) and more recently also the charm quark (Nf=2+1+1 simulations) has been included.
- The lattice approach is not universally applicable but has been used to compute from first principles many physical quantities beyond the QCD coupling constant, including the hadron mass spectrum, the quark condensate, quark masses, decay constants and form factors for leptonic and semileptonic decays.
- Also the lattice approach is mandatory in computing weak matrix elements, such as the K or B-parameters of meson-antimeson oscillations that are very important for the precise determination of the elements of the CKM mixing matrix, and for performing consistency checks of unitarity and searching possible physics beyond the SM.
- Another important contribution of lattice QCD is the computation of the moments of parton and gluon distribution functions, essential for the calculation of cross sections in the LHC and Tevatron, as well as the isosinglet and strange sigma terms that play a role in the direct searches for dark matter.

The lattice is also the method to study QCD in extreme conditions (high temperature and density) such as those that would be found in the early Universe or in astrophysical objects such as neutron stars _([IFIC](https://webific.ific.uv.es/web/en/content/lattice-qcd-numerical-approach-strong-force))_.
```

![images6-ezgif com-resize](https://github.com/eq19/maps/assets/8466209/9831d77d-9c18-4691-b0be-5bb244509368)

The simplest theory describing the above is the SU(3) one with the gluons as the basis states of the Lie algebra. That is, gluons transform in the adjoint representation of SU(3), which is 8-dimensional.

## Matrix Scheme

Quarks have three colors. Color is to the strong interaction as electric charge is to the electromagnetic interaction.

![quantum-chromodynamics-1-320](https://github.com/eq19/maps/assets/8466209/47786899-e7a8-4388-9d20-f0f7805e1ea9)

```liquid
red   anti-red,   red   anti-blue,   red   anti-green,
blue  anti-red,   blue  anti-blue,   blue  anti-green,
green anti-red,   green anti-blue,   green anti-green.
```

```note
Fermions and bosons—fermions have quantum spin = 1/2.
- The elementary fermions are leptons and quarks.
- There are three generations of leptons: electron, muon, and tau, with electric charge −1, and their neutrinos with no electric charge.
- There are three generations of quarks: (u, d); (c, s); and (t, b).

The (u, c, t) quarks have electric charge 2/3 while the (d, s, b) quarks have electric charge −1/3. _([IntechOpen](https://www.intechopen.com/chapters/71535))_
```

![UF1](https://github.com/eq19/maps/assets/8466209/649939c3-ad6d-427f-8ea6-6edb94229e08)

Interactions in quantum chromodynamics are strong, so perturbation theory does not work. Therefore, Feynman diagrams used for quantum electrodynamics cannot be used.

![UF2](https://github.com/eq19/maps/assets/8466209/4d602e7a-ac0c-4c36-9f3f-741c40af5249)

Bosons have quantum spin = 1: photon, quantum of the electromagnetic field; gluon, quantum of the strong field; and W and Z, weak field quanta, which we do not need.

```note
An animation of [color confinement](https://en.wikipedia.org/wiki/Color_confinement), a property of the strong interaction. If energy is supplied to the quarks as shown, the [gluon](https://en.wikipedia.org/wiki/Gluon) tube connecting [quarks](https://en.wikipedia.org/wiki/Quark) elongates until it reaches a point where it "snaps" and the energy added to the system results in the formation of a quark–[antiquark](https://en.wikipedia.org/wiki/Antiquark) pair. Thus single quarks are never seen in isolation. _([Wikipedia](https://en.wikipedia.org/wiki/Strong_interaction))_
```

[![Gluon_tube-color_confinement_animation](https://user-images.githubusercontent.com/8466209/297354091-7821a500-dbec-4672-b81c-1381a8c7ca32.gif)](https://en.wikipedia.org/wiki/Strong_interaction)

```txt
  Fermion  | spinors | charged | neutrinos |   quark   | components | parameter
   Field   |   (s)   |   (c)   |    (n)    | (q=s.c.n) |  Σ(c+n+q   | (complex)
===========+=========+=========+===========+===========+============+===========
bispinor-1 |    2    |    3    |     3     |    18     |     24     |   19+i5
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-2 |    2    |    3    |     3     |    18     |     24     |   17+i7 👈
===========+=========+=========+===========+===========+============+===========
bispinor-3 |    2    |    3    |     3     |    18     |     24     |   11+i13
-----------+---------+---------+-----------+-----------+------------+-----------
bispinor-4 |    2    |    3    |     3     |    18     |     24     |   19+i5
===========+=========+=========+===========+===========+============+===========
     Total |    8    |   12    |    12     |    72     |     96     |   66+i30
```

```note
When the digital root of perfect squares is sequenced within a ***modulo 30 x 3 = modulo 90 horizon***, beautiful symmetries in the form of period-24 palindromes are revealed, which the author has documented on the On-Line Encyclopedia of Integer Sequences as [Digital root of squares of numbers not divisible by 2, 3 or 5 (A24092)](https://oeis.org/A240924):

1, 4, 4, 7, 1, 1, 7, 4, 7, 1, 7, 4, 4, 7, 1, 7, 4, 7, 1, 1, 7, 4, 4, 1

In the matrix pictured below, we list ***the first 24 elements*** of our domain, take their squares, calculate the modulo 90 congruence and digital roots of each square, and display the digital root factorization dyad for each square (and map their collective bilateral 9 sum symmetry).  _([PrimesDemystified](https://primesdemystified.com/#Distribution_of_Perfect_Squares))_
```

[![root profiles](https://user-images.githubusercontent.com/36441664/277179073-e0411710-779e-4cea-8a37-ff7c635f46f7.png)](https://eq19.github.io/exponentiation/folder14/#root-profiles)

Both 1/89 and 1/109 have the Fibonacci sequence _[encoded in their decimal expansions](https://eq19.github.io/addition/#minor-hexagons)_ illustrates a period-24 palindromic that bring ***[the powers of pi](https://eq19.github.io/multiplication/#lineage-retracement)***. 

***7 x π(89) = 7 x 24 = 168 = π(1000)***

![](https://user-images.githubusercontent.com/8466209/244855108-b80b3c2e-1a13-4b55-828a-72ed15b448dd.png)

## Interactions

```
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

The subclasses of partitions systemically develops characters similar to the distribution of prime numbers. 

```note
***Unlike the strong force, the residual strong force diminishes with distance, and does so rapidly***. The decrease is approximately as a negative exponential power of distance, though there is no simple expression known for this; see [Yukawa potential](https://en.wikipedia.org/wiki/Yukawa_potential). The rapid decrease with distance of the attractive residual force and the less rapid decrease of the repulsive electromagnetic force acting between protons within a nucleus, causes the instability of larger atomic nuclei, such as all those with [atomic numbers](https://en.wikipedia.org/wiki/Atomic_number) larger than 82 (the element lead). _([Wikipedia](https://en.wikipedia.org/wiki/Strong_interaction#Between_hadrons))_
```

![gifman](https://github.com/eq19/maps/assets/8466209/0f1df87d-b377-4903-b69c-8e41b0b72f82)

```note
Feynman diagram for the same process as in the animation, with the individual quark constituents shown, to illustrate how the fundamental strong interaction gives rise to the nuclear force. Straight lines are quarks, while ***multi-colored loops are gluons (the carriers of the fundamental force). Other gluons, which bind together the proton, neutron, and pion "in-flight", are not shown***. The π⁰ pion contains an anti-quark, shown to travel in the opposite direction, as per the Feynman–Stueckelberg interpretation. _([Wikipedia](https://en.wikipedia.org/wiki/Pion))_
```

[![residual strong force](https://user-images.githubusercontent.com/36441664/274776116-17603ba1-0e83-433e-a8e2-b3df5716ff00.png)](https://en.wikipedia.org/wiki/Nuclear_force)

```note
The Gell-Mann matrices, developed by [Murray Gell-Mann](https://en.m.wikipedia.org/wiki/Murray_Gell-Mann), are a set of eight [linearly independent](https://en.m.wikipedia.org/wiki/Linear_independence) 3×3 [traceless](https://en.wikipedia.org/wiki/Matrix_trace) [Hermitian matrices](https://en.wikipedia.org/wiki/Hermitian_matrices) used in the study of the [strong interaction](https://en.wikipedia.org/wiki/Strong_interaction) in [particle physics](https://en.wikipedia.org/wiki/Particle_physics). They span the [Lie algebra](https://en.wikipedia.org/wiki/Lie_group#The_Lie_algebra_associated_with_a_Lie_group) of the [SU(3)](https://en.wikipedia.org/wiki/Special_unitary_group#SU(3)) group in the defining representation.
- These matrices are [traceless](https://en.wikipedia.org/wiki/Traceless), [Hermitian](https://en.wikipedia.org/wiki/Hermitian_matrix), and obey the extra trace orthonormality relation (so they can generate [unitary matrix](https://en.wikipedia.org/wiki/Unitary_matrix) group elements of [SU(3)](https://en.wikipedia.org/wiki/SU(3)) through [exponentiation](https://en.wikipedia.org/wiki/Matrix_exponential)[[1]](https://en.m.wikipedia.org/wiki/Gell-Mann_matrices#cite_note-Scherer-Schindler-1)). These properties were chosen by Gell-Mann because they then naturally generalize the [Pauli matrices](https://en.wikipedia.org/wiki/Pauli_matrices) for [SU(2)](https://en.wikipedia.org/wiki/SU(2)) to SU(3), which formed the basis for Gell-Mann's [quark model](https://en.wikipedia.org/wiki/Quark_model).[[2]](https://en.wikipedia.org/wiki/Gell-Mann_matrices#cite_note-2) Gell-Mann's generalization further [extends to general SU(n)](https://en.wikipedia.org/wiki/Generalizations_of_Pauli_matrices#Construction). For their connection to the [standard basis](https://en.wikipedia.org/wiki/Root_system) of Lie algebras, see the [Weyl–Cartan basis](https://en.wikipedia.org/wiki/Clebsch%E2%80%93Gordan_coefficients_for_SU(3)#Standard_basis).
- Since the eight matrices and the identity are a complete trace-orthogonal set spanning all 3×3 matrices, it is straightforward to find two Fierz completeness relations, (Li & Cheng, 4.134), analogous to that [satisfied by the Pauli matrices](https://en.wikipedia.org/wiki/Pauli_matrices#Completeness_relation_2). Namely, using the dot to sum over the eight matrices and using Greek indices for their row/column indices
- A particular choice of matrices is called a [group representation](https://en.wikipedia.org/wiki/Group_representation), because any element of SU(3) can be written in the form using the ***[Einstein notation](https://en.wikipedia.org/wiki/Einstein_notation)***, where the eight 
 are real numbers and a sum over the index j is implied. Given one representation, an equivalent one may be obtained by an arbitrary unitary similarity transformation, since that leaves the commutator unchanged.
- The matrices can be realized as a representation of the [infinitesimal generators](https://en.wikipedia.org/wiki/Lie_group#The_Lie_algebra_associated_with_a_Lie_group) of the [special unitary group](https://en.wikipedia.org/wiki/Special_unitary_group) called [SU(3)](https://en.wikipedia.org/wiki/Special_unitary_group#The_group_SU(3)). The [Lie algebra](https://en.wikipedia.org/wiki/Lie_algebra) of this group (a real Lie algebra in fact) has dimension eight and therefore it has some set with eight [linearly independent](https://en.wikipedia.org/wiki/Linear_independence) generators, which can be written as 
g_{i}, with i taking values from [1 to 8](https://en.wikipedia.org/wiki/Gell-Mann_matrices#cite_note-Scherer-Schindler-1)

These matrices serve to study the internal (color) rotations of the ***[gluon fields](https://en.m.wikipedia.org/wiki/Gluon_field) associated with the coloured quarks of [quantum chromodynamics](https://en.m.wikipedia.org/wiki/Quantum_chromodynamics) (cf. [colours of the gluon](https://en.m.wikipedia.org/wiki/Gluon#Eight_gluon_colours))***. A gauge colour rotation is a spacetime-dependent SU(3) group element where summation over the eight indices (8) is implied. _[Wikipedia](https://en.wikipedia.org/wiki/Gell-Mann_matrices))_
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

     |    168    |    618    |
-----+-----+-----+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"             19¨
-----+-----+-----+-----+-----+                                             ---
 17¨ |  5¨ |  3¨ |  ❓ |  ❓ | 4¤ ✔️ --->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  .. |  .. |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-----+-----+-----+                                                    |
 11¨ |  .. |  .. |  .. | 3¤ ---->  Np(33)  assigned to "id:33"  ----->  👉 77¨
-----+-----+-----+-----+-----+                                              |
 19¨ |  .. |  .. |  .. |  .. | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  .. |  .. |  .. | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
 43¨ |  .. |  .. |  .. |  .. |  .. |  .. |  .. |  .. |  .. | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ       
```

From the 50 we gonna split the 15 by _bilateral 9 sums_ resulting 2 times 15+9=24 which is 48. So the total of involved objects is ***50+48=98***.

```note
Consider the evidence: scattering experiments strongly suggest a meson to be composed of a quark anti-quark pair and a baryon to be composed of three quarks. The famous 3R experiment also suggests that whatever force binds the quarks together has 3 types of charge (called the 3 colors).
- Now, into the realm of theory: we are looking for an internal symmetry having a 3-dimensional representation which can give rise to a neutral combination of 3 particles (otherwise no color-neutral baryons).
- The simplest such statement is that a linear combination of each type of charge (red + green + blue) must be neutral, and following William of Occam we believe that the simplest theory describing all the facts must be the correct one.
- We now postulate that the particles carrying this force, called gluons, must occur in color anti-color units (i.e. nine of them).
- BUT, red + blue + green is neutral, which means that the linear combination red anti-red + blue anti-blue + green anti-green must be non-interacting, since otherwise the colorless baryons would be able to emit these gluons and interact with each other via the strong force—contrary to the evidence.  So, there can only be ***EIGHT gluons***.

This is just Occam's razor again: a hypothetical particle that can't interact with anything, and therefore can't be detected, doesn't exist. The simplest theory describing the above is the SU(3) one with the gluons as the basis states of the Lie algebra.  That is, gluons transform in the adjoint representation of SU(3), which is 8-dimensional. _([Physics FAQ](https://math.ucr.edu/home/baez/physics/ParticleAndNuclear/gluons.html))_
```

![0_kGdCmWqcFG_s8fIq](https://github.com/eq19/maps/assets/8466209/dbb91090-dcb6-4ad9-bcb6-427054eab4dc)

Please note that we are not talking about the number of 19 which is the 8th prime. Here we are talking about ***19th*** as sequence follow backward position of 19 as per the scheme below where the 19th prime which is 67 goes 15 from 66 to 51. 

```note
- In [quantum field theory](https://en.wikipedia.org/wiki/Quantum_field_theory), the theta vacuum is the semi-classical [vacuum state](https://en.wikipedia.org/wiki/Quantum_vacuum_state) of non-[abelian](https://en.wikipedia.org/wiki/Abelian_group) [Yang–Mills theories](https://en.wikipedia.org/wiki/Yang%E2%80%93Mills_theory) specified by the vacuum angle θ that arises when the state is written as a [superposition](https://en.wikipedia.org/wiki/Quantum_superposition) of an infinite set of [topologically](https://en.wikipedia.org/wiki/Topology) distinct vacuum states.
- The dynamical effects of the vacuum are captured in the [Lagrangian formalism](https://en.wikipedia.org/wiki/Lagrangian_mechanics) through the presence of a θ-term which in [quantum chromodynamics](https://en.wikipedia.org/wiki/Quantum_chromodynamics) leads to the [fine tuning](https://en.wikipedia.org/wiki/Fine-tuning_(physics)) problem known as the [strong CP problem](https://en.wikipedia.org/wiki/Strong_CP_problem).
- It was discovered in 1976 by [Curtis Callan](https://en.wikipedia.org/wiki/Curtis_Callan), [Roger Dashen](https://en.wikipedia.org/wiki/Roger_Dashen), and [David Gross](https://en.wikipedia.org/wiki/David_Gross),[[1]](https://en.wikipedia.org/wiki/Theta_vacuum#cite_note-1) and independently by [Roman Jackiw](https://en.wikipedia.org/wiki/Roman_Jackiw) and Claudio Rebbi  _([Wikipedia](https://en.wikipedia.org/wiki/Theta_vacuum))_.
```

***π(1000) = π(Φ x 618) = 168 = 100 + 68 = (50x2) + (66+2) = 102 + 66***

![960x0](https://github.com/eq19/maps/assets/8466209/a21fb47a-c4a7-43d4-a65f-88bfd353d7da)

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

     |    168    |    618    |
-----+-----+-----+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"             19¨
-----+-----+-----+-----+-👇--+                                             ---
 17¨ |  5¨ |  3¨ |  ❓ |  7¨ | 4¤ ✔️ --->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  .. |  .. |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-----+-----+-----+                                                    |
 11¨ |  .. |  .. |  .. | 3¤ ---->  Np(33)  assigned to "id:33"  ----->  👉 77¨
-----+-----+-----+-----+-----+                                              |
 19¨ |  .. |  .. |  .. |  .. | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  .. |  .. |  .. | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
 43¨ |  .. |  .. |  .. |  .. |  .. |  .. |  .. |  .. |  .. | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ       
```

In number theory, the [partition functionp(n)](https://gist.github.com/eq19/e9832026b5b78f694e4ad22c3eb6c3ef#partition-function) represents the number of possible partitions of a non-negative integer n. Integers can be considered either in themselves or as solutions to equations ([Diophantine geometry](https://en.wikipedia.org/wiki/Diophantine_geometry)).

```note
[Young diagrams](https://commons.wikimedia.org/wiki/Category:Young_diagrams) associated to the partitions of the positive integers 1 through 8. They are arranged so that images under the reflection about the main diagonal of the square are conjugate partitions _([Wikipedia](https://en.wikipedia.org/wiki/Partition_(number_theory)))_.
```

![Hadron_colors svg](https://github.com/eq19/maps/assets/8466209/1b1e5d20-049e-48b6-9161-d8dce3d19deb)

```note
In mathematics, orthonormality typically implies a norm which has a value of unity (1). Gell-Mann matrices, however, ***are normalized to a value of 2***.
- Thus, the [trace](https://en.wikipedia.org/wiki/Trace_(linear_algebra)) of the pairwise product results in the ortho-normalization condition where delta is the [Kronecker delta](https://en.wikipedia.org/wiki/Kronecker_delta).
- This is so the embedded Pauli matrices corresponding to the three embedded subalgebras of SU(2) are conventionally normalized.
- In this three-dimensional matrix representation, the [Cartan subalgebra](https://en.wikipedia.org/wiki/Cartan_subalgebra) is the set of linear combinations (with real coefficients) of the two matrices which commute with each other.

The SU(2) Casimirs of these subalgebras ***mutually commute***. However, any unitary similarity transformation of these subalgebras will yield SU(2) subalgebras. There is an uncountable number of such transformations. _([Wikipedia](https://en.wikipedia.org/wiki/Gell-Mann_matrices))_
```

```txt
$True Prime Pairs:
(5,7), (11,13), (17,19)

     |    168    |    618    |
-----+-----+-----+-----+-----+                                             ---
 19¨ |  3¨ |  4¨ |  6¨ |  6¨ | 4¤  ----->  assigned to "id:30"             19¨
-----+-----+-----+-👇--+-----+                                             ---
 17¨ | {5¨}| {3¨}|  2¨ |  7¨ | 4¤ ✔️ --->  assigned to "id:31"              |
     +-----+-----+-----+-----+                                              |
{12¨}|  .. |  .. |  2¤ (M & F)     ----->  assigned to "id:32"              |
     +-----+-----+-----+                                                    |
 11¨ |  .. |  .. |  .. | 3¤ ---->  Np(33)  assigned to "id:33"  ----->  👉 77¨
-----+-----+-----+-----+-----+                                              |
 19¨ |  .. |  .. |  .. |  .. | 4¤  ----->  assigned to "id:34"              |
     +-----+-----+-----+-----+                                              |
{18¨}|  .. |  .. |  .. | 3¤        ----->  assigned to "id:35"              |
     +-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
 43¨ |  .. |  .. |  .. |  .. |  .. |  .. |  .. |  .. |  .. | 9¤ (C1 & C2)  43¨
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+               ---
139¨ |  1     2     3  |  4     5     6  |  7     8     9  |
                    Δ                 Δ                 Δ       
```

So basically  there is a basic transformation between ***[addition](https://eq19.github.io/addition/)*** of `3 + 4 = 7` in to their ***[multiplication](https://eq19.github.io/multiplication/)*** of `3 x 4 = 12` while the 7 vs 12 will be treated as ***exponentiation***.

```note
Because the value 30 is the first (common) product of the first 3 primes. And this 30th order repeats itself to infinity. Even in the first 30s system, therefore, the positions are fixed in which the number information positions itself to infinity. We call it the first member of the MEC 30.
- The numbers not divisible by 2, 3 or 5 are highlighted. We call them prime positions, hence 1, 7, 11, 13, 17, 19, 23, 29. Important for our work is that in the following the term prime refers only to prime numbers that are in the prime positions. So primes 2, 3 and 5 are always excluded.
- These positions: 1 7 11 13 17 19 23 29. We refer to this basic system as MEC 30 - "Mathematical Elementary Cell 30". By repeating the positions we show the function of the basic system in the next step. If we extend the 30th order of the MEC, for example, to the number 120, the result is ***4 times a 30th order*** and thus 4 × 8 = 32 prime positions.
- Hypothetical assumption: If the product of the primes (except 2, 3, 5,) would not fall into the prime positions, thus be divided by 2, 3 or 5, the information would have 120 = 32 primes in 32 prime positions: 1, 7, 11, 13, 17, 19, 23, 29, / 31, 37, 41, 43, 47, 49, 53, 59, / 61, 67, 71, 73, 77, 79, 83, 89, / 91, 97, 101, 103, 107, 109, 113, 119
- These forms gives prime positions:  1, 7, 11, 13, 17, 19, 23, 29, / 1, 7, 11, 13, 17, 19, 23, 29, / 1, 7, 11, 13, 17 , 19, 23, 29, / 1, 7, 11, 13, 17, 19, 23, 29. The 30th order is repeated in the number space ***120 = 4 times, 4 × 8 = 32 prime positions, thus 4 terms***.

From our consideration we can conclude that the distribution of prime numbers must have a static base structure, which is also confirmed logically in the further course. This static structure is altered by the products of the primes themselves, since these products must fall into the prime positions since they are not divisible by 2, 3 and 5. _([Google Patent DE102011101032A9](https://patents.google.com/patent/DE102011101032A9/en#similarDocuments))_
```

***p(33) = p(40-7) = loop (100000) = 4 + 25 + 139 + 1091 + 8884 = 10143***

[![identities zones](https://user-images.githubusercontent.com/8466209/241491860-72da956a-1740-4ed7-83ef-3844ae1ff8d2.png)](https://eq19.github.io/#identition-zones)

So by simple words this 11 dimensions brings us back to the _[root functions](https://eq19.github.io/exponentiation/#root-functions)_. The only difference is _the base unit_. It is now carrying the above `p(33) = 10143`.

[![8 (1st-gap)](https://github.com/eq19/maps/assets/8466209/5c478950-c4e2-4a83-b5c9-ec1e36cd6fa1)](https://eq19.github.io/#identition-zones)

***1st Fermion Fields = 96 / 12 Moon Orbit = 8 (1st-gap)***

The product of each pair of terms can be given by multiplication of the coefficients and a [multiplication table](https://en.wikipedia.org/wiki/Multiplication_table) of the unit octonions, like this one:

```tip
This _[octonion](https://en.wikipedia.org/wiki/Octonion)_ with seven points and seven lines (the circle through 1, 2, and 3 is considered a line) is called the _[Fano plane](https://en.wikipedia.org/wiki/Fano_plane)_.

- The product of each pair of terms can be given by multiplication of the coefficients and a multiplication table of the unit octonions, like this one (given both by Arthur Cayley in 1845 and John T. Graves in 1843.[![](https://github.com/user-attachments/assets/8904931c-40c8-4991-953b-f6922ae0405f)](https://en.wikipedia.org/wiki/Octonion)
- Most off-diagonal elements of the table are antisymmetric, making it almost a skew-symmetric matrix except for the elements on the main diagonal, as well as the row and column for which e0 is an operand.[![Commutation relations of g2 and the incidence geometry of the Fano plane](https://github.com/user-attachments/assets/f6a69b96-d817-495c-80a2-242cca890bb4)](https://arxiv.org/abs/2207.13946v1)
- The above definition is not unique, however; it is only one of 480 possible definitions for octonion multiplication with e0 = 1. The others can be obtained by permuting and changing the signs of the non-scalar basis elements {e1, e2, e3, e4, e5, e6, e7}.
- The `16 x 30 = 480` different algebras are isomorphic, and there is rarely a need to consider which particular multiplication rule is used.
- Each of these 480 definitions is invariant up to signs under some 7 cycle of the points (1 2 3 4 5 6 7), and for each 7 cycle there are four definitions, differing by signs and reversal of order.

A common choice is to use the definition invariant under the 7 cycle (1 2 3 4 5 6 7) with e1e2 = e4 by using the triangular multiplication diagram, or Fano plane below that also shows the sorted list of 1 2 4 based 7-cycle triads and its associated multiplication matrices in both en and IJKL format. _([Wikipedia](https://en.wikipedia.org/wiki/Octonion))_
```

[![complex octonion](https://github.com/user-attachments/assets/c91dc9a3-4a8a-4a9f-84fe-2955b13aeca9)](https://eq19.github.io/exponentiation/#complex-octonions)

## Lexering Structure

If we implemented with _[trading schema](https://schema.freqtrade.io/schema.json)_, the group's action on the diagram's ***seven partitions of the subcubes yields only 168 distinct results***.

```
├── DIVISION 1: TRADING STRATEGY CORE
│   ├── Entry/Exit Strategy
│   │   ├── timeframe
│   │   ├── minimal_roi
│   │   ├── use_exit_signal
│   │   ├── exit_profit_only
│   │   ├── exit_profit_offset
│   │   ├── ignore_roi_if_entry_signal
│   │   ├── ignore_buying_expired_candle_after
│   │   ├── process_only_new_candles
│   │   └── force_entry_enable
│   │
│   └── Position Management
│       ├── position_adjustment_enable
│       ├── max_entry_position_adjustment
│       ├── amend_last_stake_amount
│       └── last_stake_amount_min_ratio
│
├── DIVISION 2: CAPITAL & RISK
│   ├── Capital Allocation
│   │   ├── stake_currency
│   │   ├── stake_amount
│   │   ├── tradable_balance_ratio
│   │   ├── available_capital
│   │   ├── dry_run_wallet
│   │   ├── amount_reserve_percent
│   │   ├── minimum_trade_amount
│   │   └── targeted_trade_amount
│   │
│   └── Risk Boundaries
│       ├── stoploss
│       ├── trailing_stop
│       ├── trailing_stop_positive
│       ├── trailing_stop_positive_offset
│       ├── trailing_only_offset_is_reached
│       ├── fee
│       ├── liquidation_buffer
│       └── custom_price_max_distance_ratio
│
├── DIVISION 3: EXCHANGE OPERATIONS
│   ├── Exchange Authentication
│   │   └── exchange (contains: name, key, secret, password, uid, account_id, wallet_address, private_key, ccxt_config, ccxt_async_config, ccxt_sync_config)
│   │
│   ├── Market Connection
│   │   ├── trading_mode
│   │   ├── margin_mode
│   │   ├── proxy_coin
│   │   ├── coingecko
│   │   ├── exchange.pair_whitelist
│   │   ├── exchange.pair_blacklist
│   │   ├── exchange.log_responses
│   │   ├── exchange.enable_ws
│   │   ├── exchange.unknown_fee_rate
│   │   ├── exchange.outdated_offset
│   │   └── exchange.markets_refresh_interval
│   │
│   └── Order Routing
│       ├── order_types
│       ├── order_time_in_force
│       ├── unfilledtimeout
│       └── cancel_open_orders_on_exit
│
├── DIVISION 4: MARKET DATA
│   ├── Storage Layer
│   │   ├── user_data_dir
│   │   ├── dataformat_ohlcv
│   │   ├── dataformat_trades
│   │   ├── db_url
│   │   ├── export
│   │   └── disableparamexport
│   │
│   ├── Data Pipeline
│   │   ├── datadir
│   │   ├── startup_candle
│   │   ├── pairlists ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ 👈 Center
│   │   ├── new_pairs_days
│   │   └── download_trades
│   │
│   └── Price Discovery
│       ├── entry_pricing
│       └── exit_pricing
│
├── DIVISION 5: INTELLIGENCE & ANALYTICS
│   ├── Intelligence Suite
│   │   ├── freqai
│   │   └── orderflow
│   │
│   └── Analytics Dashboard
│       ├── reduce_df_footprint
│       ├── lookahead_analysis_exportfilename
│       ├── recursive_strategy_search
│       ├── disable_dataframe_checks
│       ├── analyze_per_epoch
│       └── print_all
│
├── DIVISION 6: DEVELOPMENT & OPTIMIZATION
│   └── Development Suite
│       ├── backtest_breakdown
│       ├── backtest_cache
│       ├── hyperopt_path
│       ├── epochs
│       ├── early_stop
│       ├── spaces
│       ├── hyperopt_loss
│       ├── hyperopt_jobs
│       ├── hyperopt_random_state
│       └── hyperopt_min_trades
│
└── DIVISION 7: SYSTEM INTEGRATION
    ├── External Communications
    │   ├── telegram
    │   ├── webhook
    │   ├── discord
    │   ├── api_server
    │   └── bot_name
    │
    └── System Operations
        ├── dry_run
        ├── initial_state
        ├── internals
        ├── log_config
        ├── external_message_consumer
        ├── experimental
        ├── add_config_files
        ├── fiat_display_currency
        └── max_open_trades
```

The product of each pair of terms can be given by multiplication of the coefficients and a [multiplication table](https://en.wikipedia.org/wiki/Multiplication_table) of the unit octonions.

[![Freqtrade Database](https://github.com/user-attachments/assets/aeeda3c9-c22a-41e9-af41-66e6255df1fc)](https://databasesample.com/database/freqtrade-database)

[<img width="1183" height="574" alt="17806090949934473714611364250223" src="https://github.com/user-attachments/assets/e4078dad-3925-411c-b2ce-dbf713935bb7" />](https://github.com/ariga/atlas)

[![](https://github.com/user-attachments/assets/4570dde6-9052-464f-959b-696784da3a07)](https://GitHub.com/eq19/parser)

[![teaching-machines-glouppe_compressed.pdf](https://user-images.githubusercontent.com/8466209/222966425-9da703ef-9189-44e6-8fc1-8b766cf9f7bb.png)](https://eq19.github.io/identition/)

