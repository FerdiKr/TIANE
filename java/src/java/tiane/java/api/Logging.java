package tiane.java.api;

import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.Marker;
import org.apache.logging.log4j.message.Message;
import org.apache.logging.log4j.spi.AbstractLogger;
import org.apache.logging.log4j.spi.StandardLevel;
import tiane.util.NativeEntryPoint;

/**
 * Diese Klasse ermöglicht den Zugriff auf den TIANE-Log. Um eine Instanz dieser
 * Klasse zu erhalten, nutze die statische {@link Logging#get() get} Methode.
 * <p>
 * Diese Klasse ist ein log4j-Logger.
 */
public class Logging extends AbstractLogger {

    private final NativeLogger underlying;

    @NativeEntryPoint
    protected Logging(long pointer) {
        underlying = new NativeLogger(pointer);
        instance = this;
    }

    private static Logging instance;

    /**
     * Gibt sie Singleton-Instanz des TIANE-Logs zurück.
     */
    public static Logging get() {
        return instance;
    }

    private void writeRaw(Level type, String message) {
        if (type.intLevel() == 0) { // OFF
            underlying.writeRaw("OFF", message, false);
        } else if (type.intLevel() >= StandardLevel.TRACE.intLevel()) { // TRACE
            underlying.writeRaw("TRACE", message, true);
        } else if (type.intLevel() >= StandardLevel.DEBUG.intLevel()) { // TRACE
            underlying.writeRaw("DEBUG", message, true);
        } else if (type.intLevel() >= StandardLevel.INFO.intLevel()) { // INFO
            underlying.writeRaw("INFO", message, true);
        } else if (type.intLevel() >= StandardLevel.WARN.intLevel()) { // WARN
            underlying.writeRaw("WARNING", message, true);
        } else if (type.intLevel() >= StandardLevel.ERROR.intLevel()) { // ERROR
            underlying.writeRaw("ERROR", message, true);
        } else { // FATAL
            underlying.writeRaw("ERROR", "FATAL - " + message, true);
        }
    }

    private static class NativeLogger extends LazyPythonObject {

        protected NativeLogger(long pointer) {
            super(pointer);
        }

        public native void writeRaw(String type, String message, boolean show);
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, Message message, Throwable t) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, CharSequence message, Throwable t) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, Object message, Throwable t) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Throwable t) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object... params) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3, Object p4) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3, Object p4, Object p5) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3, Object p4, Object p5, Object p6) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3, Object p4, Object p5, Object p6, Object p7) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3, Object p4, Object p5, Object p6, Object p7, Object p8) {
        return true;
    }

    @Override
    public boolean isEnabled(Level level, Marker marker, String message, Object p0, Object p1, Object p2, Object p3, Object p4, Object p5, Object p6, Object p7, Object p8, Object p9) {
        return true;
    }

    @Override
    public void logMessage(String fqcn, Level level, Marker marker, Message message, Throwable t) {
        writeRaw(level, message.getFormattedMessage());
        if (t != null) {
            Throwable e = t;
            writeRaw(level, "Excetion: " + e.getClass().getSimpleName() + ": " + e.getMessage());
            for (StackTraceElement strace : e.getStackTrace()) {
                writeRaw(level, "   at " + strace);
            }
            if (e.getSuppressed() != null && e.getSuppressed().length > 0) {
                writeRaw(level, " The exception suppressed several others:");
                for (Throwable ee : e.getSuppressed()) {
                    writeRaw(level, "  - " + ee.getClass().getSimpleName() + ": " + e.getMessage());
                }
            }
            while (e.getCause() != null && e.getCause() != e) {
                e = e.getCause();
                writeRaw(level, " Caused by " + e.getClass().getSimpleName() + ": " + e.getMessage());
                for (StackTraceElement strace : e.getStackTrace()) {
                    writeRaw(level, "   at " + strace);
                }
                if (e.getSuppressed() != null && e.getSuppressed().length > 0) {
                    writeRaw(level, " The exception suppressed several others:");
                    for (Throwable ee : e.getSuppressed()) {
                        writeRaw(level, "  - " + ee.getClass().getSimpleName() + ": " + e.getMessage());
                    }
                }
            }
        }
    }

    @Override
    public Level getLevel() {
        return Level.ALL;
    }
}