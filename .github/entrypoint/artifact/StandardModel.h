/*
  This class is used for parameters in ElectroWeak theory
  Created on January 5 2019 by Bin Wu.
*/

class ElectroWeak{
 private:
  
  double _mZ;//Z boson mass
  double _mW;//W boson mass
  double _GF;//Fermi coupling constant G_F
  double _sw2;//sin(theta_W)^2
  double _cw2;//cos(theta_W)^2
  double _alpha;//electromagnetic coupling
  
 public:
  ElectroWeak();
  //~ElectroWeak();
};
