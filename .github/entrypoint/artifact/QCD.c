#include <string>
#include "QCD.h"
#include <gsl/gsl_math.h>

using namespace std;

QCD::QCD(unsigned int nf){
  /*Here, one needs to download the pdfset from
    https://lhapdf.hepforge.org/pdfsets.html
    and put it into the folder which can be found out by lhapdf-config --datadir.
  */
  _nf=nf;
  init();
}

QCD::QCD(){
  /*Here, one needs to download the pdfset from 
    https://lhapdf.hepforge.org/pdfsets.html
    and put it into the folder which can be found out by lhapdf-config --datadir.
   */
  _nf=5;
  init();
}

void QCD::init(){
  const int imem = 0;
  _Nc=3.0;_CF=4.0/3.0;
  _beta0=11.0*_Nc/3.0 - 2.0*_nf/3.0;
  _beta1=34.0*_Nc*_Nc/3.0-10.0*_Nc*_nf/3.0-2.0*_CF*_nf;
  _gcusp0=4.0;_gcusp1=(268.0/9.0-4.0*M_PI*M_PI/3.0)*_Nc-40.0*_nf/9.0;
  _pdf = mkPDF("CT14nlo", imem);
  _partons=new Particle[7];
  _partons[0].setParticle("g",21, 0.0, 0.0);
  _partons[1].setParticle("d",1, 0.0, -1.0/3.0);
  _partons[2].setParticle("u",2, 0.0, 2.0/3.0);
  _partons[3].setParticle("s",3, 0.0, -1.0/3.0);
  _partons[4].setParticle("c",4, 0.0, 2.0/3.0);
  _partons[5].setParticle("b",5, 0.0, -1.0/3.0);
  _partons[6].setParticle("t",6,173.0, 2.0/3.0);

}

QCD::~QCD(){
  delete _pdf;
  delete [] _partons;
}

double QCD::pdf(int f,double x,double Q){
  return _pdf->xfxQ(f,x,Q)/x; 
}

double QCD::alphas(double Q){
  return _pdf->alphasQ(Q);
}

double QCD::Pqg(double z){
  double res=0.0;
  if(z>0&&z<=1.0)
    res=z*z-z+0.5;
  return res;
}

double QCD::Pqg(double z,double x, double Q){
  double res=0.0;
  if(z<1.0&&z>x)
    res=Pqg(z)*pdf(21,x/z,Q)/z;
  return res;
}

double QCD::Pgq(double z){
  double res=0.0;
  if(z>0&&z<1.0)
    res=_CF*(z-2.0+2.0/z);
  return res;
} 

double QCD::Pgq(double z,double x, double Q){
  double res=0.0;
  if(z<1.0&&z>x){
    for(unsigned int i=1;i<=_nf;i++){
      res+=pdf(i,x/z,Q);
    }
    res*=Pgq(z)/z;       
  }          
  return res;
}

double QCD::Pgqb(double z,double x, double Q){
  double res=0.0;
  if(z<1.0&&z>x){
    for(unsigned int i=1;i<=_nf;i++){
      res+=pdf(-i,x/z,Q);
    }
    res*=Pgq(z)/z;       
  }          
  return res;
}

double QCD::Pqq(int flavor, double z,double x, double Q){
  double res=0.0;
  if(z<1.0&&z>0.0){
    double qsumx=pdf(flavor,x,Q);
    res=1.5*qsumx;//Here, we have to make sure the range for z integration is from 0 to 1
    double qsum=0.0;
    if(z>x) qsum=pdf(flavor,x/z,Q);
    res+=((1.0+z*z)*qsum/z-2.0*qsumx)/((1.0-z));
    res*=_CF;
  }
  return res;
}

double QCD::Pgg(double z, double x, double Q){
  double res=0.0;
  if(z<1.0&&z>0.0){
    res=(11.0*_Nc/6.0-_nf/3.0)*pdf(21,x,Q);//Here, we have to make sure the range for z integration is from 0 to 1
    if(z>x)
      res+=2.0*_Nc*( ( z*z-z+1.0 )*(z*z-z+1.0)*pdf(21,x/z,Q)/(z*z) - pdf(21,x,Q) )/(1.0-z);
    else
      res+=-2.0*_Nc*pdf(21,x,Q)/(1.0-z);
  }
  return res;
}
