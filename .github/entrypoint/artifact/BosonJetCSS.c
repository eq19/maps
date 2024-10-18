#include <math.h>
#include "BosonJetCSS.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_sf_dilog.h>

//#define SCREEN_ONLY

using namespace std;

BosonJetCSS::BosonJetCSS():BosonJetResum(){
}

BosonJetCSS::BosonJetCSS(double Ecm, Particle *boson):BosonJetResum(Ecm, boson){
}


//CSS
double BosonJetCSS::H1qqb(double muh){
  double lmuhomz2=log(muh*muh/_mB2), lRpTomuh2=_R*_pT/muh,mz2t=_mB2/(_mB2-_that),mz2u=_mB2/(_mB2-_uhat);
  double lsomz2=log(_shat/_mB2),ltomz2=log(-_that/_mB2),luomz2=log(-_uhat/_mB2),lmz2t=log(mz2t),lmz2u=log(mz2u);
  lRpTomuh2=2.0*log(lRpTomuh2);
  return 0.5*_qcd.alphas(muh)*( _qcd._Nc*( -_qcd._beta0*lRpTomuh2/6.0 +0.5*lRpTomuh2*lRpTomuh2 + gsl_sf_dilog(mz2t)+ gsl_sf_dilog(mz2u)-lmuhomz2*log(_shat*_mB2/(_that*_uhat)) - 0.5*lmuhomz2*lmuhomz2+0.5*lsomz2*lsomz2-0.5*(ltomz2+luomz2)*(ltomz2+luomz2) + ltomz2*luomz2 + 0.5*lmz2t*lmz2t+0.5*lmz2u*lmz2u-2.0*log(_R)*log(_R)-2.0*M_PI*M_PI/3.0+67.0/9.0-23.0*_nf/54.0 ) + _qcd._CF*( 2.0*lsomz2*lmuhomz2-lmuhomz2*lmuhomz2-3.0*lmuhomz2-lsomz2*lsomz2+M_PI*M_PI-8.0 ) )/M_PI;
}

double BosonJetCSS::H1qg(double muh){
  double lmuhomz2=log(muh*muh/_mB2), lRpTomuh2=_R*_pT/muh,mz2t=_mB2/(_mB2-_that),mz2u=_mB2/(_mB2-_uhat);
  double lsomz2=log(_shat/_mB2),ltomz2=log(-_that/_mB2),luomz2=log(-_uhat/_mB2),lmz2t=log(mz2t),lmz2u=log(mz2u);
  lRpTomuh2=2.0*log(lRpTomuh2);
  return 0.5*_qcd.alphas(muh)*( _qcd._CF*( -1.5*lRpTomuh2 +0.5*lRpTomuh2*lRpTomuh2 + 2.0*luomz2*lmuhomz2-lmuhomz2*lmuhomz2-3.0*lmuhomz2-luomz2*luomz2-2.0*log(_R)*log(_R)-2.0*M_PI*M_PI/3.0-1.5) + _qcd._Nc*( gsl_sf_dilog(mz2t)-gsl_sf_dilog(_mB2/_shat) - lmuhomz2*log(_uhat*_mB2/(_shat*_that))-0.5*lmuhomz2*lmuhomz2-0.5*(lsomz2+ltomz2)*(lsomz2+ltomz2)+lsomz2*ltomz2-lsomz2*log(_that/(_mB2-_shat)) -0.5*lsomz2*lsomz2+0.5*lmz2t*lmz2t+0.5*luomz2*luomz2+0.5*M_PI*M_PI ) )/M_PI;
}
/*

double BosonJetCSS::H1qg(double muh){
  double lmuhomz2=log(muh*muh/_mB2), lRpTomuh2=_R*_pT/muh,mz2t=_mB2/(_mB2-_that),mz2u=_mB2/(_mB2-_uhat);
  double lsomz2=log(_shat/_mB2),ltomz2=log(-_that/_mB2),luomz2=log(-_uhat/_mB2),lmz2t=log(mz2t),lmz2u=log(mz2u);
  lRpTomuh2=2.0*log(lRpTomuh2);
  return 0.5*_qcd.alphas(muh)*( _qcd._CF*( -1.5*lRpTomuh2 +0.5*lRpTomuh2*lRpTomuh2 + 2.0*luomz2*lmuhomz2-lmuhomz2*lmuhomz2-3.0*lmuhomz2-luomz2*luomz2-2.0*log(_R)*log(_R)-2.0*M_PI*M_PI/3.0-1.5) + _qcd._Nc*( gsl_sf_dilog(mz2t)-gsl_sf_dilog(_mB2/_shat) - lmuhomz2*log(_uhat*_mB2/(_shat*_that))-0.5*lmuhomz2*lmuhomz2-0.5*(lsomz2+ltomz2)*(lsomz2+ltomz2)+lsomz2*ltomz2+lsomz2*log(_shat-_mB2) -0.5*lsomz2*lsomz2+0.5*lmz2t*lmz2t+0.5*luomz2*luomz2+0.5*M_PI*M_PI ) )/M_PI;
}
*/

