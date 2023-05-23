# iOS REST Battery
A REST API for reporting the battery percentage of jailbroken iOS devices

## Installation

### Requirements
- Jailbroken iOS device (only 32-bit devices are supported at the moment)
- Terminal/SSH access to your iOS device
- (Recommended) A tweak that keeps Wi-Fi on even when the device is locked (like `iNoSleep`)
- Git CLI (`apt-get install git`) on your iOS device
- Python 2.5.1 (`apt-get install python`) on your iOS device

## Setup
1. Meet the requirements
2. Follow the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to generate an SSH key on your iOS device to be able to access GitHub
3. Run `cat /path/to/<your key>.pub` and copy its contents to this [GitHub](https://github.com/settings/ssh/new) page
4. Clone this repository to your iOS device (`git clone git@github.com:ShonP40/iOS-REST-Battery.git`)
5. Clone the `SimpleJSON` repository to your iOS device (`git clone git@github.com:simplejson/simplejson.git`)
6. cd into the `simplejson` directory
7. Install the `simplejson` package using `python setup.py install`
8. cd into the `iOS-REST-Battery` directory
9. Install `batterydata-arm32.deb` using `dpkg -i batterydata-arm32.deb`
10. Start the script by running `python script.py` to test it out
11. Press `Ctrl + C` to stop the script

## Running (You will need to do this every time you reboot your device)
1. cd into the `iOS-REST-Battery` directory
2. Create a new screen session by running `screen -S battery`
3. Start the script by running `python script.py`
4. Detach from the screen session by pressing `Ctrl + A + D`

## Updating
1. Reattach to the screen session by running `screen -r battery`
2. Press `Ctrl + C` to stop the script
3. Run `git pull`
4. Start the script again by running `python script.py`
5. Detach from the screen session by pressing `Ctrl + A + D`

## Usage
If you are using this sctipt to display the battery status of your iOS device on Home Assistant, you can use the following configuration as an example:

```yaml
sensor:
  - platform: rest
    name: iPad battery status
    unique_id: ipad_battery_status
    resource: http://<iPad IP>:8000/status
    method: GET
    value_template: "{{ value_json.Battery }}"
    unit_of_measurement: "%"
    device_class: battery
    json_attributes:
      - Battery
      - Battery status
```
