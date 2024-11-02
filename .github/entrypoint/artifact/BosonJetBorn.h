#include "BosonJet.h"

class BosonJetBorn: public BosonJet{

 public:
    BosonJetBorn(double Ecm, Particle *boson);
    void getFilename(stringstream &filename, double ymax);

};
