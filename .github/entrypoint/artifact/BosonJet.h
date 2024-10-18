//#define MC_MISER
#include "QCD.h"
#include "ElectroWeak.h"
#include <gsl/gsl_math.h>
#include <gsl/gsl_monte.h>
#include <gsl/gsl_monte_vegas.h>
#include <gsl/gsl_monte_miser.h>

using namespace std;


class BosonJet{

 protected:

  unsigned int _nf;//flavors of quarks, 5 by default
  
  //pdfs and parameters
  double _Ecm;//=sqrt{s} characterizes the collision. We always choose the CM frame.
  QCD _qcd;
  ElectroWeak _ew;
  Particle *_boson;

  double _preXsection;//prefactor for calculting cross secton
  double _s;
  double _mB2;//boson mass squared

  double _x1, _x2, _yB, _yJ, _shat, _that, _uhat,_pT;//Kinematics for a scattering process
  
  //unit conversion 1 GeV fm=0.1973269788 from PDG 2018
  double invGeV2topb;//1/GeV^2 to pb

  //Variables for Monte Carlo
  const gsl_rng_type *_T;
  gsl_rng *_r;

#ifdef MC_MISER
  gsl_monte_miser_state * _mcStatus;
#else
 gsl_monte_vegas_state * _mcStatus;
#endif
 gsl_monte_function _mcFun;
  size_t _dim, _calls;

  double *_ymin, *_ymax;//integration boundary

 public:

  BosonJet();
  BosonJet(double Ecm, Particle *boson);

  //calculte the effective charge
  double e2(double);

  void setEcm(double Ecm);
  void setBoson(Particle *boson);
  void getxBs(double *xB, double pT, double yB, double yJ);//calculate Bjorken x's from Ecm, pT and the rapidities of the two produced particles
  void Mandelstam(double x1, double x2, double pT, double yB, double &s, double &t, double &u);
  void setNf(unsigned int nf);
  void setKinematics(double pT, double yB, double yJ);
  bool kinematicsQ();//return whether it is allowed kinematics.
  void getKinematics();
  void setpT(double pT);
  double getpT();
  
  //Born amplitudes squared: basically the hard function
  double Mgq2(double s, double t, double u);//averged amplitude squared for gq channel
  double Mgq2();//averged amplitude squared for gq channel
  double Mqg2();//averged amplitude squared for gq channel
  double Mqqb2(double s, double t, double u);//averaged amplitude squared for qqbar channel
  double Mqqb2();//averaged amplitude squared for qqbar channel

  //differential cross section at LO, used for tests
  double M2toXsection(double Q);//The prefactor*M^2 gives Born cross section.
  double M2toXsection(double pT, double x1, double x2, double Q);//The prefactor*M^2 gives Born cross section.
  double sigmagqLO(double pT, double yB, double yJ, double Q);//differential cross section for gq channel
  double sigmagqLO(double Qh, double QPDF);//differential cross section for gq+gqb channel
  double sigmaqgLO(double Q, double QPDF);//differential cross section for gq+gqb channel
  double sigmaqgLO(double pT, double yB, double yJ, double Q);//differential cross section for qg+qbg channel
  double sigmaqqbLO(double pT, double yB, double yJ, double Q);//differential cross section for qqb+qbq channel
  double sigmaqqbLO(double Q,double QPDF);//differential cross section for qq channel
  double sigmaLO(double pT, double yB, double yJ, double Q);
  double sigmaLO(double Q,double QPDF);

  //Monte Carlo
  void setupMC(double (*pds)(double *, size_t, void *), size_t dim, double *ymin, double *ymax, void *para);
  void cleanupMC();void setCalls(size_t);
  void calculate(double, ostream &);
  void calculate(double, double *);
  void calculate(double *);
};

