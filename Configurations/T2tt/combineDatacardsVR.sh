#!/bin/bash

combineCards.py em=$1/VR1_Tag_em/MT2ll/datacard.txt     ee=$1/VR1_Tag_ee/MT2ll/datacard.txt     mm=$1/VR1_Tag_mm/MT2ll/datacard.txt   > datacardVR1T.txt
combineCards.py em=$1/VR1_NoTag_em/MT2ll/datacard.txt   ee=$1/VR1_NoTag_ee/MT2ll/datacard.txt   mm=$1/VR1_NoTag_mm/MT2ll/datacard.txt > datacardVR1V.txt
#
combineCards.py tag=datacardVR1T.txt                  notag=datacardVR1V.txt                    > datacardVR1.txt 
combineCards.py tag=$1/VR1_Tag_em/MT2ll/datacard.txt  notag=$1/VR1_NoTag_em/MT2ll/datacard.txt  > datacardVR1em.txt 
#
mv datacard*.txt $1/
#
