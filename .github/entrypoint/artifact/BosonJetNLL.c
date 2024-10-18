#include <math.h>
#include "BosonJetNLL.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_sf_dilog.h>

//#define SCREEN_ONLY

BosonJetNLL::BosonJetNLL():BosonJetResum(){
  initNLL();
}

BosonJetNLL::BosonJetNLL(double Ecm, Particle *boson):BosonJetResum(Ecm, boson){
  initNLL();
}

void BosonJetNLL::initNLL(){
  _css=false;_imgcphix=true;;_ngl=true;
  _angl=0.85*_qcd._Nc;_bngl=0.86*_qcd._Nc;_cngl=1.33;
  _cNGL=_qcd._Nc*_qcd._CF*M_PI*M_PI/(3.0);
  _muhV=1.0;_muJV=1.0;_mutV=1.0;_muxTV=1.0;

  _mutMin=10.0;
  _ll=false;
}

void BosonJetNLL::setScaleVar(double vh, double vb, double vJ, double vt){
  _muhV=vh;_muxTV=vb;_muJV=vJ;_mutV=vt;
}

void BosonJetNLL::setCSS(bool cssQ){
  _css=cssQ;
}

void BosonJetNLL::setNGL(bool nglQ){
  _ngl=nglQ;
}

void BosonJetNLL::setImgcphix(bool cssQ){
  _imgcphix=cssQ;
}

double BosonJetNLL::CHqg(){
  //cout << _mu <<", " << _muh << ", " << _pT <<  ", " << aHqg() << ", " << bHqg() << ", " << aHqg()*log(_mu/_muh)+bHqg() << endl;
  return rge(_mu,_muh,aHqg(),bHqg());
}

double BosonJetNLL::CJqg(){
  return rge(_mu,_muJ,aJqg(),bJqg());
}

double BosonJetNLL::Ccoftqg(){
  return rge(_mu,_mut,acoftqg(),bcoftqg());
}

double BosonJetNLL::Csbbqg(){
  return rge(_mu,_muxT,asbbqg(),bsbbqg());
}

double BosonJetNLL::CHqqb(){
  return rge(_mu,_muh,aHqqb(),bHqqb());
}

double BosonJetNLL::CJqqb(){
  return rge(_mu,_muJ,aJqqb(),bJqqb());
}

double BosonJetNLL::Ccoftqqb(){
  return rge(_mu,_mut,acoftqqb(),bcoftqqb());
}

double BosonJetNLL::Csbbqqb(){
  return rge(_mu,_muxT,asbbqqb(),bsbbqqb());
}

//R resum
double BosonJetNLL::Ccphixqg(){
  return cos(2.0*M_PI*_qcd._CF*log(_qcd.alphas(_muxT)/_qcd.alphas(_mut))/_qcd._beta0);
}

double BosonJetNLL::Ccphixqqb(){
  return cos(2.0*M_PI*_qcd._Nc*log(_qcd.alphas(_muxT)/_qcd.alphas(_mut))/_qcd._beta0);
}

double BosonJetNLL::NGL(){
  double res=1.0;
  
  if(_mut<_muJ){
    double u=log(_qcd.alphas(_mut)/_qcd.alphas(_muJ))/_qcd._beta0;
    double u2=u*u;

  //cout << _mut << ", " << _muJ << endl;

  //cout << u2 << ", " << exp(-_cNGL*u2*(1.0+_angl*_angl*u2)/(1.0+pow(_bngl*u,_cngl))) << endl;
  
  res=exp(-_cNGL*u2*(1.0+_angl*_angl*u2)/(1.0+pow(_bngl*u,_cngl)));
  }
  return res;
}


void BosonJetNLL::setScales(double xT){
  _muxT=_muxTV*_b0/xT;_muh=_muhV*muh();_muJ=_muJV*_R*_pT;_mut=_mutV*_R*_b0/xT;
  _mu=_muJ;
  if(_muxT>_muh) _muxT=_muh;
  if(_mut>_muJ) _mut=_muJ;
  if(_muxT>_pT) _muxT=_pT;
  
  // if(_mut<_muJ&&_muxT<_muh){
  
  //CSS
  if(_css){
    _mut=_muxT;_muJ=_muh;_mu=_muxT;
  }
}

