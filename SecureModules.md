# Sichere Module

Server-Module können mit 

```python
SECURE = True
```

als sicher markiert werden. Der Standard ist `False`.

Ein sicheres Modul muss folgende kriterien erfüllen:

 1. Es darf keine `exec` oder `eval` Aufrufe enthalten und keine externen Befehle aufrufen (z.B mit `subprocess`)
 2. Es dark keine Dateien auf dem Server ändern (Ausnahme ist die LocalStorage, die eine Dateiänderung hervorruft). Außerdem darf keine externe Hardware, die an den Server angeschlosen ist angesteuert werden.
 3. Es darf nicht über längere Zeit blockieren und auf Zustandsänderungen in der LocalStorage warten, da es eventuell mit einer abwandlung der LocalStorage aufgerufen wird und Änderungen nicht verfügbar werden.
 4. Es darf keine Module explizit aufrufen, die nicht `SECURE` sind. Wenn einfach nur irgendein Text angegeben wird, werden automatisch nur sichere Module gesucht.
 5. Es darf nicht über die LocalStorage auf andere Benutzer oder Räume zugreifen.
 
WebSocket Clients können so konfiguriert werden, dass Anfragen von dort nur sichere Module zulassen. Das ist z.B nützlich, wenn TANE als (öffentlicher) Discord-Bot verwendet wird.