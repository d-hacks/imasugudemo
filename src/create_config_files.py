import argparse

def remove_old_file(filepath):
    if os.path.exist(filepath):
        os.remove(filepath)
    print("Remove {}".format(filepath))

## Create wsgi.ini
def create_wsgiini_file(appname):
    wsgiini_filepath = "wsgi.ini"
    remove_old_file(wsgiini_filepath)
    with open(wsgiini_filepath, "a") as f:
        f.write("[uwsgi]")
        f.write("module = wsgi:app")
        f.write("master = true")
        f.write("processes = 5")
        f.write("socket = {}.sock".format(appname))
        f.write("chmod-socket = 660")
        f.write("vacuum = true")
        f.write("die-on-term = true")
    print("Create {}".format(wsgiini_filepath))

## Create wsgi.py
def create_wsgipy_file(appname):
    wsgipy_filepath = "wsgi.py"
    remove_old_file(wsgipy_filepath)
    with open(wsgipy_filepath, "a") as f:
        f.write("from {} import app\n".format(appname))
        f.write("if __name__ == '__main__':")
        f.write("    app.run()")
    print("Create {}".format(wsgipy_filepath))

## Create systemd service file
def create_systemd_service_file(appname, appdirpath, user):
    service_filepath = "{}.service".format(appname)
    remove_old_file(service_filepath)
    with open(service_filepath, "a") as f:
        f.write("[Unit]")
        f.write("Description=uWSGI instance to serve {}".format(appname))
        f.write("After=network.target\n")
        f.write("[Service]")
        f.write("User={}".format(user))
        f.write("Group=www-data")
        f.write("WorkingDirectory={}/{}".format(appdirpath, appname))
        f.write("Environment='PATH={}/{}/{}env/bin'".format(appdirpath, appname, appname))
        f.write("ExecStart={}/{}/{}env/bin/uwsgi --ini wsgi.ini\n".format(appdirpath, appname, appname))
        f.write("[Install]")
        f.write("WantedBy=multi-user.target")
    print("Create {}".format(service_filepath))

def create_nginx_config_file(appname, appdirpath):
    nginx_filepath = "{}.conf".format(appname)
    remove_old_file(nginx_filepath)
    with open(nginx_filepath, "a") as f:
        f.write("  location ~ ^/{}(.*)$ \{".format(appname))
        f.write("    root {}/{};".format(appdirpath, appname))
        f.write("    include uwsgi_params;")
        f.write("    uwsgi_pass unix:{}/{}/{}.sock;".format(appdirpath, appname, appname))
        f.write("    uwsgi_param SCRIPT_NAME /{};".format(appname))
        f.write("    uwsgi_param PATH_INFO /$1;")
        f.write("  \}")
        f.write("  location ^~ /{}/static/js   \{ root {}/; \}".format(appname, appdirpath))
        f.write("  location ^~ /{}/static/css  \{ root {}/; \}".format(appname, appdirpath))
        f.write("  location ^~ /{}/static/img  \{ root {}/; \}".format(appname, appdirpath))
    print("Create {}".format(nginx_filepath))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--appname', type=str)
    parser.add_argument('--appdirpath', type=str)
    parser.add_argument('--user', type=str)
    args = parser.parse_args()
    create_wsgiini_file(args.appname)
    create_wsgipy_file(args.appname)
    create_systemd_service_file(args.appname, args.appdirpath, args.user)
    create_nginx_config_file(args.appname, appdirpath)
