sudo apt install byobu
sudo apt update
sudo apt upgrade

# I2S activation from
# https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-and-test
sudo nano /boot/config.txt
# uncomment #dtparam=i2s=on

sudo nano /etc/modules
# add i2c-dev and snd-bcm2835

sudo reboot

# Check if modules loaded
lsmod | grep snd

# Prepare for manually compilling i2s support
sudo apt-get update
sudo apt-get install rpi-update
sudo rpi-update
sudo reboot

# Install dependencies
sudo apt-get install git bc libncurses5-dev bison flex libssl-dev

# Copy kernel and compile
sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
sudo chmod +x /usr/bin/rpi-source
/usr/bin/rpi-source -q --tag-update
rpi-source --skip-gcc

# Compile I2S module
sudo mount -t debugfs debugs /sys/kernel/debug
git clone https://github.com/PaulCreaser/rpi-i2s-audio
nano my_loader.c

# Change
"3f203000.i2s" -> "20203000.i2s"

make -C /lib/modules/$(uname -r )/build M=$(pwd) modules
sudo insmod my_loader.ko

# Load module on start
sudo cp my_loader.ko /lib/modules/$(uname -r)
echo 'my_loader' | sudo tee --append /etc/modules > /dev/null
sudo depmod -a
sudo modprobe my_loader

# Check if everything is fine
arecord -l
arecord -D plughw:0 -c1 -r 48000 -f S32_LE -t wav -V mono -v file.wav

#-----------------------------------------------------------------------
# Change password
sudo su
passwd pi

# Change hostname on local network
sudo nano /etc/hosts
sudo nano /etc/hostname
# Change raspberrypi to nanny
sudo reboot

# Install pyenv
sudo apt-get update && sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev openssl bzip2
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

sudo nano ~/.bashrc
# Add
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

pyenv install 3.7.11
pyenv virtualenv 3.7.11 nanny

git clone https://github.com/LudwikBielczynski/nanny.git
cd nanny
pyenv activate nanny
/home/pi/.pyenv/versions/3.7.11/envs/nanny/bin/python3.7 -m pip install --upgrade pip

# install requirements for opencv
# general tools (35.8 MB)
sudo apt-get install build-essential cmake git pkg-config
# image formats (0.9 MB)
sudo apt-get install libjpeg-dev libpng-dev
# video formats (32.1 MB)
sudo apt-get install libavcodec-dev libavformat-dev
sudo apt-get install libswscale-dev libdc1394-22-dev
# video back engine (0.6 MB)
sudo apt-get install libv4l-dev v4l-utils
# the GTK+2 GUI (175 MB)
sudo apt-get install libgtk2.0-dev libcanberra-gtk* libgtk-3-dev
# install only if your have a RPi OS lite with no desktop
sudo apt-get install python3-dev python3-numpy python3-pip
sudo apt-get install python-dev python-numpy
# parallel framework (2.7 MB)
# don't install if your having a 1 core CPU (like RPi zero)
sudo apt-get install libtbb2 libtbb-dev

sudo apt-get install libtiff-dev gfortran openexr libatlas-base-dev opencl-headers

pip install -r requirements.txt


sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools