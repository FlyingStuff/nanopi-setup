# Setup NanoPi-Duo with ROS

- flash the official ubuntu to an sdcard
- connect to the debug serial port and boot the board
- run `sudo npi-config` and enable ssh
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

