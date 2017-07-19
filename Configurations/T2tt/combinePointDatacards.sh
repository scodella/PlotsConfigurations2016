#!/bin/bash

echo "Combining datacards for" $1
#
cd $1/
#
combineCards.py em=./SR1_Tag_em/MT2ll/datacard.txt      ee=./SR1_Tag_ee/MT2ll/datacard.txt      mm=./SR1_Tag_mm/MT2ll/datacard.txt   > datacardSR1T.txt
combineCards.py em=./SR1_NoTag_em/MT2ll/datacard.txt    ee=./SR1_NoTag_ee/MT2ll/datacard.txt    mm=./SR1_NoTag_mm/MT2ll/datacard.txt > datacardSR1V.txt
combineCards.py em=./SR1_NoJet_em/MT2ll/datacard.txt    ee=./SR1_NoJet_ee/MT2ll/datacard.txt    mm=./SR1_NoJet_mm/MT2ll/datacard.txt > datacardSR10.txt
#
combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      ee=./SR2_Tag_ee/MT2ll/datacard.txt      mm=./SR2_Tag_mm/MT2ll/datacard.txt   > datacardSR2T.txt
combineCards.py em=./SR2_NoTag_em/MT2ll/datacard.txt    ee=./SR2_NoTag_ee/MT2ll/datacard.txt    mm=./SR2_NoTag_mm/MT2ll/datacard.txt > datacardSR2V.txt
combineCards.py em=./SR2_NoJet_em/MT2ll/datacard.txt    ee=./SR2_NoJet_ee/MT2ll/datacard.txt    mm=./SR2_NoJet_mm/MT2ll/datacard.txt > datacardSR20.txt
#
combineCards.py em=./SR3_Tag_em/MT2ll/datacard.txt      ee=./SR3_Tag_ee/MT2ll/datacard.txt      mm=./SR3_Tag_mm/MT2ll/datacard.txt   > datacardSR3T.txt
combineCards.py em=./SR3_NoTag_em/MT2ll/datacard.txt    ee=./SR3_NoTag_ee/MT2ll/datacard.txt    mm=./SR3_NoTag_mm/MT2ll/datacard.txt > datacardSR3V.txt
combineCards.py em=./SR3_NoJet_em/MT2ll/datacard.txt    ee=./SR3_NoJet_ee/MT2ll/datacard.txt    mm=./SR3_NoJet_mm/MT2ll/datacard.txt > datacardSR30.txt
#
#combineCards.py em=./SR3_Tag_em/MT2llisr/datacard.txt   ee=./SR3_Tag_ee/MT2llisr/datacard.txt   mm=./SR3_Tag_mm/MT2llisr/datacard.txt   > datacardSR3T.txt
#combineCards.py em=./SR3_NoTag_em/MT2llisr/datacard.txt ee=./SR3_NoTag_ee/MT2llisr/datacard.txt mm=./SR3_NoTag_mm/MT2llisr/datacard.txt > datacardSR3V.txt
#combineCards.py em=./SR3_NoJet_em/MT2llisr/datacard.txt ee=./SR3_NoJet_ee/MT2llisr/datacard.txt mm=./SR3_NoJet_mm/MT2llisr/datacard.txt > datacardSR30.txt
#
combineCards.py SR1=datacardSR1T.txt SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardTag.txt 
combineCards.py SR1=datacardSR1V.txt SR2=datacardSR2V.txt SR3=datacardSR3V.txt > datacardNoTag.txt 
combineCards.py SR1=datacardSR10.txt SR2=datacardSR20.txt SR3=datacardSR30.txt > datacardNoJet.txt 
#
#combineCards.py Tag=datacardTag.txt NoTag=datacardNoTag.txt > datacardFinal.txt 
combineCards.py Tag=datacardTag.txt NoTag=datacardNoTag.txt NoJet=datacardNoJet.txt > datacardFinal.txt 
#
cd -
#mv datacard*.txt $1/

