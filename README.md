## Water Level Sensor
### Description:
Need to read the water level in a tank using [HC SR04 UltraSonic Sensor](https://www.amazon.in/dp/B078J3L8LD/ref=cm_sw_em_r_mt_dp_U_bAQDCb5DWQCZC) and [Raspberry Pi 3b+](https://www.amazon.in/dp/B07BDR5PDW/ref=cm_sw_em_r_mt_dp_U_WDQDCbZ4T3C44) and send the data to Firebase. 

### Setup Raspberry Pi 3b+ for Headless Config
* Download Latest Raspbian image
* Flash image to SD card using any image write tool. (Recommended: Balena Etcher)
* Create an empty file **ssh** on the _**boot**_ partition of the SD card. 
* Create an empty file **wpa_supplicant.conf** on the _**boot**_ partition and put the following details inside it, and save:
```bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=IN

network={
	ssid="<<your_wifi_ssid>>"
	psk="<<your_wifi_password>>"
	key_mgmt=WPA-PSK
}
```
Change the **country** code to your respectieve country ISO 2 code. 
* Remove the SD card from the computer, plug it into Pi and boot. 

For additional/detailed information to setup Pi-Headless, google it, or visit [here.](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup)
* Pi will connect to WiFi. Open router-page, find the IP of Pi, and ssh into Pi, or follow the link above to set it up. 
* Update Pi repositories using `sudo apt-get update`

### Connecting the **HC SR04** sensor to the Pi
* Visit this [website](https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi) to setup the Pi and the sensor. 
* To check the Pin Layout of RPi, visit [here.](https://pinout.xyz/)
* Once everything is connected properly, follow the **first part** of the instructions. 
* Test the program to check if everything is working. 
* Once everything works, setup the program to autorun using **daemontools**

### Installing and Setup
* Either `git clone` or download zip of the repository to any location on Pi. 
* Preferably use `git clone <<link_to_remote_git>>`. Get the link from the repository. 
* `cd` into the directory.
* `ls` in the same path to check all the files as present in the repository. 
* Change permission of **install.sh** using `sudo chmod +rwx install.sh`
* Run **install.sh** using `./install.sh`
* Check the running of the python program `~/Projects/WaterLevelSensor/water_level_sensor.py`
* *******************************************************************************************
* Once verified, need to run the `setup_daemontools.sh` Change permission of **setup_daemontools.sh** using `sudo chmod +rwx setup_daemontools.sh`
* Run **setup_daemontools.sh** using `./setup_daemontools.sh`
* Follow the instructions on screen. 
* Pi will reboot after 5 mins, take that time to setup the Firebase Database link in the appropriate file, as given in the instructions in the setup. 
* A service will be created using **daemontools** named **water_level_sensor** and will run automatically. 

To manage services using daemontools, visit [here](http://samliu.github.io/2017/01/10/daemontools-cheatsheet.html), and/or [here.](https://cr.yp.to/daemontools.html)

### Aliases for handling daemontools service
* The script **setup_daemontools.sh** has setup some aliases to start/stop/pause/status the **water_level_sensor** services
* The list of aliases are as follows:
	* `wls_start` --> Starts the service
	* `wls_stop`  --> Stops the service
	* `wls_pause` --> Pauses the service
	* `wls_stat`  --> Checks the status of the service

### Project Path and Logs
* Project path in RPi is `~/Projects/WaterLevelSensor/`
* Logs are present in `~/Projects/WaterLevelSensor/Log/`
* Check the Logs or your firebase database to see if the program is working or not. 
