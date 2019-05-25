#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import json
from threading import Thread
import importlib

__author__     = "olagino"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"

def checkServerInstallation():
    """
    Checks for all python modules needed for the TIANE-Server-App.
    Each module is represented in a dictionary with a few extras:
        - `okay` means "the module is installed and can be used"
        - `partially` means "the module isn't installed but it isn't mandatory"
        - `error` means "the module isn't installed and is needed to make TIANE work"
    """
    status = {}

    try:
        import cv2
        status["opencv"] = {"status": "okay", "version": cv2.__version__}
    except ImportError:
        status["opencv"] = {
            "status": "partially",
            "desc": "OpenCV wird nur benötigt, wenn TIANE Kamerabilder verarbeiten soll"
            }

    try:
        import imutils
        status["imutils"] = {"status": "okay", "version": version}
    except ImportError:
        status["imutils"] = {
            "status": "partially",
            "desc": "Das Python-Modul imutils wird nur benötigt, wenn TIANE Kamerabilder verarbeiten soll."
            }

    try:
        import face_recognition
        status["facerecognition"] = {"status": "okay", "version": face_recognition.__version__}
    except ImportError:
        status["facerecognition"] = {
            "status": "partially",
            "desc": "Das Python-Modul face_recognition wird nur benötigt, wenn du TIANEs Gesichtserkennung nutzen willst."
            }

    try:
        import sklearn
        status["sklearn"] = {"status": "okay", "version": sklearn.__version__}
    except ImportError:
        status["sklearn"] = {
            "status": "partially",
            "desc": "Das Python-Modul scikit-learn wird nur benötigt, wenn du TIANEs Gesichtserkennung nutzen willst."
            }

    try:
        import telepot
        status["telepot"] = {"status": "okay", "version": telepot.__version__}
    except ImportError:
        status["telepot"] = {
            "status": "partially",
            "desc": "Das Python-Modul telepot wird nur benötigt, wenn du TIANE auch über Telegram erreichen möchtest."
            }

    try:
        import pyaudio
        status["pyaudio"] = {"status": "okay", "version": pyaudio.__version__}
    except ImportError:
        status["pyaudio"] = {
            "status": "error",
            "desc": "Das Python-Modul pyaudio wird zwingend benötigt, sonst kann dich TIANE weder verstehen noch mit dir sprechen."
            }

    try:
        import SpeechRecognition
        status["speechrecognition"] = {"status": "okay", "version": SpeechRecognition.__version__}
    except ImportError:
        status["speechrecognition"] = {
            "status": "error",
            "desc": "Das Python-Modul SpeechRecognition wird zwingend benötigt, sonst versteht dich TIANE nicht wenn du sprichst."
            }

    try:
        import wikipedia
        status["wikipedia"] = {"status": "okay", "version": wikipedia.__version__}
    except ImportError:
        status["wikipedia"] = {
            "status": "partially",
            "desc": "Das Python-Modul wikipedia wird nur dann benötigt, wenn du das entsprechende Modul benutzt."
            }

    return status

class InstallWrapper():
    """
    The install wrapper class initiates a thread
    """
    def __init__(self):
        self._runThread = True
        self._thread = Thread(target=self._threadedLoop)
        self._thread.start()
        self.readConfig()
        # start thread

        pass

    def __del__(self):
        # stop thread
        self._runThread = False
        self._thread.join()
        pass

    def listPackages(self, status=False):
        pR = self.readConfig()
        packList = []
        for el in pR:
            data = {
                "name": el,
                "desc": pR[el]["description"] if "description" in pR[el] else "",
                "required": pR[el]["required"] if "required" in pR[el] else "no",
            }
            if status:
                data["status"] = self.checkStatus(el)
            packList.append(data)
        return packList

    def getInstallerStatus(self):
        state = {
            "status": "idle", # installing
            "log": "" # log output from installer process
        }
        return state


    def startInstallation(self, packageName):
        # start installation
        return True

    def _threadedLoop(self):
        """
        _threadedLoop is the main wrapper for installation processes. Optimally
        it gets started when the class is instanciated.
        """
        while self._runThread:
            pass

        return None


    def readConfig(self):
        """
        the readConfig is used as a basic wrapper function to read and import the
        services.json-config-file. Additionally it returns the class-internal
        packagesRaw-Variable where the contents of the services.json files are stored
        """
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "services.json")
        self.packagesRaw = json.load(open(config))
        return self.packagesRaw

    def checkStatus(self, packageName):
        """
        This function parses the install_check-Block inside of the service.json-File.
        It checks if all recommended packages are installed.
        In every case it returns a tuple consisting of two parameters. In the first
        one the general status is represented, in the second one some additional
        parameters are returned for example the version number or an error message.
        """
        pr = self.packagesRaw
        status = (False, "Malformed config file")
        if packageName in pr and "install_check" in pr[packageName]:
            v = pr[packageName]["install_check"]
            if "import" in v:
                try:
                    library = importlib.import_module(v["import"])
                    version = str(library.__version__) if hasattr(library, "__version__") else ""
                    status = (True, version)
                except ImportError as e:
                    status = (False, e)
        return status
