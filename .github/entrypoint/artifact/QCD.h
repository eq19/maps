#include "Particle.h"
#include "LHAPDF/LHAPDF.h"

using namespace LHAPDF;

/*namespace colorfactor{
  double _Nc=3.0; 
  double _CF=4.0/3.0;
}
*/

class QCD{
 private:
  const PDF* _pdf;
  unsigned int _nf;//flavors of quarks, 5 by default

 public:

  double _Nc, _CF;//number of colors
  //const static double _Nc=3.0, _CF=4.0/3.0;//number of colors
  double _beta0, _beta1, _gcusp0, _gcusp1;//_gcusp=gamma^cusp
  Particle *_partons;
  QCD();
  QCD(unsigned int);
  ~QCD();
  void init();

  double pdf(int,double x,double Q);//PDF as a function  of flavor, x and Q
  double alphas(double Q);//the strong coupling alpha_s as a function of Q

  double Pqg(double z);
  double Pqg(double z, double x, double Q);
  double Pgq(double z);
  double Pgq(double z, double x, double Q);
  double Pgqb(double z, double x, double Q);
  double Pgg(double z, double x, double Q);
  double Pqq(int flavor, double z, double x, double Q);
  
};
