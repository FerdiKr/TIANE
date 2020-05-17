package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nullable;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Die {@code local_storage}. Vorwiegend einige Hilfsfunktionen und Zwischenspeicherung von Werten
 * sind hier implementiert, um die Arbeit mit der LocalStorage als häufig verwendetem Dictionary
 * zu erleichtern.
 */
public class LocalStorage extends Dictionary {

    @NativeEntryPoint
    protected LocalStorage(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    private Path path;               // bit 0
    private String serverName;       // bit 1
    private String systemName;       // bit 2
    private String homeLocation;     // bit 3
    private String activationPhrase; // bit 4
    @SuppressWarnings("FieldCanBeLocal")
    private List<String> rooms;      // bit 5 //Currently unused as rooms are not cached.
    private List<String> users;      // bit 6

    /**
     * Gibt das Hauptverzeichnis der TIANE Installation zurück.
     */
    public Path tianePath() {
        if ((cached & (1 << 0)) == 0) {
            path = Paths.get(pathRaw()).toAbsolutePath().normalize();
            cached |= 1 << 0;
        }
        return path;
    }

    /**
     * Gibt den Namen des TIANE Servers zurück.
     */
    public String serverName() {
        if ((cached & (1 << 1)) == 0) {
            serverName = serverNameRaw();
            cached |= 1 << 1;
        }
        return serverName;
    }

    /**
     * Gibt den Namen des Sprachassistenten zurück.
     */
    public String systemName() {
        if ((cached & (1 << 2)) == 0) {
            systemName = systemNameRaw();
            cached |= 1 << 2;
        }
        return systemName;
    }

    /**
     * Gibt den bei der Installation angegebenen Wohnort zurück.
     */
    @Nullable
    public String homeLocation() {
        if ((cached & (1 << 3)) == 0) {
            homeLocation = homeLocationRaw();
            cached |= 1 << 3;
        }
        return homeLocation;
    }

    /**
     * Gibt das Aktivierungswort zurück.
     */
    public String activationPhrase() {
        if ((cached & (1 << 4)) == 0) {
            activationPhrase = activationPhraseRaw();
            cached |= 1 << 4;
        }
        return activationPhrase;
    }

    /**
     * Gibt eine Liste aller Raumnamen zurück.
     */
    public List<String> rooms() {
        //if ((cached & (1 << 5)) == 0) {
        String[] raw = roomsRaw();
        rooms = Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
            /*cached |= 1 << 5;
        }*/
        return rooms;
    }

    /**
     * Gibt eine Liste aller Nutzernamen zurück.
     */
    public List<String> users() {
        if ((cached & (1 << 6)) == 0) {
            String[] raw = usersRaw();
            users = Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
            cached |= 1 << 6;
        }
        return users;
    }

    /**
     * Gibt das {@link User}-Objekt für den gegebenen Benutzernamen zurück.
     */
    @Nullable
    public native User user(String name);

    /**
     * Gibt das {@link Room}-Objekt für den gegebenen Raumnamen zurück.
     */
    @Nullable
    public native Room room(String name);

    private native String pathRaw();

    private native String serverNameRaw();

    private native String systemNameRaw();

    @Nullable
    private native String homeLocationRaw();

    private native String activationPhraseRaw();

    private native String[] usersRaw();

    private native String[] roomsRaw();
}
