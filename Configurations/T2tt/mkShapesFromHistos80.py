#!/usr/bin/env python

import json
import sys
import ROOT
import optparse
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import logging
import os.path
import math

# ----------------------------------------------------- ShapeFactory --------------------------------------

class ShapeFactory:
    _logger = logging.getLogger('ShapeFactory')

    # _____________________________________________________________________________
    def __init__(self):
      
        variables = {}
        self._variables = variables

        cuts = {}
        self._cuts = cuts

        samples = {}
        self._samples = samples

        ## list of [processes]  
        self.processes = []
        ## list of [signal processes]
        self.signals = []
        ## list of [background processes]
        self.backgrounds = []
        ## data
        self.data = []        
        ## list of [(name of uncert, type of nuisance, list of samples affected, with value, additional value [in case of gmN])]
        self.systs   = []

    # _____________________________________________________________________________
    # 
    # _____________________________________________________________________________
    def makeShapesFromHistos( self, inputDir, outputDir, outputFileName, analysisName, lumi, variables, cuts, samples, structureFile, nuisances, signalPoint, fastsimMet):
    
        print "=============================="
        print "==== makeShapesFromHistos ===="
        print "=============================="
        
        self._variables = variables
        self._samples   = samples
        self._cuts      = cuts

        self._inputDir  = inputDir
        self._outputDir = outputDir

        self._fastsimMet = fastsimMet

        #self._fileIn = ROOT.TFile(inputFile, "READ")
        
        # divide the list of samples among signal, background and data
        for sampleName, sample in self._samples.iteritems():
          if structureFile[sampleName]['isSignal'] == 1 :
            self.signals.append(sampleName)
          if structureFile[sampleName]['isData'] == 1 :
            self.data.append(sampleName)
          if structureFile[sampleName]['isSignal'] == 0 and structureFile[sampleName]['isData'] == 0:
            self.backgrounds.append(sampleName)
          
        if not os.path.isdir (self._outputDir + "/") :
          os.mkdir (self._outputDir + "/")
          
        self._outFile = ROOT.TFile.Open( self._outputDir + "/" + outputFileName + signalPoint + ".root", 'recreate')
        ROOT.TH1.SetDefaultSumw2(True)
        
        # loop over cuts  
        for cutName in self._cuts :

          print "cut = ", cutName, " :: ", cuts[cutName]
          self._outFile.mkdir (cutName)

          # loop over variables
          for variableName, variable in self._variables.iteritems():

            cutNameSplit = cutName.split('_')
            print analysisName + "/" + cutNameSplit[0] + '_' + cutNameSplit[1] + '/h_' + variableName + '_' + cutNameSplit[2]
            shapeName = analysisName + "/02_" + cutNameSplit[0] + '_' + cutNameSplit[1] + '/h_' + variableName + '_' + cutNameSplit[2]
            shapeNameGen = analysisName + "/02_" + cutNameSplit[0] + 'gen_' + cutNameSplit[1] + '/h_' + variableName + 'gen_' + cutNameSplit[2]

            print "  variableName = ", variableName
            tagNameToAppearInDatacard = cutName
            self._outFile.mkdir (cutName + "/" + variableName)
           
            for sampleName in self.signals:
              inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + signalPoint + '.root'
              fileIn = ROOT.TFile(inputFile, "READ")
              #histo = fileIn.Get(shapeName)
              histo = self._getFastSimShape(fileIn, shapeName, shapeNameGen)
              histo.SetName('histo_' + sampleName)
              histo.Scale(lumi)
              histo = self._checkBadBins(histo)
              self._outFile.cd(cutName + "/" + variableName)
              histo.Write()
              fileIn.Close()
              
            for sampleName in self.backgrounds:
              inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
              fileIn = ROOT.TFile(inputFile, "READ")
              #shapeName = analysisName + "/" + cutName + '/h_' + variableName
              histo = fileIn.Get(shapeName)
              histo.SetName('histo_' + sampleName)
              histo.Scale(lumi)
              if (sampleName == "10_TTZ") :
                  histo.Scale(1.47)
              if (sampleName == "07_ZJetsHT" or sampleName == "03_VZ") :
                  histo.Scale(1.40)
              histo = self._checkBadBins(histo)
              self._outFile.cd(cutName + "/" + variableName)
              histo.Write()
              fileIn.Close()
            
            for sampleName in self.data:
              inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
              fileIn = ROOT.TFile(inputFile, "READ")
              #shapeName = analysisName + "/" + cutName + '/h_' + variableName
              histo = fileIn.Get(shapeName)
              histo.SetName('histo_' + sampleName)
              if (sampleName != "01_Data") :
                  histo.Scale(lumi)
                  nBins = histo.GetNbinsX()
                  for iBin in range(1, nBins+1):
                      yValue = histo.GetBinContent(iBin)
                      histo.SetBinError(iBin, math.sqrt(abs(yValue)))
              histo = self._checkBadBins(histo)
              self._outFile.cd(cutName + "/" + variableName)
              histo.Write()
              fileIn.Close()
                                     
            # Now make nuisances
            for nuisanceName, nuisance in nuisances.iteritems():
              
              # check if a nuisance can be skipped because not in this particular cut
              use_this_nuisance = False
              if  'cuts' in nuisance.keys() :
                for Cuts_where_to_use_nuisance  in   nuisance['cuts'] :
                  if Cuts_where_to_use_nuisance == cutName :
                    # use this niusance
                    use_this_nuisance = True
              else :
                # default is use the nuisance everywhere
                use_this_nuisance = True 
              
              if use_this_nuisance :
               
                if (nuisanceName != 'stat' and nuisanceName != 'Metfastsim' and 'MT2llBin' not in nuisanceName): # 'stat' has a separate treatment, it's the MC/data statistics
                  
                  if 'type' in nuisance.keys() : # some nuisances may not have "type" ... why?
                    print "nuisance[type] = ", nuisance ['type']," ","nuisance[name] = ", nuisance ['name']
                    if (nuisance ['type'] == 'shape' or nuisance ['type'] == 'shapeN') :
                        if 'all' in nuisance.keys() and nuisance ['all'] == 1 : # for all samples
                            print 'what about the shapes?'
                        else :
                            # apply only to selected samples
                            for sampleName in self.signals:
                                if sampleName in nuisance['samples'].keys() :
                                    # save the nuisance histograms in the root file
                                    inputFile = inputDir + '/' + nuisance['name'] + 'up/' + analysisName + '/' + sampleName + signalPoint + '.root'
                                    fileInUp = ROOT.TFile(inputFile, "READ")
                                    #histo = fileInUp.Get(shapeName)
                                    histo = self._getFastSimShape(fileInUp, shapeName, shapeNameGen)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Up")
                                    histo.Scale(lumi)
                                    histo = self._checkBadBins(histo)
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInUp.Close()
                                    inputFile = inputDir + '/' + nuisance['name'] + 'do/' + analysisName + '/' + sampleName + signalPoint + '.root'
                                    fileInDo = ROOT.TFile(inputFile, "READ")
                                    #histo = fileInDo.Get(shapeName)
                                    histo = self._getFastSimShape(fileInDo, shapeName, shapeNameGen)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Down")
                                    histo.Scale(lumi)
                                    histo = self._checkBadBins(histo)
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInDo.Close()
                                    
                            for sampleName in self.backgrounds:
                                if sampleName in nuisance['samples'].keys() :
                                    # save the nuisance histograms in the root file
                                    inputFile = inputDir + '/' + nuisance['name'] + 'up/' + analysisName + '/' + sampleName + '.root'
                                    fileInUp = ROOT.TFile(inputFile, "READ")                            
                                    histo = fileInUp.Get(shapeName)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Up")
                                    histo.Scale(lumi)
                                    if (sampleName == "10_TTZ") :
                                        histo.Scale(1.47)
                                    if (sampleName == "07_ZJetsHT" or sampleName == "03_VZ") :
                                        histo.Scale(1.40)
                                    histo = self._checkBadBins(histo)
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInUp.Close()
                                    inputFile = inputDir + '/' + nuisance['name'] + 'do/' + analysisName + '/' + sampleName + '.root'
                                    fileInDo = ROOT.TFile(inputFile, "READ")
                                    histo = fileInDo.Get(shapeName)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Down")
                                    histo.Scale(lumi)
                                    if (sampleName == "10_TTZ") :
                                        histo.Scale(1.47)
                                    if (sampleName == "07_ZJetsHT" or sampleName == "03_VZ") :
                                        histo.Scale(1.40)
                                    histo = self._checkBadBins(histo)
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInDo.Close()

                # MT2ll bin nuisances
                if 'MT2llBin' in nuisanceName:

                    print "nuisance[type] = ", nuisance ['type']," ","nuisance[name] = ", nuisance ['name']
                    for sampleName in self.backgrounds:
                        if sampleName in nuisance['samples'].keys() :

                            inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
                            fileIn = ROOT.TFile(inputFile, "READ")
                            histoTemplate = fileIn.Get(shapeName)
                            histoTemplate.Scale(lumi)
                            histoTemplate = self._checkBadBins(histoTemplate)

                            nBins = histoTemplate.GetNbinsX()
                            xInitial = histoTemplate.GetBinLowEdge(1)
                            xFinal = histoTemplate.GetBinLowEdge(nBins+1)
                            
                            histoBinUpName = 'histo_' + sampleName + '_' + (nuisance['name']) + "Up"
                            histoBinUp = ROOT.TH1F(histoBinUpName, '', nBins, xInitial, xFinal)
                            
                            histoBinDoName = 'histo_' + sampleName + '_' + (nuisance['name']) + "Down"
                            histoBinDo = ROOT.TH1F(histoBinDoName, '', nBins, xInitial, xFinal)
                      
                            for iBin in range(1, nBins+1):
                                     
                                yValue = histoTemplate.GetBinContent(iBin)

                                if ( ("Bin4" in nuisanceName and iBin==1) or 
                                     ("Bin5" in nuisanceName and iBin==2) or 
                                     ("Bin6" in nuisanceName and iBin==3) or 
                                     ("Bin7" in nuisanceName and iBin==4) ):

                                    rError = float(nuisance['samples'][sampleName])
                                    if ("Bin4" in nuisanceName and iBin==1): # Bleah: manually for the moment
                                        rError = 0.00
                                    if ("Bin5" in nuisanceName and iBin==2):
                                        rError = 0.10
                                    if ("Bin6" in nuisanceName and iBin==3):
                                        rError = 0.20
                                    if ("Bin7" in nuisanceName and iBin==4):
                                        rError = 0.30
                                    yError = yValue * rError

                                    histoBinUp.SetBinContent(iBin, yValue + yError)
                                    histoBinUp.SetBinError  (iBin, yError)
                                    histoBinDo.SetBinContent(iBin, yValue - yError)
                                    histoBinDo.SetBinError  (iBin, yError)

                                else:

                                    yError = histoTemplate.GetBinError(iBin)
                          
                                    histoBinUp.SetBinContent(iBin, yValue)
                                    histoBinUp.SetBinError  (iBin, yError)
                                    histoBinDo.SetBinContent(iBin, yValue)
                                    histoBinDo.SetBinError  (iBin, yError)
                                  
                            self._outFile.cd(cutName + "/" + variableName)
                            #histoBinUp = self._checkBadBins(histoBinUp)
                            histoBinUp.Write()
                            #histoBinDo = self._checkBadBins(histoBinDo)
                            histoBinDo.Write()

                            fileIn.Close()

                # Metfastsim https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSRecommendationsMoriond17#Special_treatment_of_MET_uncerta
                if nuisanceName == 'Metfastsim' :

                    print "nuisance[type] = ", nuisance ['type']," ","nuisance[name] = ", nuisance ['name']
                    for sampleName in self.signals:
                        if sampleName in nuisance['samples'].keys() :
                   
                            inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + signalPoint + '.root'
                            fileIn = ROOT.TFile(inputFile, "READ")
                            shapeNameUp = shapeName
                            if self._fastsimMet=="gen": 
                                shapeNameUp = shapeNameGen
                            shapeNameDo = shapeNameGen
                            if self._fastsimMet=="reco":
                                shapeNameDo = shapeName
                            histoUp = fileIn.Get(shapeNameUp)
                            histoUp.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Up")
                            histoUp.Scale(lumi)
                            histoUp = self._checkBadBins(histoUp)
                            histoDo = fileIn.Get(shapeNameDo)
                            histoDo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Down")
                            histoDo.Scale(lumi)
                            histoDo = self._checkBadBins(histoDo)
                            self._outFile.cd(cutName + "/" + variableName)
                            histoUp.Write()
                            histoDo.Write()
                            fileIn.Close()
                            

                # stat nuisances  
                if nuisanceName == 'stat' : # 'stat' has a separate treatment, it's the MC/data statistics
                
                  for sampleName in self.signals:
                    if sampleName in nuisance['samples'].keys() :

                      inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + signalPoint + '.root'
                      fileIn = ROOT.TFile(inputFile, "READ")
                      #histoTemplate = fileIn.Get(shapeName)
                      histoTemplate = self._getFastSimShape(fileIn, shapeName, shapeNameGen)
                      histoTemplate.Scale(lumi)
                      histoTemplate = self._checkBadBins(histoTemplate)

                      nBins = histoTemplate.GetNbinsX()
                      xInitial = histoTemplate.GetBinLowEdge(1)
                      xFinal = histoTemplate.GetBinLowEdge(nBins+1)
                           
                      histoUpName = 'histo_' + sampleName + '_stat' + "Up"
                      histoUp = ROOT.TH1F(histoUpName, '', nBins, xInitial, xFinal)
                      
                      histoDoName = 'histo_' + sampleName + '_stat' + "Down"
                      histoDo = ROOT.TH1F(histoDoName, '', nBins, xInitial, xFinal)
                      
                      for iBin in range(1, nBins+1):
                          
                          yValue = histoTemplate.GetBinContent(iBin)
                          yError = histoTemplate.GetBinError(iBin)
                          
                          histoUp.SetBinContent(iBin, yValue + yError)
                          histoUp.SetBinError  (iBin, yError)
                          histoDo.SetBinContent(iBin, yValue - yError)
                          histoDo.SetBinError  (iBin, yError)
                          
                          histoBinUpName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statUp'
                          histoBinUp = ROOT.TH1F(histoBinUpName, '', nBins, xInitial, xFinal)

                          histoBinDoName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statDown'
                          histoBinDo = ROOT.TH1F(histoBinDoName, '', nBins, xInitial, xFinal)
                          
                          histoBinUp.SetBinContent(iBin, yValue + yError)
                          histoBinUp.SetBinError  (iBin, yError)
                          histoBinDo.SetBinContent(iBin, yValue - yError)
                          histoBinDo.SetBinError  (iBin, yError)

                          for iBin2 in range(1, nBins+1):
                              if iBin2 != iBin:

                                  yValue2 = histoTemplate.GetBinContent(iBin2)
                                  yError2 = histoTemplate.GetBinError(iBin2)
                          
                                  histoBinUp.SetBinContent(iBin2, yValue2)
                                  histoBinUp.SetBinError  (iBin2, yError2)
                                  histoBinDo.SetBinContent(iBin2, yValue2)
                                  histoBinDo.SetBinError  (iBin2, yError2)
                                  
                        
                          self._outFile.cd(cutName + "/" + variableName)
                          histoBinUp = self._checkBadBins(histoBinUp)
                          histoBinUp.Write()
                          histoBinDo = self._checkBadBins(histoBinDo)
                          histoBinDo.Write()
                          
                          
                      self._outFile.cd(cutName + "/" + variableName)
                      histoUp = self._checkBadBins(histoUp)
                      histoUp.Write()
                      histoDo = self._checkBadBins(histoDo)
                      histoDo.Write()  
                      
                      fileIn.Close()

                  for sampleName in self.backgrounds:
                    if sampleName in nuisance['samples'].keys() :

                      inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
                      fileIn = ROOT.TFile(inputFile, "READ")
                      histoTemplate = fileIn.Get(shapeName)
                      histoTemplate.Scale(lumi)
                      if (sampleName == "10_TTZ") :
                          histoTemplate.Scale(1.47)
                      if (sampleName == "07_ZJetsHT" or sampleName == "03_VZ") :
                          histoTemplate.Scale(1.40)
                      histoTemplate = self._checkBadBins(histoTemplate)

                      nBins = histoTemplate.GetNbinsX()
                      xInitial = histoTemplate.GetBinLowEdge(1)
                      xFinal = histoTemplate.GetBinLowEdge(nBins+1)
                           
                      histoUpName = 'histo_' + sampleName + '_stat' + "Up"
                      histoUp = ROOT.TH1F(histoUpName, '', nBins, xInitial, xFinal)
                      
                      histoDoName = 'histo_' + sampleName + '_stat' + "Down"
                      histoDo = ROOT.TH1F(histoDoName, '', nBins, xInitial, xFinal)

                      for iBin in range(1, nBins+1):

                          yValue = histoTemplate.GetBinContent(iBin)
                          yError = histoTemplate.GetBinError(iBin)
                          
                          histoUp.SetBinContent(iBin, yValue + yError)
                          histoUp.SetBinError  (iBin, yError)
                          histoDo.SetBinContent(iBin, yValue - yError)
                          histoDo.SetBinError  (iBin, yError)
                          
                          histoBinUpName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statUp'
                          histoBinUp = ROOT.TH1F(histoBinUpName, '', nBins, xInitial, xFinal)

                          histoBinDoName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statDown'
                          histoBinDo = ROOT.TH1F(histoBinDoName, '', nBins, xInitial, xFinal)
                          
                          histoBinUp.SetBinContent(iBin, yValue + yError)
                          histoBinUp.SetBinError  (iBin, yError)
                          histoBinDo.SetBinContent(iBin, yValue - yError)
                          histoBinDo.SetBinError  (iBin, yError)

                          for iBin2 in range(1, nBins+1):
                              if iBin2 != iBin:

                                  yValue2 = histoTemplate.GetBinContent(iBin2)
                                  yError2 = histoTemplate.GetBinError(iBin2)
                          
                                  histoBinUp.SetBinContent(iBin2, yValue2)
                                  histoBinUp.SetBinError  (iBin2, yError2)
                                  histoBinDo.SetBinContent(iBin2, yValue2)
                                  histoBinDo.SetBinError  (iBin2, yError2)
                                  
                        
                          self._outFile.cd(cutName + "/" + variableName)
                          histoBinUp = self._checkBadBins(histoBinUp)
                          histoBinUp.Write()
                          histoBinDo = self._checkBadBins(histoBinDo)
                          histoBinDo.Write()
                          
                          
                      self._outFile.cd(cutName + "/" + variableName)
                      histoUp = self._checkBadBins(histoUp)
                      histoUp.Write()
                      histoDo = self._checkBadBins(histoDo)
                      histoDo.Write()  
                      
                      fileIn.Close()


    def _checkBadBins(self, histo):
 
        histoName = histo.GetName() 
       
        if 'Data' not in histoName :
            
            histoIntegral = histo.Integral()
            nBins = histo.GetNbinsX()
            for iBin in range(1, nBins+1):
                yValue = histo.GetBinContent(iBin)
                if yValue <= 0. :
                    histo.SetBinContent(iBin, 0.001)
            histoIntegralCorrected = histo.Integral()
            if (histoIntegralCorrected!=0 and histoIntegral > 0) :
                histo.Scale(histoIntegral/histoIntegralCorrected)

        if ('_stat' in histoName or '_ibin' in histoName) : 
            return histo    
        else :
            
            nBins = histo.GetNbinsX()
            nBins2 = 1
            for iBin in range(1, nBins+1):
                if histo.GetXaxis().GetBinCenter(iBin)>80 :
                    nBins2 += 1       
            fitHisto = ROOT.TH1F('fitHisto', '', nBins2, 0, nBins2)
        
            firstBinContent = 0.
            firstBinError = 0.
            for iBin in range(1, nBins+1):
                yValue = histo.GetBinContent(iBin)
                yError = histo.GetBinError(iBin)
                if histo.GetXaxis().GetBinCenter(iBin)>80 :
                    fitHisto.SetBinContent(iBin-nBins+nBins2, yValue)
                    fitHisto.SetBinError(iBin-nBins+nBins2, yError)
                else :
                    firstBinContent += yValue
                    firstBinError += (yError*yError)
            fitHisto.SetBinContent(1, firstBinContent)
            fitHisto.SetBinError(1, math.sqrt(firstBinError))

            fitHisto.SetName(histoName)
            return fitHisto


    def _getFastSimShape(self, fileIn, shapeName, shapeNameGen):

        historeco = fileIn.Get(shapeName)

        if self._fastsimMet=="reco" :
            return historeco
        
        histogen  = fileIn.Get(shapeNameGen)
        
        if self._fastsimMet=="gen" :
            return histogen

        nBins = historeco.GetNbinsX()
        xInitial = historeco.GetBinLowEdge(1)
        xFinal = historeco.GetBinLowEdge(nBins+1)
        
        histo = ROOT.TH1F('histo', '', nBins, xInitial, xFinal)

        for iBin in range(1, nBins+1):

            yValue = (historeco.GetBinContent(iBin) + histogen.GetBinContent(iBin))/2.
            yError = (historeco.GetBinError(iBin)   + histogen.GetBinError(iBin))/2.
            
            histo.SetBinContent(iBin, yValue)
            histo.SetBinError(iBin, yError)
            
        return histo



