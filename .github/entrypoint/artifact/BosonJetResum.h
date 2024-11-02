
#include "BosonJet.h"

class BosonJetResum: public BosonJet{

protected:
  
  double _R;
  double _qT;
  double _mu, _muJ, _muh, _muxT, _cphix, _mut, _xT, _b0;
  double _aHqg, _aJqg, _asbbqg, _acoftqg;
  double _aHqqb, _aJqqb, _asbbqqb, _acoftqqb;
  double _eps;//regulator for xT integration

  double _b2i, _beta0, _nc, _cf;//constant for RG evolution

  bool _nonpert;
  bool _ll;

  void init();
  
public:
  
  BosonJetResum();
  BosonJetResum(double Ecm, Particle *boson);

  void setR(double R);
  void setqT(double qT);
  void setmu(double mu);
  void setPara(double R, double qT, double mu);
  void setRegulator(double eps);
  void setScale(double mu, double muh, double muJ, double muxT, double mut,double xT, double cphix);
  void setNonPert(bool);
  void setLL(bool);

  double rge(double mu, double mu0, double a, double b);//gives the solution of RG equation

  double aHqg();//a for anomalous dimension of hard function Hqg
  double bHqg();//b for anomalous dimension of hard function Hqg

  double aJqg();//a for anomalous dimension of Jet function in qg
  double bJqg();//b for anomalous dimension of Jet function in qg

  double acoftqg();//a for coft function in qg
  double bcoftqg();

  double asbbqg();//a for anomalous dimension of soft+beams in qg->BJ
  double bsbbqg();//b for anomalous dimension 0of soft+beams in qg->BJ
  
  double aHqqb();//a for anomalous dimension of hard function Hqqb
  double bHqqb();//b for anomalous dimension of hard function Hqqb

  double aJqqb();//a for anomalous dimension of Jet function in qqb
  double bJqqb();//b for anomalous dimension of Jet function in qqb

  double acoftqqb();//a for coft function in qqb
  double bcoftqqb();//a for coft function in qqb

  double asbbqqb();//a for anomalous dimension of soft+beams in qqb->BJ
  double bsbbqqb();//b for anomalous dimension of soft+beams in qqb->BJ

  double Ccphixq();
  double Ccphixg();

  double RGInvariance(double mu, double muh, double muxT, double muJ, double mut, double xT, double cphix);
  
  double muxT(double xT);
  double muh();
  double muxTCSS(double xT);
  double muhCSS();
  double muJ();
  
  //Mathematical tricks

  double NonPert(double xT, double Q);
  double regulator(double xT);
};

