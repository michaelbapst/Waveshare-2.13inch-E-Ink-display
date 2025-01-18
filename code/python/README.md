Python Code:<br><br>
I'm assumming that you have your Waveshare 2.13in E-Ink display correcly setup with your hardware. I'm using Waveshare 2.13in E-Ink display HAT V4 connecteted to a Raspberry Pi Zero 2W. If you haven't set it up yet, visit https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual and follow the directions for your hardware.<br><br>
This next step is for use with Raspberry Pi hardware.<br><br>
Install the necessary python libraries:<code>
sudo apt update<br>
sudo apt install python3-pip<br>
sudo apt install python3-pil<br>
sudo apt install python3-numpy<br>
sudo apt install python3-gpiozero<br>
sudo pip3 install spidev<br>
</code><br>
For WeatherInk.py, GeoPy and Open-Meteo libraries are needed:<code>
pip install openmeteo-requests<br>
pip install requests-cache retry-requests numpy pandas<br>
pip install geopy<br>
</code>
