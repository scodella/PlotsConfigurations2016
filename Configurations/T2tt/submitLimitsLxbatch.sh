#!/bin/bash

export WORKDIRECTORY=$PWD

mkdir -p jobs

cd jobs/

cat $WORKDIRECTORY/MassPointList${1}.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       bsub -q cmscaf1nd -o $WORKDIRECTORY/jobs $WORKDIRECTORY/runPointLimitLxbatch.sh $line $WORKDIRECTORY $2
   fi
done
