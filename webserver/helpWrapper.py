#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import time
import json
import subprocess
import importlib
from threading import Thread

__author__     = "olagino"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"

class InstallWrapper():
    """
    The install wrapper class initiates a thread and enables a few helper functions
    to install components described in the services.json file
    """
    def __init__(self):
        self.readConfig()
        self.installQueue = []
        self.installStatus = "idle"
        self.installLog = ""

        self._runThread = True
        self._thread = Thread(target=self._threadedLoop)
        self._thread.start()


    def __del__(self):
        # stop thread
        self._runThread = False
        self._thread.join()

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
                data["status"] = str(self.checkStatus(el))
            packList.append(data)
        return packList

    def getInstallerStatus(self):
        state = {
            "status": self.installStatus,
            "log": self.installLog
        }
        return state


    def startInstallation(self, packageName):
        if packageName in self.packagesRaw:
            self.installQueue.append(packageName)
            return True
        else:
            return False

    def _threadedLoop(self):
        """
        _threadedLoop is the main wrapper for installation processes. Optimally
        it gets started when the class is instanciated.
        """
        while self._runThread:
            if len(self.installQueue) == 0:
                self.installStatus = "idle"
                self.installLog = ""
                time.sleep(0.3)
            else:
                package = self.installQueue.pop()
                self.installStatus = "installing"
                data = self.packagesRaw[package]
                if "apt_installs" in data:
                    t_1 = time.time()
                    self.installLog += "\n Updating package cache…"
                    proc = subprocess.Popen(["apt-get", "update", "-y"])
                    proc.wait()
                    n = time.time() - t_1
                    self.installLog += "\n took " + str(round(n*10,1)) + " seconds."
                    for ai in data["apt_installs"]:
                        self._installRaw(ai, "apache")
                if "python_installs" in data:
                    # pip.main() is depracted so let's use subprocesses
                    for pi in data["python_installs"]:
                        self._installRaw(pi, "pip3")
        return None

    def _installRaw(self, packageName, type):
        "This"
        try:
            self.installLog += "\n Starting installation for " + str(packageName) + "."
            t_2 = time.time()
            if type == "apache":
                command = ["apt-get", "install", packageName, "-y"]
            elif type == "pip3":
                command = ["pip3", "install", packageName]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while process.returncode == None:
                text = process.stdout.read()
                if len(text) > 0:
                    self.installLog += str(text)
                errs = process.stderr.read()
                if len(errs) > 0:
                    self.installLog += str(errs)
                self.installLog += "poll" + str(process.poll())
            if process.returncode == 0:
                self.installLog += "\n " + str(packageName) + " got installed properly."
                self.installLog += " Took " + str(round(time.time() - t_2, 1)) + " seconds."
            else:
                self.installLog += "\n Installation for " + str(packageName) + " failed. (apt returned a non-zero code: " + str(process.returncode) + ")"
        except OSError as e:
            self.installLog += "\n Installation for " + str(packageName) + " failed. (" + str(e) + ")"


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
