import traceback

try:
    import jiane
except ImportError:
    jiane = None


class JavaModule:
    def __init__(self, jianeModule):
        self.mod = jianeModule
        self.PRIORITY = jianeModule.PRIORITY
        self.SECURE = jianeModule.SECURE
        self.WORDS = jianeModule.WORDS
        self.__name__ = jianeModule.MODNAME

    def isValid(self, text):
        return jiane.javaModuleIsValid(self.mod, text)

    def telegram_isValid(self, text):
        return jiane.javaModuleIsValidTelegram(self.mod, text)

    def handle(self, text, tiane, profile):
        return jiane.javaModuleHandle(self.mod, text, tiane, profile)


class JavaModuleContinuous:
    def __init__(self, jianeModule):
        self.mod = jianeModule
        self.PRIORITY = jianeModule.PRIORITY
        self.INTERVAL = jianeModule.INTERVAL
        self.INTERVALL = jianeModule.INTERVAL
        self.__name__ = jianeModule.MODNAME

    def start(self, tiane, profile):
        return jiane.javaContinuousModuleStart(self.mod, tiane, profile)

    def run(self, tiane, profile):
        return jiane.javaContinuousModuleRun(self.mod, tiane, profile)

    def stop(self, tiane, profile):
        return jiane.javaContinuousModuleStop(self.mod, tiane, profile)


def loadModules(path):
    if jiane is not None:
        try:
            mods = jiane.loadModules(path)
            wrappedMods = []
            for x in mods:
                if x is not None: # Wenn das Modul von Java aus deaktiviert wurde gibt es einen None-Eintrag.
                    wrappedMods.append(JavaModule(x))
                    print("[INFO] Java-Modul " + x.MODNAME + " geladen")
            return wrappedMods
        except:
            traceback.print_exc()
            print("Konnte JAVA-Module nicht laden.")
    return []


def loadModulesContinuous(path):
    if jiane is not None:
        try:
            mods = jiane.loadModulesContinuous(path)
            wrappedMods = []
            for x in mods:
                if x is not None: # Wenn das Modul von Java aus deaktiviert wurde gibt es einen None-Eintrag.
                    wrappedMods.append(JavaModuleContinuous(x))
                    print("[INFO] Fortlaufendes Java-Modul " + x.MODNAME + " geladen")
            return wrappedMods
        except:
            traceback.print_exc()
            print("Konnte JAVA-Module nicht laden.")
    return []

def createJavalogger(logging):
    if jiane is not None:
        try:
            jiane.createLogger(logging)
        except:
            traceback.print_exc()
            print("Der JAVA-Logger konnte nicht instanziiert werden.")

def setSignalHandlers():
    if jiane is not None:
        jiane.setSignalHandlers()

def shouldStop():
    if jiane is not None:
        return jiane.shouldStop()
    else:
        return False