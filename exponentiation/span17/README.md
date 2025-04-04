---
sort: 22
spin: 31
span: 
suit: 113
description: 
---
# Electrodynamics (maps)

The term of electrodynamics is referring to Quantum Electrodynamics ([QED](https://en.wikipedia.org/wiki/Quantum_electrodynamics)) which is the [relativistic](https://en.wikipedia.org/wiki/Theory_of_relativity) [quantum field theory](https://en.wikipedia.org/wiki/Quantum_field_theory) of [Electromagnetism](https://en.wikipedia.org/wiki/Electrodynamics).

{% include list.liquid all=true %}

In essence, it describes how [light](https://en.wikipedia.org/wiki/Light) and [matter](https://en.wikipedia.org/wiki/Matter) interact and is **the first theory** where full agreement between [quantum mechanics](https://en.wikipedia.org/wiki/Quantum_mechanics) and [special relativity](https://en.wikipedia.org/wiki/Special_relativity) is achieved.

## Basic Transformation

The first formulation of a [quantum theory](https://en.wikipedia.org/wiki/Quantum_mechanics) describing radiation and matter interaction is attributed to British scientist [Paul Dirac](https://en.wikipedia.org/wiki/Paul_Dirac).

```note
Dirac described the quantization of the [electromagnetic field](https://en.wikipedia.org/wiki/Electromagnetic_field) as an ensemble of [harmonic oscillators](https://en.wikipedia.org/wiki/Harmonic_oscillator) with the introduction of the concept of [creation and annihilation operators](https://en.wikipedia.org/wiki/Creation_and_annihilation_operators) of particles. 

Based on Bethe's intuition and fundamental papers on the subject by [Shin'ichirō Tomonaga](https://en.wikipedia.org/wiki/Shin%27ichir%C5%8D_Tomonaga),[[16]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-tomonaga-16) [Julian Schwinger](https://en.wikipedia.org/wiki/Julian_Schwinger),[[17]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-schwinger1-17)[[18]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-schwinger2-18) [Richard Feynman](https://en.wikipedia.org/wiki/Richard_Feynman)[[1]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-feynman1-1)[[19]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-feynman2-19)[[20]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-feynman3-20) and [Freeman Dyson](https://en.wikipedia.org/wiki/Freeman_Dyson),[[21]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-dyson1-21)[[22]](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-dyson2-22) it was finally possible to get fully [covariant](https://en.wikipedia.org/wiki/Lorentz_covariance) formulations that were finite at any order in a perturbation series of quantum electrodynamics.

The key components of Feynman's presentation of QED are [three basic actions](https://en.wikipedia.org/wiki/Quantum_electrodynamics#cite_note-feynbook-2)

- A [photon](https://en.wikipedia.org/wiki/Photon) goes from one place and time to another place and time.
- An [electron](https://en.wikipedia.org/wiki/Electron) goes from one place and time to another place and time.
- An electron emits or absorbs a photon at a certain place and time.

These actions are represented in the form of visual shorthand by the three basic elements of [diagrams](https://en.wikipedia.org/wiki/Feynman_diagram): a wavy line for the photon, a straight line for the electron and a junction of two straight lines and a wavy one for a vertex representing emission or absorption of a photon by an electron. _([Wikipedia](https://en.wikipedia.org/wiki/Quantum_electrodynamics))_
```

[![1_RMV1kvtEZ-o-_8WKQLnCSA](https://github.com/eq19/maps/assets/8466209/715b20a8-d5c2-4b72-8993-b696a8b25d23)](https://platosrealm.wordpress.com/2019/02/26/unsolved-problems-in-physics-baryon-asymmetry/)

QED is based on the above three building blocks and then using the probability amplitudes to calculate the probability of any such complex interaction.

```note
It turns out that the basic idea of QED can be communicated while assuming that the square of the total of the probability amplitudes mentioned above (P(A to B), E(C to D) and j) acts just like our everyday probability (a simplification made in [Feynman's book](https://github.com/eq19/maps/files/13930690/PhysRev.76.769.pdf)). Later on, this will be corrected to include specifically quantum-style mathematics, following Feynman.

The basic rules of probability amplitudes that will be used are:
- If an event can occur via a number of indistinguishable alternative processes (a.k.a. "virtual" processes), then its probability amplitude is the ***sum of the probability amplitudes of the alternatives***.
- If a virtual process involves a number of independent or concomitant sub-processes, then the probability amplitude of the total (compound) process is the ***product of the probability amplitudes of the sub-processes***.

The indistinguishability criterion in (a) is very important: it means that there is no observable feature present in the given system that in any way "reveals" which alternative is taken. In such a case, one cannot observe which alternative actually takes place without changing the experimental setup in some way (e.g. by introducing a new apparatus into the system). _([Wikipedia](https://en.wikipedia.org/wiki/Quantum_electrodynamics))_
```

[![First_Feynman_Diagram](https://github.com/eq19/maps/assets/8466209/c381a212-cf38-45db-a166-f8e8716886da)](https://github.com/eq19/maps/files/13930690/PhysRev.76.769.pdf)

They are related to our everyday ideas of probability by the simple rule that the probability of an event is the square of the length of the corresponding amplitude arrow.

```note
Feynman replaces complex numbers with spinning arrows, which start at emission and end at detection of a particle.

[![Feynmans_QED_probability_amplitudes](https://github.com/user-attachments/assets/df7b0132-ccc2-4372-8f4e-ca2211b7956c)](https://en.wikipedia.org/wiki/Quantum_electrodynamics#probability-amplitudes)

- The sum of all resulting arrows gives a final arrow whose length squared equals the probability of the event.
- In this diagram, light emitted by the source S can reach the detector at P by bouncing off the mirror (in blue) at various points.
- Each one of the paths has an arrow associated with it (whose direction changes uniformly with the time taken for the light to traverse the path).
- To correctly calculate the total probability for light to reach P starting at S, one needs to sum the arrows for all such paths.

The graph below depicts the total time spent to traverse each of the paths above.
```

![008869256_1-75ca18aad2faf65f52f4c7706d7d8bd3-768x994](https://github.com/eq19/maps/assets/8466209/7c7f069f-dcfb-439e-961e-68c63c76dc9d)

Feynman avoids exposing the reader to the mathematics of complex numbers by using a simple but accurate representation of them as arrows on a piece of paper or screen.

```note
Mathematically, QED is an [abelian](https://en.wikipedia.org/wiki/Abelian_group) [gauge theory](https://en.wikipedia.org/wiki/Gauge_theory) with the symmetry group [U(1)](https://en.wikipedia.org/wiki/U(1)), defined on [Minkowski space](https://en.wikipedia.org/wiki/Minkowski_space) (flat spacetime). The [gauge field](https://en.wikipedia.org/wiki/Gauge_field), which mediates the interaction between the charged [spin-1/2](https://en.wikipedia.org/wiki/Spin_(physics)) [fields](https://en.wikipedia.org/wiki/Field_(physics)), is the [electromagnetic field](https://en.wikipedia.org/wiki/Electromagnetic_field). The QED [Lagrangian](https://en.wikipedia.org/wiki/Lagrangian_(field_theory)) for a spin-1/2 field interacting with the electromagnetic field in natural units gives rise to the QED Action
```

[![image-18](https://github.com/eq19/maps/assets/8466209/f233cea8-77c7-4456-bc5c-65b0e98b3f73)](https://slidetodoc.com/particle-physics-michaelmas-term-2011-prof-mark-thomson-6/)

Finally, one has to compute P(A to B) and E(C to D) corresponding to the probability amplitudes for the photon and the electron respectively.

## Subsequent Theories

QED has served as the model and template for all subsequent quantum field theories. One such subsequent theory is Quantum Chromodynamics ([QCD](https://www.eq19.com/lexer/exponentiation/span15/)).

```note
Quantum Chromo Dynamics (in short QCD) is the field that studies the strong force between quarks . Like QED (Quantum Electro Dynamics) studies the electromagnetic force on the basis of quantum field theory, QCD does so as well. So we will find many similarities in applying fields, waves, interactions and how the force comes about. However, many of the processes in QCD cannot be calculated exactly. So it is not as advanced as QED.
```

![images (10)](https://github.com/eq19/maps/assets/8466209/05f120ec-515e-4457-9625-bf4a6d7ee28f)

The three kinds of [charge](https://en.m.wikipedia.org/wiki/Charge_(physics)) in QCD (as opposed to one in [quantum electrodynamics](https://en.m.wikipedia.org/wiki/Quantum_electrodynamics) or QED) are usually referred to as "[color charge](https://en.m.wikipedia.org/wiki/Color_charge)" by loose analogy to the three kinds of [color](https://en.m.wikipedia.org/wiki/Color) (red, green and blue) [perceived by humans](https://en.m.wikipedia.org/wiki/Color_vision). 

![QCD](https://github.com/eq19/maps/assets/8466209/fb3bf635-808c-4105-b8d6-2821486ed219)

Other than this nomenclature, the quantum parameter "color" is completely unrelated to the everyday, familiar phenomenon of color.

```note
In the 1980s, scientists discovered that a proton's three valance quarks (red, green, blue) account for only a fraction of the proton's overall spin. More recent measurements have revealed that gluons (yellow corkscrews) contribute as much as or possibly more than the quarks. _([Brookhaven National Laboratory](https://phys.org/news/2017-03-proton.html))_
```

[![proton-1](https://github.com/eq19/maps/assets/8466209/b110ca02-ac35-400a-8c83-dfb23e1c1c4b)](https://bigthink.com/starts-with-a-bang/why-8-types-gluon/)

Since the theory of electric charge is dubbed "[electrodynamics](https://en.m.wikipedia.org/wiki/Electrodynamics)", the [Greek](https://en.m.wikipedia.org/wiki/Ancient_Greek) word χρῶμα (chrōma, "color") is applied to the theory of color charge, "chromodynamics".

```note
By 1947, physicists believed that they had a good understanding of what the smallest bits of matter were. There were [electrons](https://en.m.wikipedia.org/wiki/Electron), [protons](https://en.m.wikipedia.org/wiki/Proton), [neutrons](https://en.m.wikipedia.org/wiki/Neutron), and [photons](https://en.m.wikipedia.org/wiki/Photon) (the components that make up the vast part of everyday experience such as atoms and light) along with a handful of unstable (i.e., they undergo [radioactive decay](https://en.m.wikipedia.org/wiki/Radioactive_decay)) exotic particles needed to explain [cosmic rays](https://en.m.wikipedia.org/wiki/Cosmic_ray) observations such as [pions](https://en.m.wikipedia.org/wiki/Pion), [muons](https://en.m.wikipedia.org/wiki/Muon) and hypothesized [neutrino](https://en.m.wikipedia.org/wiki/Neutrino).
- In addition, the discovery of the [positron](https://en.m.wikipedia.org/wiki/Positron) suggested there could be [anti-particles](https://en.m.wikipedia.org/wiki/Anti-particle) for each of them.
- It was known a "[strong interaction](https://en.m.wikipedia.org/wiki/Strong_interaction)" must exist to overcome [electrostatic repulsion](https://en.m.wikipedia.org/wiki/Coulomb%27s_law) in atomic nuclei.
- Not all particles are influenced by this strong force but those that are, are dubbed "hadrons", which are now further classified as [mesons](https://en.m.wikipedia.org/wiki/Meson) (middle mass) and [baryons](https://en.m.wikipedia.org/wiki/Baryon) (heavy weight).
- But the discovery of the neutral [kaon](https://en.m.wikipedia.org/wiki/Kaon) in late 1947 and the subsequent discovery of a positively charged kaon in 1949 extended the meson family in an unexpected way and in 1950 the [lambda particle](https://en.m.wikipedia.org/wiki/Lambda_particle) did the same thing for the baryon family.
- These particles decay much more slowly than they are produced, a hint that there are two different physical processes involved. This was first suggested by [Abraham Pais](https://en.m.wikipedia.org/wiki/Abraham_Pais) in 1952.
- In 1953, [Murray Gell-Mann](https://en.m.wikipedia.org/wiki/Murray_Gell-Mann) and a collaboration in Japan, Tadao Nakano with [Kazuhiko Nishijima](https://en.m.wikipedia.org/wiki/Kazuhiko_Nishijima), independently suggested a new conserved value now known as "[strangeness](https://en.m.wikipedia.org/wiki/Strangeness)" during their attempts to understand the growing collection of known particles.[[4]](https://en.m.wikipedia.org/wiki/Eightfold_way_(physics)#cite_note-Gell-Mann-1953-11-5)[[5]](https://en.m.wikipedia.org/wiki/Eightfold_way_(physics)#cite_note-Nakano-Nishijima-1953-11-6)[[b]](https://en.m.wikipedia.org/wiki/Eightfold_way_(physics)#cite_note-7)
- The trend of discovering new mesons and baryons would continue through the 1950s as the number of known "elementary" particles ballooned. Physicists were interested in understanding hadron-hadron interactions via the strong interaction.
- The concept of [isospin](https://en.m.wikipedia.org/wiki/Isospin), introduced in 1932 by [Werner Heisenberg](https://en.m.wikipedia.org/wiki/Werner_Heisenberg) shortly after the discovery of the neutron, was used to group some hadrons together into "multiplets" but no successful scientific theory as yet covered the hadrons as a whole.

This was the beginning of a chaotic period in particle physics that has become known as the "[particle zoo](https://en.m.wikipedia.org/wiki/Particle_zoo)" era. The eightfold way represented a step out of this confusion and towards the [quark model](https://en.m.wikipedia.org/wiki/Quark_model), which proved to be the solution _([Wikipedia](https://en.m.wikipedia.org/wiki/Eightfold_way_(physics)))_.
```

![qcd-620px](https://github.com/eq19/maps/assets/8466209/3d4c5903-0d79-4c11-8c89-1a62fedb8e29)

The hadrons were sorted into groups having similar properties and masses using the **[eightfold way](https://en.m.wikipedia.org/wiki/Eightfold_way_(physics))**, invented in 1961 by Gell-Mann[[11]](https://en.m.wikipedia.org/wiki/Quantum_chromodynamics#cite_note-11).

```note
The [pseudoscalar meson](https://en.m.wikipedia.org/wiki/Pseudoscalar_meson) octet. Particles along the same horizontal line share the same [strangeness](https://en.m.wikipedia.org/wiki/Strangeness_(particle_physics)), s, while those on the same left-leaning diagonals share the same [charge](https://en.m.wikipedia.org/wiki/Electric_charge), q (given as multiples of the [elementary charge](https://en.m.wikipedia.org/wiki/Elementary_charge)).
```

[![qcd_together](https://github.com/eq19/maps/assets/8466209/86fe9814-2aa3-42ba-9549-6569858c4690)](https://github.com/user-attachments/files/17381139/eightfold.pdf)

All the theories describing fundamental interactions, except gravitation, whose quantum counterpart is only conjectural and presently under very active research, are renormalizable theories.

```note
Renormalization was first developed in quantum electrodynamics (QED) to make sense of infinite integrals in perturbation theory. Initially viewed as a suspect provisional procedure even by some of its originators, renormalization eventually was embraced as an important and self-consistent actual mechanism of scale physics in several fields of physics and mathematics. Despite his later skepticism, it was Paul Dirac who pioneered renormalization.
```

![I15-73-Feynman](https://github.com/eq19/maps/assets/8466209/1acfbce9-61d4-443e-9aba-45d09d86659f)

Via the [11 partitions](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#the-%CE%B419-vs-18-scenario) as the lexer and [13 frames](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#the-power-of-168-vs-618) as the parser we do a [recombination](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#scheme-139) to build the [grammar](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#the-prime-recycling-%CE%B6s) in 6 periods.

[![6 minor hexagons](https://github.com/eq19/maps/assets/8466209/1e7dc443-b7d8-44d9-8da0-5fe50dd7ee70)](https://www.hexspin.com/minor-hexagons/)

Renormalizability has become an essential criterion for a quantum field theory to be considered as a viable one.

```note
Renormalization is a collection of techniques in [quantum field theory](https://en.wikipedia.org/wiki/Quantum_field_theory), [statistical field theory](https://en.wikipedia.org/wiki/Statistical_field_theory), and the theory of [self-similar](https://en.wikipedia.org/wiki/Self-similarity) geometric structures, that are used to treat [infinities](https://en.wikipedia.org/wiki/Infinity) arising in calculated quantities by altering values of these quantities to compensate for effects of their self-interactions.
- But even if no infinities arose in [loop diagrams](https://en.wikipedia.org/wiki/One-loop_Feynman_diagram) in quantum field theory, it could be shown that it would be necessary to renormalize the mass and fields appearing in the original [Lagrangian](https://en.wikipedia.org/wiki/Lagrangian_(field_theory)).[[1]](https://en.wikipedia.org/wiki/Renormalization#cite_note-1)
- For example, an [electron](https://en.wikipedia.org/wiki/Electron) theory may begin by postulating an electron with an initial mass and charge. In [quantum field theory](https://en.wikipedia.org/wiki/Quantum_field_theory) a cloud of [virtual particles](https://en.wikipedia.org/wiki/Virtual_particle), such as [photons](https://en.wikipedia.org/wiki/Photon), [positrons](https://en.wikipedia.org/wiki/Positron), and others surrounds and interacts with the initial electron.
- Accounting for the interactions of the surrounding particles (e.g. collisions at different energies) shows that the electron-system behaves as if it had a different mass and charge than initially postulated.

Renormalization, in this example, mathematically replaces the initially postulated mass and charge of an electron with the experimentally observed mass and charge. _([Wikipedia](https://en.wikipedia.org/wiki/Renormalization))_
```

![axioms-12-01058-g004](https://github.com/eq19/maps/assets/8466209/b43f5e6e-8a2d-4cf2-bff8-f111c263e273)

When recombination is occur then the prime **13 is forced to → 12** where the impact (Δ1) goes to 18+The tensor product of a triplet with an octet reducing to a deciquintuplet, an anti-sextet, and a triplet appears diagrammatically as ***a total of 24 states***.

```note
The special unitary group SU is the group of unitary matrices whose determinant is equal to 1.[1] This set is closed under matrix multiplication.
- All transformations characterized by the special unitary group leave norms unchanged. The SU(3) symmetry appears in the light quark flavour symmetry (among up, down, and strange quarks) dubbed the Eightfold Way (physics).
- The same group acts in quantum chromodynamics on the colour quantum numbers of the quarks that form the fundamental (triplet) representation of the group.
- The group SU(3) is a subgroup of group U(3), the group of all 3×3 unitary matrices. The unitarity condition imposes nine constraint relations on the total 18 degrees of freedom of a 3×3 complex matrix. 
- Thus, the dimension of the U(3) group is 9. Furthermore, multiplying a U by a phase, eiφ leaves the norm invariant. Thus U(3) can be decomposed into a direct product U(1) × SU(3)/Z3. 

***Because of this additional constraint, SU(3) has dimension 8***. _([Wikipedia](https://en.m.wikipedia.org/wiki/Clebsch%E2%80%93Gordan_coefficients_for_SU(3)))_
```

[![Young_tableaux_17](https://github.com/eq19/maps/assets/8466209/6647c9e1-026f-4aaa-b3a0-102a274bbc46)
![Young_tableaux_18](https://github.com/eq19/maps/assets/8466209/9adba5c0-a334-4d06-8bc1-b52662bd7d12)](https://en.m.wikipedia.org/wiki/Clebsch%E2%80%93Gordan_coefficients_for_SU(3))

So then a logical explanation is needed. How can quantum electrodynamics (QED) be so successful when it is clearly not a complete theory?

```note
Quantum Electrodynamics (QED) is a fundamental theory of nature and also the most accurate one. Since 1947 it has been tested to ever increasing precision. The highest precision measurement now matches the theoretical prediction to 12 significant digits.
- The QED theory can best be understood as a theory of the simplest natural system interacting via electromagnetic interaction - one electron interacting with its own electromagnetic field. In addition to the quantum state of the electron interacting electromagnetically, the theory also provides the quantum state of the electromagnetic field.
- In QED or any other quantum field theory one deals with fields. A field is different from a particle in the sense that unlike the particle which has finite degrees of freedom, a field has infinite degrees of freedom.
- QED consists of 2 quantum fields - the quantum field of the electron and the quantum field of the photon. For a quantum field, the behavior of the field is governed by Heisenberg’s uncertainty principle instead of Newtonian dynamics.
- Any particle is a quantized excitation of its unique field. For example an electron is a quantized excitation of an electron's quantum field. Similarly a photon is a quantized excitation of the quantum electromagnetic field. All such excitations always lead to point particles - particles with zero sizes.
- The word quantized means the mass energy and spin of the particle is always quantized. Spin is an entirely quantum mechanical phenomenon, with no classical analogue. Mass energy, by Einstein’s special theory of relativity, is the relationship between the mass of a body and its corresponding energy by the famous mass-energy relationship. The mass energy of an electron is about 0.5 million electron volts, whereas the mass energy of a photon is zero since it is a massless particle.
- The QED allows one to take into account in a quantitatively concrete way the interaction between these two fields. This is the most important feature of the theory and also the most complex one to understand and calculate. The problem arises from the fact that since an electron is a point particle, from a purely Newtonian physics point of view, its self energy due to its interaction with its own electromagnetic field should become infinite. Since no physical quantity can have an infinite value, this is a major problem.
- It is successfully resolved in QED by a highly sophisticated and extremely complex mathematical procedure known as renormalization, that makes the theory free of infinity. After renormalization the QED provides extremely precise values of physically measurable quantities, for example the magnetic dipole moment of the electron.
- The basic equation of QED, known as the path integral, is far too complex to solve and to this ray no exact solution of this equation has ever been found. But that doesn’t mean that this equation has not been solved at all. It is possible to solve the complex path integral of QED by transforming it into an infinite series in such a way that the sum of all these terms gives the exact value of this integral.

Each term represents increasing number of Feynman loops. So the first term has zero loops, second term contains 1 loop and so on.  _([Quora](https://www.quora.com/Can-you-explain-how-Quantum-Electrodynamics-QED-works-and-how-we-can-trust-a-theory-that-is-based-on-complex-equations-that-have-not-been-solved/answer/Sanjay-Sood-8))_. 
```

[![1-quantum-electrodynamics-laguna-designscience-photo-library](https://github.com/eq19/maps/assets/8466209/968afaea-ff71-4a56-b9ff-423f4a9748d2)](https://en.wikipedia.org/wiki/Quantum_electrodynamics)

It is the measure of the complexity of QED that since 1948 only the first six terms have been computed. The last term has been calculated only partially and that too using the most powerful computers in the world

## Quantum Triviality Issues

If the only resulting value of the renormalized charge is zero, the theory is said to become a "trivial" theory of noninteracting free particles.

```note
This phenomenon is referred to as quantum triviality. Strong evidence supports the idea that a field theory involving only a scalar [Higgs boson](https://en.wikipedia.org/wiki/Higgs_boson) is trivial in four spacetime dimensions,[[1]](https://en.wikipedia.org/wiki/Quantum_triviality#cite_note-1)[[2]](https://en.wikipedia.org/wiki/Quantum_triviality#cite_note-TrivPurs-2) but the situation for realistic models including other particles in addition to the Higgs boson is not known in general. Nevertheless, because the Higgs boson plays a central role in the [Standard Model](https://en.wikipedia.org/wiki/Standard_Model) of [particle physics](https://en.wikipedia.org/wiki/Particle_physics), the question of triviality in Higgs models is of great importance. _([Wikipedia](https://en.wikipedia.org/wiki/Quantum_triviality))_
```

![InteractionVertexOfQED](https://github.com/eq19/maps/assets/8466209/821ddfaf-5e0e-4434-8ab0-2778d4a971d8)

From them, computations of probability amplitudes are straightforwardly given. An example is Compton scattering, with an electron and a photon undergoing elastic scattering.

![images (5)](https://github.com/eq19/maps/assets/8466209/d31951c3-ece1-4aff-88b3-b85f64e3e5e2)

Given a Model, [MARTY](https://github.com/user-attachments/files/17411621/2011.02478v2.pdf) may compute symbolically and automatically theoretical quantities. First, Feynman rules are derived.

```note
[MARTY](https://github.com/docbrown1955/marty-public) is a code generator. Analytical expressions, squared amplitudes or Wilson coefficients are converted into C++ code in a self-contained library compiled independently of MARTY. This code can therefore be used for numerical evaluation in different scenarios to perform a phenomenological analysis. _([marty-manual.pdf](https://github.com/user-attachments/files/17410077/marty-manual.pdf))_
```

[![300px-Compton_qed](https://github.com/eq19/maps/assets/8466209/36f87779-9386-46cb-b934-d3a01e375346)](https://marty.in2p3.fr/)

The coupling constant runs to infinity at finite energy, signalling a Landau pole. Quantum electrodynamics also leads to predictions beyond perturbation theory.

```note
Feynman was concerned that all field theories known in the 1960s had the property that the interactions become infinitely strong at short enough distance scales. This property called a Landau pole, made it plausible that quantum field theories were all inconsistent. In 1974, Gross, Politzer and Wilczek showed that another quantum field theory, quantum chromodynamics, does not have a Landau pole. Feynman, along with most others, accepted that QCD was a fully consistent theory.
```

![mqdefault](https://github.com/eq19/maps/assets/8466209/68994f5a-614a-4d63-9446-6acac3df2829)

In the presence of very strong electric fields, it predicts that electrons and positrons will be spontaneously produced, so causing the decay of the field.

```note
The Schrödinger-Pauli theory of electrons explicitly considers the spin moment of the electrons, and therefore goes beyond the Schrödinger theory description of spinless electrons.
- As a consequence of the electrons possessing a spin moment, the Schrödinger-Pauli theory Hamiltonian is derived non-relativistically via the Feynman kinetic energy operator. In this chapter, the Schrödinger-Pauli theory of electrons in the presence of static and time-dependent electromagnetic fields is described from the new perspective of the individual electron via the corresponding ‘Quantal Newtonian’ First and Second Laws.
- These laws are a description in terms of ‘classical’ fields experienced by each electron, the fields arising from sources that are quantum-mechanical expectation values of Hermitian operators taken with respect to the system wave function. In the temporal case–the Second Law–each electron experiences an external field comprised of the Coulomb and Lorentz fields, and an internal field whose components are representative of electron correlations due to the Pauli principle and Coulomb repulsion, kinetic effects, the electron density, and an internal magnetic field.
- The response of the electron is described by a field representative of the physical current density which is a sum of its paramagnetic, diamagnetic and magnetization components. The First Law, descriptive of the stationary-state theory, constitutes a special case. The Schrödinger-Pauli theory is generalized such that the Hamiltonian operator is proved to be an exactly known universal functional of the wave function.
- This then shows the stationary-state and time-dependent Schrödinger-Pauli equations to be intrinsically self-consistent. To facilitate the understanding of this new description and of proofs within it, further relevant aspects of the stationary-state Schrödinger theory of spinless electrons in an electromagnetic field are discussed.
- The Hamiltonian operator, as obtained by the correspondence principle, is expressed in terms of operators representative of the gauge invariant properties of the electronic density and physical current density. It is also written so as to explicitly show the existence of the Lorentz force via the corresponding operator. Thus, with any scalar potential representative of external electrostatic forces, the Hamiltonian can now be seen to explicitly encompass both the external Coulomb and Lorentz forces.

Finally, it is proved that the stationary state wave function is a functional of a gauge function. (As will be proved in a future chapter, for a uniform magnetic field, the wave function is also a functional of the gauge invariant ground state density and physical current density). The wave function is thus ensured to be gauge variant.
```

![axioms-12-01058-g002-550](https://github.com/eq19/maps/assets/8466209/66dc1ba2-cbfd-4063-9f65-b6f32ce21dfd)

The absence of any new particles beyond the Standard Model (SM) in high-energy collisions at the LHC highlights the need to probe the SM in low-energy experiments.

```note
Abstract flavio is an open source tool for phenomenological analyses in flavour physics and other precision observables in the Standard Model and beyond. It consists of a library to compute predictions for a plethora of observables in quark and lepton flavour physics and electroweak precision tests, a database of experimental measurements of these observables, a statistics package that allows to construct Bayesian and frequentist likelihoods, and of convenient plotting and visualization routines. _([flavio - pdf](https://github.com/user-attachments/files/17380517/1810.08132v1.pdf))_
```

[![hq720 (1)](https://github.com/eq19/maps/assets/8466209/9a6fd867-6867-416a-9b36-126198f4d259)](https://github.com/user-attachments/files/17380517/1810.08132v1.pdf)

From a modern perspective, we say that QED is not well defined as a quantum field theory to arbitrarily high energy.

![478517_2_En_18_Fig10_HTML](https://github.com/eq19/maps/assets/8466209/9a1b324a-db44-4044-8058-61bb61372ee4)

The entanglement implies that there remains a connection between the photon and the emitting atom after emission even in very strong fields.

```note
Despite the conceptual clarity of this Feynman approach to QED, almost no early textbooks follow him in their presentation. When performing calculations, it is much easier to work with the [Fourier transforms](https://en.wikipedia.org/wiki/Fourier_transform) of the [propagators](https://en.wikipedia.org/wiki/Propagator).
- Experimental tests of quantum electrodynamics are typically scattering experiments. In scattering theory, particles' [momenta](https://en.wikipedia.org/wiki/Momentum) rather than their positions are considered, and it is convenient to think of particles as being created or annihilated when they interact. Feynman diagrams then look the same, but the lines have different interpretations.
- The electron line represents an electron with a given energy and momentum, with a similar interpretation of the photon line. A vertex diagram represents the annihilation of one electron and the creation of another together with the absorption or creation of a photon, each having specified energies and momenta.

Using [Wick's theorem](https://en.wikipedia.org/wiki/Wick%27s_theorem) on the terms of the **Dyson series**, all the terms of the [S-matrix](https://en.wikipedia.org/wiki/S-matrix) for quantum electrodynamics can be computed through the technique of [Feynman diagrams](https://en.wikipedia.org/wiki/Feynman_diagrams). In this case, rules for drawing are the following
```

![Diagrams-in-strong-field-quantum-electrodynamics-SFQED-versus-ordinary-quantum](https://github.com/eq19/maps/assets/8466209/d7775d3a-d9e2-4993-82be-4279f209f58d)

An argument by Freeman Dyson shows that the radius of convergence of the perturbation series in QED is zero.
Here we use [observables](https://github.com/smelli/smelli/tree/master/smelli/data/yaml) of Standard Model.

```note
New physics effects are parameterised as Wilson coefficients of dimension-six operators in the weak effective theory below the electroweak scale or the Standard Model EFT above it. To display automatically generated tables with lists of all observables currently implemented in [flavio](https://github.com/user-attachments/files/17380517/1810.08132v1.pdf). See also the notes on conventions at the bottom.
- [W± decays](https://github.com/user-attachments/files/17387607/1503.07872v2.pdf)
  - [Hadronic decays](https://github.com/user-attachments/files/17387797/1706.08945v3.pdf) (1 observable)
  - [Leptonic decays](https://github.com/user-attachments/files/17387797/1706.08945v3.pdf) (12 observables)
- Z° decays
  - FCNC decays (3 observables)
  - Flavour conserving decays (51 observables)
- τ lepton decays
  - Hadronic tree-level decays (2 observables)
  - LFV decays (16 observables)
  - Leptonic tree-level decays (2 observables)
- b hadron decays
  - FCNC decays (860 observables)
  - Leptonic tree-level decays (6 observables)
  - Lifetimes (1 observable)
  - Non-leptonic decays (2 observables)
  - Semi-leptonic tree-level decays (686 observables)
- c hadron decays
  - Leptonic tree-level decays (6 observables)
  - Semi-leptonic tree-level decays (52 observables)
- e+ e− scattering
  - VV (2 observables)
- s hadron decays
  - FCNC decays (8 observables)
  - Leptonic tree-level decays (6 observables)
  - Non-leptonic decays (1 observable)
  - Semi-leptonic tree-level decays (18 observables)
- Dipole moments
  - Atomic electric dipole moments (1 observable)
  - Lepton anomalous magnetic moments (3 observables)
  - Molecular energy shifts (3 observables)
  - Nucleon electric dipole moments (1 observable)
- Higgs production and decay
  - h→VV (30 observables)
  - h→ff (24 observables)
- Meson-antimeson mixing
  - B° B° mixing (5 observables)
  - Bs Bs mixing (5 observables)
  - D° D° mixing (8 observables)
  - K° K° mixing (1 observable)
- Nucleon decays
  - Beta decays (25 observables)
- Unflavoured meson decays
  + Leptonic tree-level decays (4 observables)
- contact interactions
  - pp→μν (1 observable)
  - pp→μ+ μ− (1 observable)
  - pp→eν (1 observable)
  - pp→e+ e− (1 observable)
- muon decays
  - LFV decays (5 observables)
- neutrino physics
  - scattering cross sections (1 observable)
- quarkonium lepton decays
  - P→ℓ+ ℓ− (16 observables)
  - S→ℓ+ ℓ− (24 observables)
  - V→ℓ+ ℓ− (135 observables)
  - V→ℓ+ ℓ−γ (120 observables)

We discuss how higher-spin operators and QED corrections alter the standard angular distribution used throughout the literature, potentially leading to differences between the method of moments and the likelihood fits. _([flavio](https://flav-io.github.io/docs/observables.html))_
```

![a-Summary-of-the-Feynman-rules-Solid-line-represents-the-fermionic-propagator-G-0-pp](https://github.com/eq19/maps/assets/8466209/f3430964-392b-43f9-80fa-84eed55f474d)

The problem is essentially that QED appears to suffer from quantum triviality issues. This is one of the motivations for embedding QED within a [Grand Unified Theory](https://www.eq19.com/syntax/exponentiation/span13/).
