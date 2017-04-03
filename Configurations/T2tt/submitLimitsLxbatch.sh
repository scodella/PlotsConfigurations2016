#!/bin/bash

cat MassPointList.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       bsub -q cmscaf1nd -o $PWD/jobs $PWD/runPointLimitLxbatch.sh $line
   fi
done
