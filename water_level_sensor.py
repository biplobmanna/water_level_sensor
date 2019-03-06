# importing all required modules
import time
# import custom python modules
import sensor_io as sio
import firebase_io as fio
from logger import wls_logger as log

# IF no connection to the internet the following data will be used
# Change this to modify the default parameters
DISTANCE_DEFAULT = sio.read_distance()
DISTANCE_SUMP_DEFAULT = sio.read_distance_sump()
MOTOR_STATUS_DEFAULT = False
SUMP_PRESENT = False

# initialise all the global variables
def init_all():
	global distance, motor_running_status, sump_present, distance_sump
	# Setting the motor as off, for safety purposes
	sio.set_motor_switch(False)
	log.debug("\n\nStarted at: "+ str(time.ctime()))
	try:
		# Fetching initial distance from FB-DB
		distance = fio.get_distance()
		# Fetch initial Motor running status from FB-DB
		motor_running_status = fio.is_motor_switch_on()
		# Fetching initial distance_sump from FB-DB
		distance_sump = fio.get_distance_sump()
		# Fetching initial data to check if sump is present or not
		sump_present = fio.is_sump_present()
	except:
		print('Error fetching data from Firebase!')
		log.debug('Error fetching data from Firebase!')
		# Setting all data as default, so that the program runs without Internet
		distance = DISTANCE_DEFAULT
		distance_sump = DISTANCE_SUMP_DEFAULT
		motor_running_status = MOTOR_STATUS_DEFAULT
		sump_present = SUMP_PRESENT_DEFAULT
	else:
		print('Initial distance fetched from FB-DB!')
		log.debug('Initial distance fetched from FB-DB!')
		print('Initial Motor running status fetched from FB-DB!')
		log.debug('Initial Motor running status fetched from FB-DB!')
		print('Initial distance_sump fetched from FB-DB!')
		log.debug('Initial distance_sump fetched from FB-DB!')
		print('Success fetching sump present or not from FB-DB!')
		log.debug('Success fetching sump present or not from FB-DB!')

# Main Switch Operation
def main_switch_op():
	try:
		# Checking main_switch status
		if not fio.is_main_switch_on():
			return False
	except:
		print('Error fetching main_switch status from Firebase!')
		log.debug('Error fetching main_switch status from Firebase!')
		# If Pi cannot connect to the Internet, assume main_switch is "ON"
		return True
	return True

# Distance Operation
def distance_op():
	global distance
	try:
		# Read the new distance
		new_distance = sio.read_distance()
		# For testing -- uncomment the below, comment the above as required
		#new_distance = int(raw_input("Enter distance:"))
		#from random import randint
		#new_distance = randint(0,30)
	except:
		print('Error reading distance data from the sensor!')
		log.debug('Error reading distance data from the sensor!')
		return False
	
	# Check if the new_distance read is different from the old data
	if new_distance != distance:
		distance = new_distance
	else:
		return True
	
	# Set the new distance in FB-DB
	try:
		# Set the distance in FB DB
		fio.set_distance(distance)
	except:
		print('Error setting the distance in Firebase!')
		log.debug('Error setting the distance in Firebase!')
		# If internet connection error, still continue working smoothly!
		return True
	return True

# Distance Sump Operation
def distance_sump_op():
	global distance_sump, sump_present
	if not sump_present:
		return True
	try:
		new_distance_sump = sio.read_distance_sump()
	except:
		print('Error reading distance_sump from the sensor!')
		log.debug('Error reading distance_sump from the sensor!')
		return False
	# Check if the new_distance_sump is different from old data
	if new_distance_sump != distance_sump:
		distance_sump = new_distance_sump
	else:
		return True
	# Set the new distance_sump in FB-DB
	try:
		fio.set_distance_sump(distance_sump)
	except:
		print('Error setting distance_sump into firebase!')
		log.debug('Error setting distance_sump into firebase!')
		# If no internet connection, still continue running smoothly
		return True
	return True

# Setting Motor Running Status Operation
def motor_run_op():
	global distance, distance_sump, motor_running_status, sump_present
	# Set the motor running status depending on the distance threshold
	new_motor_running_status = sio.is_distance_over_threshold(distance, motor_running_status)
	
	# Check if sump present or not, if present, checking if water present or not
	# If water is not present, it is by default True
	if sump_present:
		sump_water_present = not sio.is_distance_sump_over_threshold(distance_sump)
	else:
		sump_water_present = True
	
	# Doing a boolean operation of new_motor_running_status and sump_water_present
	new_motor_running_status = new_motor_running_status and sump_water_present

	# Check if the new motor status is different from the old one
	if new_motor_running_status != motor_running_status:
		motor_running_status = new_motor_running_status
		try:
			# Setting the motor running status in Firebase
			fio.set_motor_switch_status(motor_running_status)
		except:
			print('Error setting the motor running status in Firebase')
			log.debug('Error setting the motor running status in Firebase')
	return motor_running_status

# Running the entire mechanism
def run_mechanism():
	# If h/w switch is off, switch off motor
	# Perform no operation no-matter what be the case
	if not sio.read_normal_switch():
		sio.set_motor_switch(False)
		return
	
	# If s/w  main_switch is off, switch off motor
	if not main_switch_op():
		sio.set_motor_switch(False)
		return
	
	# If distance operation has any error, set off motor
	if not distance_op():
		sio.set_motor_switch(False)
		return
	
	# If sump distance operation has any error, set off motor
	if not distance_sump_op():
		sio.set_motor_switch(False)
		return
	
	motor_running_status = motor_run_op()
	# Set motor running status to motor switch
	sio.set_motor_switch(motor_running_status)

# Main run function
# Only need to call it and then leave it alone
def run():
	# Initialise all global variables
	init_all()
	while True:
		run_mechanism()
		# Sleeping for 200ms after each run
		time.sleep(0.200)

# Running th Program
run()
