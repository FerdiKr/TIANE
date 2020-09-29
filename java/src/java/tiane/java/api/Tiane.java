package tiane.java.api;

import tiane.util.NativeEntryPoint;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Noch nicht implementiert.
 */
public class Tiane extends LazyPythonObject {

    @NativeEntryPoint
    protected Tiane(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    // bit  0 unused
    private Dictionary userList;            // bit  1
    private Dictionary userDict;            // bit  2
    // bit  3 unused
    private Dictionary activeModules;       // bit  4
    private Dictionary continuousModules;   // bit  5
    private Dictionary roomDict;            // bit  6
    private Dictionary otherDevices;        // bit  7
    private Dictionary devicesConnecting;   // bit  8
    private Dictionary telegramQueuedUsers; // bit  9
    private LocalStorage lstorage;          // bit 10
    private Dictionary roomList;            // bit 11
    private Path path;                      // bit 12
    private String serverName;              // bit 13
    private String systemName;              // bit 14

    public Dictionary userList() {
        if ((cached & (1 << 1)) == 0) {
            userList = userListRaw();
            cached |= 1 << 1;
        }
        return userList;
    }

    public Dictionary userDict() {
        if ((cached & (1 << 2)) == 0) {
            userDict = userDictRaw();
            cached |= 1 << 2;
        }
        return userDict;
    }

    public Dictionary activeModules() {
        if ((cached & (1 << 4)) == 0) {
            activeModules = activeModulesRaw();
            cached |= 1 << 4;
        }
        return activeModules;
    }

    public Dictionary continuousModules() {
        if ((cached & (1 << 5)) == 0) {
            continuousModules = continuousModulesRaw();
            cached |= 1 << 5;
        }
        return continuousModules;
    }

    public Dictionary roomDict() {
        if ((cached & (1 << 6)) == 0) {
            roomDict = roomDictRaw();
            cached |= 1 << 6;
        }
        return roomDict;
    }

    public Dictionary otherDevices() {
        if ((cached & (1 << 7)) == 0) {
            otherDevices = otherDevicesRaw();
            cached |= 1 << 7;
        }
        return otherDevices;
    }

    public Dictionary devicesConnecting() {
        if ((cached & (1 << 8)) == 0) {
            devicesConnecting = devicesConnectingRaw();
            cached |= 1 << 8;
        }
        return devicesConnecting;
    }

    public Dictionary telegramQueuedUsers() {
        if ((cached & (1 << 9)) == 0) {
            telegramQueuedUsers = telegramQueuedUsersRaw();
            cached |= 1 << 9;
        }
        return telegramQueuedUsers;
    }

    public LocalStorage localStorage() {
        if ((cached & (1 << 10)) == 0) {
            lstorage = lstorageRaw();
            cached |= 1 << 10;
        }
        return lstorage;
    }

    public Dictionary roomList() {
        if ((cached & (1 << 11)) == 0) {
            roomList = roomListRaw();
            cached |= 1 << 11;
        }
        return roomList;
    }

    /**
     * Enthält den absoluten Pfad zum TIANE-Ordner dieses Geräts.
     */
    public Path path() {
        if ((cached & (1 << 12)) == 0) {
            path = Paths.get(pathRaw()).toAbsolutePath().normalize();
            cached |= 1 << 12;
        }
        return path;
    }

    /**
     * Enthält den Namen deines TIANE-Servers (den Namen, den du bei der
     * Einrichtung von TIANE festgelegt hast, nicht etwa den PC-Namen oder
     * ähnliches).
     */
    public String serverName() {
        if ((cached & (1 << 13)) == 0) {
            serverName = serverNameRaw();
            cached |= 1 << 13;
        }
        return serverName;
    }

    /**
     * Enthält den Namen deines Sprachassistenten, den du bei der Einrichtung
     * festgelegt hast (z.B. „TIANE“).
     */
    public String systemName() {
        if ((cached & (1 << 14)) == 0) {
            systemName = systemNameRaw();
            cached |= 1 << 14;
        }
        return systemName;
    }

    public native boolean openMode();

    public native void openMode(boolean openMode);

    public native boolean presentationMode();

    public native void presentationMode(boolean presentationMode);

    /**
     * Analysiert den gegebenen text mit {@code analyzer.py}
     */
    public native Analysis analyze(String text);

    /**
     * Sendet ein event an alle WebSocket-Verbindungen. Diese können dann darauf
     * reagieren. Der Name des events ist frei wählbar. Das Disctionary wird später
     * zu JSON-Daten umgewandelt.
     */
    public native void sendWebSocketEvent(String event, Dictionary data);

    private native Dictionary userListRaw();

    private native Dictionary userDictRaw();

    private native Dictionary activeModulesRaw();

    private native Dictionary continuousModulesRaw();

    private native Dictionary roomDictRaw();

    private native Dictionary otherDevicesRaw();

    private native Dictionary devicesConnectingRaw();

    private native Dictionary telegramQueuedUsersRaw();

    private native LocalStorage lstorageRaw();

    private native Dictionary roomListRaw();

    private native String pathRaw();

    private native String serverNameRaw();

    private native String systemNameRaw();
}
