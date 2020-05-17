package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nullable;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

/**
 * Ein Ergebnis aus {@code analyze.py}
 */
public class Analysis extends Dictionary {

    @NativeEntryPoint
    protected Analysis(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    private String room;        // bit 0
    private String town;        // bit 1
    private ZonedDateTime time; // bit 2

    /**
     * Gibt den gefundenen Raum zurück.
     */
    @Nullable
    public String room() {
        if ((cached & (1 << 0)) == 0) {
            room = roomRaw();
            if (room == null || room.isEmpty())
                room = null;
            cached |= 1 << 0;
        }
        return room;
    }

    /**
     * Gibt den gefundenen Ort zurück.
     */
    @Nullable
    public String town() {
        if ((cached & (1 << 1)) == 0) {
            town = townRaw();
            if (town == null || town.isEmpty())
                town = null;
            cached |= 1 << 1;
        }
        return town;
    }

    /**
     * Gibt die gefundene Zeit zurück. Das ergebnis ist ein {@code ZonedDateTime} mit der Standard-Zeitzone auf dem Server.
     */
    @Nullable
    public ZonedDateTime time() {
        if ((cached & (1 << 2)) == 0) {
            int[] ldt = timeRaw();
            if (ldt == null) {
                time = null;
            } else {
                LocalDateTime now = LocalDateTime.now();
                int year = ldt[0] < 0 ? now.getYear() : ldt[0];
                int month = ldt[1] < 0 ? now.getMonthValue() : ldt[1];
                int day = ldt[2] < 0 ? now.getDayOfMonth() : ldt[2];
                int hour = ldt[3] < 0 ? now.getHour() : ldt[3];
                int minute = ldt[4] < 0 ? now.getMinute() : ldt[4];
                time = ZonedDateTime.of(LocalDateTime.of(year, month, day, hour, minute), ZoneId.systemDefault());
            }
            cached |= 1 << 2;
        }
        return time;
    }

    @Nullable
    private native String roomRaw();

    @Nullable
    private native String townRaw();

    @Nullable
    private native int[] timeRaw();
}
