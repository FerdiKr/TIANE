#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from flask import Flask, render_template, jsonify, request, send_file, make_response, redirect
from gevent import pywsgi
import werkzeug.serving
import json
import os
import sys
import random
from helpWrapper import InstallWrapper

# TIANE_setup_wrapper-import is a bit hacky but I can't see any nicer way to realize it yet
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from TIANE_setup_wrapper import *
from distutils.dir_util import copy_tree

# Imports for handling the main-tiane-System, defining global variable for that thread
from webserverTianeCommunication import mThr

mainThread = mThr()

mainThread.start()

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
{"href": "/setup", "text": "\"Erste Schritte\""},
{"href": "/setupServer", "text": "Server einrichten"},
{"href": "/setupUser", "text": "Benutzer erstellen"},
{"href": "/setupRoom", "text": "Räume einrichten (WIP)"},
{"href": "/setupModules", "text": "Module bearbeiten (WIP)"},
]


@webapp.route("/")
@webapp.route("/index")
def index():
    firstTime = False
    if firstTime:
        return redirect("/setup")
    else:
        return render_template("index.html", nav=nav)

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

@webapp.route("/setupUser") # TODO
def setupUser():
    data = getData()
    gold = os.path.exists("../server/resources/user_default/User_Info.json")
    gold = gold and os.path.exists("../server/users/")
    gold = gold and os.path.exists("../server/TIANE_config.json")
    # per default a set of normal standard-values is loaded, via javascript and
    # the API-Endpoint "/api/loadConfig/user/<username>" another config-file can
    # be edited with that /setupUser-File.
    with open("../server/resources/user_default/User_Info.json", "r") as confFile:
        config = json.load(confFile)
    with open("../server/TIANE_config.json", "r") as confFile:
        ServerConfig = json.load(confFile)
    standards = {
        "userName": "",
        "userRole": config["User_Info"]["role"],
        "userTelegram": config["User_Info"]["telegram_id"] if "telegram" in ServerConfig and "telegram_id" in config["User_Info"] else "-1",
        "userFullName": config["User_Info"]["first_name"],
        "userFullLastName": config["User_Info"]["last_name"],
        "userBirthYear": config["User_Info"]["date_of_birth"]["year"],
        "userBirthMonth": config["User_Info"]["date_of_birth"]["month"],
        "userBirthDay": config["User_Info"]["date_of_birth"]["day"]
    }
    return render_template("setupUser.html", nav=nav, st=standards, gold=gold)

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
    with open('../server/TIANE_config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
        return "ok"
    return "err"

@webapp.route("/api/writeConfig/room/<roomName>") # TODO
def writeRoomConfig(roomName):
    return "ok"

@webapp.route("/api/writeConfig/user/<userName>") # TODO
def writeUserConfig(userName):
    data = getData()
    if "userName" in data and data["userName"].strip() != "":
        filename = "../server/users/" + data["userName"] + "/User_Info.json"
        default_path = "../server/resources/user_default/User_Info.json"
        if os.path.exists(filename):
            with open(filename, "r") as config_file:
                config_data = json.load(config_file)
        elif os.path.exists(default_path):
            with open(default_path, "r") as config_file:
                config_data = json.load(config_file)
        else:
            config_data = {"User_Info": {}}
        config_data["User_Info"]["name"] = data["userName"]

        subdirs = os.listdir("../server/users")
        config_data["User_Info"]["uid"] = len(subdirs) + 1

        if "userRole" in data and data["userRole"].strip() != "":
            if data["userRole"].strip() in ["USER", "ADMIN"]:
                config_data["User_Info"]["role"] = data["userRole"]

        if "userTelegram" in data and data["userTelegram"].strip() != "":
            try:
                config_data["User_Info"]["telegram_id"] = int(data["userTelegram"])
            except ValueError:
                config_data["User_Info"]["telegram_id"] = 0

        if "userFullName" in data and data["userFullName"].strip() != "":
            config_data["User_Info"]["first_name"] = data["userFullName"]
        if "userFullLastName" in data and data["userFullLastName"].strip() != "":
            config_data["User_Info"]["last_name"] = data["userFullLastName"]

        if "userBirthYear" in data and data["userBirthYear"].strip() != "":
            try:
                config_data["User_Info"]["date_of_birth"]["year"] = int(data["userBirthYear"])
            except ValueError:
                config_data["User_Info"]["date_of_birth"]["year"] = 0

        if "userBirthMonth" in data and data["userBirthMonth"].strip() != "":
            try:
                config_data["User_Info"]["date_of_birth"]["month"] = int(data["userBirthMonth"])
            except ValueError:
                config_data["User_Info"]["date_of_birth"]["month"] = 0

        if "userBirthDay" in data and data["userBirthDay"].strip() != "":
            try:
                config_data["User_Info"]["date_of_birth"]["day"] = int(data["userBirthDay"])
            except ValueError:
                config_data["User_Info"]["date_of_birth"]["day"] = 0

        if not os.path.exists("../server/users" + config_data["User_Info"]["name"]):
            try:
                os.mkdir("../server/users/" + config_data["User_Info"]["name"])
            except FileExistsError:
                pass
        try:
            copy_tree("../server/resources/user_default", "../server/users/" + config_data["User_Info"]["name"])
        except IOError:
            print('\n' + color.RED + '[ERROR]' + color.END + ' Fehler beim kopieren der Dateien. Bitte versuche, den Setup-Assistent mit Root-Rechten auszuführen.')
            return "err"
        with open('../server/users/' + config_data['User_Info']['name'] + '/User_Info.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        return "ok"
    else:
        return "err"



@webapp.route("/api/loadConfig/user/<userName>")
def loadUserConfig(userName):
    if os.path.exists("../server/users/" + userName + "/User_Info.json"):
        with open("../server/users/" + userName + "/User_Info.json", "r") as confFile:
            config = json.load(confFile)["User_Info"]
        data = {
            "userName": config["name"],
            "userRole": config["role"],
            "userTelegram": config["telegram_id"],
            "userBirthYear": config["date_of_birth"]["year"],
            "userBirthMonth": config["date_of_birth"]["month"],
            "userBirthDay": config["date_of_birth"]["day"],
            "userFullName": config["first_name"],
            "userFullLastName": config["last_name"]
        }
        return jsonify(data)
    else:
        return jsonify("user not found")

@webapp.route("/api/uploadSpeech/<userName>") # TODO
def uploadSnowboyFile(userName):
    data = getData()
    return "ok"

@webapp.route("/api/server/list/<action>")
def getExtraServerStatus(action="*"):
    feed = mainThread.getFeed()
    if action == "rooms":
        data = feed["rooms"] if "rooms" in feed else {}
    elif action == "users":
        data = feed["users"] if "users" in feed else {}
    elif action == "modules":
        data = feed["modules"] if "modules" in feed else {}
    elif action == "telegram":
        data = feed["rejected_telegram_messages"] if "rejected_telegram_messages" in feed else []
    else:
        data = {
            "room": feed["rooms"] if "rooms" in feed else {},
            "users": feed["users"] if "users" in feed else {},
            "modules": feed["modules"] if "modules" in feed else {}
        }
    return jsonify(data)


@webapp.route("/api/server/<action>") # TODO
def getServerStatus(action):
    if action == "status":
        feed = mainThread.getFeed()
        data = {
            "status": mainThread.status(),
            "since": feed["TIANE_starttime"] if "TIANE_starttime" in feed else 0
            }
    elif action == "start":
        mainThread.start()
        data = "ok"
    elif action == "stop":
        mainThread.stop()
        data = "ok"
    elif action == "feed":
        data = mainThread.getFeed()
    else:
        data = "err"
    return jsonify(data)

@webapp.route("/api/module/list")
def listModules():
    feed = mainThread.getFeed()
    return jsonify(feed["modules"] if "modules" in feed else {})

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

@webapp.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@webapp.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500

ws = pywsgi.WSGIServer(("0.0.0.0", 50500), webapp)
print("To connect to the TIANE-Webserver, please visit http://localhost:50500/setup ")
ws.serve_forever()
