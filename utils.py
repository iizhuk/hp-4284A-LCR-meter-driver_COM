#!/usr/bin/env python
__author__ = "Leonard Kogos"
__copyright__ = "NONE"
__credits__ = ["Leonard Kogos"]
__license__ = "NONE"
__version__ = "1.0.1"


import visa
import numpy as np
import time
import logging
import os.path

def openVisaResource(address):
    ''' 
    openVisaResource(address)
    
    Creates the intsrument handle 

    Arguments:
    
    address:GPIB address :Integer   
    '''
    try:
        rm = visa.ResourceManager()
        inst_handle = rm.open_resource('GPIB0::'+str(address)+'::INSTR')
        return inst_handle
    except:
        logging.getLogger().error("openVisaResource ERROR", 
                                   exc_info=True)
        print('openVisaResource ERROR')
        return -1

   
def initInstrument(inst_handle,do_reset):
    ''' 
    initInstrument(inst_handle)
    
    Initializes the instrument and returns the instrument name
    
    Arguments:
    
    inst_handle:intsrument handle from 'openVisaResource()' 
    do_reset:True/False
    
    '''
    try:
        name = inst_handle.query("*IDN?")
        if do_reset:
            inst_handle.write("*RST")
            
        inst_handle.write("*CLS")
        return name
    except:
        logging.getLogger().error("getintstrumentName ERROR", 
                                   exc_info=True)
        print('getintstrumentName ERROR')
        return -1
    
    
def setCorrectionParameters(inst_handle,cable_length,
                            corr_method,open_corr,short_corr,
                            load_corr,load_type,correction_channel):
    ''' 
    setCorrectionParameters(inst_handle,cable_length,
                            correction_method,open_correction,
                            short_correction,load_correction,
                            load_type,correction_channel)
                            
    Carries our any corrections before the measurements 
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    cable_length: Length in meters : Positive Integer 
    correction_method:SING/MULT
    open_correction:True/False
    short_correction:True/False
    load_correction:True/False
    load_type:CPD/CPQ/CPG/CPRP/CSD/CSQ/
              CSRS/LPQ/LPD/LPG/LPRP/LSD/
              LSQ/LSRS/RX/ZTD/ZTR/GB/YTD/YTR
    correction_channel: Channel to use (Integer)
    '''
    def isOn(mykey):
        return {
            True: 'ON',
            False: 'OFF'
        }[mykey] 
    try:
        command= '''CORR:LENG {clen} M;:CORR:METH {method}
                ;:CORR:OPEN:STAT {open}
                ;:CORR:SHORT:STAT {short}
                ;:CORR:LOAD:STAT {load}
                ;:CORR:LOAD:TYPE {load_t}
                ;:CORR:USE {channel}'''.format(
                clen=str(cable_length),
                method=corr_method,
                open=isOn(open_corr),
                short=isOn(short_corr),
                load=isOn(load_corr),
                load_t=load_type,
                channel=correction_channel)
                
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("setCorrectionParameters ERROR", 
                                   exc_info=True)
        print('setCorrectionParameters ERROR')
        return -1
        
def setSignalLevelAndFrequency(inst_handle,frequency,                               
                               voltage_or_current,
                               is_voltage_signal,
                               auto_level_control):
    ''' 
    SetSignalLevelAndFrequency(inst_handle,frequency,                                          
                               voltage_or_current,
                               is_voltage_signal,
                               auto_level_control)
    
    Sets the Signal type(Voltage or current), level and frequency
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    frequency: Frequency in Hz: Float/Decimal
    voltage_or_current: Volts if voltage and Amps if current:Float/Decimal,
    is_voltage_signal: True/False,
    auto_level_control:True/False  
    '''
    def isVoltage(mykey,value):
        return {
            True: 'VOLT '+str(value)+'V',
            False: 'CURR  '+str(value)+'A'
        }[mykey] 
        
    def isOn(mykey):
        return {
            True: 'ON',
            False: 'OFF'
        }[mykey] 
    
    try:
        command= '''FREQ {freq}HZ
                    ;:{isV}
                    ;:AMPL:ALC {alc}'''.format(
                    freq=frequency,
                    isV=isVoltage(is_voltage_signal,voltage_or_current),
                    alc=isOn(auto_level_control))
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("SetSignalLevelAndFrequency ERROR", 
                                   exc_info=True)
        print('SetSignalLevelAndFrequency ERROR')
        return -1   


def setIntegrationTime(inst_handle,aperture_type,
                 averaging_rate):
    ''' 
    setIntegrationTime(inst_handle,aperture_type,
                 averaging_rate)
    
    Sets the integration time
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    aperture_type:SHOR/MED/LONG 
    averaging_rate: 1 to 128 
    '''

    try:
        command='''APER {type},{av_rate}'''.format(
                    type=aperture_type,
                    av_rate=str(averaging_rate))
        
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("setIntegrationTime ERROR", 
                                   exc_info=True)
        print('setIntegrationTime ERROR')
        return -1

def setBiasVoltageDC(inst_handle,voltage):
    ''' 
    setBiasVoltageDC(inst_handle,voltage averaging_rate)
    
    Sets the Bias Voltage
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    voltage:Value in Volts   
    '''
    try:
        command='BIAS:VOLT ' +str(voltage)+ 'V'
                
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("setBiasVoltageDC ERROR", 
                                   exc_info=True)
        print('setBiasVoltageDC ERROR')
        return -1
        
