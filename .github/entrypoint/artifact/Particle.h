#include <string>

using namespace std;

class Particle{
 private:
  
  string _name;//particle name
  double _m;//particle mass
  double _e;//electric charge in the unit of the elementary charge e
  int _id;//particle id according to PDF particle codes
  
  
 public:

  enum _type {d=1,u=2,s=3,c=4,b=5,t=6,g=21,photon=22,Z0=23,Wp=24};

  Particle();
  Particle(string name, int id, double m,double e);
  //~Particle(){};
  void setParticle(string name, int id, double m,double e);
  double m();
  int id();
  double e();
  string name();
};
