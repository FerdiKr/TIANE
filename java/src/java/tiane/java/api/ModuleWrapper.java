package tiane.java.api;

import tiane.util.NativeEntryPoint;

import javax.annotation.Nullable;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Eine Instanz dieser Klasse wird normalen Modulen in
 * ihrer {@link Module#handle(String, ModuleWrapper, LocalStorage) handle} Methode übergeben.
 */
public class ModuleWrapper extends LazyPythonObject {

    @NativeEntryPoint
    protected ModuleWrapper(long pointer) {
        super(pointer);
    }

    private int cached = 0x00000000;
    private Analysis analysis;       // bit  0
    private String text;             // bit  1
    private LocalStorage lstorage;   // bit  2
    private User user;               // bit  3
    private Path path;               // bit  4
    private String serverName;       // bit  5
    private String systemName;       // bit  6
    private List<String> rooms;      // bit  7
    private List<String> users;      // bit  8
    private boolean telegram;        // bit  9
    private Dictionary telegramData; // bit 10
    private Tiane tiane;             // bit 11

    /**
     * Das analysis-Dictionary enthält eine
     * vollständige Analyse des gegebenen Kommandos, sofern das Modul per
     * Sprachkommando aufgerufen wurde (und nicht mit start_module()). Diese
     * Analyse wird von der Funktion analyze() der Klasse Analyzer in der Datei
     * „analyze.py“ im TIANE-Ordner des Gerätes angefertigt.
     */
    public Analysis analysis() {
        if ((cached & (1 << 0)) == 0) {
            analysis = analysisRaw();
            cached |= 1 << 0;
        }
        return analysis;
    }

    /**
     * Enthält den Text des originalen
     * Kommandos, mit dem das Modul aufgerufen wurde, bzw. den Inhalt, der dem
     * Modul beim Aufruf per start_module() unter text mitgegeben wurde.
     * Achtung: Wurde das Modul per start_module() aufgerufen, ohne den
     * text-Parameter zu setzen, enthält dieses Attribut zufälliges Kauderwelsch.
     */
    public String text() {
        if ((cached & (1 << 1)) == 0) {
            text = textRaw();
            cached |= 1 << 1;
        }
        return text;
    }

    /**
     * Enthält den {@link LocalStorage}. Eigentlich überflüssig, weil
     * redundant (Module bekommen den local_storage ja ohnehin als
     * Parameter übergeben), wurde aber aus Kompatibilitätsgründen mit einigen
     * älteren Modulen behalten.
     */
    public LocalStorage localStorage() {
        if ((cached & (1 << 2)) == 0) {
            lstorage = lstorageRaw();
            cached |= 1 << 2;
        }
        return lstorage;
    }

    /**
     * Enthält den Nutzer, der das Modul aufgerufen hat.
     */
    @Nullable
    public User user() {
        if ((cached & (1 << 3)) == 0) {
            user = localStorage().user(userRaw());
            cached |= 1 << 3;
        }
        return user;
    }

    /**
     * Enthält den absoluten Pfad zum TIANE-Ordner dieses Geräts.
     */
    public Path path() {
        if ((cached & (1 << 4)) == 0) {
            path = Paths.get(pathRaw()).toAbsolutePath().normalize();
            cached |= 1 << 4;
        }
        return path;
    }

    /**
     * Enthält den Namen deines TIANE-Servers (den Namen, den du bei der
     * Einrichtung von TIANE festgelegt hast, nicht etwa den PC-Namen oder
     * ähnliches).
     */
    public String serverName() {
        if ((cached & (1 << 5)) == 0) {
            serverName = serverNameRaw();
            cached |= 1 << 5;
        }
        return serverName;
    }

    /**
     * Enthält den Namen deines Sprachassistenten, den du bei der Einrichtung
     * festgelegt hast (z.B. „TIANE“).
     */
    public String systemName() {
        if ((cached & (1 << 6)) == 0) {
            systemName = systemNameRaw();
            cached |= 1 << 6;
        }
        return systemName;
    }

    /**
     * Enthält eine Liste der Namen aller Räume in deinem
     * TIANE-Netzwerk.
     */
    public List<String> rooms() {
        if ((cached & (1 << 7)) == 0) {
            String[] raw = roomsRaw();
            rooms = Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
            cached |= 1 << 7;
        }
        return rooms;
    }

    /**
     * Enthält eine Liste der Nutzernamen aller Nutzer in deinem TIANE-Netzwerk.
     */
    public List<String> users() {
        if ((cached & (1 << 8)) == 0) {
            String[] raw = usersRaw();
            users = Collections.unmodifiableList(Arrays.asList(Arrays.copyOf(raw, raw.length)));
            cached |= 1 << 8;
        }
        return users;
    }

    /**
     * True, wenn dieses Modul per Telegram aufgerufen wurde, andernfalls False.
     */
    public boolean telegram() {
        if ((cached & (1 << 9)) == 0) {
            telegram = telegramRaw();
            cached |= 1 << 9;
        }
        return telegram;
    }

    /**
     * Enthält das vollständige und von TIANEs
     * TelegramInterface bereits leicht erweiterte telepot-Message-Dictionary der
     * Nachricht, mit der das Modul aufgerufen wurde, falls das Modul via Telegram
     * aufgerufen wurde.
     */
    @Nullable
    public Dictionary telegramData() {
        if ((cached & (1 << 10)) == 0) {
            telegramData = telegramDataRaw();
            cached |= 1 << 10;
        }
        return telegramData;
    }

    /**
     * Enthält den „Kern“ von TIANE, nämlich die Hauptinstanz der „echten“ Tiane-
     * Klasse des Geräts, von wo aus alle anderen Objekte verwaltet werden.Ermöglicht extrem tiefe Eingriffe ins System von TIANE, aber nur wenn du
     * wirklich weißt, was du tust. Als Referenz wird auf jeden Fall die Lektüre
     * unserer allgemeinen Dokumentation empfohlen.
     *
     * @see Tiane
     */
    public Tiane core() {
        if ((cached & (1 << 11)) == 0) {
            tiane = coreRaw();
            cached |= 1 << 11;
        }
        return tiane;
    }

    /**
     * Analysiert den gegebenen text mit {@code analyzer.py}
     */
    public native Analysis analyze(String text);

    /**
     * TIANE spricht den angegebenen text per
     * Sprachausgabe aus. Wenn unter room ein bestimmter Raum (in Form eines
     * korrekten Raumnamens als String) als Ziel angegeben wurde, wird der Text in
     * diesem Raum gesprochen. Wenn stattdessen ein bestimmter user (in Form
     * eines korrekten Nutzernamens als String) als Ziel angegeben wurde, wird der
     * Text in dem Raum ausgegeben, in dem sich dieser Nutzer gerade befindet.
     * Achtung: Falls der Nutzer gerade nicht gefunden werden kann (z.B. weil er
     * nicht zu Hause ist), wird TIANE dabei so lange warten, bis sie den Nutzer
     * wieder findet! Wenn sowohl Raum als auch Nutzer angegeben werden, hat
     * der Raum Vorrang vor dem Nutzer; wenn kein Nutzer angegeben wurde, wird
     * der Nutzer, der das Modul aufgerufen hat, als Standard angenommen; ein
     * einfaches tiane.say(text) genügt also, um sehr bequem eine
     * Unterhaltung zu programmieren. Wenn kein Nutzer ermittelt werden konnte,
     * der das Modul aufgerufen hat (bei speziellen Aufrufen per start_module(),
     * ein Fall, der weiter oben schon beschrieben wurde), wird stattdessen room
     * standardmäßig auf den Namen des Raumes gesetzt, von dem aus das Modul
     * aufgerufen wurde. Wenn das Modul aber zusätzlich auf dem Server liegt, also
     * auch kein Raum ermittelt werden kann, wird sich diese Funktion sofort wieder
     * beenden (und eine kleine Fehlermeldung in der Konsole auf dem Server
     * ausgeben). Ansonsten endet die Funktion, wenn der Text fertig
     * ausgesprochen wurde, damit sich Konversationen noch leichter
     * programmieren lassen. Der zusätzliche Parameter output dient zur
     * Steuerung der (Telegram-)Ausgabe: Durch setzen von output auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass dieser Text dem Nutzer auf jeden
     * Fall per Sprachausgabe bzw. per Telegram übermittelt werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie per Telegram antworten,
     * andernfalls per Sprachausgabe. Außerdem kann für diesen Parameter auch
     * ‚telegram_speech‘ angegeben werden, damit TIANE den Text als
     * Telegram-Sprachnachricht verschickt.
     */
    public void say(String text) {
        sayRaw(text, null, null, OutputType.AUTO.out);
    }

    /**
     * TIANE spricht den angegebenen text per
     * Sprachausgabe aus. Wenn unter room ein bestimmter Raum (in Form eines
     * korrekten Raumnamens als String) als Ziel angegeben wurde, wird der Text in
     * diesem Raum gesprochen. Wenn stattdessen ein bestimmter user (in Form
     * eines korrekten Nutzernamens als String) als Ziel angegeben wurde, wird der
     * Text in dem Raum ausgegeben, in dem sich dieser Nutzer gerade befindet.
     * Achtung: Falls der Nutzer gerade nicht gefunden werden kann (z.B. weil er
     * nicht zu Hause ist), wird TIANE dabei so lange warten, bis sie den Nutzer
     * wieder findet! Wenn sowohl Raum als auch Nutzer angegeben werden, hat
     * der Raum Vorrang vor dem Nutzer; wenn kein Nutzer angegeben wurde, wird
     * der Nutzer, der das Modul aufgerufen hat, als Standard angenommen; ein
     * einfaches tiane.say(text) genügt also, um sehr bequem eine
     * Unterhaltung zu programmieren. Wenn kein Nutzer ermittelt werden konnte,
     * der das Modul aufgerufen hat (bei speziellen Aufrufen per start_module(),
     * ein Fall, der weiter oben schon beschrieben wurde), wird stattdessen room
     * standardmäßig auf den Namen des Raumes gesetzt, von dem aus das Modul
     * aufgerufen wurde. Wenn das Modul aber zusätzlich auf dem Server liegt, also
     * auch kein Raum ermittelt werden kann, wird sich diese Funktion sofort wieder
     * beenden (und eine kleine Fehlermeldung in der Konsole auf dem Server
     * ausgeben). Ansonsten endet die Funktion, wenn der Text fertig
     * ausgesprochen wurde, damit sich Konversationen noch leichter
     * programmieren lassen. Der zusätzliche Parameter output dient zur
     * Steuerung der (Telegram-)Ausgabe: Durch setzen von output auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass dieser Text dem Nutzer auf jeden
     * Fall per Sprachausgabe bzw. per Telegram übermittelt werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie per Telegram antworten,
     * andernfalls per Sprachausgabe. Außerdem kann für diesen Parameter auch
     * ‚telegram_speech‘ angegeben werden, damit TIANE den Text als
     * Telegram-Sprachnachricht verschickt.
     */
    public void say(String text, User user) {
        sayRaw(text, null, user.name(), OutputType.AUTO.out);
    }

    /**
     * TIANE spricht den angegebenen text per
     * Sprachausgabe aus. Wenn unter room ein bestimmter Raum (in Form eines
     * korrekten Raumnamens als String) als Ziel angegeben wurde, wird der Text in
     * diesem Raum gesprochen. Wenn stattdessen ein bestimmter user (in Form
     * eines korrekten Nutzernamens als String) als Ziel angegeben wurde, wird der
     * Text in dem Raum ausgegeben, in dem sich dieser Nutzer gerade befindet.
     * Achtung: Falls der Nutzer gerade nicht gefunden werden kann (z.B. weil er
     * nicht zu Hause ist), wird TIANE dabei so lange warten, bis sie den Nutzer
     * wieder findet! Wenn sowohl Raum als auch Nutzer angegeben werden, hat
     * der Raum Vorrang vor dem Nutzer; wenn kein Nutzer angegeben wurde, wird
     * der Nutzer, der das Modul aufgerufen hat, als Standard angenommen; ein
     * einfaches tiane.say(text) genügt also, um sehr bequem eine
     * Unterhaltung zu programmieren. Wenn kein Nutzer ermittelt werden konnte,
     * der das Modul aufgerufen hat (bei speziellen Aufrufen per start_module(),
     * ein Fall, der weiter oben schon beschrieben wurde), wird stattdessen room
     * standardmäßig auf den Namen des Raumes gesetzt, von dem aus das Modul
     * aufgerufen wurde. Wenn das Modul aber zusätzlich auf dem Server liegt, also
     * auch kein Raum ermittelt werden kann, wird sich diese Funktion sofort wieder
     * beenden (und eine kleine Fehlermeldung in der Konsole auf dem Server
     * ausgeben). Ansonsten endet die Funktion, wenn der Text fertig
     * ausgesprochen wurde, damit sich Konversationen noch leichter
     * programmieren lassen. Der zusätzliche Parameter output dient zur
     * Steuerung der (Telegram-)Ausgabe: Durch setzen von output auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass dieser Text dem Nutzer auf jeden
     * Fall per Sprachausgabe bzw. per Telegram übermittelt werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie per Telegram antworten,
     * andernfalls per Sprachausgabe. Außerdem kann für diesen Parameter auch
     * ‚telegram_speech‘ angegeben werden, damit TIANE den Text als
     * Telegram-Sprachnachricht verschickt.
     */
    public void say(String text, Room room) {
        sayRaw(text, room.name(), null, OutputType.AUTO.out);
    }

    /**
     * TIANE spricht den angegebenen text per
     * Sprachausgabe aus. Wenn unter room ein bestimmter Raum (in Form eines
     * korrekten Raumnamens als String) als Ziel angegeben wurde, wird der Text in
     * diesem Raum gesprochen. Wenn stattdessen ein bestimmter user (in Form
     * eines korrekten Nutzernamens als String) als Ziel angegeben wurde, wird der
     * Text in dem Raum ausgegeben, in dem sich dieser Nutzer gerade befindet.
     * Achtung: Falls der Nutzer gerade nicht gefunden werden kann (z.B. weil er
     * nicht zu Hause ist), wird TIANE dabei so lange warten, bis sie den Nutzer
     * wieder findet! Wenn sowohl Raum als auch Nutzer angegeben werden, hat
     * der Raum Vorrang vor dem Nutzer; wenn kein Nutzer angegeben wurde, wird
     * der Nutzer, der das Modul aufgerufen hat, als Standard angenommen; ein
     * einfaches tiane.say(text) genügt also, um sehr bequem eine
     * Unterhaltung zu programmieren. Wenn kein Nutzer ermittelt werden konnte,
     * der das Modul aufgerufen hat (bei speziellen Aufrufen per start_module(),
     * ein Fall, der weiter oben schon beschrieben wurde), wird stattdessen room
     * standardmäßig auf den Namen des Raumes gesetzt, von dem aus das Modul
     * aufgerufen wurde. Wenn das Modul aber zusätzlich auf dem Server liegt, also
     * auch kein Raum ermittelt werden kann, wird sich diese Funktion sofort wieder
     * beenden (und eine kleine Fehlermeldung in der Konsole auf dem Server
     * ausgeben). Ansonsten endet die Funktion, wenn der Text fertig
     * ausgesprochen wurde, damit sich Konversationen noch leichter
     * programmieren lassen. Der zusätzliche Parameter output dient zur
     * Steuerung der (Telegram-)Ausgabe: Durch setzen von output auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass dieser Text dem Nutzer auf jeden
     * Fall per Sprachausgabe bzw. per Telegram übermittelt werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie per Telegram antworten,
     * andernfalls per Sprachausgabe. Außerdem kann für diesen Parameter auch
     * ‚telegram_speech‘ angegeben werden, damit TIANE den Text als
     * Telegram-Sprachnachricht verschickt.
     */
    public void say(String text, OutputType type) {
        sayRaw(text, null, null, type.out);
    }

    /**
     * TIANE spricht den angegebenen text per
     * Sprachausgabe aus. Wenn unter room ein bestimmter Raum (in Form eines
     * korrekten Raumnamens als String) als Ziel angegeben wurde, wird der Text in
     * diesem Raum gesprochen. Wenn stattdessen ein bestimmter user (in Form
     * eines korrekten Nutzernamens als String) als Ziel angegeben wurde, wird der
     * Text in dem Raum ausgegeben, in dem sich dieser Nutzer gerade befindet.
     * Achtung: Falls der Nutzer gerade nicht gefunden werden kann (z.B. weil er
     * nicht zu Hause ist), wird TIANE dabei so lange warten, bis sie den Nutzer
     * wieder findet! Wenn sowohl Raum als auch Nutzer angegeben werden, hat
     * der Raum Vorrang vor dem Nutzer; wenn kein Nutzer angegeben wurde, wird
     * der Nutzer, der das Modul aufgerufen hat, als Standard angenommen; ein
     * einfaches tiane.say(text) genügt also, um sehr bequem eine
     * Unterhaltung zu programmieren. Wenn kein Nutzer ermittelt werden konnte,
     * der das Modul aufgerufen hat (bei speziellen Aufrufen per start_module(),
     * ein Fall, der weiter oben schon beschrieben wurde), wird stattdessen room
     * standardmäßig auf den Namen des Raumes gesetzt, von dem aus das Modul
     * aufgerufen wurde. Wenn das Modul aber zusätzlich auf dem Server liegt, also
     * auch kein Raum ermittelt werden kann, wird sich diese Funktion sofort wieder
     * beenden (und eine kleine Fehlermeldung in der Konsole auf dem Server
     * ausgeben). Ansonsten endet die Funktion, wenn der Text fertig
     * ausgesprochen wurde, damit sich Konversationen noch leichter
     * programmieren lassen. Der zusätzliche Parameter output dient zur
     * Steuerung der (Telegram-)Ausgabe: Durch setzen von output auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass dieser Text dem Nutzer auf jeden
     * Fall per Sprachausgabe bzw. per Telegram übermittelt werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie per Telegram antworten,
     * andernfalls per Sprachausgabe. Außerdem kann für diesen Parameter auch
     * ‚telegram_speech‘ angegeben werden, damit TIANE den Text als
     * Telegram-Sprachnachricht verschickt.
     */
    public void say(String text, User user, OutputType type) {
        sayRaw(text, null, user.name(), type.out);
    }

    /**
     * TIANE spricht den angegebenen text per
     * Sprachausgabe aus. Wenn unter room ein bestimmter Raum (in Form eines
     * korrekten Raumnamens als String) als Ziel angegeben wurde, wird der Text in
     * diesem Raum gesprochen. Wenn stattdessen ein bestimmter user (in Form
     * eines korrekten Nutzernamens als String) als Ziel angegeben wurde, wird der
     * Text in dem Raum ausgegeben, in dem sich dieser Nutzer gerade befindet.
     * Achtung: Falls der Nutzer gerade nicht gefunden werden kann (z.B. weil er
     * nicht zu Hause ist), wird TIANE dabei so lange warten, bis sie den Nutzer
     * wieder findet! Wenn sowohl Raum als auch Nutzer angegeben werden, hat
     * der Raum Vorrang vor dem Nutzer; wenn kein Nutzer angegeben wurde, wird
     * der Nutzer, der das Modul aufgerufen hat, als Standard angenommen; ein
     * einfaches tiane.say(text) genügt also, um sehr bequem eine
     * Unterhaltung zu programmieren. Wenn kein Nutzer ermittelt werden konnte,
     * der das Modul aufgerufen hat (bei speziellen Aufrufen per start_module(),
     * ein Fall, der weiter oben schon beschrieben wurde), wird stattdessen room
     * standardmäßig auf den Namen des Raumes gesetzt, von dem aus das Modul
     * aufgerufen wurde. Wenn das Modul aber zusätzlich auf dem Server liegt, also
     * auch kein Raum ermittelt werden kann, wird sich diese Funktion sofort wieder
     * beenden (und eine kleine Fehlermeldung in der Konsole auf dem Server
     * ausgeben). Ansonsten endet die Funktion, wenn der Text fertig
     * ausgesprochen wurde, damit sich Konversationen noch leichter
     * programmieren lassen. Der zusätzliche Parameter output dient zur
     * Steuerung der (Telegram-)Ausgabe: Durch setzen von output auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass dieser Text dem Nutzer auf jeden
     * Fall per Sprachausgabe bzw. per Telegram übermittelt werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie per Telegram antworten,
     * andernfalls per Sprachausgabe. Außerdem kann für diesen Parameter auch
     * ‚telegram_speech‘ angegeben werden, damit TIANE den Text als
     * Telegram-Sprachnachricht verschickt.
     */
    public void say(String text, Room room, OutputType type) {
        sayRaw(text, room.name(), null, type.out);
    }

    /**
     * TIANE hört einem Nutzer zu, nachdem sie
     * ihm einen kurzen Signalton ausgegeben hat, und übersetzt seine Eingabe mit
     * ihrer Spracherkennung in einen String, den diese Funktion returnt. Wenn kein
     * Nutzer angegeben wurde, wird der Nutzer, der das Modul aufgerufen hat, als
     * Standard angenommen, ein einfaches tiane.listen() genügt also, um
     * sehr bequem eine Unterhaltung zu programmieren. Sollte sich aber aus
     * speziellen Gründen kein Nutzer ermitteln lassen (siehe oben), returnt diese
     * Funktion null. Wenn die Spracherkennung den Satz -aus welchen Gründen auch
     * immer - nicht erkennen konnte, sich der Nutzer
     * mit der Antwort länger als drei Sekunden Zeit gelassen hat oder irgendein
     * anderer Fehler auftritt, returnt diese Funktion ebenfalls
     * null. Der zusätzliche Parameter input dient zur
     * Steuerung der (Telegram-)Eingabe: Durch setzen von input auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass die Antwort des Nutzers auf jeden
     * Fall per Spracheingabe bzw. per Telegram erwartet werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie eine Eingabe per
     * Telegram erwarten, andernfalls per Spracheingabe. Bitte beachte, dass es bei
     * der Eingabe per Telegram KEIN Timeout gibt, sprich, die Funktion wartet ggf.
     * ewig auf eine Antwort des Nutzers. Der Return-Wert
     * null kann trotzdem auftreten, wenn z.B. ein Medium
     * gesendet wurde, das keinen Text enthält.
     */
    @Nullable
    public String listen() {
        return modifyListen(listenRaw(null, OutputType.AUTO.in));
    }

    /**
     * TIANE hört einem Nutzer zu, nachdem sie
     * ihm einen kurzen Signalton ausgegeben hat, und übersetzt seine Eingabe mit
     * ihrer Spracherkennung in einen String, den diese Funktion returnt. Wenn kein
     * Nutzer angegeben wurde, wird der Nutzer, der das Modul aufgerufen hat, als
     * Standard angenommen, ein einfaches tiane.listen() genügt also, um
     * sehr bequem eine Unterhaltung zu programmieren. Sollte sich aber aus
     * speziellen Gründen kein Nutzer ermitteln lassen (siehe oben), returnt diese
     * Funktion null. Wenn die Spracherkennung den Satz -aus welchen Gründen auch
     * immer - nicht erkennen konnte, sich der Nutzer
     * mit der Antwort länger als drei Sekunden Zeit gelassen hat oder irgendein
     * anderer Fehler auftritt, returnt diese Funktion ebenfalls
     * null. Der zusätzliche Parameter input dient zur
     * Steuerung der (Telegram-)Eingabe: Durch setzen von input auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass die Antwort des Nutzers auf jeden
     * Fall per Spracheingabe bzw. per Telegram erwartet werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie eine Eingabe per
     * Telegram erwarten, andernfalls per Spracheingabe. Bitte beachte, dass es bei
     * der Eingabe per Telegram KEIN Timeout gibt, sprich, die Funktion wartet ggf.
     * ewig auf eine Antwort des Nutzers. Der Return-Wert
     * null kann trotzdem auftreten, wenn z.B. ein Medium
     * gesendet wurde, das keinen Text enthält.
     */
    @Nullable
    public String listen(User user) {
        return modifyListen(listenRaw(user.name(), OutputType.AUTO.in));
    }

    /**
     * TIANE hört einem Nutzer zu, nachdem sie
     * ihm einen kurzen Signalton ausgegeben hat, und übersetzt seine Eingabe mit
     * ihrer Spracherkennung in einen String, den diese Funktion returnt. Wenn kein
     * Nutzer angegeben wurde, wird der Nutzer, der das Modul aufgerufen hat, als
     * Standard angenommen, ein einfaches tiane.listen() genügt also, um
     * sehr bequem eine Unterhaltung zu programmieren. Sollte sich aber aus
     * speziellen Gründen kein Nutzer ermitteln lassen (siehe oben), returnt diese
     * Funktion null. Wenn die Spracherkennung den Satz -aus welchen Gründen auch
     * immer - nicht erkennen konnte, sich der Nutzer
     * mit der Antwort länger als drei Sekunden Zeit gelassen hat oder irgendein
     * anderer Fehler auftritt, returnt diese Funktion ebenfalls
     * null. Der zusätzliche Parameter input dient zur
     * Steuerung der (Telegram-)Eingabe: Durch setzen von input auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass die Antwort des Nutzers auf jeden
     * Fall per Spracheingabe bzw. per Telegram erwartet werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie eine Eingabe per
     * Telegram erwarten, andernfalls per Spracheingabe. Bitte beachte, dass es bei
     * der Eingabe per Telegram KEIN Timeout gibt, sprich, die Funktion wartet ggf.
     * ewig auf eine Antwort des Nutzers. Der Return-Wert
     * null kann trotzdem auftreten, wenn z.B. ein Medium
     * gesendet wurde, das keinen Text enthält.
     */
    @Nullable
    public String listen(OutputType type) {
        return modifyListen(listenRaw(null, type.in));
    }

    /**
     * TIANE hört einem Nutzer zu, nachdem sie
     * ihm einen kurzen Signalton ausgegeben hat, und übersetzt seine Eingabe mit
     * ihrer Spracherkennung in einen String, den diese Funktion returnt. Wenn kein
     * Nutzer angegeben wurde, wird der Nutzer, der das Modul aufgerufen hat, als
     * Standard angenommen, ein einfaches tiane.listen() genügt also, um
     * sehr bequem eine Unterhaltung zu programmieren. Sollte sich aber aus
     * speziellen Gründen kein Nutzer ermitteln lassen (siehe oben), returnt diese
     * Funktion null. Wenn die Spracherkennung den Satz -aus welchen Gründen auch
     * immer - nicht erkennen konnte, sich der Nutzer
     * mit der Antwort länger als drei Sekunden Zeit gelassen hat oder irgendein
     * anderer Fehler auftritt, returnt diese Funktion ebenfalls
     * null. Der zusätzliche Parameter input dient zur
     * Steuerung der (Telegram-)Eingabe: Durch setzen von input auf ‚speech‘
     * oder ‚telegram‘ lässt sich festlegen, dass die Antwort des Nutzers auf jeden
     * Fall per Spracheingabe bzw. per Telegram erwartet werden soll. Die
     * Voreinstellung ‚auto‘ bedeutet, dass TIANE selbst entscheidet, sprich, wenn
     * das Modul per Telegram aufgerufen wurde, wird sie eine Eingabe per
     * Telegram erwarten, andernfalls per Spracheingabe. Bitte beachte, dass es bei
     * der Eingabe per Telegram KEIN Timeout gibt, sprich, die Funktion wartet ggf.
     * ewig auf eine Antwort des Nutzers. Der Return-Wert
     * null kann trotzdem auftreten, wenn z.B. ein Medium
     * gesendet wurde, das keinen Text enthält.
     */
    @Nullable
    public String listen(User user, OutputType type) {
        return modifyListen(listenRaw(user.name(), type.in));
    }

    /**
     * Gleiche Funktion wie say(), nur dass diese Funktion sofort returnt
     * und nicht darauf wartet, dass der Text fertig ausgesprochen wurde. Kann
     * nützlich sein, um Wartezeiten zu überbrücken, während dein Modul etwas
     * berechnet oder im Internet sucht. Nur in normalen Modulen verfügbar.
     *
     * @see ModuleWrapper#say(String)
     */
    public void asyncSay(String text) {
        asyncSayRaw(text, null, null, OutputType.AUTO.out);
    }

    /**
     * Gleiche Funktion wie say(), nur dass diese Funktion sofort returnt
     * und nicht darauf wartet, dass der Text fertig ausgesprochen wurde. Kann
     * nützlich sein, um Wartezeiten zu überbrücken, während dein Modul etwas
     * berechnet oder im Internet sucht. Nur in normalen Modulen verfügbar.
     *
     * @see ModuleWrapper#say(String, User)
     */
    public void asyncSay(String text, User user) {
        asyncSayRaw(text, null, user.name(), OutputType.AUTO.out);
    }

    /**
     * Gleiche Funktion wie say(), nur dass diese Funktion sofort returnt
     * und nicht darauf wartet, dass der Text fertig ausgesprochen wurde. Kann
     * nützlich sein, um Wartezeiten zu überbrücken, während dein Modul etwas
     * berechnet oder im Internet sucht. Nur in normalen Modulen verfügbar.
     *
     * @see ModuleWrapper#say(String, Room)
     */
    public void asyncSay(String text, Room room) {
        asyncSayRaw(text, room.name(), null, OutputType.AUTO.out);
    }

    /**
     * Gleiche Funktion wie say(), nur dass diese Funktion sofort returnt
     * und nicht darauf wartet, dass der Text fertig ausgesprochen wurde. Kann
     * nützlich sein, um Wartezeiten zu überbrücken, während dein Modul etwas
     * berechnet oder im Internet sucht. Nur in normalen Modulen verfügbar.
     *
     * @see ModuleWrapper#say(String, OutputType)
     */
    public void asyncSay(String text, OutputType type) {
        asyncSayRaw(text, null, null, type.out);
    }

    /**
     * Gleiche Funktion wie say(), nur dass diese Funktion sofort returnt
     * und nicht darauf wartet, dass der Text fertig ausgesprochen wurde. Kann
     * nützlich sein, um Wartezeiten zu überbrücken, während dein Modul etwas
     * berechnet oder im Internet sucht. Nur in normalen Modulen verfügbar.
     *
     * @see ModuleWrapper#say(String, User, OutputType)
     */
    public void asyncSay(String text, User user, OutputType type) {
        asyncSayRaw(text, null, user.name(), type.out);
    }

    /**
     * Gleiche Funktion wie say(), nur dass diese Funktion sofort returnt
     * und nicht darauf wartet, dass der Text fertig ausgesprochen wurde. Kann
     * nützlich sein, um Wartezeiten zu überbrücken, während dein Modul etwas
     * berechnet oder im Internet sucht. Nur in normalen Modulen verfügbar.
     *
     * @see ModuleWrapper#say(String, Room, OutputType)
     */
    public void asyncSay(String text, Room room, OutputType type) {
        asyncSayRaw(text, room.name(), null, type.out);
    }

    /**
     * Diese Funktion sollte dringend
     * aufgerufen werden, wenn ein Modul nicht mehr (durch Sprechen oder
     * Zuhören) mit dem Nutzer interagieren will, aber zum Beispiel für
     * Berechnungen im Hintergrund noch weiterläuft. Nach einem Aufruf von
     * end_Conversation() können später trotzdem noch Aufrufe von listen()
     * oder say() folgen, diese sind aber eventuell mit einer Wartezeit verbunden,
     * da dafür erst eine neue Konversation für dieses Modul reserviert werden muss
     * (und es sein kann, dass die Konversationsrechte mit diesem Nutzer / in
     * diesem Raum zur Zeit noch bei einem anderen Modul liegen).
     */
    public native void endConversation();

    private native void sayRaw(String text, @Nullable String room, @Nullable String user, @Nullable String type);

    private native String listenRaw(@Nullable String user, @Nullable String type);

    private native void asyncSayRaw(String text, @Nullable String room, @Nullable String user, @Nullable String type);

    public native boolean startModule(@Nullable String name, @Nullable String text, @Nullable String user, @Nullable String room);

    private native Analysis analysisRaw();

    private native String textRaw();

    private native LocalStorage lstorageRaw();

    private native String userRaw();

    private native String pathRaw();

    private native String serverNameRaw();

    private native String systemNameRaw();

    private native String[] roomsRaw();

    private native String[] usersRaw();

    private native boolean telegramRaw();

    private native Dictionary telegramDataRaw();

    private native Tiane coreRaw();

    @Nullable
    private static String modifyListen(@Nullable String in) {
        if (in != null && in.equals("TIMEOUT_OR_INVALID")) {
            return null;
        } else {
            return in;
        }
    }
}
