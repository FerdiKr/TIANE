package tiane.java;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Pattern;

/**
 * Eine native Bibliothek, die geladen werden kann.
 */
public final class Library {

    private final String name;
    private final Path path;
    private final boolean found;

    /**
     * Erstellt ein neues {@code Library} Objekt.
     *
     * @param name Der Name der Bibliothek
     * @param path Der absolute Pfad zur Biblothek.
     */
    public Library(@Nonnull String name, @Nullable String path) {
        if (path == null) {
            this.found = false;
            this.name = Objects.requireNonNull(name);
            this.path = null;
        } else {
            this.name = Objects.requireNonNull(name);
            this.path = Objects.requireNonNull(Paths.get(Objects.requireNonNull(path)));
            this.found = Files.exists(this.path);
        }
    }

    /**
     * Erstellt ein neues {@code Library} Objekt.
     *
     * @param name Der Name der Bibliothek
     * @param path Der absolute Pfad zur Biblothek.
     */
    public Library(@Nonnull String name, @Nullable Path path) {
        if (path == null) {
            this.found = false;
            this.name = Objects.requireNonNull(name);
            this.path = null;
        } else {
            this.name = Objects.requireNonNull(name);
            this.path = Objects.requireNonNull(path);
            this.found = Files.exists(this.path);
        }
    }

    /**
     * Gibt zurück, ob die Bibliothek gefunden wurde. Dazu muss {@code path != null} sein.
     */
    public boolean found() {
        return found;
    }

    /**
     * Gibt den Namen der Bibliothek zurück.
     */
    @Nonnull
    public String name() {
        return name;
    }

    /**
     * Gibt den Pfad zur Bibliothek zurück.
     */
    @Nullable
    public Path path() {
        return found ? path : null;
    }

    /**
     * Gibt alle Bibliotheken zurück, die JIANE zum starten benötigt.
     */
    @Nonnull
    public static Queue<Library> getLibraries() {
        Queue<Library> libs = new LinkedList<>();

        libs.add(new Library(Main.pycompile(), locateOne("lib" + Main.pycompile(), Pattern.compile("^/usr(/local)?/lib/.*?lib" + Main.pycompile() + ".*?\\.so$"))));
        libs.add(new Library("jiane", Main.path().resolve("server").resolve("jiane.so")));

        return libs;
    }

    @Nullable
    private static String locateOne(@Nonnull String str, @Nonnull Pattern predicate) {
        try {
            List<String> allMatch = new ArrayList<>(locate(str));
            allMatch.removeIf(predicate.asPredicate().negate());

            if (allMatch.isEmpty()) {
                return null;
            } else {
                return allMatch.get(0);
            }
        } catch (IOException e) {
            return null;
        }
    }

    @Nonnull
    private static List<String> locate(@Nonnull String str) throws IOException {
        Process process = Runtime.getRuntime().exec("locate " + str);
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        List<String> paths = new ArrayList<>();
        for (String line = in.readLine(); line != null; line = in.readLine()) {
            paths.add(line);
        }
        try {
            process.waitFor();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return Collections.emptyList();
        }

        return Collections.unmodifiableList(paths);
    }
}
