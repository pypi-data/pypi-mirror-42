'''
  This is a Python port of the Arduino library for
  the One Pin Keypad Board:
  (https://github.com/ProgettoCompany/Progetto_One_Pin_Keypad_Arduino_Library)
  which can be purchased here:
  (https://www.tindie.com/products/Progetto/one-pin-keypad/)
  It supports 3x4 and 4x4 membrane keypads and outputs
  the key you pressed as a character, based on an
  analog value this ananlog value is converted to digital using an ADS1115 ADC:
  (https://www.adafruit.com/product/1085)
  Written y: John Wolf, Progetto
  Based on code by: Hari Wiguna: https://www.youtube.com/watch?v=G14tREsVqz0
'''
import time
from timeit import default_timer as timer
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)
_pin = 0
# analog values that correspond to each button:
thresholds = [
  225,    # 1
  2116,   # 2
  3904,   # 3
  5200,   # A
  6300,   # 4
  7350,   # 5
  8450,   # 6
  9325,   # B
  10000,  # 7
  10750,  # 8
  11500,  # 9
  12100,  # C
  12550,  # *
  13100,  # 0
  13800,  # #
  14250   # D
]

# Keypad char values (button names):
buttonIDs = ['1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D']

class OnePinKeypad:
    NO_TIMEOUT = 0
    key_value = '\0'
    
    def __init__(self, pin):
        _pin = pin

    def analog_read(self):
        chan = AnalogIn(ads, _pin)
        return chan.value

    def use_calibrated_thresholds(self, calibrated_thresholds):
        # replace thresholds with calibratedThresholds
        for i in range(16):
            thresholds[i] = calibrated_thresholds[i]

    '''
    Returns the input from the keypad at the moment this function
    is executed. Note that the function does not wait for input
    from the keypad, and returns null if no key is being pressed
    during the keypad value check.
    @return char representing pressed key, or null if no input is detected.
    '''
    def read_keypad_instantaneous(self): # Read the input on the analog pin
        analog_value = OnePinKeypad.analog_read(self)

        key_value = '\0'
        
        # FOR DEBUG:
        # print("analog_value: " + str(analog_value))
        
        # If no button is being pressed, return null
        if analog_value > 20000:
            key_value = '\0'

        else:
            # Compare the input value to each threshold value
            for i in range(16):
                # Check value against keypad thresholds
                thresholdCheck = analog_value - thresholds[i]
                if abs(thresholdCheck) <= 200:
                    # return the name of the key closest to the input value
                    thresholdCheck = 0
                    key_value = buttonIDs[i]
        return key_value

    '''
    Waits until keypad input is received, or the timeout expires,
    should it be set, in which case a null is returned
    @return a char representing the keypad input or a null, if no
    input is detected before the timeout expires
    @timeout value specified in milliseconds, set to 0 if are to
    wait indefinitely
    '''
    def read_keypad_with_timeout(self, timeout):
        key_value = '\0'

        if timeout == 0:
            while True:
                key_value = OnePinKeypad.read_keypad_instantaneous(self)
                if key_value != '\0':
                    # Wait until the button is released
                    while OnePinKeypad.analog_read(self) < 20000:
                        time.sleep(0.1)
                    break
                time.sleep(0.01)
        else:
            start = timer()
            end = timer()
            delta = int(1000 * (end - start))
            while delta < timeout:
                key_value = OnePinKeypad.read_keypad_instantaneous(self)
                if key_value != '\0':
                    # Wait until the button is released
                    while OnePinKeypad.analog_read(self) < 20000:
                        time.sleep(0.1)
                    break
                time.sleep(0.01)
                end = timer()
                delta = int(1000 * (end - start))

        return key_value
