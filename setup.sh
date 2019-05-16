#!/usr/bin/bash

APPNAME=newapp
APPDIRPATH=/home/hirono/projetcs
USER=hirono

APPSCRIPT="${APPNAME}/${APPNAME}.py"

# https://shellscript.sunone.me/parameter.html

mv newapp/imasugudemo.py $APPSCRIPT

cd /home/hirono/projects/newapp/src

python create_config_files.py --appname 'newapp' --appdirpath '/home/hirono/projects' --user 'hirono'


echo "パスワード" | sudo -S /etc/rc.d/init.d/httpd restart


# 1. 雛形Flaskアプリのclone

# カレントディレクトリ以下の任意の場所に雛形Flaskアプリをclone
$ git clone git@github.com:d-hacks/imasugudemo.git newapp ## newappの部分を書き換えてください

# アプリ名を変更
$ mv newapp/imasugudemo.py newapp/newapp.py
# Nginx、uWSGI、systemd serviceの設定ファイルを作成

$ cd /home/hirono/projects/newapp/src

$ python create_config_files.py --appname 'newapp' --appdirpath '/home/hirono/projects' --user 'hirono'


# 2. virtualEnvの作成

# 対象のFlaskアプリのディレクトリの中でvenvを立ち上げる
$ cd /home/hirono/projects/newapp
$ python -m venv newappenv
$ source newappenv/bin/activate

# 使用しているライブラリ全てと、Flask、uWSGIをvenv内にインストール
(newappenv) $ pip install uwsgi flask
venvから出る
(newappenv) $ deactivate
