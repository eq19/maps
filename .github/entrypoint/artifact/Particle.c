#include <iostream>
#include "Particle.h"

Particle::Particle(){
  _m=0.0;_e=0.0;_name="UFO";_id=-273;
}

Particle::Particle(string name, int id, double m, double e){
  _name=name;_id=id;_m=m;_e=e;
}

void Particle::setParticle(string name, int id, double m, double e){
  _name=name;_id=id;_m=m;_e=e;
}


double Particle::m(){
  return _m;
}

int Particle::id(){return _id;}
double Particle::e(){return _e;}
string Particle::name(){return _name;}  

/*
int main(){
  Particle pl;
  return 0;
}
*/
