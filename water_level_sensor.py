# importing all required modules
import time
# import custom python modules
import sensor_io as sio
import firebase_io as fio
from logger import wls_logger as log

# initialise all the global variables
def init_all():
	global distance, motor_running_status
	log.debug("\n\nStarted at: "+ str(time.ctime()))
	try:
		# Fetching initial distance from FB-DB
		distance = fio.get_distance()
		# Fetch initial Motor running status from FB-DB
		motor_running_status = fio.is_motor_switch_on()
	except:
		print('Error fetching data from Firebase!')
		log.debug('Error fetching data from Firebase!')
		return False
	else:
		print('Initial distance fetched from FB-DB!')
		log.debug('Initial distance fetched from FB-DB!')
		print('Initial Motor running status fetched from FB-DB!')
		log.debug('Initial Motor running status fetched from FB-DB!')
		return True

# Running the entire mechanism
def run_mechanism():
	global distance, motor_running_status
	
	try:
		# Checking main_switch status
		if not fio.is_main_switch_on():
			return
	except:
		print('Error fetching main_switch status from Firebase!')
		log.debug('Error fetching main_switch status from Firebase!')
		return
	
	try:
		# Read the new distance
		new_distance = sio.read_distance()
	except:
		print('Error reading data from the sensor!')
		log.debug('Error reading data from the sensor!')
		return
	
	# Check if the new_distance read is different from the old data
	if new_distance != distance:
		distance = new_distance
	else:
		return
	
	try:
		# Set the distance in FB DB
		fio.set_distance(distance)
	except:
		print('Error setting the distance in Firebase!')
		log.debug('Error setting the distance in Firebase!')
		return
	
	# Set the motor running status depending on the distance threshold
	new_motor_running_status = sio.is_distance_over_threshold(distance, motor_running_status)
	
	# Check if the new motor status is different from the old one
	if new_motor_running_status != motor_running_status:
		motor_running_status = new_motor_running_status
		try:
			# Setting the motor running status in Firebase
			fio.set_motor_switch_status(motor_running_status)
		except:
			print('Error setting the motor running status in Firebase')
			log.debug('Error setting the motor running status in Firebase')
			return

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
