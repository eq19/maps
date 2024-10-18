#include "BosonJet.h"
#include <cmath>
#define PI 3.141592653589793

BosonJet::BosonJet(){
  invGeV2topb=3.893793656233564944e8;
  _nf=5;_calls=50000;
}

BosonJet::BosonJet(double Ecm, Particle *boson){
  _boson=boson;_Ecm=Ecm;invGeV2topb=3.893793656233564944e8;
  _nf=5;_calls=50000;

  //calculate some universal prefactors:
  _s=_Ecm*_Ecm;
  _preXsection=2.0*PI*_ew.alpha()/(_s*_s);
  _mB2=_boson->m()*_boson->m();

}

void BosonJet::setpT(double pT){
  _pT=pT;
}

double BosonJet::getpT(){
  return _pT;
}

void BosonJet::getKinematics(){
  cout << "x1=" << _x1 << ", x2=" << _x2 << ", s=" << _shat << ", t=" << _that << ", u=" << _uhat << endl;
}

double BosonJet::M2toXsection(double pT, double x1, double x2, double Q){
  /*
    This function gives the prefactor for
    dsigma/dpTdyBdyJ=2*pi*pT*aEM*aS*M2/(x1*x2*s^2)*pdf1(x2)*pdf2(x2)
    without pdfs and M2 and aS.
   */
  return _preXsection*pT*_qcd.alphas(Q)/(x1*x2);
}

double BosonJet::M2toXsection(double Q){
  /*
    This function gives the prefactor for
    dsigma/dpTdyBdyJ=2*pi*pT*aEM*aS*M2/(x1*x2*s^2)*pdf1(x2)*pdf2(x2)
    without pdfs and M2 and aS.
   */
  return _preXsection*_pT*_qcd.alphas(Q)/(_x1*_x2);
}

void BosonJet::setEcm(double Ecm){
  _Ecm=Ecm;_s=_Ecm*_Ecm;_preXsection=2.0*PI*_ew.alpha()/(_Ecm*_Ecm*_Ecm*_Ecm);
}

void BosonJet::setBoson(Particle *boson){
  _boson=boson; _mB2=_boson->m()*_boson->m();
}

void BosonJet::setNf(unsigned int nf){
  _nf=nf;
}

void BosonJet::getxBs(double *xB, double pT, double yB, double yJ){
  /*
    p1=x_1 (_Ecm,0,0,_Ecm)/2, p2=x_2 (_Ecm,0,0,-_Ecm)/2, 
    pB=(sqrt(pT^2+m^2)cosh(yB),pT cos(phiB),pT sin(phiB),sqrt(pT^2+m^2)sinh(yB)),
    pJ=(sqrt(pT^2+m^2) cosh(yJ),pT cos(phiJ),pT sin(phiJ),sqrt(pT^2+m^2)sinh(yJ)).
   */
  double mT=sqrt(1.0+_boson->m()*_boson->m()/(pT*pT));
  double xT=pT/_Ecm;
  xB[0]=xT*(mT*exp(yB)+exp(yJ));xB[1]=xT*(mT*exp(-yB)+exp(-yJ));
}

void BosonJet::Mandelstam(double x1, double x2, double pT, double yB, double &s, double &t, double &u){
  /* p1=xB[0] (_Ecm, 0,0,_Ecm)/2, p2=xB[1](_Ecm,0,0,-_Ecm)/2,
     pB=(sqrt(pT^2+mB^2)cosh(yB), pT cos(phiB), pT sin(phiB),sqrt(pT^2+mB^2)sinh(yB)),
  */
  double mT=sqrt(_mB2+pT*pT);double EcmmT=_Ecm*mT;
  s=x1*x2*_s; t=_mB2-x1*EcmmT*exp(-yB); u=_mB2-x2*EcmmT*exp(yB);
}

void BosonJet::setKinematics(double pT, double yB, double yJ){
  _pT=pT;_yB=yB;_yJ=yJ;
  double xB[2];getxBs(xB, pT, yB, yJ);_x1=xB[0];_x2=xB[1];
  double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);_shat=s;_that=t;_uhat=u;
  //cout << _shat << ", " << _that << ", " << _uhat << ", " << _x1 << ", " << _x2 << endl;
  //cout << _shat*_pT*_pT/(_that*_uhat) << endl;
}

bool BosonJet::kinematicsQ(){
  return _x1>0.0&&_x1<1.0&&_x2>0.0&&_x2<1.0;
}

/*
  M^2/(g_s^2 e_q^2) aveaged and summed over the spin and color indices repectively in the intial and final states.
  See Table 7.2 in page 265 in QCD and Collider Physics.
*/

double BosonJet::Mgq2(double s, double t, double u){
  /*
    M^2/(e^2g^2) for gq->BJ. For qg->BJ, swap t and u.
   */
  return -(s*s+u*u+2.0*t*(s+t+u))/(_qcd._Nc*s*u); 
}

