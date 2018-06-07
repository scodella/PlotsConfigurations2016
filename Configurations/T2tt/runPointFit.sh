#!/bin/bash

echo "Performing MaxLikelihoodFit for " $1
#
cd /afs/cern.ch/work/s/scodella/Stop/CodeDevelopment/CMSSW_7_4_7/src/
#cd /afs/cern.ch/work/s/scodella/Stop/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -
#
cd $1/
#
if [[ -z $2 || "$2" = *"asimov"* ]]
then
    echo "     fit to asimov datasets"
    combine -M MaxLikelihoodFit -t -1 --expectSignal 0 --robustFit 1 --saveShapes --saveWithUncertainties -n "_asimov" -d datacardFinal.txt
    mv mlfit.root mlfit_asimov.root
    rm  *.mH120.root
    $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit_asimov.root -A -a -f latex --histogram pulls_asimov.root > pulls_asimov.tex
fi
#
if [[ -z $2 || "$2" = *"data"* ]]
then
    echo "     fit to data"
    combine -M MaxLikelihoodFit --robustFit 1 --saveShapes --saveWithUncertainties -n "_data" -d datacardFinal.txt
    #combineCards.py Tag=./SR3_Tag_em/MT2llisr/datacard.txt Veto=./SR3_Veto_em/MT2llisr/datacard.txt > ff.txt
    #combine -M MaxLikelihoodFit --robustFit 1 --saveShapes --saveWithUncertainties -n "_data" -d ff.txt
    #cd SR3_Tag_em/MT2llisr/
    #combine -M MaxLikelihoodFit --robustFit 1 --saveShapes --saveWithUncertainties -n "_data" -d datacard.txt
    mv mlfit.root mlfit_data.root
    rm  *.mH120.root
    $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit_data.root -A -a -f latex --histogram pulls_data.root > pulls_data_all.tex
    $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit_data.root -f latex --histogram pulls_data.root > pulls_data.tex
    combine -M Asymptotic  -d datacardFinal.txt
    mv higgsCombineTest.Asymptotic.mH120.root datacardFinal.root
fi
#
cd -

