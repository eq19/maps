
#include "BosonJetNLL.h"

class BosonJetLL: public BosonJetNLL{

protected:
  
public:
  
  BosonJetLL();
  BosonJetLL(double Ecm, Particle *boson);

  void initLL();

  virtual  double bHqg();//b for anomalous dimension of hard function Hqg


  //NGL resummation
  
  void getFilename(stringstream &filename, double ymin, double ymax);
 
};

