## Sensing the Water Level in a Tank
### Description:
* Two tanks are present:
	* An **overhead tank**, which is mandatory.
	* An **underground sump**, which is optional. 
* Need to connect 2 **Ultrasonic Depth Sensor** to measure the water level. 
	* One will be connected to the overhead tank. 
	* One will be connected to the underground sump. 
* Need to measure the depth of the water in both the tanks at **realtime**.
* A motor is connected which will pump water based on the following conditions:
	* If **underground sump** is present:
		* If the water depth in the overhead tank is greater than a **max threshold**, i.e., tank is empty, and if the water depth in the underground sump is _**lesser**_ than a **threshold**, i.e., Water is present in the underground sump.
			* Only then, switch **`Motor ON`**
		* If the water depth in the overhead tank becomes lesser than a **min threshold**, i.e., tank is full, or if the water depth in the underground sump becomes _**greater**_ than a **threshold**, i.e., Water is not present in the underground sump.
			* Switch **`Motor OFF`**
		* For all other cases, maintain the **previous state** of the motor.
	* If **underground sump** is not present:
		* If the water depth in the overhead tank is greater than a **max threshold**, i.e., tankl is empty.
			* Switch **`Motor ON`**
		* If the water depth in the overhead tank is lesser than a **min threshold**, i.e, tank is full.
			* Switch **`Motor OFF`**
		* For all other cases, maintain the **previous state** of the motor.
* A main **HW Switch** is also connected to the circuit, which can turn on the motor at leisure provided that the tank is not full to the brim and the sump(if present) has water in it to pump. 
* All the realtime **depths, motor status** is sent to firebase, which can then be viewed from a Mobile Application. 
* A **Software main switch** is also present, which can control the circuit On/Off from the Mobile App. 


### Hardware Requirements
* Raspberry Pi any model, either with inbuilt WiFi or with a WiFi dongle.
* Breadboard
* Jumper Wires
* Two HC-SR04 Ultrasonic Depth Sensor
* Two resistors **each** of 1 kOhm, 2kOhm


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
* **ssh into Pi** using `ssh pi@<your_pi_IP_in_your_router>`, or follow the instructions in the [link.](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup) 
* Default **password** is **`raspberry`**
* **Update** Pi repositories using `sudo apt-get update`


### Connecting the **HC SR04** sensor to the Pi
* Visit this [website](https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi) to setup the Pi and the sensor. 
* Setup the resistors and other connections according to the schematic provided in the [website](https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi). Keep the _**resistors connection the same**_, only change the **TRIG, ECHO** pins connection as per the information below.
* Since, there are 2 HC-SR04 sensors required for this project, connect the **Pins** as per the following:
	* For the 1st sensor, which will be connected to the main tank, connect to **`GPIO`** numbers:
		* `TRIG = 23`
		* `ECHO = 24`
	* For the 2nd sensor, which will be connected to the underground sump, connect:
		* `TRIG = 27`
		* `ECHO = 22`
	* All the GPIO numbering is as per **BCM mode**. To check the GPIO Layout of RPi, visit [here.](https://pinout.xyz/)
* For both the sensors, connect **Vcc** of the sensor to any of the **5V** pin of the Pi, and **Gnd** of the sensor to any of **Gnd** pins of the Pi.


### Connecting the Motor Switch and the Main H/W Switch
* Connect the **Motor Switch** to `GPIO 25`
	* For demo purposes, connect an LED to `GPIO 25`
	* To setup connections to LED, take help from this [website.](https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins)
* Connect the **Main HW Switch** to `GPIO 16`
	* Setup the connection of the switch as per this [website](https://electrosome.com/using-switch-raspberry-pi/).
	* For trial purposes, if **nothing is connected to the pin** it is **set to `True` by default.**
	* To **set it as `False`** connect a jumper wire between **`GPIO 16`** and **`Gnd`**


### Steps after all circuit-connections are made
* Once everything is connected properly, follow the **first part** of the **Installing and Setup**. 
* __Test the program to check if everything is working.__
* Once everything works, run the 2nd part of **Installing and Setup** to setup autorun using **daemontools**


### Installing and Setup
#### Part 1:
* Either `git clone` or download zip of the repository to any location on Pi. 
* Preferably use `git clone <<link_to_remote_git>>`. Get the link from the repository. 
* `cd` into the directory.
* `ls` in the same path to check all the files as present in the repository. 
* Run **install.sh** using `./install.sh`
	* If any error in **permissions**, change permission of **install.sh** using `chmod +rwx install.sh`
* After successful execution of the above, a file **firebase_link.conf** will be created in the project path `~/Projects/WaterLevelSensor/`
	* Inside the **firebase_link.conf** file, put the **link to firebase-database** in the **first line.**
	* **Without the link to firebase-database** present in the **conf** file, the main program will not execute.
	* **Remember to remove the last '/' of the link**
* Run the main program using: `python ~/Projects/WaterLevelSensor/water_level_sensor.py`
* *******************************************************************************************
#### Part 2:
* Once verified the run of the main program, follow the below steps.
* Run **setup_daemontools.sh** using `./setup_daemontools.sh`
	* If any error in **permissions**, change permission of **setup_daemontools.sh** using `chmod +rwx setup_daemontools.sh`
* Once everything executes successfully, Pi will reboot after 1 min. 
* A service will be created using **daemontools** named **water_level_sensor** and will run automatically thereafter. 
* To read up on daemontools, and/or to manage services using daemontools, visit [here](http://samliu.github.io/2017/01/10/daemontools-cheatsheet.html), and/or [here](https://cr.yp.to/daemontools.html), and/or [here.](https://isotope11.com/blog/manage-your-services-with-daemontools)


### Aliases for handling daemontools service
* The script **setup_daemontools.sh** has setup some aliases to start/stop/pause/status the **water_level_sensor** services
* The list of aliases are as follows:
	* `wls_start` --> Starts the service
	* `wls_stop`  --> Stops the service
	* `wls_pause` --> Pauses the service
	* `wls_stat`  --> Checks the status of the service
* Use the above aliases to manipulate the service.


### Project Path and Logs
* Project path in RPi is `~/Projects/WaterLevelSensor/`
* Logs are present in `~/Projects/WaterLevelSensor/Log/`
* Check the Logs or your firebase database to see if the program is working or not. 
