package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nonnegative;

/**
 * Ein fortlaufendes TIANE-Modul, dass in Java implementiert wurde. Das Modul muss in einer {@code jar}-Datei
 * im {@code modules} Verzeichnis des TIANE-Servers abgelegt werden. Innerhalb der {@code jar}-Datei
 * muss sich eine Datei namens {@code modules.info} befinden. Dort wird in jeder Zeile ein
 * fully-qualified-name einer Modul-Implementation angegeben.
 * Klassen, die dies implementieren, benötigen einen Standard-Konstruktor (Konstruktor ohne Argumente)
 *
 * <b>Auch jar-Dateien mit fortlaufenden Modulen kommen ins {@code modules}-Verzeichnis und nicht in das
 * Verzeichnis {@code continuous}, damit man normale und fortlaufende Module in eine Datei packen kann.</b>
 */
public interface ModuleContinuous {

    /**
     * Der Name des Moduls. Er muss eindeutig sein.
     */
    @NativeEntryPoint
    String name();

    /**
     * Die Priorität des Moduls. Höhere Zahlen bedeuten eine höhere Priorität.
     */
    @NativeEntryPoint
    default int priority() {
        return 0;
    }

    /**
     * Die Zeit (in Sekunden), die mindestens zwischen zwei Aufrufen des Moduls vergeht.
     */
    @NativeEntryPoint
    @Nonnegative
    int interval();

    /**
     * JAVA-interne Methode. wird einmal aufgerufen. Gibt sie {@code false} zurück, wird das
     * Modul nicht an TIANE weitergegeben, da die ständigen Aufrufe über die JNI unnötig viel
     * Overhead erzeugen würden.
     */
    @NativeEntryPoint
    default boolean active() {
        return true;
    }

    @NativeEntryPoint
    default void start(ModuleWrapperContinuous tiane, LocalStorage localStorage) {
    }

    @NativeEntryPoint
    void run(ModuleWrapperContinuous tiane, LocalStorage localStorage);

    @NativeEntryPoint
    default void stop(ModuleWrapperContinuous tiane, LocalStorage localStorage) {
    }
}
