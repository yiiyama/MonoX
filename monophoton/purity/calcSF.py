import os 
import sys
from pprint import pprint
import ROOT as r
from array import array

basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if basedir not in sys.path:
    sys.path.append(basedir)
import config
from plotstyle import SimpleCanvas, RatioCanvas

import selections as s

varName = 'sieie'
versDir = os.path.join('/scratch5/ballen/hist/purity',s.Version,varName)
plotDir = os.path.join(versDir, 'Plots', 'SignalContam') 
outDir = os.path.join(plotDir, 'ScaleFactor')
if not os.path.exists(outDir):
    os.makedirs(outDir)

yields = {}

for loc in s.Locations[:1]:
    yields[loc] = {}
    for pid in s.PhotonIds[:1]+s.PhotonIds[2:3]:
        yields[loc][pid] = {}
        for ptCut in s.PhotonPtSels[1:]:
            yields[loc][pid][ptCut[0]] = {}
            for metCut in s.MetSels[1:2]:
                yields[loc][pid][ptCut[0]][metCut[0]] = {}

                for chiso in s.ChIsoSbSels[:]:
                    yields[loc][pid][ptCut[0]][metCut[0]][chiso[0]] = {}

                    dirName = loc+'_'+pid+'_'+chiso[0]+'_'+ptCut[0]+'_'+metCut[0] 
                    condorFileName = os.path.join(plotDir,dirName,"results.out") 
                    # print condorFileName
                    condorFile = open(condorFileName)

                    match = False
                    count = [1., 0.]
                    for line in condorFile:
                        if "# of real photons is:" in line:
                            # print line
                            tmp = line.split()
                            if tmp:
                                match = True
                                # pprint(tmp)
                                count[0] = float(tmp[-1].strip("(),"))
                                #print count
                        elif "Total unc yield is:" in line:
                            # print line
                            tmp = line.split()
                            if tmp:
                                match = True
                                # pprint(tmp)
                                count[1] = float(tmp[-1].strip("(),"))
                                #print count
                    
                    yields[loc][pid][ptCut[0]][metCut[0]][chiso[0]] = count

                    if not match:
                        print "No yield found for skim:", dirName
                        yields[loc][pid][ptCut[0]][metCut[0]][chiso[0]] = (-1., 0.0)
                    condorFile.close()

pprint(yields)

canvas = SimpleCanvas(lumi = config.jsonLumi)
rcanvas = RatioCanvas(lumi = config.jsonLumi)

for loc in s.Locations[:1]:
    for pid in s.PhotonIds[2:3]:
        for metCut in s.MetSels[1:2]:
            canvas.cd()
            canvas.Clear()
            canvas.legend.Clear()
            canvas.legend.setPosition(0.7, 0.3, 0.9, 0.5)

            rcanvas.cd()
            rcanvas.Clear()
            rcanvas.legend.Clear()
            rcanvas.legend.setPosition(0.7, 0.3, 0.9, 0.5)

            bins = [175, 200, 250, 300, 350, 500]

            hTrue = r.TH1F("ntrue", ";#gamma p_{T} (GeV)", len(bins)-1, array('d', bins))
            hTotal = r.TH1F("ntotal", ";#gamma p_{T} (GeV)", len(bins)-1, array('d', bins))

            for ptCut in s.PhotonPtSels[1:]:
                lowEdge = int(ptCut[0].split("t")[2])
                binNumber = 0
                for bin in bins:
                    if bin == lowEdge:
                        binNumber = bins.index(bin) + 1
            
                passes = yields[loc][pid][ptCut[0]][metCut[0]]
                totals = yields[loc]['none'][ptCut[0]][metCut[0]]

                nTrue = passes[s.ChIsoSbSels[1][0]][0]
                uncTrue = passes[s.ChIsoSbSels[1][0]][1]
                sbUncTrue = max(abs(nTrue - passes[s.ChIsoSbSels[0][0]][0]),
                                abs(nTrue - passes[s.ChIsoSbSels[2][0]][0]))
                totalUncTrue = (uncTrue**2 + sbUncTrue**2)**(0.5)

                hTrue.SetBinContent(binNumber, nTrue)
                hTrue.SetBinError(binNumber, totalUncTrue)

                nTotal = totals[s.ChIsoSbSels[1][0]][0]
                uncTotal = totals[s.ChIsoSbSels[1][0]][1]
                sbUncTotal = max(abs(nTotal - passes[s.ChIsoSbSels[0][0]][0]),
                                abs(nTotal - passes[s.ChIsoSbSels[2][0]][0]))
                totalUncTotal = (uncTotal**2 + sbUncTotal**2)**(0.5)

                print lowEdge
                print "pass:  %10.1f pm %5.1f" % (nTrue, totalUncTrue)
                print "total: %10.1f pm %5.1f" % (nTotal, totalUncTotal)

                hTotal.SetBinContent(binNumber, nTotal)
                hTotal.SetBinError(binNumber, totalUncTotal)

                # eff = nTrue / nTotal
                # sigma(eff) = sqrt(eff*(1-eff)/nTotal)

            """
            rcanvas.legend.add("total", title = "All Photons", lcolor = r.kBlack, lwidth = 2, mcolor = r.kBlack)
            rcanvas.legend.apply("total", hTotal)
            rcanvas.addHistogram(hTotal, drawOpt = 'EP')

            rcanvas.legend.add("true", title = "True Photons", lcolor = r.kRed, lwidth = 2, mcolor = r.kRed)
            rcanvas.legend.apply("true", hTrue)
            passId = rcanvas.addHistogram(hTrue, drawOpt = 'EP')
            
            rcanvas.ylimits = (0., -1.)

            plotName = "yield_"+str(loc)+"_"+str(pid)+"_ptbinned"
            rcanvas.printWeb('purity/'+s.Version+'/Fitting', plotName, logy = False)
            """

            gEff = r.TGraphAsymmErrors()
            gEff.Divide(hTrue, hTotal, "cl=0.683 b(1,1) mode")

            rcanvas.legend.add("data", title = "Data", lcolor = r.kBlack, lwidth = 2)
            rcanvas.legend.apply("data", gEff)
            rcanvas.addHistogram(gEff, drawOpt = 'EP')

            rcanvas.ylimits = (0.0, 1.2)
            rcanvas.ytitle = 'Photon Efficiency'
            rcanvas.xtitle = 'E_{T}^{#gamma} (GeV)'

            plotName = "efficiency_"+str(loc)+"_"+str(pid)+"_ptbinned"
            rcanvas.printWeb('purity/'+s.Version+'/Fitting', plotName, logy = False)