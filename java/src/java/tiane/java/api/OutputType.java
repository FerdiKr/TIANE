package tiane.java.api;

import javax.annotation.Nonnull;

/**
 * Enthält Methoden mit einem Benutzer zu kommunizieren.
 */
public enum OutputType {

    /**
     * Automatisch die beste Methode wählen. (Standard)
     */
    AUTO("auto"),

    /**
     * Sprach-Ein-/Ausgabe
     */
    SPEECH("speech"),

    /**
     * Ein-/Ausgabe über telegram
     */
    TELEGRAM("telegram"),

    /**
     * Ein-/Ausgabe über telegram, allerding sendet TIANE Nachrichten nicht als text, sondern
     * als Sprachnachricht.
     */
    TELEGRAM_SPEECH(TELEGRAM.in, "telegram_speech");

    /**
     * Der intern verwendete Wert bei der Eingabe.
     */
    @Nonnull
    public final String in;

    /**
     * Der intern verwendete Wert bei der Ausgabe.
     */
    @Nonnull
    public final String out;

    OutputType(String type) {
        this.in = type;
        this.out = type;
    }

    OutputType(String in, String out) {
        this.in = in;
        this.out = out;
    }
}