double BosonJet::Mgq2(){
  /*
    M^2/(e^2g^2) for gq->BJ.
   */
  return -(_shat*_shat+_uhat*_uhat+2.0*_that*(_shat+_that+_uhat))/(_qcd._Nc*_shat*_uhat); 
}

double BosonJet::Mqg2(){
  /*
    M^2/(e^2g^2) for qg->BJ.
   */
  return -(_shat*_shat+_that*_that+2.0*_uhat*(_shat+_uhat+_that))/(_qcd._Nc*_shat*_that); 
}

double BosonJet::Mqqb2(double s, double t, double u){
  /*M^2/(e^2g^2) for qqb->BJ. The same for qbq->BJ.
   */
  return 2.0*_qcd._CF*(t*t+u*u+2.0*s*(s+t+u))/(_qcd._Nc*t*u);
}

double BosonJet::Mqqb2(){
  /*M^2/(e^2g^2) for qqb->BJ. The same for qbq->BJ.
   */
  return 2.0*_qcd._CF*(_that*_that+_uhat*_uhat+2.0*_shat*(_shat+_that+_uhat))/(_qcd._Nc*_that*_uhat);
}

double BosonJet::e2(double eq){
  double e2eff;
  switch(_boson->id()){
  case 22:
    e2eff=eq*eq;//photon
    break;
  case 23:
    e2eff=1.0-2.0*fabs(eq)*_ew.sw2();e2eff=(e2eff*e2eff+4.0*eq*eq*_ew.sw2()*_ew.sw2())/(8.0*_ew.sw2()*_ew.cw2());//Z^0
  }
  return e2eff;
}

//differential cross sectoin at LO

double BosonJet::sigmagqLO(double pT, double yB, double yJ, double Q){
  /*
     dsigma/dpTdyZdyJ in unit pb/GeV for gq->ZJ & gqb->ZJ
   */
  double res;
  double xB[2];getxBs(xB, pT, yB, yJ);
  if(xB[0]>1.0||xB[1]>1.0||xB[0]<0.0||xB[1]<0.0) res=0.0;
  else{
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    //cout << s << ", " << t  << ", " << u << endl;
    double dsgq=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      dsgq+=(_qcd.pdf(i,xB[1],Q)+_qcd.pdf(-i,xB[1],Q))*e2(_qcd._partons[i].e());//g(p1) q(p2)->boson(pB) jet(pJ)
    }
    res=(_qcd.pdf(21,xB[0],Q)*dsgq*Mgq2(s,t,u))*M2toXsection(pT, xB[0], xB[1], Q);
    //cout << (_qcd.pdf(21,xB[0],Q)*dsgq*Mgq2(s,t,u)) << ", " << M2toXsection(pT, xB[0], xB[1], Q) << endl;

  }
  return res*invGeV2topb;//return with unit pb
}

double BosonJet::sigmagqLO(double Qh, double QPDF){
  /*
     dsigma/dpTdyZdyJ in unit pb/GeV for gq->ZJ & gqb->ZJ
   */
  double res=0.0;
  if(kinematicsQ()){
    double dsgq=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      dsgq+=(_qcd.pdf(i,_x2,QPDF)+_qcd.pdf(-i,_x2,QPDF))*e2(_qcd._partons[i].e());//g(p1) q(p2) or g(p1) qb(p2)->boson(pB) jet(pJ)
    }
    res=(_qcd.pdf(21,_x1,QPDF)*dsgq*Mgq2())*M2toXsection(Qh);
    //cout << (_qcd.pdf(21,xB[0],Q)*dsgq*Mgq2(s,t,u)) << ", " << M2toXsection(pT, xB[0], xB[1], Q) << endl;

  }
  return res*invGeV2topb;//return with unit pb
}


double BosonJet::sigmaqgLO(double pT, double yB, double yJ, double Q){
  /*
    dsigma/dpTdyZdyJ in unit pb/GeV for qg->ZJ and qbg->ZJ
   */
  double res;
  double xB[2];getxBs(xB, pT, yB, yJ);
  if(xB[0]>1.0||xB[1]>1.0||xB[0]<0.0||xB[1]<0.0) res=0.0;
  else{
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    double dsqg=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      dsqg+=(_qcd.pdf(i,xB[0],Q)+_qcd.pdf(-i,xB[0],Q))*e2(_qcd._partons[i].e());//q(p1) g(p2) or qb(p1) g(p2)->boson(pB) jet(pJ)
    }
    res=dsqg*_qcd.pdf(21,xB[1],Q)*Mgq2(s,u,t)*M2toXsection(pT, xB[0], xB[1], Q);
  }
  return res*invGeV2topb;
}

double BosonJet::sigmaqgLO(double Q,double QPDF){
  /*
    dsigma/dpTdyZdyJ in unit pb/GeV for qg->ZJ and qbg->ZJ
   */
  double res=0.0;
  if(kinematicsQ()){
    double dsqg=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      dsqg+=(_qcd.pdf(i,_x1,QPDF)+_qcd.pdf(-i,_x1,QPDF))*e2(_qcd._partons[i].e());//q(p1) g(p2) or qb(p1) g(p2)->boson(pB) jet(pJ)
    }
    res=dsqg*_qcd.pdf(21,_x2,QPDF)*Mqg2()*M2toXsection(Q);
  }
  return res*invGeV2topb;
}

