#include "BosonJetBorn.h"


BosonJetBorn::BosonJetBorn(double Ecm, Particle *boson):BosonJet(Ecm, boson){
}

void BosonJetBorn::getFilename(stringstream &filename, double yJmax){
  filename << "s" << _Ecm << "etaJ" << yJmax << "Born.dat";

}
