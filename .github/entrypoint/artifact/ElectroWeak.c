#include "ElectroWeak.h"
#include <cmath>
#define PI 3.141592653589793


/*ElectroWeak::ElectroWeak(){
  //Here, all the values are taken from PDG 2018
  _GF=1.1663787e-5;//in GeV^{-2}
  _mZ=91.1876;//in GeV
  _mW=80.379;//in GeV

  //gmu scheme shall be used by taking the above three parameters as an input
  _cw2=_mW/_mZ; _cw2*=_cw2;_sw2=1.0-_cw2;_alpha=_mW*_mW*sqrt(2.0)*_GF*_sw2/PI;
}
*/


ElectroWeak::ElectroWeak(){
  //Here, all the values are taken from PDG 2018
  //_GF=1.1663787e-5;//in GeV^{-2}
  _mZ=91.1876;//in GeV
  _mW=80.398;//in GeV

  //gmu scheme shall be used by taking the above three parameters as an input
  _sw2=0.22264585;_cw2=1-_sw2;_alpha=1.0/132.33843228;
}

