#!/usr/bin/python3
import os,pip


def clr():
    os.system('clear')

def install(package):
    pip.main(['install', package])

clr()
print("""
rPi-Project-Controller Installer
--------------------------------------
Duinotech
--------------------------------------
Author D.k.West

This script will prompt you with options
and the capital letter is the default 
when you press enter.

Press Enter to continue
""")
input()
clr()
print('='*20)
print('WARNING')
print('='*20)
print('''
this script will make changes to your
device, and presumes that this is a fresh install

If something goes wrong, you might have to re-image
your SD card.

''')
if str(input('ok to continue? [Y/n]')).lower() == 'n':
    exit()

clr()
print('testing internet connection....')
if os.system('ping -c 1 github.com'):
    print('unable to connect to github')
    print('you need an internet connection for this to work')
    exit()

clr()
print("""
Installing dependencies..
""")

install('flask')
install('gitpython')

from git import Repo
try:
    Repo.clone_from('http://github.com/duinotech/rPi-Project-Controller',
        '/home/pi/rPi-Project-Controller')
except GitCommandError as e:
    pass

os.chdir('/home/pi/rPi-Project-Controller')
install('-e .')

clr()
print('setting up webserver to autoboot..')
os.system('echo "@./rPi-Project-Controller/start_neuron.sh" >> ~/.config/lxsession/LXDE-pi/autostart')

clr()
print('-='*10)
print('LCD screen set-up')
print('-='*10)
print('''
    Are you planning on using the 5" touch screen (XC9024)

    and if so, are you going to use it in (P)ortriat or (L)andscape mode?
    
    (n for 'no screen', either webserver or self-provided screen mode)
''')
screen = None
while screen not in ['p','l','n']:
    screen = input('screen? [P/l/n]').lower()

if screen == 'p' or screen == 'l':
    try:
        Repo.clone_from('http://github.com/goodtft/LCD-show','/home/pi/LCD-show')
    except GitCommandError as e:
        #assumed already have it
        pass

    os.chdir('/home/pi/LCD-show')
    for line in """
    sudo rm -rf /etc/X11/xorg.conf.d/40-libinput.conf
    sudo cp -rf ./boot/config-5.txt /boot/config.txt
    sudo cp ./usr/inittab /etc/
    sudo cp -rf ./usr/99-fbturbo.conf-HDMI /usr/share/X11/xorg.conf.d/99-fbturbo.conf 
    sudo mkdir /etc/X11/xorg.conf.d/
    sudo cp -rf ./usr/99-calibration.conf-5 /etc/X11/xorg.conf.d/99-calibration.conf 
    sudo dpkg -i -B xserver-xorg-input-evdev_2.10.5-1_armhf.deb
    sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
    """.split():
        os.system(line)
    
    if screen == 'p':
        os.system('echo "display_rotate 1" >> /boot/config.txt')
        os.system('sed -i "4s/.*/Option \"Calibration\" \"208 3905 3910 288\"/" /etc/X11/xorg.conf.d/99-calibration.conf')
        os.system('sed -i "5s/.*/Option \"SwapAxes\" \"1\"/" /etc/X11/xorg.conf.d/99-calibration.conf')

