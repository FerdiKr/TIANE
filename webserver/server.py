#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from flask import Flask, render_template, jsonify, request, send_file, make_response
from gevent import pywsgi
import werkzeug.serving
from helpWrapper import checkServerInstallation as cSI

webapp = Flask("TIANE", template_folder="template")

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

@webapp.route("/api/checkServerInstallation")
def checkServerInstallation():
    data = cSI()
    return jsonify(data)

ws = pywsgi.WSGIServer(("0.0.0.0", 50500), webapp)
ws.serve_forever()
