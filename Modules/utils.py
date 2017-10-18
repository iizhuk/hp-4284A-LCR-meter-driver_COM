#!/usr/bin/env python
__author__ = "Leonard Kogos"
__copyright__ = "NONE"
__credits__ = ["Leonard Kogos"]
__license__ = "NONE"
__version__ = "1.0.1"


import visa
import numpy
import time

def openVisaResource(address):
	''' 
	openVisaResource(address)
	
	Creates the intsrument handle 
	
	Arguments:
	
    address:GPIB address :Integer	
	'''
	try:
		rm = visa.ResourceManager()
		inst_handle = rm.open_resource('GPIB0::'+str(address)+'::inst_handleR')
		return inst_handle
	except:Exception:
		logging.getLogger().error("openVisaResource ERROR", 
		                           exc_info=True)
		print('openVisaResource ERROR')
		return -1

   
def getintstrumentName(inst_handle):
	''' 
	getintstrumentName(inst_handle)
	
	Returns the instrument name
    
	Arguments:
	
    inst_handle:intsrument handle from 'openVisaResource()'	
	'''
	try:
		name = inst_handle.query("*IDN?")
		return name
	except:Exception:
		logging.getLogger().error("getintstrumentName ERROR", 
		                           exc_info=True)
		print('getintstrumentName ERROR')
		return -1
	
	
def setCorrectionParameters(inst_handle,cable_length=4,
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
	open_correction:OFF/ON
	short_correction:OFF/ON
	load_correction:OFF/ON
	load_type:CPD/CPQ/CPG/CPRP/CSD/CSQ/
			  CSRS/LPQ/LPD/LPG/LPRP/LSD/
			  LSQ/LSRS/RX/ZTD/ZTR/GB/YTD/YTR
	correction_channel: Channel to use (Integer)
	'''	
	try:
	command= 'CORR:LENG'+ str(cable_length)+'M'+
			';: CORR:METH '+corr_method+
			';:CORR:OPEN:STAT '+open_corr+
			';:CORR:SHORT:STAT '+short_corr+
			';:CORR:LOAD:STAT '+load_corr+
			';:CORR:LOAD:TYPE '+load_type+
			';:CORR:USE '+correction_channel

		result = inst_handle.write(command)
		return 1
	except:Exception:
		logging.getLogger().error("setCorrectionParameters ERROR", 
		                           exc_info=True)
		print('setCorrectionParameters ERROR')
		return -1
		
def SetSignalLevelAndFrequency(inst_handle,frequency,       						voltage_or_current,
							   is_voltage_signal,
							   auto_level_control):
	''' 
	SetSignalLevelAndFrequency(inst_handle,frequency,       								   voltage_or_current,
							   is_voltage_signal,
							   auto_level_control)
	
	Sets the Signal type(Voltage or current), level and frequency
    
	Arguments:
	
    inst_handle:instrument handle from 'openVisaResource()'
    frequency: Frequency in Hz: Float/Decimal
	voltage_or_current: Volts if voltage and Amps if current:Float/Decimal,
	is_voltage_signal: True/False,
	auto_level_control:OFF/ON	
	'''
	def isVoltage(mykey,value):
    return {
        'True': 'VOLT'+str(value)+'V',
        'False': 'CURR  '+str(value)+'A'
    }[mykey] 
	
	try:
		command= 'FREQ'+ str(frequency)+'HZ'+
			';:'+isVoltage(is_voltage_signal,voltage_or_current)+
			';:AMPL:ALC '+auto_level_control

		result = inst_handle.write(command)
		return 1
	except:Exception:
		logging.getLogger().error("SetSignalLevelAndFrequency ERROR", 
		                           exc_info=True)
		print('SetSignalLevelAndFrequency ERROR')
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
	auto_range:ON/OFF
	impedance_type:CPD/CPQ/CPG/CPRP/CSD/CSQ/CSRS/LPQ/
				   LPD/LPG/LPRP/LSD/LSQ/LSRS/RX/ZTD/
				   ZTR/GB/YTD/YTR	
	'''
	try:
		command='FUNC:IMP:RANG '+impedance_range+'OHM'+
                ';:FUNC:IMP:RANG:AUTO '+auto_range+
                ';:FUNC:IMP '+impedance_type
				
		result = inst_handle.query(command)
		return 1
	except:Exception:
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
        'True': 'DISP:PAGE  '+value,
        'False': 'DISP:LINE \"'+value'\"'
    }[mykey] 
	
	try:
		command=isPage(is_page,display_type)
				
		result = inst_handle.query(command)
		return 1
	except:Exception:
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
		command='INIT:CONT '+continuous+
		';:TRIG:SOUR '+source+
        ';:TRIG:DEL '+str(delay)

				
		result = inst_handle.query(command)
		return 1
	except:Exception:
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

		result = inst_handle.query(command)
		return 1
	except:Exception:
		logging.getLogger().error("sendTrigger ERROR", 
		                           exc_info=True)
		print('sendTrigger ERROR')
		return -1
	
def fetchData(inst_handle):
	WAIT_TIME_SEC=0.25
	''' 
	fetchData(inst_handle):
	
	Fetches the data
    
	Arguments:
	
    inst_handle:instrument handle from 'openVisaResource()'
	
	'''
	try:
		
		values = inst_handle.query_ascii_values('FETC?', 
		          container=numpy.array)
		time.sleep(WAIT_TIME_SEC) 
		return values
	except:Exception:
		logging.getLogger().error("fetchData ERROR", 
		                           exc_info=True)
		print('fetchData ERROR')
		return -1