double BosonJetNLL::sigmaqgR(double xT, double cphix, double pT, double yB, double yJ){
  /*
    dsigma/qTdqTdpTdyBdyJ in pb/GeV for qg->ZJ+qbg->ZJ.
  */

  setKinematics(pT,yB,yJ);double res=0.0;
  if(kinematicsQ()){
    
    _xT=xT; _cphix=cphix; setScales(xT);
    if((_qcd.alphas(_muxT)/_qcd.alphas(_mut)>exp(-0.25*_qcd._beta0/_qcd._CF))){
      //cout << "RGI: " << RGInvariance(_mu, _muh, _muxT, _muJ, _mut, xT, cphix) << endl;
      if(_mutMin>_mut) _mutMin=_mut;
      //cout << _mutMin << ", " << _mut << endl;
      res=xT*gsl_sf_bessel_J0(_qT*xT)*Ccphixq()*CHqg()*CJqg()*Csbbqg()*Ccoftqg()*sigmaqgLO(_muh,_muxT)/M_PI;
      if(_nonpert){
	res*=NonPert(xT,_muh);
      }
      if(_imgcphix){
	res*=Ccphixqg();
      }
      if(_ngl){
	res*=NGL();
      }
    }
      //}
  }
  return res;
}


double BosonJetNLL::sigmaqqbR(double xT, double cphix, double pT, double yB, double yJ){
  /*
    dsigma/qTdqTdpTdyBdyJ in pb/GeV for qqb->ZJ+qbg->ZJ.
  */

  setKinematics(pT,yB,yJ);double res=0.0;
  if(kinematicsQ()){
    
    _xT=xT; _cphix=cphix; setScales(xT);
    //cout << "qqb: " << Ccphixqqb()*Csbbqqb() << ", " << CHqqb()*CJqqb()*Csbbqqb()*Ccoftqqb() << endl;
    //cout << "mu=" << _mu << ", muxT=" << _muxT << ", muh=" << _muh << ", muJ" << _muJ << ", mut=" << _mut << endl;
    //    cout << exp(-0.25*_qcd._beta0/_qcd._Nc) << ", " << exp(-0.25*_qcd._beta0/_qcd._CF) << endl;
    if((_qcd.alphas(_muxT)/_qcd.alphas(_mut)>exp(-0.25*_qcd._beta0/_qcd._Nc))){
      if(_mutMin>_mut) _mutMin=_mut;
      res=xT*gsl_sf_bessel_J0(_qT*xT)*Ccphixg()*CHqqb()*CJqqb()*Csbbqqb()*Ccoftqqb()*sigmaqqbLO(_muh,_muxT)/M_PI;
      if(_nonpert){
	res*=NonPert(xT,_muh);
      }
      if(_imgcphix){
	res*=Ccphixqqb();
      }
      if(_ngl){
	double ngl=NGL();
	res*=pow(ngl,_qcd._Nc/_qcd._CF);
      }
    //}
    }
  }
  return res;
}

double BosonJetNLL::sigmaR(double xT, double cphix, double pT, double yB, double yJ){
  /*
    dsigma/qTdqTdpTdyBdyJ in pb/GeV.
  */

  return 2.0*sigmaqgR(xT, cphix, pT, yB, yJ)+sigmaqqbR(xT, cphix, pT, yB,yJ);
}



//filename

void BosonJetNLL::getFilename(stringstream &filename, double ymin, double ymax){
  filename << "R" << _R << "pT" << ymin << "." << ymax;
  if(_css){
    filename << "CSS";
  }
  if(_nonpert){
    filename << "NP";
  }
  if(_ngl){
    filename << "NGL";
  }
  if(_ll){
    filename << "LL";
  }
  filename <<"muh" << _muhV << "mub" << _muxTV << "muJ" << _muJV << "mut" << _mutV;
  filename <<"s"<< _Ecm << ".dat";
}

