import sys
import os
import math

thisdir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(thisdir)
sys.path.append(basedir)

from main.plotutil import *

argv = list(sys.argv)
sys.argv = []
import ROOT
black = ROOT.kBlack # need to load something from ROOT to actually import
sys.argv = argv

photonData = ['sph-16b2-d', 'sph-16c2-d', 'sph-16d2-d'] # , 'sph-16b2s']
photonDataPrescaled = [('sph-16b2-d', 1), ('sph-16c2-d', 1), ('sph-16d2-d', 1)]
muonData = ['smu-16b2-d', 'smu-16c2-d', 'smu-16d2-d']
electronData = ['sel-16b2-d', 'sel-16c2-d', 'sel-16d2-d']

dPhiPhoMet = 'TVector2::Phi_mpi_pi(photons.phi[0] - t1Met.phi)'
mtPhoMet = 'TMath::Sqrt(2. * t1Met.met * photons.scRawPt[0] * (1. - TMath::Cos(photons.phi[0] - t1Met.phi)))'
        
def getConfig(confName):

    if confName == 'monoph':
        config = PlotConfig('monoph')
        config.blind = True
        for sname, prescale in photonDataPrescaled:
            config.addObs(sname, prescale = prescale)

        config.baseline = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi > 2. && t1Met.minJetDPhi > 0.5'
        config.fullSelection = 't1Met.met > 170.'
        config.sigGroups = [
#            GroupSpec('add', 'ADD', samples = ['add-*']),
            GroupSpec('dmv', 'DM V', samples = ['dmv-*']),
            GroupSpec('dma', 'DM A', samples = ['dma-*']),
            GroupSpec('dmewk', 'DM EWK', samples = ['dmewk-*']),
            GroupSpec('dmvfs', 'DM V', samples = ['dmvfs-*']),
            GroupSpec('dmafs', 'DM A', samples = ['dmafs-*'])
        ]            
        config.signalPoints = [
#            SampleSpec('add-5-2', 'ADD n=5 M_{D}=2TeV', group = config.findGroup('add'), color = 41), # 0.07069/pb
             SampleSpec('dmv-500-1', 'DM V M_{med}=500GeV M_{DM}=1GeV', group = config.findGroup('dmv'), color = 46), # 0.01437/pb
             SampleSpec('dma-500-150', 'DM A M_{med}=500GeV M_{DM}=150GeV', group = config.findGroup('dma'), color = 30), # 0.07827/pb 
#             SampleSpec('dmewk-3000-10', 'DM EWK #Lambda=3000GeV M_{DM}=10GeV', group = config.findGroup('dmewk'), color = 50) # 0.07827/pb 
        ]
        config.bkgGroups = [
            # GroupSpec('spike', 'Spikes', count = 26.8, color = None),
            # GroupSpec('ttg', 'tt#gamma', samples = ['ttg'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            # GroupSpec('tg', 't#gamma', samples = ['tg'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            # GroupSpec('zllg', 'Z#rightarrowll+#gamma', samples = ['zllg-130'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            # GroupSpec('wlnu', 'W#rightarrow#mu#nu, W#rightarrow#tau#nu', samples = ['wlnu'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            # GroupSpec('gg-80', '#gamma#gamma', samples = ['gg-80'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('minor', 'Minor SM', samples = ['ttg', 'tg', 'zllg-130', 'wlnu', 'gg-80'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('gjets', '#gamma + jets', samples = ['gj-40', 'gj-100', 'gj-200', 'gj-400', 'gj-600'], color = ROOT.TColor.GetColor(0xff, 0xaa, 0xcc)),
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('halo', 'Beam halo', samples = photonData, region = 'halo', color = ROOT.TColor.GetColor(0xff, 0x99, 0x33)),
            GroupSpec('hfake', 'Hadronic fakes', samples = photonData, region = 'hfake', color = ROOT.TColor.GetColor(0xbb, 0xaa, 0xff)),
            GroupSpec('efake', 'Electron fakes', samples = photonData, region = 'efake', color = ROOT.TColor.GetColor(0xff, 0xee, 0x99)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff)),
            GroupSpec('zg', 'Z#rightarrow#nu#nu+#gamma', samples = ['znng-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.met', [170., 190., 250., 400., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('metWide', 'E_{T}^{miss}', 't1Met.met', [0. + 10. * x for x in range(10)] + [100. + 20. * x for x in range(5)] + [200. + 50. * x for x in range(9)], unit = 'GeV', overflow = True),
            VariableDef('metHigh', 'E_{T}^{miss}', 't1Met.met', [170., 230., 290., 350., 410., 500., 600., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('metScan', 'E_{T}^{miss}', 't1Met.met', [175. + 25. * x for x in range(14)], unit = 'GeV', overflow = True),
            VariableDef('mtPhoMet', 'M_{T#gamma}', mtPhoMet, (22, 200., 1300.), unit = 'GeV', overflow = True), # blind = (600., 2000.)),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [175.] + [180. + 10. * x for x in range(12)] + [300., 350., 400., 450.] + [500. + 100. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('phoPtScan', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [175. + 25. * x for x in range(14)], unit = 'GeV', overflow = True),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5)),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('nphotons', 'N_{#gamma}', 'photons.size', (4, 0., 4.)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', "t1Met.photonDPhi", (30, 0., math.pi), applyBaseline = False, cut = 'photons.scRawPt[0] > 175. && t1Met.minJetDPhi > 0.5 && t1Met.met > 50.', overflow = True),
            VariableDef('metPhi', '#phi(E_{T}^{miss})', 't1Met.phi', (20, -math.pi, math.pi)),
            VariableDef('dPhiJetMet', '#Delta#phi(E_{T}^{miss}, j)', 'TMath::Abs(TVector2::Phi_mpi_pi(jets.phi - t1Met.phi))', (30, 0., math.pi), cut = 'jets.pt > 30.'),
            VariableDef('dPhiJetMetMin', 'min#Delta#phi(E_{T}^{miss}, j)', 't1Met.minJetDPhi', (30, 0., math.pi), applyBaseline = False, cut = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi > 2.', overflow = True),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)),
            VariableDef('njetsHighPt', 'N_{jet} (p_{T} > 100 GeV)', 'jets.size', (10, 0., 10.), cut = 'jets.pt > 100.'),
            VariableDef('jetPt', 'p_{T}^{jet}', 'jets.pt', (20, 30., 530.) , unit = 'GeV', cut = 'jets.pt > 30', overflow = True),
            VariableDef('jetPtCorrection',  '#Delta p_{T}^{jet} (raw, corrected)', 'jets.pt - jets.ptRaw', (11, -10., 100.), unit = 'GeV', cut = 'jets.pt > 30'),
            VariableDef('phoPtOverMet', 'E_{T}^{#gamma}/E_{T}^{miss}', 'photons.scRawPt[0] / t1Met.met', (30, 0., 3.)),
            VariableDef('phoPtOverJetPt', 'E_{T}^{#gamma}/p_{T}^{jet}', 'photons.scRawPt[0] / jets.pt[0]', (20, 0., 10.)),
            VariableDef('metSignif', 'E_{T}^{miss} Significance', 't1Met.met / TMath::Sqrt(t1Met.sumEt)', (15, 0., 30.)),
            VariableDef('nVertex', 'N_{vertex}', 'npv', (20, 0., 40.)),
            VariableDef('sieie', '#sigma_{i#eta i#eta}', 'photons.sieie[0]', (40, 0., 0.020)),
            VariableDef('sipip', '#sigma_{i#phi i#phi}', 'photons.sipip[0]', (40, 0., 0.020)),
            VariableDef('r9', 'r9', 'photons.r9[0]', (25, 0.7, 1.2)),
            VariableDef('e2e9', 'E2/E9', '(photons.emax[0] + photons.e2nd[0]) / photons.e33[0]', (25, 0.7, 1.2)),
            VariableDef('eStripe9', 'E_{Strip}/E9', 'photons.e15[0] / photons.e33[0]', (40, 0.4, 1.4)),
            VariableDef('etaWidth', 'etaWidth', 'photons.etaWidth[0]', (30, 0.005, .020)),
            VariableDef('phiWidth', 'phiWidth', 'photons.phiWidth[0]', (18, 0., 0.05)),
            VariableDef('time', 'time', 'photons.time[0]', (20, -5., 5.), unit = 'ns'),
            VariableDef('timeSpan', 'timeSpan', 'photons.timeSpan[0]', (20, -20., 20.), unit = 'ns')
        ]

        for variable in list(config.variables): # need to clone the list first!
            if variable.name not in ['met', 'metWide', 'metHigh', 'metScan']:
                config.variables.append(variable.clone(variable.name + 'HighMet', applyFullSel = True))
                config.variables.remove(variable)

        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]

        # config.sensitiveVars = ['met', 'metWide', 'metHigh', 'metScan', 'phoPtHighMet', 'phoPtScanHighMet', 'mtPhoMet', 'mtPhoMetHighMet'] # , 'phoPtVsPhoPhiHighMet']
        
        config.treeMaker = 'MonophotonTreeMaker'

        # Standard MC systematic variations
        for group in config.bkgGroups + config.sigGroups:
            if group.name in ['efake', 'hfake', 'halo', 'spike']:
                continue

            group.variations.append(Variation('lumi', reweight = 0.027))

            group.variations.append(Variation('photonSF', reweight = 'photonSF'))
            group.variations.append(Variation('customIDSF', reweight = 0.055))
            group.variations.append(Variation('leptonVetoSF', reweight = 1.02))
     
            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECUp'), ('t1Met.met', 't1Met.metCorrUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECDown'), ('t1Met.met', 't1Met.metCorrDown')]
            group.variations.append(Variation('jec', replacements = (replUp, replDown)))

            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECUp'), ('photons.scRawPt', 'photons.ptVarUp'), ('t1Met.met', 't1Met.metGECUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECDown'), ('photons.scRawPt', 'photons.ptVarDown'), ('t1Met.met', 't1Met.metGECDown')]
            group.variations.append(Variation('gec', replacements = (replUp, replDown)))

        for group in config.bkgGroups:
            if group.name in ['zg', 'wg', 'efake', 'hfake', 'halo', 'spike']:
                continue

            if group.name != 'vvg':
                group.variations.append(Variation('minorPDF', reweight = 'pdf'))
            group.variations.append(Variation('minorQCDscale', reweight = 0.033))

        # Specific systematic variations
        config.findGroup('halo').variations.append(Variation('haloNorm', reweight = 0.69))
        config.findGroup('halo').variations.append(Variation('haloShape', region = ('haloUp', 'halo')))
        # config.findGroup('spike').variations.append(Variation('spikeNorm', reweight = 0.5))
        config.findGroup('hfake').variations.append(Variation('hfakeTfactor', region = ('hfakeUp', 'hfakeDown')))
        config.findGroup('hfake').variations.append(Variation('purity', reweight = 'purity'))
        config.findGroup('efake').variations.append(Variation('egFakerate', reweight = 0.079))
        config.findGroup('wg').variations.append(Variation('vgPDF', reweight = 'pdf'))
        config.findGroup('wg').variations.append(Variation('vgQCDscale', reweight = 'qcdscale'))
        config.findGroup('wg').variations.append(Variation('wgEWK', reweight = 'ewk'))
        config.findGroup('zg').variations.append(Variation('vgPDF', reweight = 'pdf'))
        config.findGroup('zg').variations.append(Variation('vgQCDscale', reweight = 'qcdscale'))
        config.findGroup('zg').variations.append(Variation('zgEWK', reweight = 'ewk'))

    
    elif confName == 'lowdphi':
        config = PlotConfig('monoph', photonData)
        config.baseline = 'photons.scRawPt[0] > 175. && t1Met.minJetDPhi < 0.5'
        config.fullSelection = 't1Met.met > 170.'
        config.bkgGroups = [
            GroupSpec('minor', 'minor SM', samples = ['ttg', 'tg', 'zllg-130', 'wlnu', 'gg-80'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('halo', 'Beam halo', samples = photonData, region = 'halo', color = ROOT.TColor.GetColor(0xff, 0x99, 0x33)),
            GroupSpec('efake', 'Electron fakes', samples = photonData, region = 'efake', color = ROOT.TColor.GetColor(0xff, 0xee, 0x99)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff)),
            GroupSpec('zg', 'Z#rightarrow#nu#nu+#gamma', samples = ['znng-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa)),
            GroupSpec('hfake', 'Hadronic fakes', samples = photonData, region = 'hfake', color = ROOT.TColor.GetColor(0xbb, 0xaa, 0xff)),
            GroupSpec('gjets', '#gamma + jets', samples = ['gj-40', 'gj-100', 'gj-200', 'gj-400', 'gj-600'], color = ROOT.TColor.GetColor(0xff, 0xaa, 0xcc))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.met', [170., 190., 250., 400., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('metWide', 'E_{T}^{miss}', 't1Met.met', [0. + 10. * x for x in range(10)] + [100. + 20. * x for x in range(5)] + [200. + 50. * x for x in range(9)], unit = 'GeV', overflow = True),
            VariableDef('mtPhoMet', 'M_{T#gamma}', mtPhoMet, (22, 200., 1300.), unit = 'GeV', overflow = True),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [175.] + [180. + 10. * x for x in range(12)] + [300., 350., 400., 450.] + [500. + 100. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('metPhi', '#phi(E_{T}^{miss})', 't1Met.phi', (20, -math.pi, math.pi)),
            VariableDef('dPhiJetMet', '#Delta#phi(E_{T}^{miss}, j)', 'TMath::Abs(TVector2::Phi_mpi_pi(jets.phi - t1Met.phi))', (30, 0., math.pi), cut = 'jets.pt > 30.'),
            VariableDef('dPhiJetMetMin', 'min#Delta#phi(E_{T}^{miss}, j)', 't1Met.minJetDPhi', (30, 0., math.pi), overflow = True),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)),
            VariableDef('njetsHightPt', 'N_{jet} (p_{T} > 100 GeV)', 'jets.size', (10, 0., 10.), cut = 'jets.pt > 100.'),
            VariableDef('metSignif', 'E_{T}^{miss} Significance', 't1Met.met / TMath::Sqrt(t1Met.sumEt)', (15, 0., 30.)),
            VariableDef('nVertex', 'N_{vertex}', 'npv', (20, 0., 40.))
        ]

        for variable in list(config.variables):
            if variable.name not in ['met', 'metWide']:
                config.variables.append(variable.clone(variable.name + 'HighMet', applyFullSel = True))
                config.variables.remove(variable)
    
    elif confName == 'phodphi':
        metCut = 't1Met.met > 170.'
        
        config = PlotConfig('monoph', photonData)
        config.baseline = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi < 0.5 && t1Met.minJetDPhi > 0.5'
        config.fullSelection = metCut
        config.bkgGroups = [
            GroupSpec('minor', 'minor SM', samples = ['ttg', 'tg', 'zllg-130', 'wlnu'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('digam', '#gamma#gamma', samples = ['gg-80'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('gjets', '#gamma + jets', samples = ['gj-40', 'gj-100', 'gj-200', 'gj-400', 'gj-600'], color = ROOT.TColor.GetColor(0xff, 0xaa, 0xcc)),
            GroupSpec('halo', 'Beam halo', samples = photonData, region = 'halo', color = ROOT.TColor.GetColor(0xff, 0x99, 0x33)),
            GroupSpec('hfake', 'Hadronic fakes', samples = photonData, region = 'hfake', color = ROOT.TColor.GetColor(0xbb, 0xaa, 0xff)),
            GroupSpec('efake', 'Electron fakes', samples = photonData, region = 'efake', color = ROOT.TColor.GetColor(0xff, 0xee, 0x99)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff)),
            GroupSpec('zg', 'Z#rightarrow#nu#nu+#gamma', samples = ['znng-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.met', [170., 190., 250., 400., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('metWide', 'E_{T}^{miss}', 't1Met.met', [0. + 10. * x for x in range(10)] + [100. + 20. * x for x in range(5)] + [200. + 50. * x for x in range(9)], unit = 'GeV', overflow = True),
            VariableDef('metHigh', 'E_{T}^{miss}', 't1Met.met', [170., 230., 290., 350., 410., 500., 600., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('mtPhoMet', 'M_{T#gamma}', mtPhoMet, [0. + 10. * x for x in range(21)], unit = 'GeV', overflow = True, blind = (600., 2000.)),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [175.] + [180. + 10. * x for x in range(12)] + [300., 350., 400., 450.] + [500. + 100. * x for x in range(6)], unit = 'GeV', overflow = True), # , ymax = 1.2),
            VariableDef('phoEta', '#eta^{#gamma}', 'TMath::Abs(photons.eta[0])', (10, 0., 1.5)), # , ymax = 250),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('nphotons', 'N_{#gamma}', 'photons.size', (4, 0., 4.)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', "t1Met.photonDPhi", (30, 0., math.pi), applyBaseline = False, cut = 'photons.scRawPt[0] > 175. && t1Met.minJetDPhi > 0.5 && t1Met.met > 40.', overflow = True),
            VariableDef('metPhi', '#phi(E_{T}^{miss})', 't1Met.phi', (20, -math.pi, math.pi)),
            VariableDef('dPhiJetMet', '#Delta#phi(E_{T}^{miss}, j)', 'TMath::Abs(TVector2::Phi_mpi_pi(jets.phi - t1Met.phi))', (30, 0., math.pi), cut = 'jets.pt > 30.'),
            VariableDef('dPhiJetMetMin', 'min#Delta#phi(E_{T}^{miss}, j)', 't1Met.minJetDPhi', (30, 0., math.pi), applyBaseline = False, cut = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi < 2.', overflow = True),
            VariableDef('dPhiPhoJetMin', 'min#Delta#phi(#gamma, j)', 'photons.minJetDPhi[0]', (30, 0., math.pi), overflow = True),
            VariableDef('dPhiJetPho', '#Delta#phi(j, #gamma)', 'jets.photonDPhi', (30, 0., math.pi), cut = 'jets.pt > 30.', overflow = True),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)), # , ymax = 1200.),
            VariableDef('njetsHightPt', 'N_{jet} (p_{T} > 100 GeV)', 'jets.size', (10, 0., 10.), cut = 'jets.pt > 100.'), # , ymax = 1200.),
            VariableDef('jetPt', 'p_{T}^{jet}', 'jets.pt', (20, 30., 1030.) , unit = 'GeV', cut = 'jets.pt > 30', overflow = True),
            VariableDef('jetPtCorrection',  '#Delta p_{T}^{jet} (raw, corrected)', 'jets.pt - jets.ptRaw', (11, -10., 100.), unit = 'GeV', cut = 'jets.pt > 30'),
            VariableDef('jetEta', '#eta^{j}', 'jets.eta', (40, -5.0, 5.0), cut = 'jets.pt > 30.'), # , ymax = 500.),
            VariableDef('jetPhi', '#phi^{j}', 'jets.phi', (20, -math.pi, math.pi), cut = 'jets.pt > 30'), # , ymax = 250),
            VariableDef('phoPtOverMet', 'E_{T}^{#gamma}/E_{T}^{miss}', 'photons.scRawPt[0] / t1Met.met', (20, 0., 4.)),
            VariableDef('phoPtOverJetPt', 'E_{T}^{#gamma}/p_{T}^{jet}', 'photons.scRawPt[0] / jets.pt[0]', (20, 0., 4.)),
            VariableDef('metSignif', 'E_{T}^{miss} Significance', 't1Met.met / TMath::Sqrt(t1Met.sumEt)', (15, 0., 30.)),
            VariableDef('nVertex', 'N_{vertex}', 'npv', (20, 0., 40.)),
            VariableDef('sieie', '#sigma_{i#eta i#eta}', 'photons.sieie[0]', (30, 0.005, 0.020)), 
            VariableDef('r9', 'r9', 'photons.r9[0]', (25, 0.7, 1.2)),
            VariableDef('eStripe9', 'E_{Strip}/E9', 'photons.e15[0] / photons.e33[0]', (50, 0.4, 1.4)),
            VariableDef('etaWidth', 'etaWidth', 'photons.etaWidth[0]', (30, 0.005, .020)),
            VariableDef('phiWidth', 'phiWidth', 'photons.phiWidth[0]', (18, 0., 0.05)),
            VariableDef('time', 'time', 'photons.time[0]', (20, -5., 5.), unit = 'ns'),
            VariableDef('runNumber', 'Run Number / 1000.', 'run / 1000.', (9, 256.5, 261.0)),
            VariableDef('lumiSection', 'Lumi Section', 'lumi', (10, 0., 2000.))
        ]

        for variable in list(config.variables): # need to clone the list first!
            if variable.name not in ['met', 'metWide', 'metHigh']:
                config.variables.append(variable.clone(variable.name + 'HighMet', applyFullSel = True))
                config.variables.remove(variable)
                
        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]

    elif confName == 'dimu':
        mass = 'TMath::Sqrt(2. * muons.pt[0] * muons.pt[1] * (TMath::CosH(muons.eta[0] - muons.eta[1]) - TMath::Cos(muons.phi[0] - muons.phi[1])))'
        dR2_00 = 'TMath::Power(photons.eta[0] - muons.eta[0], 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - muons.phi[0]), 2.)'
        dR2_01 = 'TMath::Power(photons.eta[0] - muons.eta[1], 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - muons.phi[1]), 2.)'

        config = PlotConfig('dimu', muonData)
        config.baseline = mass + ' > 50. && photons.scRawPt[0] > 175. && t1Met.met > 170.' # met is the recoil (Operator LeptonRecoil)
        config.fullSelection = ''
        config.bkgGroups = [
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('zjets', 'Z#rightarrowll+jets', samples = ['dy-50-100', 'dy-50-200', 'dy-50-400', 'dy-50-600'], color = ROOT.TColor.GetColor(0xbb, 0x66, 0xff)),
            GroupSpec('top', 't#bar{t}#gamma', samples = ['ttg'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('zg', 'Z#rightarrowll+#gamma', samples = ['zllg-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.realMet', [10. * x for x in range(6)] + [60. + 20. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('recoil', 'Recoil', 't1Met.met', [100. + 10. * x for x in range(6)] + [160. + 40. * x for x in range(7)], unit = 'GeV', overflow = True),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [80. + 10. * x for x in range(22)] + [300. + 40. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5)),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', 't1Met.photonDPhi', (10, 0., math.pi)),
            VariableDef('dPhiPhoRecoil', '#Delta#phi(#gamma, U)', 'TMath::Abs(TVector2::Phi_mpi_pi(photons.phi[0] - t1Met.phi))', (10, 0., math.pi)),
            VariableDef('dimumass', 'M_{#mu#mu}', mass, (30, 50., 200.), unit = 'GeV'),
            VariableDef('dRPhoMu', '#DeltaR(#gamma, #mu)_{min}', 'TMath::Sqrt(TMath::Min(%s, %s))' % (dR2_00, dR2_01), (20, 0., 4.)),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)),
            VariableDef('partonID', 'PGD ID', 'TMath::Abs(photons.matchedGen[0])', (25, 0., 25.), overflow = True)
        ]

        config.variables.append(config.getVariable('phoPt').clone('phoPtHighMet', applyFullSel = True))
        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]

        # Standard MC systematic variations
        for group in config.bkgGroups:

            group.variations.append(Variation('lumi', reweight = 0.04))

            group.variations.append(Variation('photonSF', reweight = 'photonSF'))
            group.variations.append(Variation('customIDSF', reweight = 0.055))
            group.variations.append(Variation('muonSF', reweight = 'MuonSF'))
            
            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECUp'), ('t1Met.met', 't1Met.metCorrUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECDown'), ('t1Met.met', 't1Met.metCorrDown')]
            group.variations.append(Variation('jec', replacements = (replUp, replDown)))

            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECUp'), ('photons.scRawPt', 'photons.ptVarUp'), ('t1Met.met', 't1Met.metGECUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECDown'), ('photons.scRawPt', 'photons.ptVarDown'), ('t1Met.met', 't1Met.metGECDown')]
            group.variations.append(Variation('gec', replacements = (replUp, replDown)))
            
            if group.name in 'zg':
                continue

            if group.name != 'vvg':
                group.variations.append(Variation('minorPDF', reweight = 'pdf'))
            group.variations.append(Variation('minorQCDscale', reweight = 0.033))
        
        config.findGroup('zg').variations.append(Variation('vgPDF', reweight = 'pdf'))
        config.findGroup('zg').variations.append(Variation('vgQCDscale', reweight = 'qcdscale'))
        config.findGroup('zg').variations.append(Variation('zgEWK', reweight = 'ewk'))

    elif confName == 'diel':
        mass = 'TMath::Sqrt(2. * electrons.pt[0] * electrons.pt[1] * (TMath::CosH(electrons.eta[0] - electrons.eta[1]) - TMath::Cos(electrons.phi[0] - electrons.phi[1])))'
        dR2_00 = 'TMath::Power(photons.eta[0] - electrons.eta[0], 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - electrons.phi[0]), 2.)'
        dR2_01 = 'TMath::Power(photons.eta[0] - electrons.eta[1], 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - electrons.phi[1]), 2.)'

        config = PlotConfig('diel', electronData)
        config.baseline = mass + ' > 50. && photons.scRawPt[0] > 175. && t1Met.met > 170.' # met is the recoil (Operator LeptonRecoil)
        config.fullSelection = ''
        config.bkgGroups = [
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('top', 't#bar{t}#gamma', samples = ['ttg'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('zjets', 'Z#rightarrowll+jets', samples = ['dy-50-100', 'dy-50-200', 'dy-50-400', 'dy-50-600'], color = ROOT.TColor.GetColor(0xbb, 0x66, 0xff)),
            GroupSpec('zg', 'Z#rightarrowll+#gamma', samples = ['zllg-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.realMet', [10. * x for x in range(6)] + [60. + 20. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('recoil', 'Recoil', 't1Met.met', [100. + 10. * x for x in range(6)] + [160. + 40. * x for x in range(7)], unit = 'GeV', overflow = True),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [80. + 10. * x for x in range(22)] + [300. + 40. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5)),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', 't1Met.photonDPhi', (10, 0., math.pi)),
            VariableDef('dPhiPhoRecoil', '#Delta#phi(#gamma, U)', 'TMath::Abs(TVector2::Phi_mpi_pi(photons.phi[0] - t1Met.phi))', (10, 0., math.pi)),
            VariableDef('dielmass', 'M_{ee}', mass, (30, 50., 200.), unit = 'GeV'),
            VariableDef('dRPhoEl', '#DeltaR(#gamma, e)_{min}', 'TMath::Sqrt(TMath::Min(%s, %s))' % (dR2_00, dR2_01), (20, 0., 4.)),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)),
            VariableDef('partonID', 'PGD ID', 'TMath::Abs(photons.matchedGen[0])', (25, 0., 25.), overflow = True)
        ]

        config.variables.append(config.getVariable('phoPt').clone('phoPtHighMet', applyFullSel = True))
        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]

        # Standard MC systematic variations
        for group in config.bkgGroups:

            group.variations.append(Variation('lumi', reweight = 0.027))

            group.variations.append(Variation('photonSF', reweight = 'photonSF'))
            group.variations.append(Variation('customIDSF', reweight = 0.055))
            group.variations.append(Variation('electronSF', reweight = 'ElectronSF'))
            
            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECUp'), ('t1Met.met', 't1Met.metCorrUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECDown'), ('t1Met.met', 't1Met.metCorrDown')]
            group.variations.append(Variation('jec', replacements = (replUp, replDown)))

            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECUp'), ('photons.scRawPt', 'photons.ptVarUp'), ('t1Met.met', 't1Met.metGECUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECDown'), ('photons.scRawPt', 'photons.ptVarDown'), ('t1Met.met', 't1Met.metGECDown')]
            group.variations.append(Variation('gec', replacements = (replUp, replDown)))

            if group.name in 'zg':
                continue

            if group.name != 'vvg':
                group.variations.append(Variation('minorPDF', reweight = 'pdf'))
            group.variations.append(Variation('minorQCDscale', reweight = 0.033))
        
        config.findGroup('zg').variations.append(Variation('vgPDF', reweight = 'pdf'))
        config.findGroup('zg').variations.append(Variation('vgQCDscale', reweight = 'qcdscale'))
        config.findGroup('zg').variations.append(Variation('zgEWK', reweight = 'ewk'))

    elif confName == 'monomu':

        dPhiPhoMet = 'TMath::Abs(TVector2::Phi_mpi_pi(photons.phi[0] - t1Met.realPhi))'
        dPhiJetMetMin = '(jets.size == 0) * 4. + (jets.size == 1) * TMath::Abs(TVector2::Phi_mpi_pi(jets.phi[0] - t1Met.realPhi)) + MinIf$(TMath::Abs(TVector2::Phi_mpi_pi(jets.phi - t1Met.realPhi)), jets.size > 1 && Iteration$ < 4)'
        dRPhoParton  = 'TMath::Sqrt(TMath::Power(photons.eta[0] - promptFinalStates.eta, 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - promptFinalStates.phi), 2.))'
        # MinIf$() somehow returns 0 when there is only one jet

        config = PlotConfig('monomu', muonData)
        config.baseline = 'photons.medium[0] && photons.scRawPt[0] > 175. && ((t1Met.met > 170. && t1Met.photonDPhi > 2. && t1Met.minJetDPhi > 0.5) || (t1Met.realMet > 170. && ' + dPhiPhoMet + ' > 2. && ' + dPhiJetMetMin + ' > 0.5))' # met is the recoil

        config.fullSelection = ''
        config.bkgGroups = [
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('zgamm', 'Z#rightarrowll+#gamma', samples = ['zllg-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa)),
            # GroupSpec('wjets', 'W#rightawoowl#nu+jets', samples = ['wlnu'], color = ROOT.TColor.GetColor(0xcc, 0x99, 0x11)),
            GroupSpec('top', 't#bar{t}#gamma/t#gamma', samples = ['ttg', 'tg'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.realMet', [10. * x for x in range(16)] + [160. + 40. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('recoil', 'Recoil', 't1Met.met', [10. * x for x in range(16)] + [160. + 40. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('mt', 'M_{T}', 'TMath::Sqrt(2. * t1Met.realMet * muons.pt[0] * (1. - TMath::Cos(TVector2::Phi_mpi_pi(t1Met.realPhi - muons.phi[0]))))', [0. + 10. * x for x in range(16)] + [160. + 40. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [60.] + [80. + 10. * x for x in range(22)] + [300. + 40. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5)),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('muEta', '#eta^{#mu}', 'muons.eta[0]', (20, -2.4, 2.4)),
            VariableDef('muIso', 'I^{#mu}_{comb.}/p_{T}', 'muons.combRelIso[0]', (20, 0., 0.4)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', dPhiPhoMet, (30, 0., math.pi)),
            VariableDef('dRPhoMu', '#DeltaR(#gamma, #mu)', 'TMath::Sqrt(TMath::Power(photons.eta[0] - muons.eta[0], 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - muons.phi[0]), 2.))', (20, 0., 4.)),
            VariableDef('dPhiJetMetMin', 'min#Delta#phi(E_{T}^{miss}, j)', dPhiJetMetMin, (30, 0., math.pi), cut = 'jets.size != 0'),
            VariableDef('dPhiJetRecoilMin', 'min#Delta#phi(U, j)', 'TMath::Abs(t1Met.minJetDPhi)', (30, 0., math.pi), cut = 'jets.size != 0'),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)),
            VariableDef('partonID', 'PGD ID', 'TMath::Abs(photons.matchedGen[0])', (25, 0., 25.), overflow = True)
        ]

        config.variables.append(config.getVariable('phoPt').clone('phoPtHighMet', applyFullSel = True))
        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]

        # Standard MC systematic variations
        for group in config.bkgGroups:

            group.variations.append(Variation('lumi', reweight = 0.027))

            group.variations.append(Variation('photonSF', reweight = 'photonSF'))
            group.variations.append(Variation('customIDSF', reweight = 0.055))
            group.variations.append(Variation('muonSF', reweight = 'MuonSF'))
            
            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECUp'), ('t1Met.met', 't1Met.metCorrUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECDown'), ('t1Met.met', 't1Met.metCorrDown')]
            group.variations.append(Variation('jec', replacements = (replUp, replDown)))

            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECUp'), ('photons.scRawPt', 'photons.ptVarUp'), ('t1Met.met', 't1Met.metGECUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECDown'), ('photons.scRawPt', 'photons.ptVarDown'), ('t1Met.met', 't1Met.metGECDown')]
            group.variations.append(Variation('gec', replacements = (replUp, replDown)))

            if group.name in 'wg':
                continue
            
            if group.name != 'vvg':
                group.variations.append(Variation('minorPDF', reweight = 'pdf'))
            group.variations.append(Variation('minorQCDscale', reweight = 0.033))
        
        config.findGroup('wg').variations.append(Variation('vgPDF', reweight = 'pdf'))
        config.findGroup('wg').variations.append(Variation('vgQCDscale', reweight = 'qcdscale'))
        config.findGroup('wg').variations.append(Variation('wgEWK', reweight = 'ewk'))

    elif confName == 'monoel':

        dPhiPhoMet = 'TMath::Abs(TVector2::Phi_mpi_pi(photons.phi[0] - t1Met.realPhi))'
        dPhiJetMetMin = '(jets.size == 0) * 4. + (jets.size == 1) * TMath::Abs(TVector2::Phi_mpi_pi(jets.phi[0] - t1Met.realPhi)) + MinIf$(TMath::Abs(TVector2::Phi_mpi_pi(jets.phi - t1Met.realPhi)), jets.size > 1 && Iteration$ < 4)'
        dRPhoParton  = 'TMath::Sqrt(TMath::Power(photons.eta[0] - promptFinalStates.eta, 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - promptFinalStates.phi), 2.))'
        # MinIf$() somehow returns 0 when there is only one jet

        config = PlotConfig('monoel', electronData)
        config.baseline = 'photons.scRawPt[0] > 175. && ((t1Met.met > 170. && t1Met.photonDPhi > 2. && t1Met.minJetDPhi > 0.5) || (t1Met.realMet > 170. && ' + dPhiPhoMet + ' > 2. && ' + dPhiJetMetMin + ' > 0.5))' # met is the recoil

        config.fullSelection = ''
        config.bkgGroups = [
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('zgamm', 'Z#rightarrowll+#gamma', samples = ['zllg-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa)),
            # GroupSpec('wjets', 'W#rightawoowl#nu+jets', samples = ['wlnu'], color = ROOT.TColor.GetColor(0xcc, 0x99, 0x11)),
            GroupSpec('top', 't#bar{t}#gamma/t#gamma', samples = ['ttg', 'tg'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.realMet', [10. * x for x in range(16)] + [160. + 40. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('recoil', 'Recoil', 't1Met.met', [10. * x for x in range(16)] + [160. + 40. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('mt', 'M_{T}', 'TMath::Sqrt(2. * t1Met.realMet * electrons.pt[0] * (1. - TMath::Cos(TVector2::Phi_mpi_pi(t1Met.realPhi - electrons.phi[0]))))', [0. + 10. * x for x in range(16)] + [160. + 40. * x for x in range(3)], unit = 'GeV', overflow = True),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [60.] + [80. + 10. * x for x in range(22)] + [300. + 40. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5)),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('elEta', '#eta^{e}', 'electrons.eta[0]', (20, -2.4, 2.4)),
            VariableDef('elIso', 'I^{e}_{comb.}/p_{T}', 'electrons.combRelIso[0]', (20, 0., 0.4)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', dPhiPhoMet, (30, 0., math.pi)),
            VariableDef('dRPhoMu', '#DeltaR(#gamma, e)', 'TMath::Sqrt(TMath::Power(photons.eta[0] - electrons.eta[0], 2.) + TMath::Power(TVector2::Phi_mpi_pi(photons.phi[0] - electrons.phi[0]), 2.))', (20, 0., 4.)),
            VariableDef('dPhiJetMetMin', 'min#Delta#phi(E_{T}^{miss}, j)', dPhiJetMetMin, (30, 0., math.pi), cut = 'jets.size != 0'),
            VariableDef('dPhiJetRecoilMin', 'min#Delta#phi(U, j)', 'TMath::Abs(t1Met.minJetDPhi)', (30, 0., math.pi), cut = 'jets.size != 0'),
            VariableDef('njets', 'N_{jet}', 'jets.size', (10, 0., 10.)),
            VariableDef('partonID', 'PGD ID', 'TMath::Abs(photons.matchedGen[0])', (25, 0., 25.), overflow = True)
        ]

        config.variables.append(config.getVariable('phoPt').clone('phoPtHighMet', applyFullSel = True))
        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]

        # Standard MC systematic variations
        for group in config.bkgGroups:

            group.variations.append(Variation('lumi', reweight = 0.027))
            
            group.variations.append(Variation('photonSF', reweight = 'photonSF'))
            group.variations.append(Variation('customIDSF', reweight = 0.055))
            group.variations.append(Variation('electronSF', reweight = 'ElectronSF'))
            
            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECUp'), ('t1Met.met', 't1Met.metCorrUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiJECDown'), ('t1Met.met', 't1Met.metCorrDown')]
            group.variations.append(Variation('jec', replacements = (replUp, replDown)))

            replUp = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECUp'), ('photons.scRawPt', 'photons.ptVarUp'), ('t1Met.met', 't1Met.metGECUp')]
            replDown = [('t1Met.minJetDPhi', 't1Met.minJetDPhiGECDown'), ('photons.scRawPt', 'photons.ptVarDown'), ('t1Met.met', 't1Met.metGECDown')]
            group.variations.append(Variation('gec', replacements = (replUp, replDown)))

            if group.name in 'wg':
                continue

            if group.name != 'vvg':
                group.variations.append(Variation('minorPDF', reweight = 'pdf'))
            group.variations.append(Variation('minorQCDscale', reweight = 0.033))
        
        config.findGroup('wg').variations.append(Variation('vgPDF', reweight = 'pdf'))
        config.findGroup('wg').variations.append(Variation('vgQCDscale', reweight = 'qcdscale'))
        config.findGroup('wg').variations.append(Variation('wgEWK', reweight = 'ewk'))

    elif confName == 'lowmt':
        config = PlotConfig('lowmt', photonData)
        config.baseline = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi < 2. && t1Met.minJetDPhi > 0.5 && ' + mtPhoMet + ' > 40. && ' + mtPhoMet + ' < 150.'
        config.fullSelection = 'photons.scRawPt[0] < 400. && t1Met.met > 170.'
        config.bkgGroups = [
            GroupSpec('minor', 't#bar{t}, Z, #gamma#gamma', samples = ['ttg', 'zg', 'gg-80'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('multiboson', 'multiboson', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('gjets', '#gamma + jets', samples = ['gj-40', 'gj-100', 'gj-200', 'gj-400', 'gj-600'], color = ROOT.TColor.GetColor(0xff, 0xaa, 0xcc)),
            # GroupSpec('hfake', 'Hadronic fakes', samples = photonData, region = 'hfakelowmt', color = ROOT.TColor.GetColor(0xbb, 0xaa, 0xff)),
            GroupSpec('efake', 'Electron fakes', samples = photonData, region = 'lowmtEfake', color = ROOT.TColor.GetColor(0xff, 0xee, 0x99)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff)),
            GroupSpec('zg', 'Z#rightarrow#nu#nu+#gamma', samples = ['znng-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa))
        ]
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.met', [100. + 10. * x for x in range(5)] + [150. + 50. * x for x in range(6)], cut = 'photons.scRawPt[0] < 400.', unit = 'GeV', overflow = True),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [175. + 15. * x for x in range(20)], cut = 't1Met.met > 170.', unit = 'GeV', logy = False, ymax = 0.5),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5), applyFullSel = True),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi), applyFullSel = True, logy = False, ymax = 20.),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', 'TVector2::Phi_mpi_pi(photons.phi[0] - t1Met.phi)', (20, -1., 1.), applyBaseline = False, applyFullSel = True, cut = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi < 2. && t1Met.minJetDPhi > 0.5', logy = False, ymax = 20.),
            VariableDef('mtPhoMet', 'M_{T#gamma}', mtPhoMet, (11, 40., 150.), applyFullSel = True, unit = 'GeV', logy = False, ymax = 0.6),
            VariableDef('metPhi', '#phi(E_{T}^{miss})', 't1Met.phi', (20, -math.pi, math.pi), applyFullSel = True, logy = False, ymax = 20.),
            VariableDef('njets', 'N_{jet}', 'jets.size', (6, 0., 6.), applyFullSel = True),
            VariableDef('jetPt', 'p_{T}^{j1}', 'jets.pt[0]', (30, 30., 800.), cut = 'jets.size != 0', applyFullSel = True, unit = 'GeV'),
            VariableDef('r9', 'R_{9}', 'photons.r9', (50, 0.5, 1.), applyFullSel = True),
        ]

    elif confName == 'phistack':
        config = PlotConfig('monoph', photonData)
        config.baseline = 'photons.scRawPt[0] > 175. && t1Met.photonDPhi > 2. && t1Met.minJetDPhi > 0.5'
        config.fullSelection = 't1Met.met > 170.'
        config.signalPoints = [
            GroupSpec('add-5-2', 'ADD n=5 M_{D}=2TeV', color = 41), # 0.07069/pb
            GroupSpec('dmv-1000-150', 'DM V M_{med}=1TeV M_{DM}=150GeV', color = 46), # 0.01437/pb
            GroupSpec('dma-500-1', 'DM A M_{med}=500GeV M_{DM}=1GeV', color = 30) # 0.07827/pb 
        ]
        config.bkgGroups = [
            GroupSpec('minor', 'minor SM', samples = ['ttg', 'tg', 'zllg-130', 'wlnu', 'gg-80'], color = ROOT.TColor.GetColor(0x55, 0x44, 0xff)),
            GroupSpec('vvg', 'VV#gamma', samples = ['wwg', 'wz', 'zz'], color = ROOT.TColor.GetColor(0xff, 0x44, 0x99)),
            GroupSpec('gjets', '#gamma + jets', samples = ['gj-40', 'gj-100', 'gj-200', 'gj-400', 'gj-600'], color = ROOT.TColor.GetColor(0xff, 0xaa, 0xcc)),
            # GroupSpec('halo', 'Beam halo', samples = photonData, region = 'halo', color = ROOT.TColor.GetColor(0xff, 0x99, 0x33)),
            GroupSpec('hfake', 'Hadronic fakes', samples = photonData, region = 'hfake', color = ROOT.TColor.GetColor(0xbb, 0xaa, 0xff)),
            GroupSpec('efake', 'Electron fakes', samples = photonData, region = 'efake', color = ROOT.TColor.GetColor(0xff, 0xee, 0x99)),
            GroupSpec('wg', 'W#rightarrowl#nu+#gamma', samples = ['wnlg-130'], color = ROOT.TColor.GetColor(0x99, 0xee, 0xff)),
            GroupSpec('zg', 'Z#rightarrow#nu#nu+#gamma', samples = ['znng-130'], color = ROOT.TColor.GetColor(0x99, 0xff, 0xaa))
        ]
        config.variables = [
            VariableDef('phoPhiHighMet', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi), logy = False, applyFullSel = True, blind = (-math.pi, math.pi), ymax = 8.)
        ]

    elif confName == 'nosel':
        metCut = ''
        
        config = PlotConfig('monoph', photonData)
        config.baseline = '1'
        config.fullSelection = '1'

        config.sigGroups = [
            GroupSpec('add', 'ADD', samples = ['add-*']),
            GroupSpec('dmv', 'DM V', samples = ['dmv-*']),
            GroupSpec('dma', 'DM A', samples = ['dma-*']),
            GroupSpec('dmvfs', 'DM V', samples = ['dmvfs-*']),
            GroupSpec('dmafs', 'DM A', samples = ['dmafs-*'])
        ]
        config.signalPoints = [
            SampleSpec('add-5-2', 'ADD n=5 M_{D}=2TeV', group = config.findGroup('add'), color = 41), # 0.07069/pb
            SampleSpec('dmv-1000-150', 'DM V M_{med}=1TeV M_{DM}=150GeV', group = config.findGroup('dmv'), color = 46), # 0.01437/pb
            SampleSpec('dma-500-1', 'DM A M_{med}=500GeV M_{DM}=1GeV', group = config.findGroup('dma'), color = 30) # 0.07827/pb 
        ]

        config.bkgGroups = []
        config.variables = [
            VariableDef('met', 'E_{T}^{miss}', 't1Met.met', [170., 190., 250., 400., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('metWide', 'E_{T}^{miss}', 't1Met.met', [0. + 10. * x for x in range(10)] + [100. + 20. * x for x in range(5)] + [200. + 50. * x for x in range(9)], unit = 'GeV', overflow = True),
            VariableDef('metHigh', 'E_{T}^{miss}', 't1Met.met', [170., 230., 290., 350., 410., 500., 600., 700., 1000.], unit = 'GeV', overflow = True),
            VariableDef('mtPhoMet', 'M_{T#gamma}', mtPhoMet, (22, 200., 1300.), unit = 'GeV', overflow = True, blind = (600., 2000.)),
            VariableDef('phoPt', 'E_{T}^{#gamma}', 'photons.scRawPt[0]', [175.] + [180. + 10. * x for x in range(12)] + [300., 350., 400., 450.] + [500. + 100. * x for x in range(6)], unit = 'GeV', overflow = True),
            VariableDef('phoEta', '#eta^{#gamma}', 'photons.eta[0]', (20, -1.5, 1.5)),
            VariableDef('phoPhi', '#phi^{#gamma}', 'photons.phi[0]', (20, -math.pi, math.pi)),
            VariableDef('dPhiPhoMet', '#Delta#phi(#gamma, E_{T}^{miss})', "t1Met.photonDPhi", (30, 0., math.pi), cut = 't1Met.met > 40.'),
            VariableDef('metPhi', '#phi(E_{T}^{miss})', 't1Met.phi', (20, -math.pi, math.pi)),
            VariableDef('dPhiJetMet', '#Delta#phi(E_{T}^{miss}, j)', 'TMath::Abs(TVector2::Phi_mpi_pi(jets.phi - t1Met.phi))', (30, 0., math.pi), cut = 'jets.pt > 30.'),
            VariableDef('dPhiJetMetMin', 'min#Delta#phi(E_{T}^{miss}, j)', 't1Met.minJetDPhi', (30, 0., math.pi)),
            VariableDef('njets', 'N_{jet}', 'jets.size', (6, 0., 6.)),
            VariableDef('phoPtOverMet', 'E_{T}^{#gamma}/E_{T}^{miss}', 'photons.scRawPt[0] / t1Met.met', (20, 0., 4.)),
            VariableDef('phoPtOverJetPt', 'E_{T}^{#gamma}/p_{T}^{jet}', 'photons.scRawPt[0] / jets.pt[0]', (20, 0., 10.)),
            VariableDef('nVertex', 'N_{vertex}', 'npv', (20, 0., 40.)),
            VariableDef('sieie', '#sigma_{i#eta i#eta}', 'photons.sieie[0]', (30, 0.005, 0.020)),
            VariableDef('r9', 'r9', 'photons.r9[0]', (50, 0.5, 1.)),
            VariableDef('s4', 's4', 'photons.s4[0]', (50, 0.5, 1.), logy = False),
            VariableDef('etaWidth', 'etaWidth', 'photons.etaWidth[0]', (30, 0.005, .020)),
            VariableDef('phiWidth', 'phiWidth', 'photons.phiWidth[0]', (18, 0., 0.05)),
            VariableDef('timeSpan', 'timeSpan', 'photons.timeSpan[0]', (20, -20., 20.)),
        ]

        for variable in list(config.variables): # need to clone the list first!
            if variable.name not in ['met', 'metWide', 'metHigh']:
                config.variables.append(variable.clone(variable.name + 'HighMet', applyFullSel = True))
                config.variables.remove(variable)

        config.getVariable('phoPtHighMet').binning = [175., 190., 250., 400., 700., 1000.]
    
    else:
        print 'Unknown configuration', confName
        return

    return config

