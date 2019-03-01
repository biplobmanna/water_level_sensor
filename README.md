## Water Level Sensor
### Description:
Need to read the water level in a tank using [HC SR04 UltraSonic Sensor](https://www.amazon.in/dp/B078J3L8LD/ref=cm_sw_em_r_mt_dp_U_bAQDCb5DWQCZC) and [Raspberry Pi 3b+](https://www.amazon.in/dp/B07BDR5PDW/ref=cm_sw_em_r_mt_dp_U_WDQDCbZ4T3C44) and send the data to Firebase. 

### Setup Raspberry Pi for Headless Config
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
* **For additional/detailed information to setup Pi-Headless, google it, or visit [here.](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup)**
* Pi will **connect to WiFi.**
* Alternatively, you can directly connect your Pi **via Ethernet cable to router.**
* Open **router-page**, find the IP of Pi -- **default hostname of the pi is `raspberrypi`**
* **ssh into Pi** using `ssh pi@<your_pi_IP_in_your_router>`, or follow the instructions in the [link.](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup) Default **password** is **`raspberry`**
* **Update** Pi repositories using `sudo apt-get update`

### Connecting the **HC SR04** sensor to the Pi
* Visit this [website](https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi) to setup the Pi and the sensor. 
* Setup the resistors and other connections according to the schematic provided in the [website](https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi). Keep the _**resistors connection the same**_, only change the **TRIG, ECHO** pins connection as per the information below.
* Since, there are 2 HC-SR04 sensors required for this project, connect the **Pins** as per the following:
	* For the 1st sensor, which will be connected to the main tank, connect:
		* `TRIG = 23`
		* `ECHO = 24`
	* For the 2nd sensor, which will be connected to the underground sump, connect:
		* `TRIG = 27`
		* `ECHO = 22`
	* All the Pin numbering is as per **BCM mode**. To check the Pin Layout of RPi, visit [here.](https://pinout.xyz/)
* For both the sensors, connect **Vcc** of the sensor to any of the **3V** pin of the Pi, and **Gnd** of the sensor to any of **Gnd** pins of the Pi.

### Connecting the Motor Switch and the Main H/W Switch'
* Connect the **Motor Switch** to `PIN 25`
	* For demo purposes, connect an LED to `PIN 25`
	* To setup connections to LED, take help from this [website.](https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins)
* Connect the **Main HW Switch** to `PIN 16`
	* Setup the connection of the switch as per this [website](https://electrosome.com/using-switch-raspberry-pi/).
	* For trial purposes, if **nothing is connected to the pin** it is **set to `True` by default.**
	* To **set it as `False`** connect a jumper wire between **`PIN 16`** and **`Gnd`**

### Steps after all circuit-connections are made
* Once everything is connected properly, follow the **first part** of the **Installing and Setup**. 
* **Test the program to check if everything is working. **
* Once everything works, run the 2nd part of **Installing and Setup** to setup autorun using **daemontools**

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

To manage services using daemontools, visit [here](http://samliu.github.io/2017/01/10/daemontools-cheatsheet.html), and/or [here](https://cr.yp.to/daemontools.html), and/or [here.](https://isotope11.com/blog/manage-your-services-with-daemontools)

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
