# -*- coding: utf-8 -*-
import visa

def openVisaResource(address):
	''' 
	openVisaResource(address)
	
	Creates the instrument handle 
	
	Arguments:
	
    address:GPIB address :Integer	
	'''
	try:
		rm = visa.ResourceManager()
		instrument = rm.open_resource('GPIB0::'+str(address)+'::INSTR')
		return instrument
	except:
		print('openVisaResource ERROR')
		return -1

   
def getInstrumentName(intstrument):
	''' 
	getInstrumentName(intstrument)
	
	Returns the instrument name
    
	Arguments:
	
    intstrument:Instrument handle from 'openVisaResource()'	
	'''
	try:
		name = inst.query("*IDN?")
		return name
	except:
		print('getInstrumentName ERROR')
		return -1
	
def setCorrectionParameters(intstrument,cable_length=4,
							corr_method,open_corr,short_corr,
							load_corr,load_type,correction_channel):
	''' 
	setCorrectionParameters(intstrument,cable_length,
							correction_method,open_correction,
							short_correction,load_correction,
							load_type,correction_channel)
							
	Carries our any corrections before the measurements 
	
	Arguments:
	
	intstrument:Instrument handle from 'openVisaResource()'
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

		name = inst.write(command)
		return 1
	except:
		print('setCorrectionParameters ERROR')
		return -1
		
def SetSignalLevelAndFrequency(intstrument,frequency,       						voltage_or_current,
							   is_voltage_signal,
							   auto_level_control):
	''' 
	SetSignalLevelAndFrequency(intstrument,frequency,       											   voltage_or_current,
							   is_voltage_signal,
							   auto_level_control)
	
	Sets the Signal type(Voltage or current), level and frequency
    
	Arguments:
	
    intstrument:Instrument handle from 'openVisaResource()'
    frequency: Frequency in Hz: Float/Decimal
	voltage_or_current: Volts if voltage and Amps if current:Float/Decimal,
	is_voltage_signal: True/False,
	auto_level_control:OFF/ON	
	'''
	def isVoltageSignal(mykey,value):
    return {
        'True': 'VOLT'+str(value)+'V',
        'False': 'CURR  '+str(value)+'A'
    }[mykey] 
	
	try:
		command= 'FREQ'+ str(frequency)+'HZ'+
			';:'+isVoltageSignal(is_voltage_signal,voltage_or_current)+
			';:AMPL:ALC '+auto_level_control

		name = inst.write(command)
		return 1
	except:
		print('SetSignalLevelAndFrequency ERROR')
		return -1		
		
		                                                                          