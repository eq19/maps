#include "BosonJetLO.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <gsl/gsl_math.h>
#include <gsl/gsl_monte.h>
#include <gsl/gsl_monte_vegas.h>

//#define SCREEN_ONLY

using namespace std;

double dsigmadqT(double y[], size_t dim, void *p){
  //dim=5 dimensional integration variables: y[]={pT, yB,yJ,z};
  //parameter list p: BosonJet, qT, R, chan
  struct ParaQT *para=(struct ParaQT *)p;
  double res;
  switch(para->_chan){
  case 0:
    res=para->_bj->sigma(para->_qT, y[0],y[1],y[2],y[3],para->_R,y[0]);
    break;
  case 1:
    res=para->_bj->sigmaqg(para->_qT, y[0],y[1],y[2],y[3],para->_R,y[0]);
    break;
  case 2:
    res=para->_bj->sigmaqqb(para->_qT, y[0],y[1],y[2],y[3],para->_R,y[0]);
    break;
  case 3:
    res=para->_bj->sigmagg(para->_qT, y[0],y[1],y[2],y[3],y[0]);
    break;
  case 4:
    res=para->_bj->sigmaqq(para->_qT, y[0],y[1],y[2],y[3],y[0]);
    break;
  case 5:
    res=para->_bj->sigmaqbqb(para->_qT, y[0],y[1],y[2],y[3],y[0]);
    break;
  }
  return res;
}

int main(){
  
  //Particle photon("photon",Particle::photon,0.0,0.0);
  Particle Z0("Z0",Particle::Z0,91.1876,0.0);
  //BosonJet gammaJ(1.3e4,&photon);
  BosonJetLO ZJ(1.3e4,&Z0);
  //double qT=0.1, pT=500.0, yB=0.5, yJ=0.1,z=0.9999;
  //cout << ZJ.sigmaqqb(qT, pT, yB, yJ, z, 0.01, pT) << endl;

  //range of the integration: from ymin to ymax
  double ymin[]={30.0,-10.0,-2.4,0.0};
  double ymax[]={6500.0,10.0,2.4,1.0};

  //integration
  struct ParaQT para;
  para._bj=&ZJ; para._R=0.2;para._chan=0;
  
  int dim=4;
  size_t calls = 50000;
  ZJ.setupMC( &dsigmadqT, dim, ymin,ymax, &para);
  ZJ.setCalls(calls);
  //output file:

  stringstream filename;
  ZJ.getFilename(filename, para._R, para._chan, ymin[0], ymax[0]);
  cout << filename.str() << endl;
  ofstream f(filename.str(), ofstream::out | ofstream::app);

  double qT[]={1., 1.1273, 1.27082, 1.4326, 1.61497, 1.82056, 2.05233, 2.3136,
	       2.60813, 2.94016, 3.31445, 3.7364, 4.21206, 4.74827, 5.35275,
	       6.03418, 6.80235, 7.66832, 8.64453, 9.74502, 10.9856, 12.3841,
	       13.9607, 15.7379, 17.7414, 20., 22.5461, 25.4163, 28.6519, 32.2994,
	       36.4113, 41.0466, 46.272, 52.1626, 58.8032, 66.2891, 74.728, 84.2412,
	       94.9654, 107.055, 120.684, 136.047, 153.366, 172.891, 194.9, 219.712,
	       247.682, 279.213, 314.759, 354.829, 400.};/*{0.106101, 0.119047, 0.133573, 0.149872, 0.168159, 0.188677,
	       0.211699, 0.23753, 0.266513, 0.299033, 0.335521, 0.37646, 0.422395,
	       0.473935, 0.531764, 0.596649, 0.669452, 0.751137, 0.84279, 0.945625,
	       1.06101, 1.19047, 1.33573, 1.49872, 1.68159, 1.88677, 2.11699,
	       2.3753, 2.66513, 2.99033, 3.35521, 3.7646, 4.22395, 4.73935, 5.31764,
	       5.96649, 6.69452, 7.51137, 8.4279, 9.45625};
    {1., 1.25893, 1.58489, 1.99526, 2.51189, 3.16228, 3.98107, 5.01187,
     6.30957, 7.94328, 10., 12.5893, 15.8489, 19.9526, 25.1189, 31.6228,
     39.8107, 50.1187, 63.0957, 79.4328, 100.};*/
  for(int i=0;i<51;i++){
    para._qT=qT[i];
    if(para._chan>5){
      int chan=para._chan;
      double res[2];
      f << qT[i];
      for(para._chan=0;para._chan<=5;para._chan++){
	//cout << para._chan << endl;
	ZJ.calculate(qT[i],res);
	f << "   " << res[0] << "   " << res[1];
      }
      f << endl;
      para._chan=chan;
    }
    else{
      double res[2];
      f << qT[i];
      //cout << para._chan << endl;
      ZJ.calculate(qT[i],res);
      f << "   " << res[0]/qT[i] << "   " << res[1]/qT[i] << endl;//save as dsigma/dqT
    }
  }

  f << "\n\n";
  f.close();

  ZJ.cleanupMC();
  
  return 0;
}
