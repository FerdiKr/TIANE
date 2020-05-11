package tiane.java;

import javax.annotation.Nonnull;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Objects;
import java.util.Queue;

/**
 * Das HAuptprogramm.
 */
public class Main {

    private static String COMPILED_PYTHON = null;
    private static Path TIANE_PATH = null;
    private static Thread TIANE_THREAD = null;

    /**
     * Lädt alle Bibliotheken und started TIANE.
     */
    public static void main(String[] args) {

        try {
            COMPILED_PYTHON = new BufferedReader(new InputStreamReader(Main.class.getResourceAsStream("COMPILED_PYTHON"))).readLine();
        } catch (IOException e) {
            System.err.println("Could not get the python version that was linked against. Invalid jarfile: " + e.getMessage());
            System.exit(1);
        }
        System.out.println("Python Version: " + COMPILED_PYTHON);

        if (args.length == 0) {
            try {
                Path aPath = Paths.get(Main.class.getProtectionDomain().getCodeSource().getLocation().toURI());
                if (!Files.isDirectory(aPath))
                    aPath = aPath.getParent();
                TIANE_PATH = aPath.getParent().toAbsolutePath().normalize();
            } catch (URISyntaxException e) {
                throw new Error(e);
            }
        } else if (args.length == 1) {
            TIANE_PATH = Paths.get(args[0]).toAbsolutePath().normalize();
        } else {
            System.err.println("Usage: jiane.jar [main tiane path]");
            System.exit(1);
        }

        if (!Files.exists(TIANE_PATH) || !Files.isDirectory(TIANE_PATH) || !Files.isReadable(TIANE_PATH)) {
            System.err.println("Der TIANE Hauptpfad konnte nicht gefunden werden: " + TIANE_PATH.toString());
            System.exit(1);
        }

        if (!Files.isRegularFile(TIANE_PATH.resolve("server/jiane.so")) || !Files.isRegularFile(TIANE_PATH.resolve("server/TIANE_server.py"))) {
            System.err.println("Keine gültige TIANE-Server Installation gefunden unter: " + TIANE_PATH.toString());
            System.exit(1);
        }

        System.out.println("Lade Bibliotheken...");
        Queue<Library> libs = Library.getLibraries();
        for (Library lib : libs) {
            if (lib.found()) {
                try {
                    System.load(Objects.requireNonNull(lib.path()).toAbsolutePath().normalize().toString());
                    System.out.println("Bibliothek geladen - " + lib.name() + ": " + lib.path());
                } catch (UnsatisfiedLinkError e) {
                    System.err.println("Konnte Bibliothek '" + lib.name() + "' nicht laden: " + e.getMessage());
                    System.exit(1);
                }
            } else {
                System.err.println("Konnte Bibliothek '" + lib.name() + "' nicht finden.");
                System.exit(1);
            }
        }

        System.out.println("TIANE wird gestartet...");
        TIANE_THREAD = new Thread(() -> {
            TIANEWrapper.startTiane(
                    TIANE_PATH.resolve("server/TIANE_server.py").toAbsolutePath().normalize().toString(),
                    TIANE_PATH.resolve("server").toAbsolutePath().normalize().toString(),
                    new String[]{"lib" + COMPILED_PYTHON + ".so"}
            );
            System.out.println("Der TIANE-Haupthread ist fertig.");
        });
        TIANE_THREAD.setUncaughtExceptionHandler((thread, throwable) -> {
            if (throwable instanceof TianeException) {
                System.err.println("TIANE meldet einen Fehler. Das Programm wurde beendet.");
                throwable.setStackTrace(new StackTraceElement[]{
                        new StackTraceElement("__main__", "runMain", "TIANE_server.py", -1),
                        new StackTraceElement("tiane.java.TIANEWrapper", "startTiane", "TIANEWrapper.java", -2)
                });
            } else {
                System.err.println("Es gab einen Fehler beim Starten oder Beenden von TIANE. Das Programm wurde beendet.");
            }
            throwable.printStackTrace();
            System.exit(-1);
        });
        TIANE_THREAD.start();
    }

    /**
     * Gibt den TIANE-Pfad zurück. <b>Module sollten dazu den {@code local_storage} benutzen.
     * Nur das {@code tiane.java.api} Paket ist für die Modulentwicklung gedacht.</b>
     */
    @Nonnull
    public static Path path() {
        if (TIANE_PATH == null)
            throw new IllegalStateException("TIANE_PATH not initialised yet.");
        return TIANE_PATH;
    }

    /**
     * Gibt den TIANE-Hauptthread zurück.
     */
    @Nonnull
    public static Thread thread() {
        if (TIANE_THREAD == null)
            throw new IllegalStateException("TIANE_THREAD not initialised yet.");
        return TIANE_THREAD;
    }

    /**
     * Gibt die python version zurück.
     */
    @Nonnull
    public static String pycompile() {
        if (COMPILED_PYTHON == null)
            throw new IllegalStateException("COMPILED_PYTHON not initialised yet.");
        return COMPILED_PYTHON;
    }
}
