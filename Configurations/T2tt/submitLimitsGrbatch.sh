#!/bin/bash

cat MassPointList.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       qsub ./runPointLimitGrbatch.sh $line
   fi
done
