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

Like electromagnetism ([QED](https://www.eq19.com/maps/exponentiation/span17/)), it is a gauge theory, where the force between charged particles originates in the exchange of intermediate massless vector bosons: _one photon in the case of QED and eight gluons in the case of QCD_.

```note
QCD is extremely predictive:
- One gauge coupling constant, six quark masses and the so-called theta vacuum angle are the only free parameters from which a plethora of phenomena can in principle be predicted, such as the spectrum of hadrons and their interactions.
- The famous theta vacuum angle is the only source of CP violation (asymmetry between matter and antimatter) of the strong interactions, but has been constrained from the measurement of the neutron electric dipole moment to be unnaturally small.

The fact that this parameter is so small is the so-called strong CP problem.
```

![quark-quark_scattering](https://github.com/eq19/maps/assets/8466209/06a2f256-191f-438b-aa24-0c8d75bb254e)

The gauge symmetry of QCD is based on the special unitary group, SU(3), and the associated charge is called color. Quarks carry three basic charges or colors: red, blue and green.

```note
In spite of the simplicity of the QCD Lagrangian, quantitative predictions are highly non trivial.
- Indeed the colored quarks or gluons have not been observed in isolation.
- This fact is referred to as confinement, an essential property of QCD which implies that only states that carry no color charge can propagate freely.

The neutral composites that we observe in nature are the hadrons: mesons composed of a quark and an antiquark, or baryons composed of three quarks.
```

![SmallBookPile](https://github.com/eq19/maps/assets/8466209/0971f647-c8f7-4fc7-8ec6-0a11e1767773)

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

## Matrix Scheme

Quarks have three colors. Color is to the strong interaction as electric charge is to the electromagnetic interaction.

![quantum-chromodynamics-1-320](https://github.com/eq19/maps/assets/8466209/47786899-e7a8-4388-9d20-f0f7805e1ea9)

```liquid
red   anti-red,   red   anti-blue,   red   anti-green,
blue  anti-red,   blue  anti-blue,   blue  anti-green,
green anti-red,   green anti-blue,   green anti-green.
```

This exponentiation takes important roles since by the _[multiplication zones](https://www.eq19.com/multiplication/#parsering-structure)_ the MEC30 forms a matrix of  `8 x 8 = 64 = 8²` where the power of 2 stands as exponent

```note
During the last few years of the 12th century, ***Fibonacci*** undertook a series of travels around the Mediterranean. At this time, the world’s most prominent mathematicians were Arabs, and he spent much time studying with them. His work, whose title translates as the Book of Calculation, was extremely influential in that ***it popularized the use of the Arabic numerals in Europe***, thereby revolutionizing arithmetic and allowing scientific experiment and discovery to progress more quickly. _([Famous Mathematicians](https://famous-mathematicians.org/leonardo-pisano-bigollo/))_
```

[![MEC30 Square](https://user-images.githubusercontent.com/36441664/262213707-63aa0a64-cf7d-4fb7-9f1a-f3d1ba805643.png)](https://www.eq19.com/multiplication/#parsering-structure)

Since the first member is 30 then the form is initiated by a matrix of `5 x 6 = 30` which has to be transformed first to `6 x 6 = 36 = 6²` prior to the above MEC30's square. 

```note
A square system of coupled nonlinear equations can be solved iteratively by Newton's method. This method uses the Jacobian matrix of the system of equations. _([Wikipedia](https://en.wikipedia.org/Jacobian_matrix_and_determinant))_
```

[![gradien](https://user-images.githubusercontent.com/36441664/128025898-187ba576-795f-4578-af71-ff02a8b682b1.png)](https://www.eq19.com/multiplication/#transformation-to-exponentiation)

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

## Interactions

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

So basically  there is a basic transformation between ***[addition](https://www.eq19.com/addition/)*** of `3 + 4 = 7` in to their ***[multiplication](https://www.eq19.com/multiplication/)*** of `3 x 4 = 12` while the 7 vs 12 will be treated as ***exponentiation***.