double BosonJet::sigmaqqbLO(double pT, double yB, double yJ, double Q){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for qqb->ZJ and qbq->ZJ
  */
    double res;
    double xB[2];getxBs(xB, pT, yB, yJ);
    if(xB[0]>1.0||xB[1]>1.0||xB[0]<0.0||xB[1]<0.0) res=0.0;
    else{
      double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
      double ds=0.0;
      for(unsigned int i=1;i<=_nf;i++){
	//qg->Zj
	ds+=_qcd.pdf(i,xB[0],Q)*_qcd.pdf(-i,xB[1],Q)*e2(_qcd._partons[i].e());//g(p1) q(p2)->boson(pB) jet(pJ)
	//qbg->ZJ
	ds+=_qcd.pdf(i,xB[1],Q)*_qcd.pdf(-i,xB[0],Q)*e2(_qcd._partons[i].e());//q(p1) g(p2)->boson(pB) jet(pJ)
      }
      res=ds*Mqqb2(s,t,u)*M2toXsection(pT, xB[0], xB[1], Q);
    }
    return res*invGeV2topb;//return with unit pb
}

double BosonJet::sigmaqqbLO(double Q, double QPDF){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for qqb->ZJ and qbq->ZJ
  */
    double res=0.0;
    if(kinematicsQ()){
      double ds=0.0;
      for(unsigned int i=1;i<=_nf;i++){
	//qqb and qb q->Zj
	ds+=(_qcd.pdf(i,_x1,QPDF)*_qcd.pdf(-i,_x2,QPDF)+_qcd.pdf(i,_x2,QPDF)*_qcd.pdf(-i,_x1,QPDF))*e2(_qcd._partons[i].e());
      }
      res=ds*Mqqb2()*M2toXsection(Q);
    }
    return res*invGeV2topb;//return with unit pb
}

double BosonJet::sigmaLO(double pT, double yB, double yJ, double Q){
  return sigmaqgLO(pT, yB, yJ, Q)+sigmagqLO(pT, yB, yJ, Q)+sigmaqqbLO(pT, yB, yJ, Q);
}

double BosonJet::sigmaLO(double Q, double QPDF){
  double res=0.0;
  if(kinematicsQ()){
    res=sigmaqgLO(Q, QPDF)+sigmagqLO(Q, QPDF)+sigmaqqbLO(Q, QPDF);
  }
  return res;
}

//MC integration

void BosonJet::setupMC(double (*pds)(double *, size_t, void *), size_t dim, double *ymin, double *ymax, void *para){

  gsl_rng_env_setup ();
  _T = gsl_rng_default;
  _r = gsl_rng_alloc (_T);

  _dim=dim;_mcFun.f=pds;_mcFun.dim=dim;_mcFun.params=para;
#ifdef MC_MISER
  cout << "miser is used..." << endl;
  _mcStatus = gsl_monte_miser_alloc (dim);
#else
  cout << "vegas is used..." << endl;
  _mcStatus = gsl_monte_vegas_alloc (dim);
#endif
  _ymin=ymin;_ymax=ymax;

}

void BosonJet::cleanupMC(){
#ifdef MC_MISER
  gsl_monte_miser_free (_mcStatus);
#else
  gsl_monte_vegas_free (_mcStatus);
#endif
  gsl_rng_free (_r);

}

void BosonJet::setCalls(size_t calls){
  _calls=calls;
}

void BosonJet::calculate(double qT, ostream &out){
  double res, err;
#ifdef MC_MISER
  gsl_monte_miser_integrate (&_mcFun, _ymin, _ymax, _dim, _calls, _r, _mcStatus, &res, &err);
#else
  gsl_monte_vegas_integrate (&_mcFun, _ymin, _ymax, _dim, _calls, _r, _mcStatus, &res, &err);
#endif
  out << setprecision(15) << qT << "   " << qT*res << "   " << qT*err << endl;//here, in resum, we actually calculate dsigam/qTdqT but we only save dsigma/dqT.
}

void BosonJet::calculate(double qT, double *res){
#ifdef MC_MISER
  gsl_monte_miser_integrate (&_mcFun, _ymin, _ymax, _dim, _calls, _r, _mcStatus, &res[0], &res[1]);
#else
  gsl_monte_vegas_integrate (&_mcFun, _ymin, _ymax, _dim, _calls, _r, _mcStatus, &res[0], &res[1]);
#endif
}

void BosonJet::calculate(double *res){//calculate the total cross section in pb
#ifdef MC_MISER
  gsl_monte_miser_integrate (&_mcFun, _ymin, _ymax, _dim, _calls, _r, _mcStatus, &res[0], &res[1]);
#else
  gsl_monte_vegas_integrate (&_mcFun, _ymin, _ymax, _dim, _calls, _r, _mcStatus, &res[0], &res[1]);
#endif
}

