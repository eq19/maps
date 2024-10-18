#include <math.h>
#include "BosonJetResum.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_sf_dilog.h>

//#define SCREEN_ONLY

using namespace std;

void BosonJetResum::init(){
  _R=0.0;_qT=0.0;_eps=1.0e-4;_b0=1.1229189671337703;
  _aHqg=-2.0*(_qcd._Nc+2.0*_qcd._CF)/M_PI;_asbbqg=2.0*(_qcd._Nc+2.0*_qcd._CF)/M_PI;
  _aJqg=2.0*_qcd._CF/M_PI;_acoftqg=-2.0*_qcd._CF/M_PI;
  _aHqqb=-2.0*(_qcd._Nc+2.0*_qcd._CF)/M_PI;_aJqqb=2.0*_qcd._Nc/M_PI;
  _acoftqqb=-2.0*_qcd._Nc/M_PI;_asbbqqb=2.0*(_qcd._Nc+2.0*_qcd._CF)/M_PI;

  //constant for RG evolution
  _b2i=2.0*M_PI/_qcd._beta0;double b2ia=0.5/_qcd._beta0;
  _aHqg*=b2ia;_aJqg*=b2ia;_asbbqg*=b2ia;_acoftqg*=b2ia;
  _aHqqb*=b2ia;_aJqqb*=b2ia;_asbbqqb*=b2ia;_acoftqqb*=b2ia;

  _beta0=_qcd._beta0/M_PI;_nc=_qcd._Nc/M_PI;_cf=_qcd._CF/M_PI;

  _nonpert=false;
}

BosonJetResum::BosonJetResum(){
  init();
}

BosonJetResum::BosonJetResum(double Ecm, Particle *boson):BosonJet(Ecm, boson){
  init();
}

void BosonJetResum::setNonPert(bool npQ){
  _nonpert=npQ;
}

void BosonJetResum::setLL(bool ll){
  _ll=ll;
}


void BosonJetResum::setRegulator(double eps){
  _eps=eps;
}

void BosonJetResum::setScale(double mu, double muh, double muJ, double muxT, double mut,double xT, double cphix){
  _mu=mu;_muJ=muJ;_muh=muh;_mut=mut;_muxT=muxT, _xT=xT, _cphix=cphix;
}

double BosonJetResum::rge(double mu, double mu0, double a, double b){
  //double b2i=2.0*M_PI/_qcd._beta0;double b2ia=0.5*a/_qcd._beta0;
    //return pow(_qcd.alphas(mu)/_qcd.alphas(mu0),-b2i*b)*exp( -b2ia*log(mu/mu0)*log(_qcd.alphas(mu))-b2ia*b2i*( (log(_qcd.alphas(mu0))+1.0)/_qcd.alphas(mu0)- (log(_qcd.alphas(mu))+1.0)/_qcd.alphas(mu)) );
  double r=_qcd.alphas(mu)/_qcd.alphas(mu0);
  double lr=log(r);
    return exp(-_b2i*b*log(r)-_b2i*a*(4.0*M_PI*(1.0- 1.0/r-lr)/_qcd.alphas(mu0) + ( _qcd._gcusp1/_qcd._gcusp0-_qcd._beta1/_qcd._beta0 )*(1.0-r+lr) + 0.5*_qcd._beta1*lr*lr/_qcd._beta0 ) );
}

void BosonJetResum::setR(double R){
  if(R>0.0)
    _R=R;
  else{
    cout << "The cone size can not be less than zero!" << endl;
    throw exception();
  }
}

void BosonJetResum::setqT(double qT){
  if(qT>0.0)
    _qT=qT;
  else{
    cout << "qT can not be less than zero!" << endl;
    throw exception();
  }
}

void BosonJetResum::setmu(double mu){
  if(mu>0.0)
    _mu=mu;
  else{
    cout << "mu can not be less than zero!" << endl;
    throw exception();
  }
}

void BosonJetResum::setPara(double R, double qT, double mu){
  setR(R);setqT(qT);setmu(mu);
}

double BosonJetResum::regulator(double xT){
    return exp(-_eps*xT*xT);
  }

double BosonJetResum::aHqg(){
  return _aHqg;
}

double BosonJetResum::bHqg(){
  double b;
  if(_ll){
    b=-(_cf*(2.0*log(-_muh*_muh/_uhat))+_nc*log(_muh*_muh*_uhat/(_shat*_that)));
  }
  else{
    b=-(0.5*_beta0+_cf*(3.0+2.0*log(-_muh*_muh/_uhat))+_nc*log(_muh*_muh*_uhat/(_shat*_that)));
  }
  return b;
}


