# Server

## Installation

Der gesamte Prozess der durchgeführt werden muss, um ein lauffähiges System zu erhalten ist [hier](https://github.com/FerdiKr/TIANE/blob/master/TIANE%20-%20Installationsanleitung.pdf) beschrieben.
Das System kann manuell aufgesetzt werden oder es kann das Dockerfile genutzt werden, um das System in einem Docker-Container zu starten.

### Manuell
Die manuelle Installation ist [hier](https://github.com/FerdiKr/TIANE/blob/master/TIANE%20-%20Installationsanleitung.pdf) detailliert beschrieben.

### Docker
Um das System mithilfe von [Docker](https://www.docker.com/) aufzusetzen, muss erst die nötige config mithilfe der setup-skripte erstellt werden.
Nachdem dies getan ist kann ein Docker-Image mit `docker build . -t tiane_container` gebaut werden. Das Image kann, nachdem es fertig gebaut ist, mit `docker run tiane_container:latest` gestartet werden. [Beide Kommandos müssen im *server*-Verzeichnis ausgeführt werden.]

#### Docker Compose
Alternativ kann auch docker-compose genutzt werden.
Die Installation erfolgt mit `pip install docker-compose`.
Nun gibt es zwei Möglichkeiten:
* **mit** Webserver:
Dazu wird der Container mit `docker-compose up -d tiane-webserver` gestartet.
* **ohne** Webserver:
Dazu wird der Container mit `docker-compose up -d tiane` gestartet.
In beiden Fällen wird das Image dabei automatisch gebaut.
[Das Kommando muss im *TIANE*-Verzeichnis ausgeführt werden.]

Bei dieser Methode den TIANE-Server aufzusetzen sind die (TIANE-)Dateien auf dem Hostrechner mit denen im Container identisch. Daher ist es, wenn notwendig, möglich, die Dateien auf dem Host zu bearbeiten. Diese werden sofort im Conatiner übernommen.
