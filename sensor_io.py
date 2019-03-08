# importing all required modules
import RPi.GPIO as GPIO
import time

# ASSUMPTIONS:
# Speed of sound in air = 34300 cm/s
# Change the value here if required
speed_of_sound = 34300

# if distance less than a minumum threshold; set STATUS = OFF
# if distance greater than a maximum threshold; set STATUS = ON
MIN_DISTANCE = 10 #cm
MAX_DISTANCE = 20 #cm
MAX_DISTANCE_SUMP = 20 #cm

# Setting up the Pi for GPIO
# Setting up in BCM mode
# For pin config in this mode, visit: https://pinout.xyz/
GPIO.setmode(GPIO.BCM)
# Disable Warings
GPIO.setwarnings(False)

# Change the following PIN no's to change the circuit
# Reading distance of Main Tank
TRIG = 23
ECHO = 24
# Reading distance of SUMP
TRIG_SUMP = 27
ECHO_SUMP = 22

# Motor Switch to set on/off
MOTOR_SWITCH = 25 # Will be connected to the relay middle pin

# The parallel switch which will control whether the motor is on/off
NORMAL_SWITCH = 16
SWITCH_STATUS = False
SWITCH_SOFT_STATUS = SWITCH_STATUS

# Setting the appropriate PIN mode
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG_SUMP, GPIO.OUT)
GPIO.setup(ECHO_SUMP, GPIO.IN)

# Setting the appropriate PIN mode switch
GPIO.setup(NORMAL_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set the motor_switch as On/Off
# Since motor switch will be connected to a relay,
# This will update teh relay with the "status"
def set_motor_switch(status):
	#global SWITCH_STATUS
	global SWITCH_SOFT_STATUS
	SWITCH_SOFT_STATUS = status
	#SWITCH_STATUS = status
	if status:
		print('Motor turned ON')
		GPIO.setup(MOTOR_SWITCH, GPIO.OUT)
		GPIO.output(MOTOR_SWITCH, True)
	else:
		print('Motor turned OFF')
		GPIO.setup(MOTOR_SWITCH, GPIO.IN)
		#GPIO.output(MOTOR_SWITCH, False)

# Read the physical switch:
# Since it is connected to GND, by default it is HIGH
# and on press, it becomes LOW
# So, if the button is pressed, reverse the existing status and return
def read_normal_switch():
	global SWITCH_STATUS, SWITCH_SOFT_STATUS
	if not GPIO.input(NORMAL_SWITCH):
		SWITCH_STATUS = not SWITCH_STATUS
		SWITCH_SOFT_STATUS = SWITCH_STATUS
		time.sleep(0.100)
	return SWITCH_STATUS

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
	# Setting a limitation to the infinite loop
	iter_count = 0
	# Initially when the pulse is being sent, the ECHO is LOW
	while GPIO.input(ECHO)==0:
		iter_count+=1
		pulse_start = time.time()
		if iter_count >= 50000:
			raise Exception("Cannot read from the sensor!")
	
	# Setting a limitation to the infinite loop
	iter_count = 0
	# After the Pulse is sent, the ECHO becomes HIGH
	while GPIO.input(ECHO)==1:
		iter_count+=1
		pulse_end=time.time()
		if iter_count >= 50000:
			raise Ecxeption("Cannot read from the sensor!")
	
	# Difference in time is the duration
	pulse_duration = pulse_end - pulse_start
	# Calculating: distance = speed * time
	distance = int(pulse_duration * (speed_of_sound / 2))
	
	print(str(distance)+" cm")
	#wls_logger.debug("Distance: "+str(distance)+" cm")
	return distance

# Function that reads distance of sump from the HC-SR04 sensor
def read_distance_sump():
	# Clearing the TRIG Pin
	GPIO.output(TRIG_SUMP, False)
	# Waiting for sensor to settle( 10us // minimum is 2us)
	time.sleep(0.00001)
	
	# Sending TRIG Pulse
	GPIO.output(TRIG_SUMP, True)
	# Stopping the Pulse after 10us
	time.sleep(0.00001)
	GPIO.output(TRIG_SUMP, False)
	
	# Calculating Pulse duration and distance
	# Setting a limitation to the infinite loop
	iter_count = 0
	# Initially when the pulse is being sent, the ECHO is LOW
	while GPIO.input(ECHO_SUMP)==0:
		iter_count+=1
		pulse_start = time.time()
		if iter_count >= 50000:
			raise Exception("Cannot read from the sensor! 1")
	
	# Setting a limitation to the infinite loop
	iter_count = 0
	# After the Pulse is sent, the ECHO becomes HIGH
	while GPIO.input(ECHO_SUMP)==1:
		iter_count+=1
		pulse_end=time.time()
		if iter_count >= 50000:
			raise Ecxeption("Cannot read from the sensor! 2")
	
	# Difference in time is the duration
	pulse_duration = pulse_end - pulse_start
	# Calculating: distance = speed * time
	distance = int(pulse_duration * (speed_of_sound / 2))
	
	print(str(distance)+" cm")
	#wls_logger.debug("Distance: "+str(distance)+" cm")
	return distance

# Checking Distance Treshold for main Tank
def is_distance_over_threshold(distance, prev_status=True):
	if distance <= MIN_DISTANCE:
		return False
	elif distance >= MAX_DISTANCE:
		return True
	else:
		return prev_status
# Checking Distance Treshold for sump
def is_distance_sump_over_threshold(distance):
	if distance >= MAX_DISTANCE_SUMP:
		return True
	else:
		return False
