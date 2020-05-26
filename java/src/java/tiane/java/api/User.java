package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nullable;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;

/**
 * Ein Eintrag in der Liste {@code users} in der {@link LocalStorage}.
 */
public class User extends Dictionary {

    @NativeEntryPoint
    protected User(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    private String name;        // bit 0
    private String firstName;   // bit 1
    private String lastName;    // bit 2
    private String role;        // bit 3
    private int uid;            // bit 4
    private long telegramId;    // bit 5
    private Path path;          // bit 6
    private LocalDate birthday; // bit 7

    /**
     * Gibt den Benutzernamen des Benutzers zurück.
     */
    public String name() {
        if ((cached & (1 << 0)) == 0) {
            name = nameRaw();
            cached |= 1 << 0;
        }
        return name;
    }

    /**
     * Gibt den Vornamen des Benutzers zurück.
     */
    public String firstName() {
        if ((cached & (1 << 1)) == 0) {
            firstName = firstNameRaw();
            cached |= 1 << 1;
        }
        return firstName;
    }

    /**
     * Gibt den Nachnamen des Benutzers zurück.
     */
    public String lastName() {
        if ((cached & (1 << 2)) == 0) {
            lastName = lastNameRaw();
            cached |= 1 << 2;
        }
        return lastName;
    }

    /**
     * Gibt die Rolle auf dem Server zurück. ("USER" oder "ADMIN". Bis jetzt nicht verwendet.)
     */
    public String role() {
        if ((cached & (1 << 3)) == 0) {
            role = roleRaw();
            cached |= 1 << 3;
        }
        return role;
    }

    /**
     * Gibt die uid des Benutzers zurück. Ein int-Wert, der pro Benutzer eindeutig ist.
     */
    public int uid() {
        if ((cached & (1 << 4)) == 0) {
            uid = uidRaw();
            cached |= 1 << 4;
        }
        return uid;
    }

    /**
     * Gibt die Telegram-User-Id des Benutzers zurück.
     */
    public long telegramId() {
        if ((cached & (1 << 5)) == 0) {
            telegramId = telegramIdRaw();
            cached |= 1 << 5;
        }
        return telegramId;
    }

    /**
     * Gibt das Verzeichnis des Benutzers auf dem Server zurück.
     */
    public Path path() {
        if ((cached & (1 << 6)) == 0) {
            path = Paths.get(pathRaw()).toAbsolutePath().normalize();
            cached |= 1 << 6;
        }
        return path;
    }

    /**
     * Gibt das Geburtsdatum des Benutzers zurück.
     */
    @Nullable
    public LocalDate birthday() {
        if ((cached & (1 << 7)) == 0) {
            int[] ldt = birthdayRaw();
            if (ldt == null) {
                birthday = null;
            } else {
                LocalDate now = LocalDate.now();
                int year = ldt[0] < 0 ? now.getYear() : ldt[0];
                int month = ldt[1] < 0 ? now.getMonthValue() : ldt[1];
                int day = ldt[2] < 0 ? now.getDayOfMonth() : ldt[2];
                birthday = LocalDate.of(year, month, day);
            }
            cached |= 1 << 7;
        }
        return birthday;
    }

    /**
     * Gibt den Raumnamen des Raum, in dem sich der Benutzer befindet zurück.
     */
    @Nullable
    public native String room();

    private native String nameRaw();

    private native String firstNameRaw();

    private native String lastNameRaw();

    private native String roleRaw();

    private native int uidRaw();

    private native long telegramIdRaw();

    private native String pathRaw();

    @Nullable
    private native int[] birthdayRaw();
}
