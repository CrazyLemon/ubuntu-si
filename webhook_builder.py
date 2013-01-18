#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import threading
import logging
import os

try:
    from flask import Flask, render_template, request
except Exception, e:
    print "pip install flask"

try:
    import envoy
except Exception, e:
    print "pip install envoy"


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
app = Flask(__name__)


def build_all(flavor):
    #git_dir = os.path.dirname(os.path.abspath(__file__))

    git = envoy.run("git pull")

    logging.debug(git.std_out)
    if git.status_code is 0:

        deb = envoy.run("make deb" + flavor)
        logging.debug(deb.std_out)

        if deb.status_code is 0:
            iso = envoy.run("make iso" + flavor)
            logging.debug(iso.std_out)

            dist = envoy.run("make dist" + flavor)
            logging.debug(dist.std_out)


def build_amd64():
    logging.debug('Starting')
    build_all("64")
    logging.debug('Exiting')

build_amd64_handle = threading.Thread(name='build_amd64', target=build_amd64)


def build_i386():
    logging.debug('Starting')
    build_all("32")
    logging.debug('Exiting')

build_i386_handle = threading.Thread(name='build_i386', target=build_i386)


@app.route("/")
def status():
    return render_template('status.html',
                           status_amd64={
                               "alive": build_amd64_handle.isAlive(),
                               "history": build_amd64_handle.isAlive(),
                               "checks": build_amd64_handle.isAlive(),
                           },
                           status_i386={
                               "alive": build_i386_handle.isAlive(),
                               "history": build_i386_handle.isAlive(),
                               "checks": build_i386_handle.isAlive(),
                           })


@app.route("/web_hook", methods=['POST'])
def web_hook():
    if request.method == 'POST':
        if request.remote_addr in ["207.97.227.253", "50.57.128.197",
                                   "108.171.174.178", "50.57.231.61"]:
            logging.debug(request.form["payload"])
            if not build_i386_handle.isAlive():
                try:
                    build_i386_handle.start()
                except Exception, e:
                    logging.debug(e)
                    build_i386_handle.start_new_thread(name='build_i386', target=build_i386)
                    build_i386_handle.start()
            return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
