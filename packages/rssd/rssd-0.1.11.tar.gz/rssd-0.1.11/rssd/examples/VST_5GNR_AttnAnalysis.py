##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Sweep FSW/SMW Frequncy
### Author:  mclim
### Date:    2018.05.17
##########################################################
### User Entry
##########################################################
SMW_IP = '192.168.1.114'                    #IP Address
FSW_IP = '192.168.1.109'                    #IP Address
freqArry = [24e9, 26e9, 28e9, 39e9]
pwrArry = range(-30,0,5)

##########################################################
### Code Start
##########################################################
from rssd.SMW_5GNR_K144 import VSG
from rssd.FSW_5GNR_K144 import VSA
from rssd.FileIO        import FileIO
import time

OFileCSV = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFileCSV)  #Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFileCSV)  #Create FSW Object

##########################################################
### Instrument Settings
##########################################################

### SMW Setup
SMWArb = SMW.Get_ArbInfo()
SMWPwr = SMW.Get_PowerInfo()
SMW.Set_RFState('ON')                       #Turn RF Output on

### FSW Setup
FSW.Set_SweepCont(0)
FSW.Set_Span(fSpan)

### CCDF Setup
FSW.write('INST:CRE:NEW SAN,"CCDF";*OPC?')  #Create Channel
FSW.write(':INST:SEL "CCDF";*OPC?')         #Select Channel
FSW.Set_CCDF('ON')
FSW.Set_CCDF_BW(100)
FSW.Set_CCDF_Samples(2e9)

### 5G Setup
FSW.Init_5GNR()

for freq in freqArry:
    for pwr in pwrArry:
        SMW.Set_RFPwr(pwr)                  #Output Power
        SMW.Set_Freq(freq)
        FSW.Set_Freq(freq)

        ### Measure CCDF
        FSW.Set_Channel("CCDF")
        FSW.Set_Autolevel()
        ccdf = FSW.Get_CCDF()
        
        ### Measure Best EVM
        FSW.Set_Autolevel()
        amps1 = FSW.Get_AmpSettings()
        #AutoEVM
        amps2 = FSW.Get_AmpSettings()

        OFileCSV.write(f'{freq},{pwr},{SMWPwr},{SMWArb},{amps1},{amps2},{ccdf}')

SMW.jav_ClrErr()                          #Clear Errors
FSW.jav_ClrErr()                          #Clear Errors
