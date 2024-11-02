CC=g++
IPDF=-I/Users/biwu/Software/LHAPDF/include
LPDF=-L/Users/biwu/Software/LHAPDF/lib -lLHAPDF
#IGSL=-I/usr/local/include/
#LGSL=-L/usr/local/lib -lgsl -lgslcblas -lm

#IPDF=-I/home/bwu/Softwares/LHAPDF/include
#LPDF=-L/home/bwu/Softwares/LHAPDF/lib -lLHAPDF
IGSL=-I/usr/local/include/
LGSL=-L/usr/local/lib -lgsl -lgslcblas -lm


All: resum

Particle.o: Particle.c Particle.h
	$(CC) -Wall -c Particle.c

QCD.o: QCD.c QCD.h
	$(CC) -Wall $(IPDF) -c QCD.c

ElectroWeak.o: ElectroWeak.c ElectroWeak.h
	$(CC) -Wall -c ElectroWeak.c

BosonJet.o: BosonJet.c BosonJet.h
	$(CC) -Wall $(IPDF) -c BosonJet.c

#Born cross section

BosonJetBorn.o: BosonJetBorn.c BosonJetBorn.h
	$(CC) -Wall $(IPDF) -c BosonJetBorn.c

born.o: born.c
	$(CC) -Wall $(IPDF) $(IGSL) -c born.c

born: born.o BosonJetBorn.o BosonJet.o QCD.o ElectroWeak.o Particle.o
	$(CC) -Wall  born.o BosonJetBorn.o BosonJet.o ElectroWeak.o QCD.o Particle.o $(LPDF) $(LGSL) -o born

#properties of qcd

test_qcd.o: test_qcd.c
	$(CC) -Wall $(IPDF) -c test_qcd.c

test_qcd: test_qcd.o QCD.o Particle.o
	$(CC) -Wall  test_qcd.o QCD.o Particle.o $(LPDF) -o test_qcd

#Fixed order result at LO (O(alphas))

BosonJetLO.o: BosonJetLO.c BosonJetLO.h
	$(CC) -Wall $(IPDF) -c BosonJetLO.c

main.o: main.c
	$(CC) -Wall $(IPDF) $(IGSL) -c main.c

LO: main.o BosonJetLO.o BosonJet.o QCD.o ElectroWeak.o Particle.o
	$(CC) -Wall  main.o BosonJetLO.o BosonJet.o ElectroWeak.o QCD.o Particle.o $(LPDF) $(LGSL) -o LO

#Resummed result

BosonJetResum.o: BosonJetResum.c BosonJetResum.h
	$(CC) -Wall $(IPDF) -c BosonJetResum.c

#css

BosonJetCSS.o: BosonJetCSS.c BosonJetCSS.h
	$(CC) -Wall $(IPDF) -c BosonJetCSS.c

css.o: css.c
	$(CC) -Wall $(IPDF) $(IGSL) -c css.c

css: css.o BosonJetCSS.o BosonJetResum.o BosonJet.o QCD.o ElectroWeak.o Particle.o
	$(CC) -Wall css.o BosonJetCSS.o BosonJetResum.o BosonJet.o ElectroWeak.o QCD.o Particle.o $(LPDF) $(LGSL) -o css

#R resummed

BosonJetNLL.o: BosonJetNLL.c BosonJetNLL.h
	$(CC) -Wall $(IPDF) -c BosonJetNLL.c

resum.o: resum.c
	$(CC) -Wall $(IPDF) $(IGSL) -c resum.c

resum: resum.o BosonJetNLL.o BosonJetResum.o BosonJet.o QCD.o ElectroWeak.o Particle.o
	$(CC) -Wall resum.o BosonJetNLL.o BosonJetResum.o BosonJet.o ElectroWeak.o QCD.o Particle.o $(LPDF) $(LGSL) -o resum

#tot

BosonJetNLL.o: BosonJetNLL.c BosonJetNLL.h
	$(CC) -Wall $(IPDF) -c BosonJetNLL.c

tot.o: tot.c
	$(CC) -Wall $(IPDF) $(IGSL) -c tot.c

tot: tot.o BosonJetNLL.o BosonJetResum.o BosonJet.o QCD.o ElectroWeak.o Particle.o
	$(CC) -Wall tot.o BosonJetNLL.o BosonJetResum.o BosonJet.o ElectroWeak.o QCD.o Particle.o $(LPDF) $(LGSL) -o tot


clean:
	rm *.o
	rm resum
	rm tot
