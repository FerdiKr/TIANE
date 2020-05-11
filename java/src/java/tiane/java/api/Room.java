package tiane.java.api;

import tiane.util.NativeEntryPoint;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Ein Eintrag in der Liste {@code rooms} in der {@link LocalStorage}.
 */
public class Room extends Dictionary {

    @NativeEntryPoint
    protected Room(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    private String name; // bit 0

    /**
     * Gibt den Namen des Raums zurück.
     */
    public String name() {
        if ((cached & (1 << 0)) == 0) {
            name = nameRaw();
            cached |= 1 << 0;
        }
        return name;
    }

    /**
     * Testet, ob sich ein Benutzer in diesem Raum befindet.
     */
    public boolean user(User user) {
        return users().contains(user.name());
    }

    /**
     * Testet, ob sich ein Benutzer in diesem Raum befindet.
     */
    public boolean user(String user) {
        return users().contains(user);
    }

    /**
     * Gibt eine Liste aller Benutzernamen der Benutzer in diesem Raum zurück.
     */
    public List<String> users() {
        String[] raw = usersRaw();
        return Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
    }

    private native String nameRaw();

    private native String[] usersRaw();
}
