#!/bin/sh
# /home/hirono/projects

python src/create_config_files --appname '[appname]' --appdirpath '[appdir path]' --user '[username]'
# ex) python src/create_config_files --appname 'vashoapp' --appdirpath '/home/hirono/projects' --user 'hirono'

mv sampleapp.py [appname].py
# ex) sampleapp.py vashoapp.py

grep -l 'sampleapp' ./* | xargs sed -i.bak -e 's/sampleapp/[appname]/g'
# ex) grep -l 'sampleapp' ./* | xargs sed -i.bak -e 's/sampleapp/vashoapp/g'
