#ifndef MITCROMBIE_MONOJET_MONOJETTREE_H
#define MITCROMBIE_MONOJET_MONOJETTREE_H

#include "TFile.h"
#include "TTree.h"

class MonoJetTree
{
public:
  MonoJetTree( const char *name );
  virtual ~MonoJetTree();

  int   runNum;
  int   lumiNum;
  int   eventNum;
  float jet1Pt;
  float jet1Eta;
  float jet1Phi;
  float jet1dRmet;
  int   n_jets;
  float lep1Pt;
  float lep1Eta;
  float lep1Phi;
  int   lep1PdgId;
  int   lep1IsTight;
  float lep2Pt;
  float lep2Eta;
  float lep2Phi;
  int   lep2PdgId;
  int   lep2IsTight;
  float dilep_pt;
  float dilep_eta;
  float dilep_phi;
  float dilep_m;
  float mt;
  int   n_tightlep;
  int   n_looselep;
  float photonPt;
  float photonEta;
  float photonPhi;
  int   photonIsTight;
  int   n_tightpho;
  int   n_loosepho;
  float met;
  float metPhi;
  float u_perpZ;
  float u_paraZ;
  float u_magZ;
  float u_phiZ;
  float u_perpW;
  float u_paraW;
  float u_magW;
  float u_phiW;
  float u_perpPho;
  float u_paraPho;
  float u_magPho;
  float u_phiPho;
  float mcWeight;
  std::vector<int>*   triggerFired;

  TTree  *ReturnTree()                { return t;                            }
  void    Fill()                      { t->Fill(); Reset();                  }
  void    WriteToFile( TFile *file )  { file->WriteTObject(t, t->GetName()); }

protected:

  TTree *t;
  void   Reset();

  ClassDef(MonoJetTree,1)
};
#endif
