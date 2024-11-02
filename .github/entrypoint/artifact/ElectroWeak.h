
class ElectroWeak{
 private:
  
  double _mZ;//Z boson mass in GeV
  double _mW;//W boson mass in GeV
  double _GF;//G_F in GeV^{-2}

  double _cw2;//cos(theta_W)^2
  double _sw2;//sin(theta_W)^2
  double _alpha;//elecromagnetic alpha

 public:
  ElectroWeak();
  //ElectroWeak~();
  double cw2(){return _cw2;}
  double sw2(){return _sw2;}
  double alpha(){return _alpha;}
};

