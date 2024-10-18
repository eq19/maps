
#include "BosonJetResum.h"

class BosonJetNLL: public BosonJetResum{

protected:
  bool _css,_imgcphix,_ngl;
  double _cNGL,_angl,_bngl,_cngl;
  double _muhV,_muxTV,_muJV,_mutV;

  
public:
  
  BosonJetNLL();
  BosonJetNLL(double Ecm, Particle *boson);

  double _mutMin;

  void initNLL();
  void setScales(double xT);//var is a prefactor for the scale variation
  void setScaleVar(double vh, double vb, double vJ, double vt);
  
  double CHqg();//nll resummed for hard function in qg
  double CJqg();//nll resummed for Jet function in qg
  double Ccoftqg();//nll resummed for Jet function in qg
  double Csbbqg();//nll resummed for SBB in qg
  double CHqqb();//nll resummed for hard function: Hqqb
  double CJqqb();//nll resummed for Jet function in qqb
  double Ccoftqqb();//nll resummed for Jet function in qqb
  double Csbbqqb();//nll resummed for SBB: Hqqb

  //R resummation
  double Ccphixqg();
  double Ccphixqqb();
  double sigmaqgR(double xT, double cphix, double pT, double yB, double yJ);
  double sigmaqqbR(double xT,double cphix, double pT, double yB, double yJ);
  double sigmaR(double xT,double cphix, double pT, double yB, double yJ);

  //NGL resummation
  double NGL();

  
  void getFilename(stringstream &filename, double ymin, double ymax);
 
  //check css limit
  void setCSS(bool cssQ);
  void setImgcphix(bool icphix);

  //switch on and off NGL
  void setNGL(bool nglQ);

  //print _mut min
  double mutMin();
};

