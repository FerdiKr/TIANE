import traceback

try:
    import jiane
except ImportError:
    jiane = None

def loadModules(path):
    if jiane is not None:
        try:
            mods = jiane.loadModules(path)
            for x in mods:
                print(str(x.PRIORITY))
                print(str(x.WORDS))
                print(str(x.isValid))
                print(str(x.isValid(None)))
            print(str(len(mods)) + " JAVA-Module geladen.")
            return mods
        except:
            traceback.print_exc()
            print("Konnte JAVA-Module nicht laden.")
    return []

def loadModulesContinuous(path):
    if jiane is not None:
        try:
            mods = jiane.loadModulesContinuous(path)
            print(str(len(mods)) + " JAVA-Continuous-Module geladen.")
            return mods
        except:
            traceback.print_exc()
            print("Konnte JAVA-Continuous-Module nicht laden.")
    return []