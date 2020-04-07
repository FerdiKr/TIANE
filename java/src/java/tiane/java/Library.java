package tiane.java;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Pattern;

public final class Library {

    private final String name;
    private final Path path;
    private final boolean found;

    public Library(String name, String path) {
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

    public Library(String name, Path path) {
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

    public boolean found() {
        return found;
    }

    public String name() {
        return name;
    }

    public Path path() {
        return found ? path : null;
    }

    public static Queue<Library> getLibraries() {
        Queue<Library> libs = new LinkedList<>();

        libs.add(new Library(Main.pycompile(), locateOne("lib" + Main.pycompile(), Pattern.compile("^/usr(/local)?/lib/.*?lib" + Main.pycompile() + ".*?\\.so$"))));
        libs.add(new Library("jiane", Main.path().resolve("server").resolve("jiane.so")));

        return libs;
    }

    private static String locateOne(String str, Pattern predicate) {
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

    private static List<String> locate(String str) throws IOException {
        Process process = Runtime.getRuntime().exec("locate " + str);
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        List<String> paths = new ArrayList<>();
        for (String line = in.readLine();line != null;line = in.readLine()) {
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
