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

# Checking Distance Treshold
def is_distance_over_threshold(distance, prev_status=True):
	if distance <= MIN_DISTANCE:
		return False
	elif distance >= MAX_DISTANCE:
		return True
	else:
		return prev_status
