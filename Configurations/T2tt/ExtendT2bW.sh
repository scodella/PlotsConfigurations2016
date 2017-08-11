#!/bin/bash
#
echo "Extending T2bW in " $1
#
rm -r $1/MassPoint2bW_Sm375_Xm*
cp -r $1/MassPoint2bW_Sm400_Xm225 $1/MassPoint2bW_Sm375_Xm200
cp -r $1/MassPoint2bW_Sm400_Xm200 $1/MassPoint2bW_Sm375_Xm175
cp -r $1/MassPoint2bW_Sm400_Xm175 $1/MassPoint2bW_Sm375_Xm150
cp -r $1/MassPoint2bW_Sm400_Xm150 $1/MassPoint2bW_Sm375_Xm125
#
rm -r $1/MassPoint2bW_Sm350_Xm125 
cp -r $1/MassPoint2bW_Sm375_Xm150 $1/MassPoint2bW_Sm350_Xm125  
#
rm -r $1/MassPoint2bW_Sm325_Xm*
cp -r $1/MassPoint2bW_Sm350_Xm175 $1/MassPoint2bW_Sm325_Xm150
cp -r $1/MassPoint2bW_Sm350_Xm150 $1/MassPoint2bW_Sm325_Xm125
cp -r $1/MassPoint2bW_Sm350_Xm125 $1/MassPoint2bW_Sm325_Xm100
cp -r $1/MassPoint2bW_Sm350_Xm100 $1/MassPoint2bW_Sm325_Xm75
#
rm -r $1/MassPoint2bW_Sm300_Xm75
cp -r $1/MassPoint2bW_Sm325_Xm100 $1/MassPoint2bW_Sm300_Xm75  
#
rm -r $1/MassPoint2bW_Sm275_Xm*
cp -r $1/MassPoint2bW_Sm300_Xm125 $1/MassPoint2bW_Sm275_Xm100
cp -r $1/MassPoint2bW_Sm300_Xm100 $1/MassPoint2bW_Sm275_Xm75
cp -r $1/MassPoint2bW_Sm300_Xm75  $1/MassPoint2bW_Sm275_Xm50
cp -r $1/MassPoint2bW_Sm300_Xm50  $1/MassPoint2bW_Sm275_Xm25
#
rm -r $1/MassPoint2bW_Sm250_Xm25
cp -r $1/MassPoint2bW_Sm275_Xm50  $1/MassPoint2bW_Sm250_Xm25  
#
rm -r $1/MassPoint2bW_Sm225_Xm*
cp -r $1/MassPoint2bW_Sm250_Xm75  $1/MassPoint2bW_Sm225_Xm50
cp -r $1/MassPoint2bW_Sm250_Xm50  $1/MassPoint2bW_Sm225_Xm25
cp -r $1/MassPoint2bW_Sm250_Xm25  $1/MassPoint2bW_Sm225_Xm1
#


