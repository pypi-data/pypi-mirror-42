#!/usr/bin/env python3

from __future__ import print_function
import subprocess
import os
import signal
import time
import glob
import sys
from flask import Flask, request, render_template, app, redirect

CONFIG_DIR = os.path.join(os.getenv('HOME'),
                         'stallyns')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

ES = "/opt/retropie/supplementary/emulationstation/emulationstation"

USER_DIR = "~/roms"

app = Flask(__name__)

def es_running(pid=None):
    try:
        cmd = ['pidof', ES]
        pid = subprocess.check_output(cmd, shell=False)
        try:
            pid = int(pid.decode("utf-8").rstrip())
        except AttributeError:
            pass
        return pid 
    except Exception:
        return None

def kill_es():
    pid = es_running()
    if pid:
        print("killing pid: %d" % pid)
        os.kill(pid, signal.SIGTERM)

@app.route("/restart", methods=['POST'])
def restart_es():
    try:
        os.mknod("/tmp/es-restart")
    except FileExistsError:
        pass
    kill_es()
    return redirect("/", 302)

@app.route("/pi/reboot", methods=['POST'])
def pi_restart():
    try:
        os.mknod("/tmp/es-sysrestart")
    except FileExistsError:
        pass
    kill_es()
    return redirect("/", 302)

@app.route("/pi/shutdown", methods=['POST'])
def pi_shutdown():
    try:
        os.mknod("/tmp/es-shutdown")
    except FileExistsError:
        pass
    kill_es()
    return redirect("/", 302)

def update_symlink(user_name):
    rompath = os.path.join(os.path.expanduser('~/'),
                           "RetroPie",
                           "roms")
    if os.path.exists(rompath) and not os.path.islink(rompath):
        os.rename(rompath, "{}.{}".format(rompath, "orig"))
    profdir = os.path.join(os.path.expanduser(USER_DIR), user_name)
    try:
        os.remove(rompath)
    except FileNotFoundError:
        pass
    os.symlink(profdir, rompath)
    restart_es()
    return profdir

@app.route("/change_user", methods=['POST'])
def change_user():
    requested_user = request.form.get("user")
    if requested_user and os.path.isdir(os.path.join(
                     os.path.expanduser(USER_DIR), requested_user)):
        update_symlink(requested_user)
        return redirect("/", 302)
    return "No such user", 500

def current_user():
    rompath = os.path.join(os.path.expanduser('~/'),
                           "RetroPie",
                           "roms")
    if os.path.exists(rompath) and not os.path.islink(rompath):
        return None
    rp = os.path.realpath(rompath)
    return os.path.basename(rp)

def user_list():
    users = set()
    dirs = glob.glob(os.path.join(os.path.expanduser(USER_DIR), '*'))
    for node in dirs:
        if os.path.isdir(node) and 'lost+found' not in node and 'BIOS' not in node:
            users.add(os.path.basename(node))
    return sorted(users)

def main():
    app.run(host= '0.0.0.0', port=5000)

@app.route("/")
def index():
    data = {}
    data['users'] = user_list()
    data['current_user'] = current_user()
    return render_template('index.html', data=data)

if __name__ == "__main__":
    main()