def changeStateVoltageDC(inst_handle,state):
    ''' 
    changeStateVoltageDC(inst_handle,state)
    
    Sets the Bias Voltage
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    state: (Number)1 for ON or 0 for OFF     
    '''
    try:
        command='BIAS:STAT '+str(state)
                
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("changeStateVoltageDC ERROR", 
                                   exc_info=True)
        print('changeStateVoltageDC ERROR')
        return -1
        
def setImpedance(inst_handle,impedance_range,
                 auto_range,impedance_type):
    ''' 
    setImpedance(inst_handle,impedance_range,
                 auto_range,impedance_type)
    
    Sets the impedance
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    impedance_range:Impedance in OHMS
    auto_range:True/False
    impedance_type:CPD/CPQ/CPG/CPRP/CSD/CSQ/CSRS/LPQ/
                   LPD/LPG/LPRP/LSD/LSQ/LSRS/RX/ZTD/
                   ZTR/GB/YTD/YTR   
    '''
    def isOn(mykey):
        return {
            True: 'ON',
            False: 'OFF'
        }[mykey] 
    
    try:
        command='''FUNC:IMP:RANG {range}OHM
                   ;:FUNC:IMP:RANG:AUTO {auto_r}
                   ;:FUNC:IMP {type}'''.format(
                range=impedance_range,
                auto_r=isOn(auto_range),
                type=impedance_type)
        
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("setImpedance ERROR", 
                                   exc_info=True)
        print('setImpedance ERROR')
        return -1
    
def selectDisplay(inst_handle,display_type,is_page):
    ''' 
    setDisplay(inst_handle,display_type)
    
    Selects the Display
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    display_type:MEAS/BNUM/BCO/LIST/MSET/CSET/LTAB/LSET/
                 SYST/CAT/SELF 
                 (if display page) else: 
                 Any string for display line
    is_page: Select whether it is display page or line: True/False
    
    '''
    def isPage(mykey,value):
        return {
            'True': 'DISP:PAGE  {v}'.format(v=value),
            'False': 'DISP:LINE \"{v}\"'.format(v=value)
        }[mykey] 
    
    try:
        command=isPage(is_page,display_type)
                
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("selectDisplay ERROR", 
                                   exc_info=True)
        print('selectDisplay ERROR')
        return -1

        
def setTrigger(inst_handle,continuous,source,delay):
    ''' 
    setTrigger(inst_handle,continuous,source,delay):
    
    Sets the Trigger
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    continuous:OFF/ON
    source:INT/EXT/BUS/HOLD
    delay:Time in seconds decimal number
    
    '''
    try:
        command='''INIT:CONT {cont}
        ;:TRIG:SOUR {src}
        ;:TRIG:DEL {dly}'''.format(
        cont=continuous,
        src=source,
        dly=delay)
                
        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("setTrigger ERROR", 
                                   exc_info=True)
        print('setTrigger ERROR')
        return -1
    
                         
def sendTrigger(inst_handle):
    ''' 
    sendTrigger(inst_handle):
    
    Sends the Trigger. Should be called after: setTrigger()
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    
    '''
    try:
        command='TRIG:IMM'

        result = inst_handle.write(command)
        return 1
    except:
        logging.getLogger().error("sendTrigger ERROR", 
                                   exc_info=True)
        print('sendTrigger ERROR')
        return -1
    
def fetchData(inst_handle):
    ''' 
    fetchData(inst_handle):
    
    Fetches the data
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    
    '''
    
    WAIT_TIME_SEC=0.25
    
    try:
        
        values = inst_handle.query_ascii_values('FETC?', 
                  container=np.array)
        time.sleep(WAIT_TIME_SEC) 
        return values
    except:
        logging.getLogger().error("fetchData ERROR", 
                                   exc_info=True)
        print('fetchData ERROR')
        return -1

def runCVLoop(inst_handle,freq,VBias,filename,parent):
    ''' 
    fetchData(inst_handle):
    
    Fetches the data
    
    Arguments:
    
    inst_handle:instrument handle from 'openVisaResource()'
    freq:Frequency in HZ at which to measure CV
    VBias:Array with voltage data points at which to measure Capacitance
    
    '''
    CMeas = []
    GMeas = []
    omega = 2.0 * np.pi * freq
    save_path = 'Data'
    fullName = os.path.join(save_path, filename+".csv")   
    f = open(fullName, 'w+')
    f.write('Voltage (V), Capacitance_P (F), Conductance_P (S)\r')
    f.close()
    
    try:
        for v in VBias:
            #Set Bias Voltage - Turn on Bias Voltage - Pause - Read Front Panel
            setBiasVoltageDC(inst_handle,v)
            time.sleep(1.0)
            changeStateVoltageDC(inst_handle,1)#Turns on DC Bias
            time.sleep(6.0)
            data=fetchData(inst_handle)#Get Capacitance Reading
                 
            C = data[0]
            G = data[1]
            
            
            f = open(fullName, 'a')
            f.write(str(v) + ',' + str(C) + ',' + str(G) + '\r')
            f.close()
           
            CMeas.append(C)
            GMeas.append(G)
            
            #Check if Leakage Current is gettting too High
            Q = (omega*C) / G
            
            print('Q:'+str(Q))
            if np.abs(Q) < 5.0:
                print('Leakage Current is gettting too High')
                break	
        parent.updatePlot(VBias,CMeas,GMeas)      
    except:
        logging.getLogger().error("runCVLoop ERROR", 
                                   exc_info=True)
        print('runCVLoop ERROR')
        return -1       


   
