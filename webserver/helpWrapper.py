#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

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
