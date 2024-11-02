#include "BosonJetNLL.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;

double sigma(double y[], size_t dim, void *p){
  //dim=5 dimensional integration variables: y[]={xT, phi, pT, yB,yJ, qT};
   BosonJetNLL *bj=(BosonJetNLL *)p;
   double cphix=cos(y[1]);
   bj->setqT(y[5]);
   return y[5]*(bj->sigmaR(y[0],cphix,y[2],y[3],y[4]));
}

int main(){
  
  //Particle photon("photon",Particle::photon,0.0,0.0);
  Particle Z0("Z0",Particle::Z0,91.1876,0.0);
  //BosonJet gammaJ(1.3e4,&photon);
  BosonJetNLL ZJ(1.3e4,&Z0);

  double R=0.1;ZJ.setR(R);

  //range of the integration: from ymin to ymax
  double pT=200.0;
  double ymin[]={0.0,-0.5*M_PI,pT,-10.0,-2.4,0.0};
  double ymax[]={1.5,0.5*M_PI,6500.0,10.0,2.4,pT};

  int dim=6;
  size_t calls = 500000;
  ZJ.setupMC( &sigma, dim, ymin,ymax, &ZJ);
  ZJ.setCalls(calls);
  //output file:

  ZJ.setImgcphix(true);
  ZJ.setCSS(false);
  ZJ.setNGL(true);
  ZJ.setLL(false);
  ZJ.setNonPert(false);
  ZJ.setScaleVar(1.0,1.0,1.0,1.0);

  double res[2];
  double Rls[]={0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0};

  for(int i=0;i<10;i++){
    ZJ.setR(Rls[i]);ZJ.calculate(res);
    cout << Rls[i] << "   " << res[0] << "   " << res[1] << endl;
  }
  ZJ.cleanupMC();

  return 0;
}
