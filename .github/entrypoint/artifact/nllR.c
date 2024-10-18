#include "BosonJetResum.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;

struct ParaQT{BosonJetResum *_bj; int _chan;};

double dsigmadqT(double y[], size_t dim, void *p){
  //dim=5 dimensional integration variables: y[]={xT, phi, pT, yB,yJ};
   BosonJetResum *bj=(BosonJetResum *)p;
   double cphix=cos(y[1]);
   return bj->sigmaqqbR(y[0],cphix,y[2],y[3],y[4]);
}


int main(){
  
  //Particle photon("photon",Particle::photon,0.0,0.0);
  Particle Z0("Z0",Particle::Z0,91.1876,0.0);
  //BosonJet gammaJ(1.3e4,&photon);
  BosonJetResum ZJ(1.3e4,&Z0);

  double R=0.4;ZJ.setR(R);

  /*
  double pT=30.0,yB=0.1,yJ=0.2,muh=100.0,mu=10.0,muJ=10.0,xT=0.2,qT=1.0;ZJ.setqT(qT);
  ZJ.setKinematics(pT,yB,yJ);ZJ.getKinematics();
  ZJ.setScale(mu,muJ,muh);
  cout << setprecision(15) << ZJ. RGInvariance(0.1,0.2,0.3,0.4,0.5,0.6,0.7) << endl;
  cout << setprecision(15) << ZJ. RGInvariance(1.1,3.2,5.3,9.4,1.5,0.6,0.7) << endl;

  */  
  //range of the integration: from ymin to ymax
  double ymin[]={0.0,-0.5*M_PI,30.0,-10.0,-2.4};
  double ymax[]={3.0,0.5*M_PI,6500.0,10.0,2.4};

  int dim=5;
  size_t calls = 500000;
  ZJ.setupMC( &dsigmadqT, dim, ymin,ymax, &ZJ);
  ZJ.setCalls(calls);
  //output file:

  stringstream filename;
  ZJ.getFilename(filename, ymin[2],ymax[2]);
  cout << filename.str() << endl;
  ofstream f(filename.str(), ofstream::out | ofstream::app);
  
  
  double qT[]={1., 1.25893, 1.58489, 1.99526, 2.51189, 3.16228, 3.98107, 5.01187,
	       6.30957, 7.94328, 10., 12.5893, 15.8489, 19.9526, 25.1189, 31.6228,
	       39.8107, 50.1187, 63.0957, 79.4328, 100.};
  for(int i=0;i<21;i++){
    ZJ.setqT(qT[i]);
    ZJ.calculate(qT[i],f);
    //cout << (0.5772156649015329+log(0.5*qT[i]))/(M_PI*qT[i]*qT[i]) << endl;
  }
  
  f << "\n\n";
  f.close();

  ZJ.cleanupMC();
  
  return 0;
}
