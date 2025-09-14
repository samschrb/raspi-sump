My order of operations differ from the original author's.
Install.md is useful, but refers to steps that will pull down the original raspi-sump which is based on an ultrasonic sensor

My install steps:

Put Raspian image on SD card
Update Pi
sudo apt install git
sudo apt install python3-pip
Install VL53L0X
  Run VL53L0X as user (not sudo) to test functionality of sensor
Git Raspi-Sump to /opt/raspi-sump
Install Raspi-Sump
  sudo python setup.py build
  sudo python setup.py install
sudo apt get install python3-numby
sudo apt get install python3-matplotlib
sudo apt get install python3-pandas
Install Services according to install.md
Install web server according to install.md
