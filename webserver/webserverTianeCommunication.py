import sys
import os
from multiprocessing import Process
import mmap
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), "../server/"))
from TIANE_server import runMain
class mThr():
    """
    the mThr-Class wraps around the main TIANE-Server. TIANE is started in a
    seperate Process and not a Thread - so you can kill them without modifying
    the TIANE-Part. The communication runs via two memory-maps which can be
    accessed by both processes.
    """
    def __init__(self):
        self.thr = None
        self.command = mmap.mmap(-1, 2048) # reserve 128kiB in Vstor
        self.feedback = mmap.mmap(-1, 1024*1024) # reserve one Megabyte in Vstor

    def start(self):
        """
        The process is started and the two memory maps linked into the process
        """
        self.thr = Process(target=runMain, args=(self.command, self.feedback,))
        try:
            self.thr.start()
        except AssertionError:
            pass
    def stop(self):
        """
        The process is killed without asking, use with care!
        """
        self.thr.terminate()

    def status(self):
        """
        If the thread wasn't started yet, it returns "unknown", if it is running,
        it returns "running". If the process crashed or was stopped manually, it
        responds with "stopped"
        """
        if self.thr is not None:
            data = "running" if self.thr.is_alive() else "stopped"
        else:
            data = "unknown"
        return data

    def getFeed(self):
        """
        This method parses the Local storage-Variable and returns it for later
        use in other functions.
        """
        self.feedback.seek(0)
        try:
            pick = pickle.load(self.feedback)
        except EOFError:
            pick = {}
        return pick
