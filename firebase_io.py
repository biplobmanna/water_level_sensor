# importing all required modules
import time
from firebase import firebase

# Getting Firebase DB Path from firebase_link.conf
# Reading link from firebase_link.conf
try:
	with open("firebase_link.conf","r") as fblink:
		FIREBASE_PATH=fblink.readline().strip()
	if not len(FIREBASE_PATH)>0:
		raise Exception("File is empty!")
except:
	print("firebase_link.conf file not found!\nOR, File is empty!")


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
		firebase.put('/', "motor_switch", "ON")
	else:
		print('Motor Swtiched OFF')
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

# Fetch the distance from FB-DB
def get_distance():
	return firebase.get('/distance', None)
