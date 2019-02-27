# importing all required modules
import RPi.GPIO as GPIO
import time
from firebase import firebase
import glob
import logging
import logging.handlers

# Getting Firebase DB Path from firebase_link.py
from firebase_link import FIREBASE_PATH

# Setting up LOGGER
LOG_FILENAME = '/home/pi/Projects/WaterLevelSensor/Log/wls_log'
wls_logger = logging.getLogger('wls_log')
wls_logger.setLevel(logging.DEBUG)
# Setting up Timed Rotating File Handler
handler = logging.handlers.TimedRotatingFileHandler(\
	LOG_FILENAME, when="midnight", backupCount=1000)
wls_logger.addHandler(handler)


# ASSUMPTIONS:
# Speed of sound in air = 34300 cm/s
# Change the value here if required
speed_of_sound = 34300

# if distance less than a minumum threshold; set STATUS = OFF
# if distance greater than a maximum threshold; set STATUS = ON
MIN_DISTANCE = 10 #cm
MAX_DISTANCE = 20 #cm

# Setting up the Pi for GPIO
# Setting up in BCM mode
# For pin config in this mode, visit: https://pinout.xyz/
GPIO.setmode(GPIO.BCM)
# Disable Warings
GPIO.setwarnings(False)

# Change the following PIN no's to change the circuit
TRIG = 23
ECHO = 24

# Setting the appropriate PIN mode
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function that reads distance from the HC-SR04 sensor
def read_distance():
	# Clearing the TRIG Pin
	GPIO.output(TRIG, False)
	# Waiting for sensor to settle( 10us // minimum is 2us)
	time.sleep(0.00001)
	
	# Sending TRIG Pulse
	GPIO.output(TRIG, True)
	# Stopping the Pulse after 10us
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	
	# Calculating Pulse duration and distance
	# Initially when the pulse is being sent, the ECHO is LOW
	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
	# After the Pulse is sent, the ECHO becomes HIGH
	while GPIO.input(ECHO)==1:
		pulse_end=time.time()
	# Difference in time is the duration
	pulse_duration = pulse_end - pulse_start
	# Calculating: distance = speed * time
	distance = int(pulse_duration * (speed_of_sound / 2))
	
	print(str(distance)+" cm")
	wls_logger.debug("Distance: "+str(distance)+" cm")
	return distance

# Setting up communication with the Firebase DB
# Change the FIREBASE_PATH variable in firebase_link.py file to connect to
# a different Firebase DB
firebase = firebase.FirebaseApplication(FIREBASE_PATH, authentication=None)

# Getting the status of the MAIN SWITCH
def is_main_switch_on():
	main_switch = firebase.get('/main_switch', None)
	if main_switch == "ON":
		return True
	else:
		return False

# Getting the status of Motor Switch
def is_motor_switch_on():
	motor_switch = firebase.get('/motor_switch', None)
	if motor_switch == "ON":
		return True
	else:
		return False


# Change the MOTOR SWITCH status in the FB-DB
def set_motor_switch_status(status):
	if status:
		print('Motor Switched ON')
		wls_logger.debug('Motor Switched ON')
		firebase.put('/', "motor_switch", "ON")
	else:
		print('Motor Swtiched OFF')
		wls_logger.debug('Motor Swtiched OFF')
		firebase.put('/', "motor_switch", "OFF")

# Change the MAIN SWITCH status in the FB-DB
def set_main_switch_status(status):
	if status:
		firebase.put('/', "main_switch", "ON")
	else:
		firebase.put('/', "main_switch", "OFF")

# Put the changed data into FB-DB
def set_distance(distance):
	firebase.put('/', 'distance', distance)
	print('Distance Updated!')
	wls_logger.debug('Distance Updated!')


# Checking Distance Treshold
def is_distance_over_threshold(distance, prev_status=True):
	if distance <= MIN_DISTANCE:
		return False
	elif distance >= MAX_DISTANCE:
		return True
	else:
		return prev_status

# initialise all the global variables
def init_all():
	global distance, motor_running_status
	wls_logger.debug("\n\nStarted at: "+ str(time.ctime()))
	try:
		# Fetching initial distance from FB-DB
		distance = firebase.get('/distance', None)
		# Fetch initial Motor running status from FB-DB
		motor_running_status = is_motor_switch_on()
	except:
		print('Error fetching data from Firebase!')
		wls_logger.debug('Error fetching data from Firebase!')
		return False
	else:
		print('Initial distance fetched from FB-DB!')
		wls_logger.debug('Initial distance fetched from FB-DB!')
		print('Initial Motor running status fetched from FB-DB!')
		wls_logger.debug('Initial Motor running status fetched from FB-DB!')
		return True

# Running the entire mechanism
def run_mechanism():
	global distance, motor_running_status
	
	try:
		# Checking main_switch status
		if not is_main_switch_on():
			return
	except:
		print('Error fetching main_switch status from Firebase!')
		wls_logger.debug('Error fetching main_switch status from Firebase!')
		return
	
	try:
		# Read the new distance
		new_distance = read_distance()
	except:
		print('Error reading data from the sensor!')
		wls_logger.debug('Error reading data from the sensor!')
		return
	
	# Check if the new_distance read is different from the old data
	if new_distance != distance:
		distance = new_distance
	else:
		return
	
	try:
		# Set the distance in FB DB
		set_distance(distance)
	except:
		print('Error setting the distance in Firebase!')
		wls_logger.debug('Error setting the distance in Firebase!')
		return
	
	# Set the motor running status depending on the distance threshold
	new_motor_running_status = is_distance_over_threshold(distance, motor_running_status)
	
	# Check if the new motor status is different from the old one
	if new_motor_running_status != motor_running_status:
		motor_running_status = new_motor_running_status
		try:
			# Setting the motor running status in Firebase
			set_motor_switch_status(motor_running_status)
		except:
			print('Error setting the motor running status in Firebase')
			wls_logger.debug('Error setting the motor running status in Firebase')
			return
	
	# Check if motor running
	#if not motor_running_status:
		#return

# Main run function
# Only need to call it and then leave it alone
def run():
	while True:
		run_mechanism()
		# Sleeping for 200ms after each run
		time.sleep(0.200)

# initialise global variables
while not init_all():
	# Sleeping for 100ms after a failure
	time.sleep(0.100)
# Calling the main run function to run everything
run()
