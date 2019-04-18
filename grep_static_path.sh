#!/bin/sh

grep -l '\/static' ./static/css/mystyle.css | xargs sed -i.bak -e 's/\/static/\/flaskapp\/static/g'
grep -l '\/static' ./static/js/myscript.js | xargs sed -i.bak -e 's/\/static/\/flaskapp\/static/g'

grep -l '\/static' ./templates/* | xargs sed -i.bak -e 's/\/static/\/flaskapp\/static/g'
