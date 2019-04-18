# Flask Sample Application

Sampleapp directory path

- sampleappでsampleappとなっているところを自分のアプリ名に書き換えて使ってください
- README内では

```
bacchus.ht.sfc.keio.ac.jp:/home/hirono/projects/sampleapp
```



## 1. virtualEnvの作成

1. python3-venvのインストール
```
$ sudo apt install python3-venv
```

2. 対象のFlaskアプリのディレクトリに移動しvenvを立ち上げる

```
$ cd ~/projects/sampleapp
$ python -m venv sampleappenv
$ source sampleappenv/bin/activate
```

3. 使用しているライブラリを全てvenv内にインストール
```
（例）
(sampleappenv) $ pip install torch
```

4. FlaskとuWSGIをインストール
```
(sampleappenv) $ pip install uwsgi flask
```

5. port5000のリクエストを許可

```
(sampleappenv) $ sudo ufw allow 5000
```

7. sampleapp.pyファイルを実行（エラーが出なければOK）

```
(sampleappenv) $ python sampleapp.py

Output
* Serving Flask app "sampleapp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

8. wsgiでsampleapp.pyを実行するためのスクリプトを作成
```
(sampleappenv) $ vim wsgi.py
```

```
（wsgi.pyの中身）

from sampleapp import app

if __name__ == "__main__":
    app.run()
```

9. wsgi.pyファイルを実行（エラーが出なければOK）

```
(sampleappenv) $ uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```

10. venvから出る

```
(sampleappenv) $ deactivate
```


## 2. uWSGIをsystemdで動かす設定

1. uWSGIの設定ファイルの編集

```
$ vim ~/projects/sampleapp/sampleapp.ini
```



```
（sampleapp.iniの中身）

[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = myproject.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

2. wsgiファイルの実行をsystemdのservice化する

```
$ sudo vim /etc/systemd/system/sampleapp.service

```

```
（/etc/systemd/system/sampleapp.serviceの中身）

[Unit]
Description=uWSGI instance to serve sampleapp
After=network.target

[Service]
User=ht
Group=www-data
WorkingDirectory=/home/hirono/projects/sampleapp
Environment="PATH=/home/hirono/projects/sampleapp/sampleappenv/bin"
ExecStart=/home/hirono/projects/sampleappenv/bin/uwsgi --ini sampleapp.ini

[Install]
WantedBy=multi-user.target
```
- User=hironoを自分のユーザー名に
- sampleappの部分を自分のアプリ名に
- WorkingDirectory, Environment, ExecStartのpathを自分のものに

3. systemdのserviceを実行 → statusを確認
```
$ sudo systemctl start sampleapp
$ sudo systemctl enable sampleapp

$ sudo systemctl status sampleapp

Output
[TODO]
```

4. statusを確認する

- 一番上の「location ~ ^/」以下の文字列が外部からアクセスする際のurl

## 3. Nginxの設定

1. flaskappに以下を追記（すでに書いてあるところはいじらないで！）

```
$ sudo vim /etc/nginx/sites-available/flaskapp
```
　
`/etc/nginx/site-avalable/flaskapp` に以下を追記
```
（/etc/nginx/site-avalable/flaskappの中身）

  location ~ ^/sampleapp(.*)$ {
    root /home/hirono/projects/sampleapp;
    include uwsgi_params;
    uwsgi_pass unix:/home/hirono/projects/sampleapp/sampleapp.sock;
    uwsgi_param SCRIPT_NAME /sampleapp;
    uwsgi_param PATH_INFO /$1;
  }

  location ^~ /sampleapp/static/js  {
    root /home/hirono/projects/;

  location ^~ /sampleapp/static/css {
    root /home/hirono/projects/;
  }
  location ^~ /sampleapp/static/img {
    root /home/hirono/projects/;
  }
```

2. sites-enabledにシンボリックリンクを貼る
```
$ sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
```

3. Nginxの設定にエラーがないかテスト
```
$ sudo nginx -t
```

4. Nginxをrestart
```
$ sudo systemctl restart nginx
```

5. https://bacchus.ht.sfc.keio.ac.jp/sampleapp にアクセス

## 4. 画像、CSS、JSのリンク修正
### 1. アプリ内の`<script>` `<img>` `<link>`タグ内のリンクを書き換える

```
$ bash grep_static_path.sh
```

※手動で直す場合は以下のように書き換えてください
```
（例）
<img src="/static/img/d-hacks-logo.img">
<link rel="stylesheet" href="/static/css/mystyle.css">
<script src="/static/js/myscript.js"></script>
↓
<img src="/sampleapp/static/img/d-hacks-logo.img">
<link rel="stylesheet" href="/sampleapp/static/css/mystyle.css">
<script src="/sampleapp/static/js/myscript.js"></script>
```

※ locationの評価条件にimg, js, cssを明記しないと、nginxのデフォルトの設定で/usr/www/html以下にファイルを探しに行ってしまう。

またGETでリクエストされるurlからどのアプリのファイルをリクエストしているのかを判断しなければならないため、タグ内のリンクにアプリ名を含めなければならない（Flaskの基本設定には反する書き方になります）。詳しくは https://www.digitalocean.com/community/questions/nginx-image-folder-and-declaration


2. applicationファイルの再読み込み&Nginxの再起動

```
$ sudo systemctl restart sampleapp
$ sudo systemctl restart nginx
```

3. https://bacchus.ht.sfc.keio.ac.jp/sampleapp にアクセス


## エラー対処
とりあえずやってみること
- serviceの再起動→nginxの再起動
- キャッシュの消去とハード再読み込み

Nginxのlog
- Access log　`/var/log/nginx/access.log`
- Error log`/var/log/nginx/error.log`

参考URL

- ほぼこれ通り
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
