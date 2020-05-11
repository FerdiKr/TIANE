package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nullable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Ein Python-Dictionary oder eine Python-Liste. Beim Umgang mit dieser Klasse gibt es einiges zu beachten:
 * <ul>
 *     <li>Werte, die nicht im Dictionary vorhanden sind oder einen falschen Typ haben liefern {@code null}, 0 oder {@code false} zurück.</li>
 *     <li>Es kann auf untergeordnete Dictionaries zugegriffen werden. Der Schlüssel {@code users.Ferdi.room} zeigt auf den Wert {@code room} im untergeordneten dictionary {@code Ferdi} des untergeordneten Dictionaries {@code users}</li>
 *     <li>Die {@code set}-Methoden können keine untergeordneten Dictionaries anlegen, da das Programm nicht wissen kann, ob ein echtes dictionary oder eine Liste gewünscht ist.</li>
 *     <li>Wenn als Listenindex ein Wert angegeben wird, der keine Zahl ist, gibt es eine {@code NumberFormatException}</li>
 *     <li>Wie in python sind negative Listenschlüssel erlaubt.</li>
 *     <li>Werte aus einem Dictionary sollten zwischengespeichert werden anstatt sie sehr häufig abzufragen. Ausnahmen sin die konkreteren Methoden in {@link LocalStorage}, {@link User} und {@link Room}.</li>
 * </ul>
 */
public class Dictionary extends LazyPythonObject {

    @NativeEntryPoint
    protected Dictionary(long pointer) {
        super(pointer);
    }

    /**
     * Erstellt ein neuer {@code Dictionary}, dem ein echtes python dictionary zu Grunde liegt.
     */
    public static native Dictionary createDict();

    /**
     * Erstellt ein neuer {@code Dictionary}, dem eine python liste zu Grunde liegt.
     */
    public static native Dictionary createList();

    /**
     * Gibt ein untergeordnetes Dictionary am gegebenen Pfad zurück.
     */
    @Nullable
    public Dictionary getDict(String path) {
        return getDictRaw(getTokens(path));
    }

    /**
     * Gibt eine Zeichenkette am gegebenen Pfad zurück.
     */
    @Nullable
    public String getString(String path) {
        return getStringRaw(getTokens(path));
    }

    /**
     * Gibt eine ganze Zahl (int) am gegebenen Pfad zurück.
     */
    public int getInt(String path) {
        return getIntRaw(getTokens(path));
    }

    /**
     * Gibt eine ganze Zahl (long) am gegebenen Pfad zurück.
     */
    public long getLong(String path) {
        return getLongRaw(getTokens(path));
    }

    /**
     * Gibt ein Gleitkommazahl am gegebenen Pfad zurück.
     */
    public double getDouble(String path) {
        return getDoubleRaw(getTokens(path));
    }

    /**
     * Gibt einen Wahrheitswert am gegebenen Pfad zurück.
     */
    public boolean getBool(String path) {
        return getBoolRaw(getTokens(path));
    }

    /**
     * Gibt eine Liste mit allen Schlüsseln des Dictionaries zurück.
     */
    public List<String> keys() {
        return Collections.unmodifiableList(new ArrayList<>(Arrays.asList(keysRaw())));
    }

    @Nullable
    private native Dictionary getDictRaw(String[] tokens);

    @Nullable
    private native String getStringRaw(String[] tokens);

    private native int getIntRaw(String[] tokens);

    private native long getLongRaw(String[] tokens);

    private native double getDoubleRaw(String[] tokens);

    private native boolean getBoolRaw(String[] tokens);

    private native String[] keysRaw();

    /**
     * Setzt das gegebene Dictionary an den gegebenen Pfad.
     */
    public void setDict(String path, Dictionary dictionary) {
        setDictRaw(getTokens(path), dictionary);
    }

    /**
     * Setzt die gegebene Zeichenkette an den gegebenen Pfad.
     */
    public void setString(String path, String string) {
        setStringRaw(getTokens(path), string);
    }

    /**
     * Setzt die gegebene Zahl an den gegebenen Pfad.
     */
    public void setInt(String path, int value) {
        setIntRaw(getTokens(path), value);
    }

    /**
     * Setzt die gegebene Zahl an den gegebenen Pfad.
     */
    public void setLong(String path, long value) {
        setLongRaw(getTokens(path), value);
    }

    /**
     * Setzt die gegebene Zahl an den gegebenen Pfad.
     */
    public void setDouble(String path, double value) {
        setDoubleRaw(getTokens(path), value);
    }

    /**
     * Setzt den gegebenen Wahrheitswert an den gegebenen Pfad.
     */
    public void setBool(String path, boolean value) {
        setBoolRaw(getTokens(path), value);
    }

    private native void setDictRaw(String[] tokens, Dictionary dictionary);

    private native void setStringRaw(String[] tokens, String string);

    private native void setIntRaw(String[] tokens, int value);

    private native void setLongRaw(String[] tokens, long value);

    private native void setDoubleRaw(String[] tokens, double value);

    private native void setBoolRaw(String[] tokens, boolean value);

    private static String[] getTokens(String path) {
        if (path.contains(".")) {
            String[] tokens = path.split("[^\\\\]\\.");
            boolean removeEmpties = false;
            for (int i = 0; i < tokens.length; i++) {
                if (tokens[i].isEmpty()) {
                    removeEmpties = true;
                } else {
                    tokens[i] = tokens[i].replace("\\\\", "\\");
                }
            }
            if (removeEmpties) {
                ArrayList<String> list = new ArrayList<>();
                for (String token : tokens) {
                    if (!token.isEmpty()) {
                        list.add(token);
                    }
                }
                return list.toArray(new String[]{});
            } else {
                return tokens;
            }
        } else {
            return new String[]{path};
        }
    }
}
