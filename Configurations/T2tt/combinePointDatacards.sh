#!/bin/bash

echo "Combining datacards for" $1
#
cd $1/
#
if [[ "$1" = *"MassPoint2"* ]]
then
    # SR1
    combineCards.py em=./SR1_Tag_em/MT2ll/datacard.txt      sf=./SR1_Tag_sf/MT2ll/datacard.txt      > datacardSR1T.txt
    combineCards.py em=./SR1_Veto_em/MT2ll/datacard.txt     sf=./SR1_Veto_sf/MT2ll/datacard.txt     > datacardSR1V.txt
    # SR2
    combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      sf=./SR2_Tag_sf/MT2ll/datacard.txt      > datacardSR2T.txt
    combineCards.py em=./SR2_Veto_em/MT2ll/datacard.txt     sf=./SR2_Veto_sf/MT2ll/datacard.txt     > datacardSR2V.txt
    # SR3
    #combineCards.py em=./SR3_Tag_em/MT2ll/datacard.txt      sf=./SR3_Tag_sf/MT2ll/datacard.txt      > datacardSR3T.txt
    #combineCards.py em=./SR3_Veto_em/MT2ll/datacard.txt     sf=./SR3_Veto_sf/MT2ll/datacard.txt     > datacardSR3V.txt
    # SR3 ISR
    combineCards.py em=./SR3_Tag_em/MT2llisr/datacard.txt   sf=./SR3_Tag_sf/MT2llisr/datacard.txt   > datacardSR3T.txt
    combineCards.py em=./SR3_Veto_em/MT2llisr/datacard.txt  sf=./SR3_Veto_sf/MT2llisr/datacard.txt  > datacardSR3V.txt
    #
    combineCards.py SR1=datacardSR1T.txt SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardTag.txt 
    combineCards.py SR1=datacardSR1V.txt SR2=datacardSR2V.txt SR3=datacardSR3V.txt > datacardVeto.txt 
    #
    combineCards.py Tag=datacardTag.txt NoTag=datacardVeto.txt > datacardFinal.txt 
fi
#
if [[ "$1" = *"MassPointChi"* ]]
then
    # SR1
    combineCards.py em=./SR1_Tag_em/MT2ll/datacard.txt      sf=./SR1_Tag_sf/MT2ll/datacard.txt      > datacardSR1T.txt
    combineCards.py em=./SR1_NoTag_em/MT2ll/datacard.txt    sf=./SR1_NoTag_sf/MT2ll/datacard.txt    > datacardSR1J.txt
    combineCards.py em=./SR1_NoJet_em/MT2ll/datacard.txt    sf=./SR1_NoJet_sf/MT2ll/datacard.txt    > datacardSR10.txt
    # SR2
    combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      sf=./SR2_Tag_sf/MT2ll/datacard.txt      > datacardSR2T.txt
    combineCards.py em=./SR2_NoTag_em/MT2ll/datacard.txt    sf=./SR2_NoTag_sf/MT2ll/datacard.txt    > datacardSR2J.txt
    combineCards.py em=./SR2_NoJet_em/MT2ll/datacard.txt    sf=./SR2_NoJet_sf/MT2ll/datacard.txt    > datacardSR20.txt
    # SR3
    combineCards.py em=./SR3_Tag_em/MT2ll/datacard.txt      sf=./SR3_Tag_sf/MT2ll/datacard.txt      > datacardSR3T.txt
    combineCards.py em=./SR3_Veto_em/MT2ll/datacard.txt     sf=./SR3_Veto_sf/MT2ll/datacard.txt     > datacardSR3V.txt
    #
    combineCards.py SR1=datacardSR1T.txt SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardTag.txt 
    combineCards.py SR1=datacardSR1J.txt SR2=datacardSR2J.txt SR3=datacardSR3V.txt > datacardNoTag.txt 
    combineCards.py SR1=datacardSR10.txt SR2=datacardSR20.txt > datacardNoJet.txt 
    #
    combineCards.py Tag=datacardTag.txt NoTag=datacardNoTag.txt NoJet=datacardNoJet.txt > datacardFinal.txt 
fi
