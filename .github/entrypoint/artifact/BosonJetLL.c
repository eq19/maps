#include <math.h>
#include "BosonJetLL.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_sf_dilog.h>

//#define SCREEN_ONLY

BosonJetLL::BosonJetLL():BosonJetNLL(){
  initLL();
}

BosonJetLL::BosonJetLL(double Ecm, Particle *boson):BosonJetNLL(Ecm, boson){
  initLL();
}

void BosonJetLL::initLL(){
  _ngl=false;
}

double BosonJetLL::bHqg(){
  cout << "We are here..." << endl;
  return -(_cf*(2.0*log(-_muh*_muh/_uhat))+_nc*log(_muh*_muh*_uhat/(_shat*_that)));
}

//filename

void BosonJetLL::getFilename(stringstream &filename, double ymin, double ymax){
  filename << "R" << _R << "pT" << ymin << "." << ymax << "LL";
  if(_css){
    filename << "CSS";
  }
  if(_nonpert){
    filename << "NP";
  }
  filename <<"muh" << _muhV << "mub" << _muxTV << "muJ" << _muJV << "mut" << _mutV;
  filename <<".dat";
}

