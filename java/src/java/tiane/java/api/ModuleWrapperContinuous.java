package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nonnegative;
import javax.annotation.Nullable;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Eine Instanz dieser Klasse wird fortlaufenden Modulen in
 * ihrer {@link ModuleContinuous#run(ModuleWrapperContinuous, LocalStorage) run} Methode übergeben.
 */
public class ModuleWrapperContinuous extends LazyPythonObject {

    @NativeEntryPoint
    protected ModuleWrapperContinuous(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    private LocalStorage lstorage; // bit 0
    private Path path;             // bit 1
    private String serverName;     // bit 2
    private String systemName;     // bit 3
    private List<String> rooms;    // bit 4
    private List<String> users;    // bit 5
    private Tiane tiane;           // bit 6
    private int intervalTime;      // bit 7
    private int counter;           // bit 8

    /**
     * Enthält den {@link LocalStorage}. Eigentlich überflüssig, weil
     * redundant (Module bekommen den local_storage ja ohnehin als
     * Parameter übergeben), wurde aber aus Kompatibilitätsgründen mit einigen
     * älteren Modulen behalten.
     */
    public LocalStorage localStorage() {
        if ((cached & (1 << 0)) == 0) {
            lstorage = lstorageRaw();
            cached |= 1 << 0;
        }
        return lstorage;
    }

    /**
     * Enthält den absoluten Pfad zum TIANE-Ordner dieses Geräts.
     */
    public Path path() {
        if ((cached & (1 << 1)) == 0) {
            path = Paths.get(pathRaw()).toAbsolutePath().normalize();
            cached |= 1 << 1;
        }
        return path;
    }

    /**
     * Enthält den Namen deines TIANE-Servers (den Namen, den du bei der
     * Einrichtung von TIANE festgelegt hast, nicht etwa den PC-Namen oder
     * ähnliches).
     */
    public String serverName() {
        if ((cached & (1 << 2)) == 0) {
            serverName = serverNameRaw();
            cached |= 1 << 2;
        }
        return serverName;
    }

    /**
     * Enthält den Namen deines Sprachassistenten, den du bei der Einrichtung
     * festgelegt hast (z.B. „TIANE“).
     */
    public String systemName() {
        if ((cached & (1 << 3)) == 0) {
            systemName = systemNameRaw();
            cached |= 1 << 3;
        }
        return systemName;
    }

    /**
     * Enthält eine Liste der Namen aller Räume in deinem
     * TIANE-Netzwerk.
     */
    public List<String> rooms() {
        if ((cached & (1 << 4)) == 0) {
            String[] raw = roomsRaw();
            rooms = Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
            cached |= 1 << 4;
        }
        return rooms;
    }

    /**
     * Enthält eine Liste der Nutzernamen aller Nutzer in deinem TIANE-Netzwerk.
     */
    public List<String> users() {
        if ((cached & (1 << 5)) == 0) {
            String[] raw = usersRaw();
            users = Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
            cached |= 1 << 5;
        }
        return users;
    }

    /**
     * Enthält den „Kern“ von TIANE, nämlich die Hauptinstanz der „echten“ Tiane-
     * Klasse des Geräts, von wo aus alle anderen Objekte verwaltet werden.Ermöglicht extrem tiefe Eingriffe ins System von TIANE, aber nur wenn du
     * wirklich weißt, was du tust. Als Referenz wird auf jeden Fall die Lektüre
     * unserer allgemeinen Dokumentation empfohlen.
     *
     * @see Tiane
     */
    public Tiane core() {
        if ((cached & (1 << 6)) == 0) {
            tiane = coreRaw();
            cached |= 1 << 6;
        }
        return tiane;
    }

    /**
     * Enthält die per Hyperparameter eingestellte Mindestzeit zwischen zwei Aufrufen (in Sekunden).
     */
    @Nonnegative
    public int intervalTime() {
        if ((cached & (1 << 7)) == 0) {
            intervalTime = intervalTimeRaw();
            cached |= 1 << 7;
        }
        return intervalTime;
    }

    /**
     * Zählt, wie oft dieses continuous_module seit dem letzten Neustart/Reload bereits aufgerufen wurde.
     */
    @Nonnegative
    public int counter() {
        if ((cached & (1 << 8)) == 0) {
            counter = counterRaw();
            cached |= 1 << 8;
        }
        return counter;
    }

    public native boolean startModule(@Nullable String name, @Nullable String text, @Nullable String user, @Nullable String room);

    /**
     * Sendet ein event an alle WebSocket-Verbindungen. Diese können dann darauf
     * reagieren. Der Name des events ist frei wählbar. Das Disctionary wird später
     * zu JSON-Daten umgewandelt.
     */
    public void sendWebSocketEvent(String event, Dictionary data) {
        core().sendWebSocketEvent(event, data);
    }

    private native LocalStorage lstorageRaw();

    private native String pathRaw();

    private native String serverNameRaw();

    private native String systemNameRaw();

    private native String[] roomsRaw();

    private native String[] usersRaw();

    private native Tiane coreRaw();

    private native int intervalTimeRaw();

    private native int counterRaw();
}