double BosonJetResum::aJqg(){
  return _aJqg;
}

double BosonJetResum::bJqg(){
  double b;
  if(_ll){
    b=_cf*(-2.0*log(_pT*_R/_muJ) );
  }
  else{
    b=_cf*(1.5-2.0*log(_pT*_R/_muJ) );
  }
  return b;
}

double BosonJetResum::acoftqg(){
  return _acoftqg;
}

double BosonJetResum::bcoftqg(){
  //return -2.0*_cf*log( 2.0*fabs(_cphix)*_xT*_mut/(_b0*_R) );
  double b;
  if(_ll){
    b=-2.0*_cf*log(_xT*_mut/(_b0*_R) );
  }
  else{
    b=-2.0*_cf*log( 2.0*_xT*_mut/(_b0*_R) );
  }
  return b;
}

double BosonJetResum::asbbqg(){
  return _asbbqg;
}

double BosonJetResum::bsbbqg(){
  //return (0.5*_beta0+_cf*(1.5+2.0*log(-2.0*fabs(_cphix)*_pT*_xT*_muxT*_muxT/(_b0*_uhat)) )-2.0*_nc*log(-_that/(_pT*_muxT)) );
  double b;
  if(_ll){
    b=(_cf*(2.0*log(-_pT*_xT*_muxT*_muxT/(_b0*_uhat)) )-2.0*_nc*log(-_that/(_pT*_muxT)) );
  }
  else{
    b=(0.5*_beta0+_cf*(1.5+2.0*log(-2.0*_pT*_xT*_muxT*_muxT/(_b0*_uhat)) )-2.0*_nc*log(-_that/(_pT*_muxT)) );
  }
  return b;
}

double BosonJetResum::aHqqb(){
  return _aHqqb;
}

double BosonJetResum::bHqqb(){
  double b;
  if(_ll){
    b=(2.0*_nc*log(_pT/_muh)-_cf*(2.0*log(_muh*_muh/_shat)));
  }
  else{
    b=(2.0*_nc*log(_pT/_muh)-0.5*_beta0-_cf*(3.0+2.0*log(_muh*_muh/_shat)));
  }
  return b;
}

double BosonJetResum::aJqqb(){
  return _aJqqb;
}

double BosonJetResum::bJqqb(){
  double b;
  if(_ll){
    b=(-2.0*_nc*log(_pT*_R/_muJ) );
  }
  else{
    b=( 0.5*_beta0-2.0*_nc*log(_pT*_R/_muJ) );
  }
  return b;

}


double BosonJetResum::acoftqqb(){
  return _acoftqqb;
}

double BosonJetResum::bcoftqqb(){
  //return -2.0*_nc*log( 2.0*fabs(_cphix)*_xT*_mut/(_b0*_R) );
  double b;
  if(_ll){
    b=-2.0*_nc*log(_xT*_mut/(_b0*_R) );
  }
  else{
    b=-2.0*_nc*log( 2.0*_xT*_mut/(_b0*_R) );
 }
  return b;
}


double BosonJetResum::asbbqqb(){
  return _asbbqqb;
}

double BosonJetResum::bsbbqqb(){
  //return (2.0*_nc*log(2.0*fabs(_cphix)*_xT*_muxT/(_b0))+_cf*(3.0+2.0*log(_muxT*_muxT/_shat)) );
  double b;
  if(_ll){
    b=(2.0*_nc*log(_xT*_muxT/(_b0))+_cf*(2.0*log(_muxT*_muxT/_shat)) );
  }
  else{
    b=(2.0*_nc*log(2.0*_xT*_muxT/(_b0))+_cf*(3.0+2.0*log(_muxT*_muxT/_shat)) );
  }
  return b;
}

double BosonJetResum::Ccphixq(){
  double pre=4.0*_qcd._CF/_qcd._beta0;
  return exp(pre*log(fabs(_cphix))*log(_qcd.alphas(_muxT)/_qcd.alphas(_mut)) );
}

double BosonJetResum::Ccphixg(){
  double pre=4.0*_qcd._Nc/_qcd._beta0;
  return exp(pre*log(fabs(_cphix))*log(_qcd.alphas(_muxT)/_qcd.alphas(_mut)) );
}

