# Setup NanoPi-Duo with ROS

- flash the official ubuntu to an sdcard
- connect to the debug serial port and boot the board
- run `sudo npi-config` in Interfacing and enable ssh
- connect to a wifi
    - `sudo nmcli r wifi on`
    - `sudo nmcli dev wifi`
    - `sudo nmcli dev wifi connect "SSID" password "PASSWORD"`
- check your ip address and enter it in ansible `hosts` file
- copy your ssh key to the nanopi: `ssh-copy-id pi@IPADDRESS` (login password is pi)

## ansible

The rest of the setup is handled using ansible. It installs all the packages and configures the linux.

To setup the NanoPi-Duo using ansible run:
`ansible-playbook nano-pi-duo-ros-playbook.yml`


### Video
sudo apt-get install v4l-utils
sudo apt-get install ffmpeg
sudo apt-get install streamer


big camera
/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB_2.0_Camera_SN0179-video-index0

small camera
/dev/v4l/by-id/usb-058f_USB_2.0_HD_Camera-video-index0


### Sd card
sudo apt-get install parted