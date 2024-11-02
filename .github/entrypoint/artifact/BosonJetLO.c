#include "BosonJetLO.h"

#define PI 3.141592653589793

BosonJetLO::BosonJetLO(double Ecm, Particle *boson):BosonJet(Ecm, boson){
}


double BosonJetLO::nllqg(double qT, double pT, double yB, double yJ, double R, double Q){
  /*
    Double log + non-PDF single log at O(alpha_s) for qg->BJ channel. It is the same for qbg->BJ.
    For gq->BJ and gqb->BJ, it is given by t<->u.
  */
  double xB[2],res;getxBs(xB, pT, yB, yJ);

  if(xB[0]>1.0||xB[1]>1.0||xB[0]<0.0||xB[1]<0.0) res=0.0;
  else{
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);

    res=-_qcd.alphas(Q)*(2.0*(_qcd._Nc*log(-pT*qT/t)+_qcd._CF*log(-pT*qT*R/u))+( 11.0*_qcd._Nc/6.0-_nf/3.0+3.0*_qcd._CF/2.0))/(PI);
  }
  //
  //res=-_qcd.alphas(Q)*2.0*(_qcd._Nc+_qcd._CF)*(log(0.5*qT)+0.5772156649015329)/(PI);
  return res;
}

double BosonJetLO::nllqq(double qT, double pT, double yB, double yJ, double R, double Q){
  /*
    Double log + non-PDF single log at O(alpha_s) for qqb->BJ channel. It is the same for qbq->BJ.
  */
  double xB[2],res;getxBs(xB, pT, yB, yJ);
  if(xB[0]>1.0||xB[1]>1.0||xB[0]<0.0||xB[1]<0.0) res=0.0;
  else{
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    res=-_qcd.alphas(Q)*(_qcd._CF*(3.0+2.0*log(-pT*qT/t)+2.0*log(-pT*qT/u))+2.0*_qcd._Nc*log(R))/(PI);
  }
  return res;
}

double BosonJetLO::sigmaqg(double qT, double pT, double yB, double yJ, double R, double Q){
  /*
    Non-PDF LL and NLL for qg+qbg channel.
   */
  return sigmaqgLO(pT,yB,yJ,Q)*nllqg(qT, pT,yB,yJ,R,Q);
}

double BosonJetLO::sigmaqg(double qT, double pT, double yB, double yJ, double z, double R, double Q){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for qg->ZJ+qbg->ZJ.
  */
  double res=0.0;
  double xB[2];getxBs(xB, pT, yB, yJ);
  if(xB[0]<1.0&&xB[1]<1.0&&xB[0]>0.0&&xB[1]>0.0&&z>0.0&&z<1.0){//z has to be in the whole range (0,1) in order to get the delta function in splitting function
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    
    double dg=0.0,dq=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      //qg->q'g->BJ+qbg->qb'g
      dq+=(_qcd.Pqq(i,z,xB[0],Q)+_qcd.Pqq(-i,z,xB[0],Q))*e2(_qcd._partons[i].e());
      //qg->qg'->BJ+qbg->qb'g->BJ
      dg+=(_qcd.pdf(i,xB[0],Q)+_qcd.pdf(-i,xB[0],Q))*e2(_qcd._partons[i].e());
      //That is all.
    }
    res=_qcd.alphas(Q)*((dg*_qcd.Pgg(z,xB[1],Q)+dq*_qcd.pdf(21,xB[1],Q))*Mgq2(s,u,t)+ dg*_qcd.Pqg(z,xB[1],Q)*Mqqb2(s,t,u))*M2toXsection(pT, xB[0], xB[1], Q)/PI;//prefactor alphas/PI
  }
  return res*invGeV2topb+sigmaqgLO(pT,yB,yJ,Q)*nllqg(qT, pT,yB,yJ,R,Q);
  //return sigmaqgLO(pT,yB,yJ,Q)*nllqg(qT, pT,yB,yJ,R,Q);
}

double BosonJetLO::sigmaqqb(double qT, double pT, double yB, double yJ, double R, double Q){
  /*
    Non-PDF LL and NLL for qqb+qbq channel.
   */
  return sigmaqqbLO(pT,yB,yJ,Q)*nllqq(qT, pT,yB,yJ,R,Q);
}

double BosonJetLO::sigmaqqb(double qT, double pT, double yB, double yJ, double z, double R, double Q){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for qqb->ZJ.
  */
  double res=0.0;
  double xB[2];getxBs(xB, pT, yB, yJ);
  //z has to be in the whole range (0,1) in order to get the delta function in splitting function
  if(xB[0]<1.0&&xB[1]<1.0&&xB[0]>0.0&&xB[1]>0.0&&z>0.0&&z<1.0){
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    
    double ds=0.0,dsqg=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      //qqb->qqb'->BJ with ' indicating undergoing splitting
      ds+=_qcd.pdf(i,xB[0],Q)*_qcd.Pqq(-i,z,xB[1],Q)*e2(_qcd._partons[i].e());
      //qqb->qg->BJ
      dsqg+=_qcd.pdf(i,xB[0],Q)*_qcd.Pgqb(z,xB[1],Q)*e2(_qcd._partons[i].e());
      //qbq->qbq'->BJ
      ds+=_qcd.pdf(-i,xB[0],Q)*_qcd.Pqq(i,z,xB[1],Q)*e2(_qcd._partons[i].e());
      //qbq->qbg->BJ
      dsqg+=_qcd.pdf(-i,xB[0],Q)*_qcd.Pgq(z,xB[1],Q)*e2(_qcd._partons[i].e());
      //qqb->q'qb->BJ, qqb->gqb->BJ,qbq->qb'q->BJ & qbq->gq->BJ is taken into account by a factor of 2.
    }
    res=2.0*_qcd.alphas(Q)*( ds*Mqqb2(s,t,u)+dsqg*Mgq2(s,u,t) )*M2toXsection(pT, xB[0], xB[1], Q)/PI;//prefactor: 2 alphas/(PI)
  }

  return res*invGeV2topb+sigmaqqbLO(pT,yB,yJ,Q)*nllqq(qT, pT,yB,yJ,R,Q);
}

