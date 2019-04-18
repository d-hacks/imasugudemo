import argparse
import os

def remove_old_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        print("Remove {}".format(filepath))

## Create wsgi.ini
def create_wsgiini_file(appname):
    wsgiini_filepath = "../wsgi.ini"
    remove_old_file(wsgiini_filepath)
    with open(wsgiini_filepath, "a") as f:
        f.write("[uwsgi]\n")
        f.write("module = wsgi:app\n")
        f.write("master = true\n")
        f.write("processes = 5\n")
        f.write("socket = {}.sock\n".format(appname))
        f.write("chmod-socket = 660\n")
        f.write("vacuum = true\n")
        f.write("die-on-term = true\n")
    print("Create {}".format(wsgiini_filepath))

## Create wsgi.py
def create_wsgipy_file(appname):
    wsgipy_filepath = "../wsgi.py"
    remove_old_file(wsgipy_filepath)
    with open(wsgipy_filepath, "a") as f:
        f.write("from {} import app\n\n".format(appname))
        f.write("if __name__ == '__main__':\n")
        f.write("    app.run()\n")
    print("Create {}".format(wsgipy_filepath))

## Create systemd service file
def create_systemd_service_file(appname, appdirpath, user):
    service_filepath = "../{}.service".format(appname)
    remove_old_file(service_filepath)
    with open(service_filepath, "a") as f:
        f.write("[Unit]\n")
        f.write("Description=uWSGI instance to serve {}\n".format(appname))
        f.write("After=network.target\n\n")
        f.write("[Service]\n")
        f.write("User={}\n".format(user))
        f.write("Group=www-data\n")
        f.write("WorkingDirectory={}/{}\n".format(appdirpath, appname))
        f.write("Environment='PATH={}/{}/{}env/bin'\n".format(appdirpath, appname, appname))
        f.write("ExecStart={}/{}/{}env/bin/uwsgi --ini wsgi.ini\n\n".format(appdirpath, appname, appname))
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")
    print("Create {}".format(service_filepath))

def create_nginx_config_file(appname, appdirpath, user):
    nginx_filepath = "../{}.conf".format(appname)
    remove_old_file(nginx_filepath)
    with open(nginx_filepath, "a") as f:
        f.write("  ## {} - {}\n\n".format(appname, user))
        f.write("  location ~ ^/{}(.*)$ {{\n".format(appname))
        f.write("    root {}/{};\n".format(appdirpath, appname))
        f.write("    include uwsgi_params;\n")
        f.write("    uwsgi_pass unix:{}/{}/{}.sock;\n".format(appdirpath, appname, appname))
        f.write("    uwsgi_param SCRIPT_NAME /{};\n".format(appname))
        f.write("    uwsgi_param PATH_INFO /$1;\n")
        f.write("  }\n")
        f.write("  location ^~ /{}/static/js   {{ root {}/; }}\n".format(appname, appdirpath))
        f.write("  location ^~ /{}/static/css  {{ root {}/; }}\n".format(appname, appdirpath))
        f.write("  location ^~ /{}/static/img  {{ root {}/; }}\n".format(appname, appdirpath))
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
    create_nginx_config_file(args.appname, args.appdirpath, args.user)
