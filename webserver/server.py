#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from flask import Flask, render_template, jsonify, request, send_file, make_response
from gevent import pywsgi
import werkzeug.serving
import json
import os
import sys
from helpWrapper import InstallWrapper
# TIANE_setup_wrapper-import is a bit hacky but I can't see any nicer way to realize it yet
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from TIANE_setup_wrapper import *

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
{"href": "/setupUser", "text": "Benutzer einrichten (WIP)"},
{"href": "/setupRoom", "text": "Raum einrichten (WIP)"},
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
    if os.path.exists("../server/TIANE_config.json"):
        g = True # "config-exists"-trigger
    else:
        g = False
    with open("../server/TIANE_config.json") as conf:
        config = json.load(conf)
    standards = {
        "tianeName": config["System_name"],
        "tianeSystem": config["Server_name"],
        "tianeActivation": config["Activation_Phrase"],
        "homeLocation": config["Home_location"],
        "generateKey": True if config["TNetwork_Key"] == "" else False,
        "useCameras": True if config["use_cameras"] else False,
        "useFaceRec": True if config["use_facerec"] else False,
        "useInterface": True if config["use_interface"] else False,
    }
    return render_template("setupServer.html", nav=nav, st=standards, gold=g)

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

@webapp.route("/api/setup/prerequesites") # TODO
def getPrereqSetup():
    """
    checks things which would be checked on setup start
    os.path.exists('server/TIANE_config.json') for example
    """
    data ={}
    return jsonify(data)

@webapp.route("/api/writeConfig/server") # TODO
def writeServerConfig():
    data = getData()
    print(data)
    with open("../server/TIANE_config.json", "r") as config_file:
        config_data = json.load(config_file)
    # check every parameter and update those in the config file
    if "tianeName" in data and data["tianeName"].strip() != "":
        config_data["System_name"] = data["tianeName"]
    config_data["Local_storage"]["system_name"] = config_data["System_name"]

    if "tianeSystem" in data and data["tianeSystem"].strip() != "":
        config_data["Server_name"] = data["tianeName"]
    config_data["Local_storage"]["server_name"] = config_data["System_name"]

    if "tianeActivation" in data and data["tianeActivation"].strip() != "":
        config_data['Activation_Phrase'] = data["tianeActivation"]
    config_data['Local_storage']['activation_phrase'] = config_data['Activation_Phrase']

    if "homeLocation" in data and data["homeLocation"].strip() != "":
        config_data['Home_location'] = data["homeLocation"]
    config_data['Local_storage']['home_location'] = config_data['Home_location']

    if "keyLength" in data and data["keyLength"].strip() != "":
        try:
            key_len = int(data["keyLength"])
        except ValueError:
            key_len = 32
        config_data['TNetwork_Key'] = generate_key(key_len)

    if "telegramBotId" in data and len(data["telegramBotId"].strip()) == 45:
        config_data["telegram_key"] = data["telegramBotId"].strip()

    if "useCameras" in data and data["useCameras"].strip() != "":
        t = True if data["useCameras"] == "true" else False
        config_data["use_cameras"] = t
        bedingt_kopieren('../server/resources/optional_modules/recieve_cameras.py', '../server/modules/continuous/recieve_cameras.py', t)

        if "useFaceRec" in data and data["useFaceRec"].strip() != "":
            t = True if data["useFaceRec"] == "true" else False
            config_data["use_facerec"] = t
            bedingt_kopieren('../server/resources/optional_modules/face_recognition.py', '../server/modules/continuous/face_recognition.py', t)
            bedingt_kopieren('../server/resources/optional_modules/retrain_facerec.py', '../server/modules/retrain_facerec.py', t)

        if "useInterface" in data and data["useInterface"].strip() != "":
            t = True if data["useInterface"] == "true" else False
            config_data["use_interface"] = t
            bedingt_kopieren('../server/resources/optional_modules/POI_Interface.py', '../server/modules/continuous/POI_Interface.py', t)
            bedingt_kopieren('../server/resources/optional_modules/POI_Interface_controls.py', '../server/modules/POI_Interface_controls.py', t)
    print(config_data)
    with open('../server/TIANE_config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
        return "ok"
    return "err"

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
