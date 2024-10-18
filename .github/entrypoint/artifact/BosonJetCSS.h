
#include "BosonJetResum.h"

class BosonJetCSS: public BosonJetResum{
 public:
  BosonJetCSS();
  BosonJetCSS(double Ecm, Particle *boson);

  //CSS formalism: H=Hard+Jet, S=Soft+Coft
  double H1qg(double muh);
  double H1qqb(double muh);
    
  double aHqgCSS();//a for anomalous dimension of hard function Hqg
  double bHqgCSS(double muh);//b for anomalous dimension of hard function Hqg

  double aHqqbCSS();//a for anomalous dimension of hard function Hqg
  double bHqqbCSS(double muh);//b for anomalous dimension of hard function Hqg

  double aSqgCSS();//a for anomalous dimension of soft function Hqg
  double bSqgCSS(double);//b for anomalous dimension of soft function Hqg

  double CHqgCSS(double mu, double muH);//nll resummed for hard function: Hqg in CSS
  
  double CHqqbCSS(double mu, double muH);//nll resummed for hard function: Hqg in CSS
 
  double CSqgCSS(double mu, double muS);//nll resummed for hard function: Hqg
  double sigmaqgCSS(double xT, double pT, double yB, double yJ);
  double sigmaqqbCSS(double xT, double pT, double yB, double yJ);
  double sigmaCSS(double xT, double pT, double yB, double yJ);

  double RGInvariance(double mu, double muxT, double muh);
  void getFilename(stringstream &filename, double ymin, double ymax);
};
