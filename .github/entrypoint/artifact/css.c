#include "BosonJetCSS.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;


double dsigmadqT(double y[], size_t dim, void *p){
  //dim=5 dimensional integration variables: y[]={xT, pT, yB,yJ};
   BosonJetCSS *bj=(BosonJetCSS *)p;
   return bj->sigmaCSS(y[0],y[1],y[2],y[3]);
}


int main(){
  
  //Particle photon("photon",Particle::photon,0.0,0.0);
  Particle Z0("Z0",Particle::Z0,91.1876,0.0);
  //BosonJet gammaJ(1.3e4,&photon);
  BosonJetCSS ZJ(1.3e4,&Z0);

  double R=0.2;ZJ.setR(R);

  /*
  double pT=30.0,yB=0.1,yJ=0.2,muh=100.0,mu=10.0,muJ=10.0,xT=0.2,qT=1.0;ZJ.setqT(qT);
  ZJ.setKinematics(pT,yB,yJ);ZJ.getKinematics();
  ZJ.setScale(mu,muJ,muh);
  cout << setprecision(15) << ZJ. RGInvariance(0.1,0.2,0.3,0.4,0.5,0.6,0.7) << endl;
  cout << setprecision(15) << ZJ. RGInvariance(1.1,3.2,5.3,9.4,1.5,0.6,0.7) << endl;

  */  
  //range of the integration: from ymin to ymax
  double ymin[]={0.0,200.0,-10.0,-2.4};
  double ymax[]={3.0,6500.0,10.0,2.4};

  int dim=4;
  size_t calls = 50000;
  ZJ.setupMC( &dsigmadqT, dim, ymin,ymax, &ZJ);
  ZJ.setCalls(calls);
  //output file:

  stringstream filename;
  ZJ.getFilename(filename, ymin[1],ymax[1]);
  cout << filename.str() << endl;
  ofstream f(filename.str(), ofstream::out | ofstream::app);
  
  
  double qT[]={1., 1.1273, 1.27082, 1.4326, 1.61497, 1.82056, 2.05233, 2.3136,
	       2.60813, 2.94016, 3.31445, 3.7364, 4.21206, 4.74827, 5.35275,
	       6.03418, 6.80235, 7.66832, 8.64453, 9.74502, 10.9856, 12.3841,
	       13.9607, 15.7379, 17.7414, 20., 22.5461, 25.4163, 28.6519, 32.2994,
	       36.4113, 41.0466, 46.272, 52.1626, 58.8032, 66.2891, 74.728, 84.2412,
	       94.9654, 107.055, 120.684, 136.047, 153.366, 172.891, 194.9, 219.712,
	       247.682, 279.213, 314.759, 354.829, 400.};
  /*{1., 1.25893, 1.58489, 1.99526, 2.51189, 3.16228, 3.98107, 5.01187,
	       6.30957, 7.94328, 10., 12.5893, 15.8489, 19.9526, 25.1189, 31.6228,
	       39.8107, 50.1187, 63.0957, 79.4328, 100.};*/
  for(int i=0;i<51;i++){
    ZJ.setqT(qT[i]);
    ZJ.calculate(qT[i],f);
    //cout << (0.5772156649015329+log(0.5*qT[i]))/(M_PI*qT[i]*qT[i]) << endl;
  }
  
  f << "\n\n";
  f.close();

  ZJ.cleanupMC();
  
  return 0;
}