double BosonJetResum::muxT(double xT){
  return 1.1229189671337703/xT;//muxT=2.0*exp(-gamma_E)/xT
}

double BosonJetResum::RGInvariance(double mu, double muh, double muxT, double muJ, double mut, double xT, double cphix){
  double b2ia=0.5/_qcd._beta0;
  _mu=mu;_muh=muh; _muxT=muxT; _muJ=muJ; _mut=mut;_xT=xT;_cphix=cphix;
  //return aHqg()+asbbqg()+aJqg()+acoftqg();
  //return aHqqb()+asbbqqb()+aJqqb()+acoftqqb();
  cout << aHqg()*log(_mu/_muh)/b2ia+bHqg() << " vs " << (2.0*_cf+_nc)*log(_shat/(_mu*_mu))+_cf*log(_uhat*_uhat/(_pT*_pT*_shat))+_nc*log(_that*_that/(_pT*_pT*_shat))+_cf*log(_pT*_pT/(_shat)) << endl;
  cout << asbbqg()*log(_mu/_muxT)/b2ia+bsbbqg() << " vs " << -2.0*_cf*log(-_uhat/(_mu*_pT))-2.0*_nc*log(-_that/(_mu*_pT))+ 2.0*_cf*log(_xT*_mu/_b0)<< endl;
  cout << aJqg()*log(_mu/_muJ)/b2ia+bJqg() << " vs " <<-2.0*_cf*log(_pT*_R/_mu) << endl;
  cout << acoftqg()*log(_mu/_mut)/b2ia+bcoftqg() << " vs " << 2.0*_cf*log(_R*_b0/(_mu*_xT))<< endl;
  cout << aHqqb()*log(_mu/_muh)/b2ia+bHqqb() << " vs " << (2.0*_cf+_nc)*log(_shat/(_mu*_mu))+_cf*log(_uhat*_uhat/(_pT*_pT*_shat))+_cf*log(_that*_that/(_pT*_pT*_shat))+_nc*log(_pT*_pT/(_shat)) << endl;
  cout << asbbqqb()*log(_mu/_muxT)/b2ia+bsbbqqb() << " vs " << -2.0*_cf*log(-_uhat/(_mu*_pT))-2.0*_cf*log(-_that/(_mu*_pT))+ 2.0*_nc*log(_xT*_mu/_b0) << endl;
  cout << aJqqb()*log(_mu/_muJ)/b2ia+bJqqb() << " vs " <<-2.0*_nc*log(_pT*_R/_mu) << endl;
  cout << acoftqqb()*log(_mu/_mut)/b2ia+bcoftqqb() << " vs " << 2.0*_nc*log(_R*_b0/(_mu*_xT)) << endl;
  return aHqg()*log(_mu/_muh)/b2ia+bHqg()+asbbqg()*log(_mu/_muxT)/b2ia+bsbbqg()+aJqg()*log(_mu/_muJ)/b2ia+bJqg()+acoftqg()*log(_mu/_mut)/b2ia+bcoftqg()+aHqqb()*log(_mu/_muh)/b2ia+bHqqb()+asbbqqb()*log(_mu/_muxT)/b2ia+bsbbqqb()+aJqqb()*log(_mu/_muJ)/b2ia+bJqqb()+acoftqqb()*log(_mu/_mut)/b2ia+bcoftqqb();
  //return aHqqb()*log(_mu/_muh)/b2ia+bHqqb()+asbbqqb()*log(_mu/_muxT)/b2ia+bsbbqqb()+aJqqb()*log(_mu/_muJ)/b2ia+bJqqb()+acoftqqb()*log(_mu/_mut)/b2ia+bcoftqqb();
}

double BosonJetResum::muxTCSS(double xT){
  return muxT(xT)*sqrt(1.0+xT*xT/2.25);
}

double BosonJetResum::muhCSS(){
  //cout << _mB2 << ", " << _pT << endl;
  return sqrt(_mB2+_pT*_pT)+_pT;
}

double BosonJetResum::muh(){
  //cout << _mB2 << ", " << _pT << endl;
  //return (sqrt(_mB2)+7.0*_pT)/6.0;
  return sqrt(_mB2+_pT*_pT);
}

double BosonJetResum::muJ(){
  return _R*_pT;
}

double BosonJetResum::NonPert(double xT, double Q){
  double bmax=1.5;
  return exp(-0.21*xT*xT-0.42*log(Q/1.5491933384829668)*log(1.0+xT*xT/(bmax*bmax)));
}
