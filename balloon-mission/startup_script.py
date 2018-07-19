#!/usr/bin/env python3

import subprocess
import os
import time


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def create_log_dir(dir_template):
    r = subprocess.run(['mktemp', '-d', dir_template], stdout=subprocess.PIPE)
    return r.stdout.decode().rstrip('\n')

log_dir = create_log_dir('/sdcard/log-XXXX')
print(log_dir)


def run_cmd(cmd, timeout=None):
    cmd_list = cmd.split(' ')
    print(cmd)
    try:
        r = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        if r.returncode == 0:
            print('success')
        else:
            print('failed {}'.format(r.returncode))
            print(r.stdout)
            print(r.stderr)
        return r.returncode == 0
    except subprocess.TimeoutExpired as e:
        print(e)
        return False

def big_camera_take_image(logdir, idx):
    filename = logdir + '/img_{:05}.jpeg'.format(idx)
    cmd = 'ffmpeg -y -f video4linux2 -s 2592x1944 -i /dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB_2.0_Camera_SN0179-video-index0 -ss 0:0:2 -frames 1 {}'.format(filename)
    return run_cmd(cmd, timeout=15)

def csi_camera_take_image(logdir, idx):
    filename = logdir + '/img_{:05}_0.jpeg'.format(idx)
    cmd = 'streamer -w 1 -t 3 -s 2592x1944 -o {} -c /dev/v4l/by-path/platform-1cb0000.camera-video-index0'.format(filename)
    return run_cmd(cmd, timeout=15)

def small_camera_take_video(logdir, idx, duration):
    filename = logdir + '/vid_{:05}.mkv'.format(idx)
    cmd = 'ffmpeg -y -f v4l2 -framerate 30 -video_size 1280x720 -input_format mjpeg -i /dev/v4l/by-id/usb-058f_USB_2.0_HD_Camera-video-index0 -c:v copy -an -t {} {}'.format(duration, filename)
    return run_cmd(cmd, timeout=duration+20)



def run_shell_non_blocking(cmd):
    print(cmd)
    proc = subprocess.Popen([cmd], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    return proc



print('setting up gps log')
run_cmd('stty -F /dev/ttyS2 9600  raw clocal -echo')
time.sleep(1)
run_shell_non_blocking('cat < /dev/ttyS2 > {}/gps.log'.format(log_dir))


run_shell_non_blocking('python3 /home/pi/humidity_temperature_readout.py 0 > {}/humidity_and_temp.csv'.format(log_dir))


big_camera_dir = log_dir + '/side_camera'
create_folder(big_camera_dir)
csi_camera_dir = log_dir + '/down_camera'
create_folder(csi_camera_dir)
small_camera_dir = log_dir + '/up_camera'
create_folder(small_camera_dir)

# for i in range(10):
i = 0
while True:
    i += 1
    big_camera_take_image(big_camera_dir, i)
    csi_camera_take_image(csi_camera_dir, i)
    small_camera_take_video(small_camera_dir, i, 20)
    time.sleep(60*2)
