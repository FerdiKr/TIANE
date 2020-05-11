package tiane.java.api;

import tiane.util.NativeEntryPoint;

/**
 * Ein {@code LazyPythonObject} kapselt eine Speicheradresse auf ein echtes python-objekt. Die Daten
 * werden erst abgefragt, wenn sie gebraucht werden. Daten, die sich nicht verändern werden häufig zwischengespeichert.
 */
public class LazyPythonObject {

    @NativeEntryPoint
    private final long pointer;

    /**
     * <b>Dieser Konstruktor muss genau so überschrieben werden.</b>
     */
    @NativeEntryPoint
    protected LazyPythonObject(long pointer) {
        this.pointer = pointer;
    }

    @Override
    protected native void finalize();

    @Override
    public int hashCode() {
        return (int) pointer;
    }

    /**
     * Gibt {@code true} zurück, wenn das andere Objekt auch ein {@code LazyPythonObject} ist
     * und auf die gleiche Speicheradresse zeigt.
     */
    @Override
    public boolean equals(Object o) {
        if (o instanceof LazyPythonObject) {
            return ((LazyPythonObject) o).pointer == pointer;
        } else {
            return false;
        }
    }

    @Override
    public String toString() {
        return "WrappedPython(" + Long.toHexString(pointer) + ")";
    }
}
