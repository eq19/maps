#include "BosonJet.h"

class BosonJetLO: public BosonJet{

 public:
    BosonJetLO(double Ecm, Particle *boson);

  //differential cross section at LO
  double sigmaqg(double qT, double pT, double yB, double yJ, double R, double Q);//differential cross section for gq channel
  double sigmaqg(double qT, double pT, double yB, double yJ,double z, double R, double Q);//differential cross section for gq channel
  //differential cross section after resummation (RG evolution)
  double sigmagq(double qT,double dphi, double pT, double yB, double yJ);//differential cross section for gq channel
  double sigmagg(double qT,double pT, double yB, double yJ, double z,double Q);//differential cross section for gq channel
  double sigmaqq(double qT,double pT, double yB, double yJ, double z,double Q);//differential cross section for gq channel
  double sigmaqbqb(double qT,double pT, double yB, double yJ, double z,double Q);//differential cross section for gq channel
  double sigmaqqb(double qT,double pT, double yB, double yJ, double R, double Q);//differential cross section for gq channel
  double sigmaqqb(double qT,double pT, double yB, double yJ,double z, double R, double Q);//differential cross section for gq channel
  double sigma(double qT,double pT, double yB, double yJ, double z, double R, double Q);
  
  //Fixed-order calculation
  double nllqg(double pT, double qT, double yB, double yJ, double R, double Q);
  double nllqq(double pT, double qT, double yB, double yJ, double R, double Q);

  //Output
  void getFilename(stringstream &filename, double R, int chan, double ymin, double ymax);

};

struct ParaQT{BosonJetLO *_bj;double _R;double _qT; int _chan;};


