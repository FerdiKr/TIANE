package tiane.java;

import tiane.java.api.Logging;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Diese Klasse sucht Module.
 */
public class ModuleFinder {

    /**
     * Sucht Module im angegebenen Verzeichnis.
     *
     * @param searchPath Das Verzeichnis, in dem Module gesucht werden sollen.
     * @param baseClass  Die Klasse der Module ({@link tiane.java.api.Module} oder {@link tiane.java.api.ModuleContinuous})
     */
    public static <T> List<T> findModules(String searchPath, Class<T> baseClass) {
        try {
            List<T> modules = new ArrayList<>();
            Path path = Paths.get(searchPath);
            Files.newDirectoryStream(path).forEach(p -> {
                try {
                    if (p.getFileName().toString().toLowerCase().trim().endsWith(".jar") && isJar(p)) {
                        try {
                            modules.addAll(searchModuleClasses(p, baseClass));
                        } catch (Exception e) {
                            Logging.get().error("Konnte JAR nicht laden - " + p.toAbsolutePath().normalize().toString() + ": " + e.getMessage());
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            return Collections.unmodifiableList(modules);
        } catch (Exception e) {
            Logging.get().warn("Konnte JAVA-Module nicht laden: " + e.getMessage());
            return Collections.emptyList();
        }
    }

    private static <T> List<T> searchModuleClasses(Path path, Class<T> baseClass) throws Exception {
        ClassLoader cl = new URLClassLoader(new URL[]{path.toUri().toURL()}, Main.class.getClassLoader());
        InputStream modulesInfo = cl.getResourceAsStream("modules.info");
        if (modulesInfo == null) {
            Logging.get().warn("Jar-Datei scheint keine TIANE-Moduldatei zu sein: Doesn't declare a 'modules.info' - Wird übersprungen.");
            return Collections.emptyList();
        }
        List<T> classes = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(modulesInfo));
        for (String line = reader.readLine(); line != null; line = reader.readLine()) {
            line = line.trim();
            if (!line.isEmpty() && !line.startsWith("#")) {
                T result = null;
                try {
                    Class<?> clazz = cl.loadClass(line.trim());
                    if (baseClass.isAssignableFrom(clazz)) {
                        @SuppressWarnings("unchecked")
                        Class<? extends T> moduleClass = (Class<? extends T>) clazz;
                        try {
                            result = moduleClass.newInstance();
                        } catch (Exception e) {
                            Logging.get().error("JAVA-Modul konnte nicht initialisiert werden - '" + line + "': " + e.getMessage() + " - Wird übersprungen.");
                        }
                    }
                } catch (ClassNotFoundException | NoClassDefFoundError e) {
                    //
                }

                if (result == null) { // Ist es ein Scala-Object?
                    try {
                        Class<?> clazz = cl.loadClass(line.trim() + "$");
                        if (baseClass.isAssignableFrom(clazz)) {
                            @SuppressWarnings("unchecked")
                            Class<? extends T> moduleClass = (Class<? extends T>) clazz;
                            try {
                                Field instField = moduleClass.getDeclaredField("MODULE$");
                                instField.setAccessible(true);
                                @SuppressWarnings("unchecked")
                                T t = (T) instField.get(null);
                                result = t;
                            } catch (Exception e) {
                                Logging.get().error("JAVA-Modul konnte nicht initialisiert werden - '" + line + "': " + e.getMessage() + " - Wird übersprungen.");
                            }
                        }
                    } catch (ClassNotFoundException | NoClassDefFoundError e) {
                        //
                    }
                }

                if (result != null) {
                    classes.add(result);
                }
            }
        }
        return Collections.unmodifiableList(classes);
    }

    private static boolean isJar(Path path) throws IOException {
        String str = Files.probeContentType(path).toLowerCase().trim();
        return str.equals("application/java-archive") || str.equals("application/x-java-archive")
                || str.equals("application/x-jar") || str.equals("application/jar");
    }
}