double BosonJetLO::sigmagg(double qT, double pT, double yB, double yJ, double z, double Q){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for gg->ZJ.
  */
  double res=0.0;
  double xB[2];getxBs(xB, pT, yB, yJ);
  if(xB[0]>0.0&&xB[1]>0.0&&xB[0]<1.0&&xB[1]<1.0&&z<1.0&&z>xB[0]){
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    
    for(unsigned int i=1;i<=_nf;i++){
      //Conly gg->qg->BJ is calculated.
      //gg->qbg->BJ, gg->gq->BJ and gg->gqb is taken into account by a factor of 4.
      res+=e2(_qcd._partons[i].e());//g(p1) q(p2)->boson(pB) jet(pJ)
    }
    res*=4.0*_qcd.alphas(Q)*_qcd.Pqg(z,xB[0],Q)*_qcd.pdf(21,xB[1],Q)*Mgq2(s,u,t)*M2toXsection(pT, xB[0], xB[1], Q)/PI;//prefactor: 4*alphas/PI
  }
  return res*invGeV2topb;//return with unit pb
}


double BosonJetLO::sigmaqq(double qT, double pT, double yB, double yJ, double z, double Q){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for qq->ZJ.
  */
  double res=0.0;
  double xB[2];getxBs(xB, pT, yB, yJ);
  if(xB[0]>0.0&&xB[1]>0.0&&xB[0]<1.0&&xB[1]<1.0&&z<1.0&&z>xB[0]){
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    
    double dsqg=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      //Only qq->qg->ZJ is calculated.
      //qq->gq->ZJ is taken into account by a factor of 2.
      dsqg+=_qcd.pdf(i,xB[0],Q)*e2(_qcd._partons[i].e());
    }
    
    res=2.0*_qcd.alphas(Q)*dsqg*_qcd.Pgq(z,xB[1],Q)*Mgq2(s,u,t)*M2toXsection(pT, xB[0], xB[1], Q)/PI;//prefactor: 2*alphas/(PI)
    
  }
  return res*invGeV2topb;//return with unit pb
}

double BosonJetLO::sigmaqbqb(double qT, double pT, double yB, double yJ, double z, double Q){
  /*
    dsigma/dpTdyBdyJ in pb/GeV for qbqb->ZJ
  */
  double res=0.0;
  double xB[2];getxBs(xB, pT, yB, yJ);
  if(xB[0]>0.0&&xB[1]>0.0&&xB[0]<1.0&&xB[1]<1.0&&z<1.0&&z>xB[0]){
    double s,t,u;Mandelstam(xB[0], xB[1], pT, yB, s, t, u);
    double dsqg=0.0;
    for(unsigned int i=1;i<=_nf;i++){
      //Only qb qb->qb g->ZJ is calculated.
      //qbqb->gqb->ZJ is taken into account by a factor 2
      dsqg+=_qcd.pdf(-i,xB[0],Q)*e2(_qcd._partons[i].e());
    }
    
    res=2.0*_qcd.alphas(Q)*(dsqg*_qcd.Pgqb(z,xB[1],Q)*Mgq2(s,u,t))*M2toXsection(pT, xB[0], xB[1], Q)/PI;//prefactor: 2*alphas/PI
    
  }
  return res*invGeV2topb;//return with unit pb
}

double BosonJetLO::sigma(double qT, double pT, double yB, double yJ,double z, double R, double Q){
  return 2.0*sigmaqg(qT,pT,yB,yJ,z,R,Q)+sigmaqqb(qT,pT,yB,yJ,z,R,Q)+sigmaqq(qT,pT,yB,yJ,z,Q)+sigmaqbqb(qT,pT,yB,yJ,z,Q)+sigmagg(qT,pT,yB,yJ,z,Q);
}

//output

void BosonJetLO::getFilename(stringstream &filename, double R, int chan, double ymin, double ymax){
  filename << "R" << R << "pT" << ymin << "." << ymax;
  switch(chan){
  case 0:
    filename<< "tot";
    break;
  case 1:
    filename<< "qg";
    break;
  case 2:
    filename<< "qqb";
    break;
  case 3:
    filename<< "gg";
    break;
  case 4:
    filename<< "qq";
    break;
  case 5:
    filename<< "qbqb";
    break;
  }
  filename << "LO.dat";

}
