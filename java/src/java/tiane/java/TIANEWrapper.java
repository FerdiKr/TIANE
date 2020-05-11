package tiane.java;

import tiane.java.api.Module;
import tiane.java.api.ModuleContinuous;
import tiane.util.NativeEntryPoint;

/**
 * Diese Klasse startet TIANE und leitet  Module an sie Weiter.
 */
public class TIANEWrapper {

    /**
     * Startet TIANE.
     *
     * @param runPy  Absoluter Pfad der {@code TIANE_server.py} Datei
     * @param runDir Absoluter Pfad des TIANE-Server Hauptverzeichnisses.
     * @param dlopen Ein Array von Bibliotheken, für die {@code dlopen} aufgerufen werden soll, bevor TIANE startet.
     *               Dies wird wegen eines Bugs benötigt.
     */
    public static native void startTiane(String runPy, String runDir, String[] dlopen);

    /**
     * Sucht normale Module im angegebenen Pfad. Diese Methode wird vom nativen Code aus aufgerufen.
     */
    @NativeEntryPoint
    public static Module[] loadModules(String path) {
        return ModuleFinder.findModules(path, Module.class).toArray(new Module[]{});
    }

    /**
     * Sucht fortlaufende Module im angegebenen Pfad. Diese Methode wird vom nativen Code aus aufgerufen.
     */
    @NativeEntryPoint
    public static ModuleContinuous[] loadModulesContinuous(String path) {
        return ModuleFinder.findModules(path, ModuleContinuous.class).toArray(new ModuleContinuous[]{});
    }
}
