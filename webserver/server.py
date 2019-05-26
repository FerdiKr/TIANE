#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from flask import Flask, render_template, jsonify, request, send_file, make_response
from gevent import pywsgi
import werkzeug.serving
from helpWrapper import InstallWrapper

webapp = Flask("TIANE", template_folder="template")
installer = InstallWrapper()

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
    return render_template("setup_checkServices.html", nav=nav)

@webapp.route("/setupServer")
def setupServer():
    data = request.args.to_dict()
    data.update(request.form.to_dict())
    return render_template("setupServer.html", nav=nav)

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

ws = pywsgi.WSGIServer(("0.0.0.0", 50500), webapp)
ws.serve_forever()
