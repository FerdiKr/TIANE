#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from flask import Flask, render_template, jsonify, request, send_file, make_response
from gevent import pywsgi
import werkzeug.serving
from helpWrapper import InstallWrapper

webapp = Flask("TIANE", template_folder="template")
installer = InstallWrapper()

def getData():
    data = request.args.to_dict()
    data.update(request.form.to_dict())
    return data

# ------------------------------------------------------------------------------
# HTTP-Frontend
# ------------------------------------------------------------------------------

nav = [
{"href": "/setupServer", "text": "Server einrichten"},
{"href": "/setupUser", "text": "Benutzer einrichten"},
{"href": "/setupRoom", "text": "Raum einrichten"},
]



@webapp.route("/")
@webapp.route("/setup")
def setup_1():
    return render_template("setup.html", nav=nav)

@webapp.route("/setup_2")
def setup_2():
    firstData = installer.listPackages()
    return render_template("setup_checkServices.html", nav=nav, fD=firstData)

@webapp.route("/setup_3")
def setup_3():
    return render_template("setup_menu.html", nav=nav)

@webapp.route("/setupServer")
def setupServer():
    data = getData()
    return render_template("setupServer.html", nav=nav)

@webapp.route("/setupUpser") # TODO
def setupUser():
    data = getData()
    return render_template("setupUser.html", nav=nav)

@webapp.route("/setupRoom") # TODO
def setupRoom():
    data = getData()
    return render_template("setupRoom.html", nav=nav)

# API-like-Calls

@webapp.route("/api/installer/listPackages")
@webapp.route("/api/installer/listPackages/<extended>")
def listPackages(extended=False):
    if extended == "details":
        extended = True
    else:
        extended = False
    data = installer.listPackages(extended)
    return jsonify(data)

@webapp.route("/api/installer/getStatus")
def getStatus():
    data = installer.getInstallerStatus()
    return jsonify(data)

@webapp.route("/api/installer/startInstallation/<packageName>")
def startInstallation(packageName):
    data = installer.startInstallation(packageName)
    return jsonify(data)

@webapp.route("/api/writeConfig/server") # TODO
def writeServerConfig():
    return "ok"

@webapp.route("/api/writeConfig/room/<roomName>") # TODO
def writeRoomConfig(roomName):
    return "ok"

@webapp.route("/api/writeConfig/user/<userName>") # TODO
def writeUserConfig(userName):
    return "ok"

@webapp.route("/api/uploadSpeech/<userName>") # TODO
def uploadSnowboyFile(userName):
    data = getData()
    return "ok"

@webapp.route("/api/server/<action>") # TODO
def getServerStatus(action):
    if action == "status":
        pass
    elif action == "start":
        pass
    elif action == "stop":
        pass
    elif action == "version":
        pass
    return "ok"

@webapp.route("/api/module/<modName>/<action>") # TODO
def changeModuleMode(modName, action):
    modules = [] # dummyList
    if modName in modules:
        if action == "load":
            pass
        elif action == "unload":
            pass
        elif action == "status":
            pass
    return "ok"


ws = pywsgi.WSGIServer(("0.0.0.0", 50500), webapp)
ws.serve_forever()
