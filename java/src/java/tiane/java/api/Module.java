package tiane.java.api;

import tiane.util.NativeEntryPoint;

/**
 * Ein TIANE-Modul, dass in Java implementiert wurde. Das Modul muss in einer {@code jar}-Datei
 * im {@code modules} Verzeichnis des TIANE-Servers abgelegt werden. Innerhalb der {@code jar}-Datei
 * muss sich eine Datei namens {@code modules.info} befinden. Dort wird in jeder Zeile ein
 * fully-qualified-name einer Modul-Implementation angegeben.
 * Klassen, die dies implementieren, benötigen einen Standard-Konstruktor (Konstruktor ohne Argumente)
 */
public interface Module {

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
     * Gibt an ob das Modul "sicher" ist. Siehe SecureModules.md im repository root.
     */
    @NativeEntryPoint
    default boolean secure() {
        return false;
    }

    /**
     * Ein array von Wörtern, die als Hilfe für die Sprcherkennung verwendet werden sollen.
     */
    @NativeEntryPoint
    default String[] words() {
        return new String[]{};
    }

    /**
     * Prüft, ob das Modul für den Text geeignet ist / den Text versteht.
     */
    @NativeEntryPoint
    boolean isValid(String text);

    /**
     * Prüft, ob das Modul für den Text geeignet ist / den Text versteht. Diese Methode wird zuerst
     * aufgerufen, wenn der Text mit Telegram gesendet wurde. So können spezielle Telegram-Module
     * hier reagieren und haben dann Vorrang.
     */
    @NativeEntryPoint
    default boolean isValidTelegram(String text) {
        return false;
    }

    /**
     * JAVA-interne Methode. wird einmal aufgerufen. Gibt sie {@code false} zurück, wird das
     * Modul nicht an TIANE weitergegeben, da die ständigen Aufrufe über die JNI unnötig viel
     * Overhead erzeugen würden.
     */
    @NativeEntryPoint
    default boolean active() {
        return true;
    }

    /**
     * Führt die Aktion des Moduls aus.
     *
     * @param text         Der Text, der vom Benutzer angegeben wurde
     * @param tiane        Eine Instanz von {@link ModuleWrapper} um TIANE zusteuern
     * @param localStorage Der {@link LocalStorage}
     */
    @NativeEntryPoint
    void handle(String text, ModuleWrapper tiane, LocalStorage localStorage);
}
