#!/bin/bash

asimov=$1
signal=$2
outname=$3
datacard=$4

text2workspace.py ${datacard} -m 125 -o ${outname}.root --channel-masks

if [ ${asimov} == 1 ]
then
    echo "\n  Generating asimov data for impact study. \n"
    combineTool.py -M Impacts -d ${outname}.root -m 125 --robustFit 1 --setParameterRanges r=-5.0,5.0 --expectSignal=${signal} -t -1 --doInitialFit  
    combineTool.py -M Impacts -d ${outname}.root -m 125 --robustFit 1 --setParameterRanges r=-5.0,5.0 --expectSignal=${signal} -t -1 --doFits --parallel 24
else
    echo "\n  Using provided data for impact study. \n"
    combineTool.py -M Impacts -d ${outname}.root -m 125 --robustFit 1 --setParameterRanges r=-5.0,5.0 --expectSignal=${signal} --doInitialFit --setParameters mask_monophHighPhi=1,mask_monophLowPhi=1 --freezeNuisances freenorm_halo_monophHighPhi
    combineTool.py -M Impacts -d ${outname}.root -m 125 --robustFit 1 --setParameterRanges r=-5.0,5.0 --expectSignal=${signal} --doFits --parallel 24 --setParameters mask_monophHighPhi=1,mask_monophLowPhi=1 --freezeNuisances freenorm_halo_monophHighPhi
fi

combineTool.py -M Impacts -d ${outname}.root -m 125 -o impacts.json_${outname}
plotImpacts.py -i impacts.json_${outname} -o impacts_${outname}

echo "Done!"
