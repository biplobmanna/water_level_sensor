echo ""
echo "***************************************************************************"
# Installing daemontools
echo ">> Checking and installing the latest daemmontools ..."
echo "***************************************************************************"
echo ""
sudo apt-get install daemontools daemontools-run
echo ""

echo "***************************************************************************"
echo "** Setting up daemontools..."
echo "***************************************************************************"
# Adding a daemontools startup entry to rc.local
# so that the program runs on boot
if grep -q "csh -cf 'svscanboot &'" "/etc/rc.local"; then
	echo "** daemontools entry in /etc/rc.local present"
else
	sudo sh -c "echo \"csh -cf 'svscanboot &'\" >> /etc/rc.local"
	echo ">> Added daemontools entry in /etc/rc.local"
fi

# Creating a Service directory inside /etc/service
if [ -d /etc/service/water_level_sensor ]; then
	echo "** water_level_sensor service exists!"
else
	echo ">> creating water_level_sensor service..."
	sudo mkdir /etc/service/water_level_sensor
fi

# Creating a run file for the service
if [ -f /etc/service/water_level_sensor/run ]; then
	echo "** run file for the service exists..."
else
	sudo cp run /etc/service/water_level_sensor/
	sudo chmod u+x /etc/service/water_level_sensor/run
	echo ">> Copied and changed permission of 'run' into /etc/service/water_level_sensor/"
fi

# Restarting the RPi in 10 secs
echo ""
echo "***************************************************************************"
echo "** The RPi will restart in 5 mins..."
echo "***************************************************************************"
echo "** Take this time to add the firebase-database link in firebase_link.py"
echo "** The file is present in /home/pi/Projects/WaterLevelSensor/"
echo "** Add the path to the FIREBASE_PATH variable.."
echo "** Ensure that the trailing '/' is deleted..."
echo "***************************************************************************"
echo "** The setup is successful!"
echo "** Awating restart..."
echo "***************************************************************************"

sudo shutdown +5
