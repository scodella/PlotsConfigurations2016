#!/bin/bash

cat MassPointList.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       bsub -q cmscaf1nd /afs/cern.ch/work/s/scodella/Stop/CodeDevelopment/CMSSW_8_0_21/src/PlotsConfigurations/Configurations/T2tt/runPointLimitLxbatch.sh $line
   fi
done
