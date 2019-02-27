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

### Installing and Setup
* Either `git clone` or download zip of the repository to any location on Pi. 
* Preferably use `git clone <<link_to_remote_git>>`. Get the link from the repository. 
* `ls` in the same path to check all the files as present in the repository. 
* Change permission of **install.sh** using `sudo chmod +rwx install.sh`
* Run **install.sh** using `./install.sh`
* Follow the instructions on screen. 
* Pi will reboot after 5 mins, take that time to setup the Firebase Database link in the appropriate file, as given in the instructions in the setup. 
* A service will be created using **daemontools** named **water_level_sensor** and will run automatically. 

To manage services using daemontools, visit [here](http://samliu.github.io/2017/01/10/daemontools-cheatsheet.html), and/or [here.](https://cr.yp.to/daemontools.html)