double BosonJetCSS::aHqgCSS(){
  return -2.0*(_qcd._Nc+_qcd._CF)/M_PI;
}

double BosonJetCSS::bHqgCSS(double muh){
  return (_qcd._CF*(2.0*log(-_uhat/(_pT*muh*_R))-1.5)+_qcd._Nc*log(_shat*_that/(_uhat*muh*muh))-0.5*_qcd._beta0)/M_PI;
}

double BosonJetCSS::aHqqbCSS(){
  return _aHqqb+_aJqqb;
}

double BosonJetCSS::bHqqbCSS(double muh){
  //cout << "s=" << _shat << endl;
  return ( _qcd._CF*(2.0*log(_shat/(muh*muh))-3.0)-2.0*_qcd._Nc*log(_R) )/M_PI;
}

double BosonJetCSS::aSqgCSS(){
  return _asbbqg+_acoftqg;
}

double BosonJetCSS::bSqgCSS(double muxT){
  return (_qcd._CF*(1.5-2.0*log(-_uhat/(_pT*muxT*_R)))+2.0*_qcd._Nc*log(-_pT*muxT/_that)+0.5*_qcd._beta0)/M_PI;
}

double BosonJetCSS::CHqgCSS(double mu, double muh){
  return rge(mu,muh,aHqgCSS(),bHqgCSS(muh));
}

double BosonJetCSS::CHqqbCSS(double mu, double muh){
  return rge(mu,muh,aHqqbCSS(),bHqqbCSS(muh));
}

double BosonJetCSS::CSqgCSS(double mu, double muxT){
  return rge(mu,muxT,aSqgCSS(),bSqgCSS(muxT));
}



double BosonJetCSS::sigmaqgCSS(double xT, double pT, double yB, double yJ){
  /*
    dsigma/qTdqTdpTdyBdyJ in pb/GeV for qg->ZJ+qbg->ZJ.
  */

  setKinematics(pT,yB,yJ);double res=0.0;
  if(kinematicsQ()){
    double muT=muxTCSS(xT),muh=muhCSS();
    res=0.5*xT*NonPert(xT,muh)*gsl_sf_bessel_J0(_qT*xT)*CHqgCSS(muT,muh)*(1.0+H1qg(muh))*sigmaqgLO(muh,muT)/M_PI;
  }
  return res;
}

double BosonJetCSS::sigmaqqbCSS(double xT, double pT, double yB, double yJ){
  /*
    dsigma/qTdqTdpTdyBdyJ in pb/GeV for qqb and qbq->ZJ+qbg->ZJ.
  */

  setKinematics(pT,yB,yJ);double res=0.0;
  if(kinematicsQ()){
    double muT=muxTCSS(xT),muh=muhCSS();
    res=xT*NonPert(xT,muh)*gsl_sf_bessel_J0(_qT*xT)*CHqqbCSS(muT,muh)*(1.0+H1qqb(muh))*sigmaqqbLO(muh,muT);
  }
  return res;
}

double BosonJetCSS::sigmaCSS(double xT, double pT, double yB, double yJ){
  /*
    dsigma/qTdqTdpTdyBdyJ in pb/GeV for qqb and qbq->ZJ+qbg->ZJ.
  */

  setKinematics(pT,yB,yJ);double res=0.0;
  if(kinematicsQ()){
    double muT=muxTCSS(xT),muh=muhCSS();
    res=xT*NonPert(xT,muh)*gsl_sf_bessel_J0(_qT*xT)*((1.0+H1qqb(muh))*CHqqbCSS(muT,muh)*sigmaqqbLO(muh,muT)+2.0*(1.0+H1qg(muh))*CHqgCSS(muT,muh)*sigmaqgLO(muh,muT));
  }
  return res;
}

double BosonJetCSS::RGInvariance(double mu, double muxT, double muh){
  return aHqgCSS()*log(mu/muh)+bHqgCSS(muh)+aSqgCSS()*log(mu/muxT)+bSqgCSS(muxT);
}

//filename

void BosonJetCSS::getFilename(stringstream &filename, double ymin, double ymax){
  filename << "R" << _R << "pT" << ymin << "." << ymax;
  filename << "CSS.dat";

}
