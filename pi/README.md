# Required Python Libraries

## wiringpi2

````bash
sudo apt-get install python-dev python-pip
sudo pip install wiringpi2
````

## spidev

````bash
sudo apt-get install python-dev
mkdir python-spi
cd python-spi
wget https://raw.github.com/doceme/py-spidev/master/setup.py
wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c
sudo python setup.py install
````
