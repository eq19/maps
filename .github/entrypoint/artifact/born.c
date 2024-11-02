#include "BosonJetBorn.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;

double dsigmadqT(double y[], size_t dim, void *p){
  //dim=5 dimensional integration variables: y[]={yB,yJ};
   BosonJetBorn *bj=(BosonJetBorn*)p;
   bj->setKinematics(bj->getpT(),y[0],y[1]);
   return bj->sigmaLO(bj->getpT(),bj->getpT());
}


int main(){
  
  //Particle photon("photon",Particle::photon,0.0,0.0);
  Particle Z0("Z0",Particle::Z0,91.1876,0.0);
  //BosonJet gammaJ(1.3e4,&photon);
  BosonJetBorn ZJ(1.3e4,&Z0);

  //range of the integration: from ymin to ymax
  double ymin[]={-2.4,-2.4};
  double ymax[]={2.4,2.4};

  int dim=2;
  size_t calls = 50000;
  ZJ.setupMC( &dsigmadqT, dim, ymin,ymax, &ZJ);
  ZJ.setCalls(calls);
  //output file:

  stringstream filename;
  ZJ.getFilename(filename, ymax[1]);
  cout << filename.str() << endl;
  ofstream f(filename.str(), ofstream::out | ofstream::app);
    
  double pT[]={35.5, 50., 71., 100.5, 143., 194., 260., 350.};
  for(int i=0;i<21;i++){
    ZJ.setpT(pT[i]);
    ZJ.calculate(pT[i],f);
    //cout << (0.5772156649015329+log(0.5*qT[i]))/(M_PI*qT[i]*qT[i]) << endl;
  }
  
  f << "\n\n";
  f.close();

  ZJ.cleanupMC();

  return 0;
}
