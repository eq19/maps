#include "QCD.h"
#include <fstream>

using namespace std;

int main(){
  QCD qcd;
  /*
  for(double Q=0.1;Q<100;Q+=0.1)
    cout << Q << "   " << qcd.alphas(Q) << "  " << qcd.pdf(21, 0.1,Q) << endl;
  */
  double Q = 
  
  for(double x=0.001;x<1.0;x+=0.001){
    cout << x << "   " << qcd.pdf(1,x,3.3) << endl; 
  }
  
  return 0;
}
