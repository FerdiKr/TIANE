# JIANE

JIANE ist ein Wrapper für TIANE, der das Erstellen und Verwenden von Java-Modulen erlaubt.

### Funktionsweise

JIANE läuft nur auf dem TIANE-Server. Raum-Module müssen weiterhin in Python geschrieben werden.
Wenn JIANE verwendet wird, wird zuerst Java gestartet. Das Java-Programm startet danach Python und TIANE.

### Installation

Um JIANE zu kompilieren auszuführen wird Folgendes benötigt:

  * Java Development Kit (JDK) ab Version 8
  * CPython (das normale Python) ab Version 3.x
  * Die Python-Header (Auf Linux häufig im Paket `python3-dev` zu finden)
  * GNU Compiler Collection (gcc)
  
**JIANE wird NICHT mit CMake kompiliert. Die Möglichkeit eine `CMakeLists.txt`-Datei zu erzeugen besteht nur, um sie in IDEs zu verwenden.**
  
Zunächst muss die Datei `build.properties` im Verzeichnis `java` angepasst werden:

```properties
gccExecutable=gcc                          # Der Pfad zu deiner GCC-Installation
mainClass=tiane.java.Main                  # Die Hauptklasse von JIANE. Dieser Wert sollte im normalfall nicht geändert werden.
headers=/usr/include/python3.6             # Zusätzliche Header-Verzeichnisse. Hier müssen eventuell auch die Header deine Python-Installation angegeben werde, falls sie nicht automatisch gefunden werden.
libraryPath=/usr/lib/x86_64-linux-gnu/     # Zusätzliche Bibliotheks-Verzeichnisse. Wenn Bibliotheken nicht
libraries=dl                               # Bibliotheken, die zum linken gebraucht werden. Dieser Wert sollte im normalfall nicht geändert werden.
pythonLibrary=python3.6m                   # Die Python-Bibliothek, die verwendet werden soll. Je nach Version und Betriebssystem unterschiedlich.
```

Wenn diese Datei richtig konfiguriert ist, muss man im Verzeichnis `java` das `gradlew` starten: `./gradlew clean build`. Nun wird eventuell erst das Build-System `gradle` heruntergeladen. Dann wird JIANE kompiliert.
Dabei werden verschiedene Bibliotheken verwendet, die nachher auch ein Teil der fertigen `jar`-Date werden:

  * [findbugs-annotations](https://github.com/findbugsproject/findbugs) lizenziert unter [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.txt)
  * [apache-log4j](https://logging.apache.org/log4j/2.x/) lizenziert unter [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)
  
Wenn die Installation geklappt hat, liegen nun im Verzeichnis Server die Dateien `jiane.jar` und `jiane.so`. TIANE kann nun mit dem Befehl `java -jar jiane.jar` (ausgeführt im Ordner `server`) gestartet werden.

### Module Verwenden

TIANE-Module, die in Java geschrieben sind, werden als `jar`-Dateien verpackt. Diese `jar`-Dateien müssen im Ordner `server/modules` platziert werden. Eine `jar`-Datei kann dabei aber nicht nur ein Modul enthalten, sondern mehrere. Auch `jar`-Dateien mit fortlaufenden Modulen gehören ins Verzeichnis `server/modules` und nicht wie gewohnt in `server/modules/continuous`. Das hat den Vorteil, dass eine einzige `jar`-Datei gleichzeitig normale und fortlaufende Module bereitstellen kann. Java-Module werden nach Python-Modulen geladen.

Beim Kompilieren wurde bereits eine solche `jar`-Datei erstellt, die ein einziges Modul hinzufügt, welches dafür sorgt, dass TIANE die Frage "*Kannst du Java*" mit "*Ja natürlich*" beantwortet. Dieses Modul kann zum Beispiel verwendet werden, um zu testen, ob JIANE funktioniert.

### Module erstellen

**Bevor du mit JIANE Module erstellst, solltest du den [_Guide zur Modulentwicklung_](../TIANE%20-%20Guide%20zur%20Modulentwicklung.pdf) durchlesen.**

Jedes normale Modul wird durch eine Klasse definiert, die von `tiane.java.api.Module` erbt. Fortlaufende Module erben von `tiane.java.api.ModuleContinuous`. Die Klassen benötigen einen No-Arg-Konstruktor. Wenn du *Scala* benutzt, kannst du stattdessen auch ein Objekt definieren. Nun muss deine `jar`-Datei nur noch auf oberster Ebene eine Datei namens `modules.info` enthalten, die pro Zeile einen *fully-qualified-name* einer Modulklasse beinhaltet. Bei Scala-Objekten muss das `$`, dass intern an die Implementation angehängt wird, nicht mitgeschrieben werden.

Weitere Informationen findest du im JavaDoc. Es wird beim Kompilieren automatisch ins Verzeichnis `java/doc` generiert.