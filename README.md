## Water Level Sensor
### Description:
Need to read the water level in a tank using [HC SR04 UltraSonic Sensor](https://www.amazon.in/dp/B078J3L8LD/ref=cm_sw_em_r_mt_dp_U_bAQDCb5DWQCZC) and [Raspberry Pi 3b+](https://www.amazon.in/dp/B07BDR5PDW/ref=cm_sw_em_r_mt_dp_U_WDQDCbZ4T3C44) and send the data to Firebase. 

### Setup Raspberry Pi 3b+ for Headless Config
* Download Latest Raspbian image
* Flash image to SD card using any image write tool. (Recommended: Balena Etcher)
* Create an empty file **ssh** on the _**boot**_ partition of the SD card. 
* Create an empty file **wpa_supplicant.conf** and put the following details inside it, and save:
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
