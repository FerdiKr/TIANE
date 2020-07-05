# TIANE WebSocket

Tiane hat einen eingebauten WebSocket-Server, der es anderen Anwendungen Tiane zu benutzen um zum Beispiel Nutzern Nachrichten zu schicken, egal wo sie sind oder auf `events` zu reagieren.

## WebSocket aktivieren

Um den WebSocket zu aktivieren muss in `TIANE_config.json` der Eintrag `websocket` geändert werden. Es gibt 3 verschiedene Modi:

 * `disabled` (standard): Es wird kein WebSocket Server gestartet
 * `secure`: Es wird ein WebSocket Server gestartet, aber Anwendungen können sich nur im `secure`-Modus verbinden. Das bedeutet, dass sie manche Module nicht aufrufen können. Sieh dazu [SecureModules](SecureModules.md).
 * `enabled`: Es wird ein WebSocket Server gestartet. Anwendungen können sich wahlweise im `secure` oder im normalen Modus verbinden.
 
Außderdem kann mit `websocket_port` der Port für den WebSocket Server eingestellt werden. `websocket_timeout` gibt die Zeit (in Sekunden) an, die Tiane über WebSocket auf eine Antwort eines Benutzers wartet, wenn sie eine Nachfrage gestellt hat.

Nun kann eine WebSocket Verbindung mit Tiane aufgebaut werden.

## Nachrichten Client --> TIANE

### listen

```json
{
  "action": "listen",
  "msg": "Die Nachricht",
  "user": "Nutzer, der die Nachricht geschickt hat",
  "room": "Raum aus dem die Nachricht kam",
  "role": "Optional standard='USER', Rolle des Nutzers",
  "explicit": "True oder False, je nachdem ob TIANE  angesprochen wurde"
}
```

Simuliert, dass ein Nutzeretwas gesagt hat. `room` muss ein WebSocket-Raum sein. Um einen WebSocket-Raum zu erstellen siehe `create_room`. Wenn der Nutzer nicht existiert, wird er erstellt. Nur n diesem Fall wird `role` verwendet. Der Nutzer wird in den angegebenen Raum gesetzt. Nachrichten, bei denen `explicit` `False` ist, werden nur verarbeitet, wenn TIANE auf eine Antwort des Nutzers wartet.

### notify

```json
{
  "action": "notify",
  "msg": "Die zu versendende Nachricht",
  "user": "Der Empfänger der Nachricht"
}
```

Versucht, dem Nutzer eine Nachricht zukommen zu lassen. Es wird automatisch ein passender Raum gesucht.

### create_room

```json
{
  "action": "create_room",
  "room": "Der Name des Raums",
  "secure": "Ob der Raum SECURE sein soll"
}
```

Erstellt einen neuen WebSocket-Raum. Alle Nachrichten, die TIANE in diesem Raum sagt, werden an den Ersteller gesendet. Wenn es bereits einen Raum mit diesem Namen gibt, passiert nichts.

### set_output

```json
{
  "action": "set_output",
  "room": "Der Raum",
  "output": "Der neue Ausgabetyp"
}
```

Fügt einen neuen Ausgabetypen zu dem gegebenen WebSocket-Raum hinzu. Dies wird nicht benötigt, erlaubt aber in Modulen Dinge explizit an einen Client zu senden. Die Module funktionieren allerdings auch ohne dass der Client verbunden ist. Wenn ein Ausgabetyp nicht existiert, wird er wie `speech` behandelt. Die Nutzung von Standard-Ausgabetypen hat keinen Effekt.

### set_user_to_room

```json
{
  "action": "set_user_to_room",
  "user": "Der Nutzer",
  "room": "Der Raum"
}
```

Entfernt den gegebenen Nutzer aus seinem aktuellen Raum und setzt ihn in den gegebenen. Es können auch nicht-WebSocket-Räume verwendet werden.

## Nachrichten TIANE --> Client

### event

```json
{
  "action": "event",
  "name": "Der Name des events",
  "data": "Zusätzliche Daten"
}
```

Wird an alle WebSocket-Clients gesendet, wenn ein Modul `tiane.sendWebSocketEvent(name, data)` nutzt. Der Name und die Daten können vom Modul bestimmt werden. (`data` ist ein JSON-Element)

### say

```json
{
  "action": "say",
  "msg": "Die Nachricht von Tiane",
  "ping": "Der Nutzer an den die Nachricht gerichtet ist oder null wenn es keinenen speziellen Nutzer gibt",
  "room": "Der Raum, in den die Nachricht gesprochen werden soll."
}
```

Wird einem WebSocket-Client gesendet, wenn TIANE etwas in einen seiner WebSocket-Räume sagen möchte.