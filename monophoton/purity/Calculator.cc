#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TDirectory.h"
#include "TLorentzVector.h"
#include "TROOT.h"
#include "TEntryListArray.h"
#include "TEfficiency.h"

#include "TreeEntries_simpletree.h"

class Calculator {
public:
  Calculator() {}
  void calculate(TTree* _input);
  double* getEfficiency(unsigned iEff);

  void setMinPhoPt(float minPhoPt) { minPhoPt_ = minPhoPt; }
  void setMaxPhoPt(float maxPhoPt) { maxPhoPt_ = maxPhoPt; }
  void setMinMet(float minMet) { minMet_ = minMet; }
  void setMaxMet(float maxMet) { maxMet_ = maxMet; }
  void setMinEta(float minEta) { minEta_ = minEta; }
  void setMaxEta(float maxEta) { maxEta_ = maxEta; }
  
  void setMaxDR(float maxDR) { maxDR_ = maxDR; }
  void setMaxDPt(float maxDPt) { maxDPt_ = maxDPt; }

  void setWorkingPoint(unsigned wp) { wp_ = wp; }

private:
  float minPhoPt_{175.};
  float maxPhoPt_{6500.};
  float minMet_{0.};
  float maxMet_{60.};
  float minEta_{0.};
  float maxEta_{1.5};
  
  float maxDR_{0.2};
  float maxDPt_{0.2};

  unsigned wp_{1};
  
  const static unsigned nSteps{7};
  double efficiencies[nSteps+1][3];
  double temp [3] = {-1., 0., 0.};
  
};

double*
Calculator::getEfficiency(unsigned iEff){
  if (iEff > nSteps) {
    return temp;
  }
  else
    return efficiencies[iEff];
}


void 
Calculator::calculate(TTree* _input) {
  
  simpletree::Event event;
  event.setStatus(*_input, false, {"*"});
  event.setAddress(*_input, {"run", "lumi", "event", "weight", "npv", "npvTrue", "promptFinalStates", "photons", "t1Met"});
  float minGenPt_ = minPhoPt_ / ( 1 + maxDPt_ );
  float maxGenPt_ = maxPhoPt_ / ( 1 - maxDPt_ );
  float minGenEta_ = minEta_ - maxDR_;
  float maxGenEta_ = maxEta_ + maxDR_;

  printf("%.0f < gen pt  < %.0f \n", minGenPt_, maxGenPt_);
  printf("%.2f < gen eta < %.2f \n", minGenEta_, maxGenEta_);

  unsigned iReco(0);
  double nGenPhotons(0.);
  double nMatchedPhotons(0.);
  double nRecoPhotons[nSteps];
  for (; iReco != nSteps; iReco++)
    nRecoPhotons[iReco] = 0.;

  long iEntry(0);
  while (_input->GetEntry(iEntry++) > 0) {
    if (iEntry % 100000 == 1)
      std::cout << " " << iEntry << std::endl;
    
    if (event.t1Met.met > maxMet_ || event.t1Met.met < minMet_)
      continue;

    // printf("met: %.0f \n", event.t1Met.met);

    auto& promptFinalStates(event.promptFinalStates);

    // std::cout << "PromptFinalStates " << event.promptFinalStates.size() << std::endl;
    
    auto& photons(event.photons);

    for (unsigned iPFS(0); iPFS != promptFinalStates.size(); ++iPFS) {
      auto& pfs(promptFinalStates[iPFS]);
      
      if (std::abs(pfs.pid) != 22)
	continue;

      // printf("got a gen photon w/pt %.2f \n", pfs.pt);
      
      // if ( pfs.pt < minPhoPt_ || pfs.pt > maxPhoPt_ )
      if ( pfs.pt < minGenPt_ || pfs.pt > maxGenPt_ )
	continue;

      // printf("it's in the pt range \n");

      if ( std::abs(pfs.eta) < minGenEta_ || std::abs(pfs.eta) > maxGenEta_ )
	continue;

      // printf("it's in the eta range \n");

      nGenPhotons++;
      
      for (unsigned iPho(0); iPho != photons.size(); ++iPho) {
	auto& pho(photons[iPho]);
	
	if ( pho.pt > maxPhoPt_ || pho.pt < minPhoPt_ )
	  continue;

	if ( std::abs(pho.eta) > maxEta_ || std::abs(pho.eta) < minEta_ )
	  continue;
	
	if (pfs.dR2(pho) > maxDR_ * maxDR_)
	  continue;
	
	if ( std::abs(pfs.pt - pho.pt) / pfs.pt  > maxDPt_)
	  continue;
	
	nMatchedPhotons++;

	// if ( !(pho.passHOverE(wp_) && pho.passSieie(wp_) && pho.passCHIso(wp_) && pho.passNHIso(wp_) && pho.passPhIso(wp_)))
	//  continue;

	if ( !pho.passHOverE(wp_))
	  continue;

	iReco = 0;
	nRecoPhotons[iReco]++;

	if ( !pho.passSieie(wp_))
	  continue;

	iReco++;
	nRecoPhotons[iReco]++;

	if ( !pho.passNHIso(wp_))
	  continue;

	iReco++;
	nRecoPhotons[iReco]++;

	if ( !pho.passPhIso(wp_))
	  continue;

	iReco++;
	nRecoPhotons[iReco]++;

	if ( !pho.passCHIso(wp_))
	  continue;

	iReco++;
	nRecoPhotons[iReco]++;

	if ( !pho.pixelVeto )
	  continue;

	iReco++;
	nRecoPhotons[iReco]++;

	if ( !( std::abs(pho.time) < 3. && pho.mipEnergy < 4.9 && pho.sieie > 0.001 && pho.sipip > 0.001 && !(pho.eta > 0. && pho.eta < 0.15 && pho.phi > 0.527580 && pho.phi < 0.541795) && pho.chWorstIso < simpletree::Photon::chIsoCuts[0][wp_] ) )
	  continue;

	iReco++;
	nRecoPhotons[iReco]++;
      }
    }
  }

  printf("nGenPhotons: %f \n", nGenPhotons);
  printf("nMatchedPhotons: %f \n", nMatchedPhotons);
  
  efficiencies[0][0] = nMatchedPhotons / nGenPhotons;
  double upper = TEfficiency::ClopperPearson( nGenPhotons, nMatchedPhotons, 0.6827, true);
  double lower = TEfficiency::ClopperPearson( nGenPhotons, nMatchedPhotons, 0.6827, false);
  efficiencies[0][1] = upper - efficiencies[0][0];
  efficiencies[0][2] = efficiencies[0][0] - lower;

  for (iReco = 0; iReco != nSteps; ++iReco) {
    printf("nRecoPhotons[%d]: %f \n", iReco, nRecoPhotons[iReco]);
    efficiencies[iReco+1][0] = nRecoPhotons[iReco] / nMatchedPhotons;
    upper = TEfficiency::ClopperPearson( nMatchedPhotons, nRecoPhotons[iReco], 0.6827, true);
    lower = TEfficiency::ClopperPearson( nMatchedPhotons, nRecoPhotons[iReco], 0.6827, false);
    efficiencies[iReco+1][1] = upper - efficiencies[iReco+1][0];
    efficiencies[iReco+1][2] = efficiencies[iReco+1][0] - lower;
  }
}