if __name__ == '__main__':
    print 'SHAPE MAKER'

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--tag'                , dest='tag'               , help='Tag used for the shape file name'           , default=None)
    parser.add_option('--sigset'             , dest='sigset'            , help='Signal samples [SM]'                        , default='SM')
    parser.add_option('--inputDir'           , dest='inputDir'          , help='input directory'                            , default='./')
    parser.add_option('--outputDir'          , dest='outputDir'         , help='output directory'                           , default='./')
    parser.add_option('--outputFileName'     , dest='outputFileName'    , help='output file name'                           , default='Shapes')
    parser.add_option('--analysisName'       , dest='analysisName'      , help='analysis name'                              , default='Stop')
    parser.add_option('--structureFile'      , dest='structureFile'     , help='file with datacard configurations'          , default=None )
    parser.add_option('--nuisancesFile'      , dest='nuisancesFile'     , help='file with nuisances configurations'         , default=None )
    parser.add_option('--signalPoint'        , dest='signalPoint'       , help='signal name (mass point)'                   , default='')
    parser.add_option('--fastsimMet'         , dest='fastsimMet'        , help='treatment of Met in FastSim'                , default='mix')

    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()


    print " configuration file = ", opt.pycfg
    
    print " inputDir          =          ", opt.inputDir
    print " outputDir         =          ", opt.outputDir
    print " outputFileName    =          ", opt.outputFileName
 
    if not opt.debug:
        pass
    elif opt.debug == 2:
        print 'Logging level set to DEBUG (%d)' % opt.debug
        logging.basicConfig( level=logging.DEBUG )
    elif opt.debug == 1:
        print 'Logging level set to INFO (%d)' % opt.debug
        logging.basicConfig( level=logging.INFO )
     
    factory = ShapeFactory()
    #factory._energy    = opt.energy
    factory._lumi      = opt.lumi
    factory._tag       = opt.tag
    
    # ~~~~
    variables = {}
    if os.path.exists(opt.variablesFile) :
      handle = open(opt.variablesFile,'r')
      exec(handle)
      handle.close()
    
    cuts = {}
    if os.path.exists(opt.cutsFile) :
      handle = open(opt.cutsFile,'r')
      exec(handle)
      handle.close()
    
    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()
   
    # ~~~~
    structure = {}
    if opt.structureFile == None :
       print " Please provide the datacard structure "
       exit ()
       
    if os.path.exists(opt.structureFile) :
      handle = open(opt.structureFile,'r')
      exec(handle)
      handle.close()


    # ~~~~
    nuisances = {}
    if opt.nuisancesFile == None :
       print " Please provide the nuisances structure if you want to add nuisances "
       
    if os.path.exists(opt.nuisancesFile) :
      handle = open(opt.nuisancesFile,'r')
      exec(handle)
      handle.close()
    

    factory.makeShapesFromHistos( opt.inputDir ,opt.outputDir, opt.outputFileName, opt.analysisName, opt.lumi, variables, cuts, samples, structure, nuisances, opt.signalPoint, opt.fastsimMet)
    
        
        
