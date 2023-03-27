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
4. Clone this repository to your iOS device (`git clone git@github.com:ShonP40/iOS-REST-Battery.git`)
5. Clone the `SimpleJSON` repository to your iOS device (`git clone git@github.com:simplejson/simplejson.git`)
6. cd into the `simplejson` directory
7. Install the `simplejson` package using `python setup.py install`
8. cd into the `iOS-REST-Battery` repository
9. Install `batterydata-arm32.deb` using `dpkg -i batterydata-arm32.deb`
10. Start the script by running `python script.py`