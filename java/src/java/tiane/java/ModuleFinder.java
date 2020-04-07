package tiane.java;

import tiane.java.api.Module;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ModuleFinder {

    public static <T> List<T> findModules(String searchPath, Class<T> baseClass) {
        try {
            List<T> modules = new ArrayList<>();
            Path path = Paths.get(searchPath);
            Files.newDirectoryStream(path).forEach(p -> {
                try {
                    if (p.getFileName().toString().toLowerCase().endsWith(".jar") && Files.probeContentType(p).equalsIgnoreCase("application/x-java-archive")) {
                        try {
                            modules.addAll(searchModuleClasses(p, baseClass));
                        } catch (Exception e) {
                            System.out.println("Konnte JAR nicht laden - " + p.toAbsolutePath().normalize().toString() + ": " + e.getMessage());
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            return Collections.unmodifiableList(modules);
        } catch (Exception e) {
            System.out.println("Konnte JAVA-Module nicht laden: " + e.getMessage());
            return Collections.emptyList();
        }
    }

    private static <T> List<T> searchModuleClasses(Path path, Class<T> baseClass) throws Exception {
        ClassLoader cl = new URLClassLoader(new URL[]{path.toUri().toURL()}, Main.class.getClassLoader());
        InputStream modulesInfo = cl.getResourceAsStream("/modules.info");
        if (modulesInfo == null) {
            System.out.println("WARN: Jar-Datei scheint keine TIANE-Moduldatei zu sein: Doesn't declare a 'modules.info' - Wird übersprungen.");
            return Collections.emptyList();
        }
        List<T> classes = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(modulesInfo));
        for (String line = reader.readLine();line != null;line = reader.readLine()) {
            line = line.trim();
            if (!line.isEmpty() && ! line.startsWith("#")) {
                try {
                    Class<?> clazz = cl.loadClass(line);
                    if (baseClass.isAssignableFrom(clazz)) {
                        @SuppressWarnings("unchecked")
                        Class<? extends T> moduleClass = (Class<? extends T>) clazz;
                        try {
                            T instance = moduleClass.newInstance();
                            classes.add(instance);
                            System.out.println("JAVA-Modul gefunden: " + clazz.getName());
                        } catch (Exception e) {
                            System.out.println("JAVA-Modul konnte nicht initialisiert werden - '" + line + "': " + e.getMessage() + " - Wird übersprungen.");
                        }
                    }
                } catch (ClassNotFoundException e) {
                    System.out.println("Ein nicht-existente Klasse wurde als Modul angegeben. Wird übersprungen.");
                } catch (NoClassDefFoundError e) {
                    System.out.println("Beim laden des JAVA-Moduls '" + line + "' trat ein Fehler auf Offenbar fehlen benötigte Klassen: " + e.getMessage() + " - Wird übersprungen.");
                }
            }
        }
        return Collections.unmodifiableList(classes);
    }
}
