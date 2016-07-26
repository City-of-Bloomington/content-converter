#!/bin/bash

# launch.py is availble in:
# https://github.com/charlesbrandt/moments

# path to launch.py is defined in:
# ~/.bashrc
# example .bashrc is available in moments/editors/ directory

export ROOT=/c/bloomington-code/content_converter

launch.py -c $ROOT code

echo "Other common options:
launch.py -c $ROOT layout

#check ip
ifconfig

cd /c/bloomington-code/content_converter
python manage.py runserver 192.168.56.101:8000

"

