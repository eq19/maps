#include "BosonJetNLL.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

//#define NLL_DEBUG

using namespace std;

double dsigmadqT(double y[], size_t dim, void *p){
  //dim=5 dimensional integration variables: y[]={xT, phi, pT, yB,yJ};
   BosonJetNLL *bj=(BosonJetNLL *)p;
   double cphix=cos(y[1]);
   return bj->sigmaR(y[0],cphix,y[2],y[3],y[4]);
}

int main(){
  
  //Particle photon("photon",Particle::photon,0.0,0.0);
  Particle Z0("Z0",Particle::Z0,91.1876,0.0);
  //BosonJet gammaJ(1.3e4,&photon);
  BosonJetNLL ZJ(1.3e4,&Z0);

  double R=0.4;ZJ.setR(R);

  #ifdef NLL_DEBUG
  double pT=100.0,yB=0.1,yJ=0.2,muh=100.0,mu=30.0,muJ=10.0, mut=5.0, muxT=70.0, xT=1.2,qT=1.0,cphix=0.4;ZJ.setqT(qT);
  ZJ.setKinematics(pT,yB,yJ);ZJ.getKinematics();
  ZJ.setScale(mu,muh,muJ,muxT,mut,xT,cphix);
  cout << ZJ.aHqqb()<< ", " << ZJ.bHqqb() << endl;
  ZJ.setLL(true);
  cout << ZJ.RGInvariance(mu,muh,muxT,muJ,mut,xT,cphix) << endl;
  /*
  cout << M_PI*ZJ.sigmaqgR(xT, cphix, pT, yB, yJ) <<endl;
  cout << M_PI*ZJ.sigmaqgR(xT, 0.2*cphix, pT, yB, yJ) <<endl;  
  cout << M_PI*ZJ.sigmaqqbR(xT, cphix, pT, yB, yJ) <<endl;
  cout << M_PI*ZJ.sigmaqqbR(xT, 0.2*cphix, pT, yB, yJ) <<endl; 
  */ 
  #else
  //range of the integration: from ymin to ymax
  double ymin[]={0.0,-0.5*M_PI,200.0,-10.0,-2.4};
  double ymax[]={1.5,0.5*M_PI,6500.0,10.0,2.4};

  int dim=5;
  size_t calls = 50000;
  ZJ.setupMC( &dsigmadqT, dim, ymin,ymax, &ZJ);
  ZJ.setCalls(calls);
  //output file:

  ZJ.setImgcphix(true);
  ZJ.setCSS(false);
  ZJ.setNGL(false);
  ZJ.setLL(false);
  ZJ.setNonPert(false);
  ZJ.setScaleVar(1.0,1.0,1.0,1.0);
  stringstream filename;
  ZJ.getFilename(filename, ymin[2],ymax[2]);
  cout << filename.str() << endl;
  ofstream f(filename.str(), ofstream::out | ofstream::app);
  
  int nBins=41;
  double qT[]=/*{1., 1.1273, 1.27082, 1.4326, 1.61497, 1.82056, 2.05233, 2.3136,
	       2.60813, 2.94016, 3.31445, 3.7364, 4.21206, 4.74827, 5.35275,
	       6.03418, 6.80235, 7.66832, 8.64453, 9.74502, 10.9856, 12.3841,
	       13.9607, 15.7379, 17.7414, 20., 22.5461, 25.4163, 28.6519, 32.2994,
	       36.4113, 41.0466, 46.272, 52.1626, 58.8032, 66.2891, 74.728, 84.2412,
	       94.9654, 107.055, 120.684, 136.047, 153.366, 172.891, 194.9, 219.712,
	       247.682, 279.213, 314.759, 354.829, 400.};\\51
*/
   {1., 1.14163, 1.30332, 1.48791, 1.69865, 1.93923, 2.21388, 2.52744,
	       2.8854, 3.29406, 3.7606, 4.29322, 4.90127, 5.59545, 6.38794, 7.29266, 
	       8.32553, 9.50469, 10.8508, 12.3877, 14.1421, 16.1451, 18.4317, 
	       21.0423, 24.0225, 27.4248, 31.309, 35.7433, 40.8057, 46.5851, 53.183, 
	       60.7153, 69.3145, 79.1316, 90.339, 103.134, 117.741, 134.417, 
	       153.454, 175.188, 200.};//41
  /*
  {1., 1.25893, 1.58489, 1.99526, 2.51189, 3.16228, 3.98107, 5.01187,
	       6.30957, 7.94328, 10., 12.5893, 15.8489, 19.9526, 25.1189, 31.6228,
	       39.8107, 50.1187, 63.0957, 79.4328, 100.};//21
*/
  /*{1., 3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25., 27.,
     29., 31., 33., 35., 37., 39., 41., 43., 45., 47., 49., 51., 53., 55., 
     57., 59., 61., 63., 65., 67., 69., 71., 73., 75., 77., 79., 81., 83.,
     85., 87., 89., 91., 93.};*/
  //for(int i=0;i<nBins;i++) qT[i]=1.0+1.0*i;
  for(int i=0;i<nBins;i++){
    ZJ.setqT(qT[i]);ZJ._mutMin=10.0;
    ZJ.calculate(qT[i],f);
    cout << "mut Min= " << ZJ._mutMin << endl;
    //cout << (0.5772156649015329+log(0.5*qT[i]))/(M_PI*qT[i]*qT[i]) << endl;
  }
  
  f << "\n\n";
  f.close();

  ZJ.cleanupMC();
  #endif
  return 0;
}
