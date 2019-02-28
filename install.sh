# Installing all the python modules required for the program to run
echo "***************************************************************************"
echo "** Checking/Installing required python modules..."
echo "***************************************************************************"
if python -c 'import pkgutil; exit(not pkgutil.find_loader("requests"))'; then
	echo '** requests found!'
else
	echo '>> installing requests...'
	echo ''
	sudo pip install requests
	echo ''
fi

if python -c 'import pkgutil; exit(not pkgutil.find_loader("firebase"))'; then
	echo '** firebase found!'
else
	echo '>> installing firebase...'
	echo ''
	sudo pip install python-firebase
	echo ''
fi

echo "***************************************************************************"
echo "** Checking/Creating the required folders..."
echo "***************************************************************************"
# Creating a Projects directory if it doesn't exist
if [ -d "/home/pi/Projects" ]; then
	echo "** /home/pi/Projects Directory exists!"
else
	mkdir /home/pi/Projects
	echo ">> New directory /home/pi/Projects created!"
fi

# Creating WaterLevelSensor directory if it doesn't exist
if [ -d "/home/pi/Projects/WaterLevelSensor" ]; then
	echo "** /home/pi/Projects/WaterLevelSensor directory exists!"
else
	mkdir /home/pi/Projects/WaterLevelSensor
	echo ">> New directory /home/pi/Projects/WaterLevelSensor created!"
fi

# Creating Log directory if it doesn't exist
if [ -d "/home/pi/Projects/WaterLevelSensor/Log" ]; then
	echo "** /home/pi/Projects/WaterLevelSensor/Log directory exists!"
else
	mkdir /home/pi/Projects/WaterLevelSensor/Log
	echo ">> New directory /home/pi/WaterLevelSensor/Log created!"
fi

echo ""
echo "***************************************************************************"
echo "** Checking/Copying python files..."
echo "***************************************************************************"
# Checking if the main python file is present or not
if [ -f "/home/pi/Projects/WaterLevelSensor/water_level_sensor.py" ]; then
	echo "** water_level_sensor.py exists!"
else
	sudo cp water_level_sensor.py /home/pi/Projects/WaterLevelSensor/
	echo ">> water_level_sensor.py copied to /home/pi/Projects/WaterLevelSensor/"
fi

# Checking if the firebase_link python file is present or not
if [ -f /home/pi/Projects/WaterLevelSensor/firebase_link.py ]; then
	echo "** File firebase_link is present!"
else
	# Add Firebase link either in this file or in the created file
	# Add the link without the trailing '/'
	echo "FIREBASE_PATH=\"add_your_link_here_without_the_last_/\"" > /home/pi/Projects/WaterLevelSensor/firebase_link.py
	echo ">> Created firebase_link.py in /home/pi/Projects/WaterLevelSensor/ path!"
	echo "!!!! Add your firebase link to 'firebase_link.py' to ** FIREBASE_PATH ** variable !!!!"
	echo "!!!! Remove the last trailing '/' for the link to work !!!!"
fi

