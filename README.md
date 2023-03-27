# iOS REST Battery
A REST API for reporting the battery percentage of jailbroken iOS devices

## Installation

### Requirements
- Jailbroken iOS device (only 32-bit devices are supported at the moment)
- Terminal/SSH access to your iOS device
- git cli (`apt-get install git`)
- Python 2.5.1 (`apt-get install python`)

## Setup
1. Meet the requirements
2. Follow the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to generate an SSH key on your iOS device to be able to access GitHub
3. Run `cat /path/to/<your key>.pub` and copy its contents to this [GitHub](https://github.com/settings/ssh/new) page
4. Clone this repository to your iOS device (`git clone git@github.com:ShonP40/iOS-MQTT-Battery.git`)
5. Install `batterydata-arm32.deb` using `dpkg -i batterydata-arm32.deb`
6. cd into the repository
7. Start the script by running `python script.py`