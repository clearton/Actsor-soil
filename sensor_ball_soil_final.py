#SENSOR_BALL_SOIL

import time
import os
import glob

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
#adc_a = Adafruit_ADS1x15.ADS1115()

#ADS for Sensor_Ball_Soil (12-bit)
adc_a = Adafruit_ADS1x15.ADS1015(0x48)
adc_b = Adafruit_ADS1x15.ADS1015(0x49)
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

#For Digital temperature sensor (from file: thermometer.py)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

#device_folder = glob.glob(base_dir + '28*')[0]
device_folder = glob.glob(base_dir + '28-0215525*')[0] #sensor temperature 1
device_folder2 = glob.glob(base_dir + '28-031503*')[0] #sensor temperature 2
device_file = device_folder + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'
temp_out1 = 0
temp_out2 = 0

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    #print lines
    f.close()
    return lines

def read_temp_raw2():
    f2 = open(device_file2, 'r')
    lines2 = f2.readlines()
    f2.close()
    return lines2

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
        print lines
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return temp_f

#while True:
#print(read_temp())
# read_temp()
# time.sleep(1)

def read_temp2():
    lines2 = read_temp_raw2()
    while lines2[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines2 = read_temp_raw2()
        print lines2
    equals_pos2 = lines2[1].find('t=')
    if equals_pos2 != -1:
        temp_string2 = lines2[1][equals_pos2+2:]
        temp_c2 = float(temp_string2)/1000.0
        temp_f2 = temp_c2 * 9.0 / 5.0 + 32.0
        return temp_f2

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN1 = 2/3  #for ADC 1
GAIN2 = 2/3  #for ADC 2

#12 bits factor conversion - Change if the GAIN change.
factor12_a =  6144/2047
factor12_b =  6144/2047

# print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# print ('SENSOR BALL SOIL')
# print('| {0:>8} | {1:>8} | {2:>8} | {3:>8} | {4:>8} | {5:>8} | {6:>8} #|'.format('NO2-(pH)','NO3-
#(pH)','K+(pH)','Moisture','DO(mg/L)','Temp1(F)','Temp2(F)'))
#print('-' * 78)
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values_a = [0]*4
    values_b = [0]*4
    #++ For Digital temperature sensor
    temp_out1 = read_temp()
    temp_out2 = read_temp2()
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values_a[i] = adc_a.read_adc(i, gain=GAIN1)
        values_b[i] = adc_b.read_adc(i, gain=GAIN2)
    # Note you can also pass in an optional data_rate parameter that controls
    # the ADC conversion time (in samples/second). Each chip has a different
    # set of allowed data rate values, see datasheet Table 9 config register
    # DR bit values.
    #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
    # Each value will be a 12 or 16 bit signed integer value depending on the
    # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    #print('| {0:>8} | {1:>8} | {2:>8} | {3:>8} | {4:>8} | {5:>8} | {6:>8} |'.format(values_b[0],values_b[1],values_b[2],values_a[0],values_a[1],temp_out1,((((values_b[3]*factor12_a)-500)/10)*9/5)+32))
    
    #ADS1015 12-Bit ADC (Address: 0x49)
    #NICO sensors, resolution: (56 +/-6)mV / pH
    #Outputs of NICO sensors in pH and ppm:
    #N02- : (4.6 to 8) pH | (460 to 0.5) ppm    ADC->A0
    #NO3- : (2 to 11) pH | (62,000 to 0.4) ppm  ADC->A1
    #K+   : (1 to 9) pH  | (39,000 to 0.04) ppm ADC->A2
    
    #ADS1015 12-Bit ADC (Address: 0x48)
    #Moisture sensor, Unknown resolution or some conversion factor.       ADC->A0
    
    #Dissolved Oxygen (DO), 12 bit resolution: 0.014 mg/L, Range: 0 to 15 mg/L (or ppm)  |  (Sensor_lecture = Intercept + Voltage *Slope) Note: Voltage in V ADC->A1
    #Intercept = 13.720 (source: www.vernier.com/manuals/do-bta/#section8)
    #Slope = -3.838     (source: www.vernier.com/manuals/do-bta/#section8)
    do_intercept = 13.720
    do_slope = -3.838
# print('| {0:>8} | {1:>8} | {2:>8} | {3:>8} | {4:>8} | {5:>8} | {6:>8} #|'.format(values_b[0]*factor12_b/56,values_b[1]*factor12_b/56,values_b[2]*fac#tor12_b/56,values_a[0]*factor12_a,(((values_a[1]*factor12_a)/1000)*do_slope)+ #do_intercept,temp_out1,temp_out2))
#OUTPUT for AWS IoT
print values_b[0]*factor12_b/56,values_b[1]*factor12_b/56,values_b[2]*factor12_b/56,values_a[0]*factor12_a,(((values_a[1]*factor12_a)/1000)*do_slope)+do_intercept,temp_out1,temp_out2
#print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values_a))
#Pause for half a second.
#time.sleep(0.5)


