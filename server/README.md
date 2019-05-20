# Server

## Installation

Der gesamte Prozess der durchgeführt werden muss, um ein lauffähiges System zu erhalten ist [hier](https://github.com/FerdiKr/TIANE/blob/master/TIANE%20-%20Installationsanleitung.pdf) beschrieben.
Das System kann manuell aufgesetzt werden oder es kann das Dockerfile genutzt werden um das System in einem Docker-container zu starten.

### Manuell
Die manuelle Installation ist [hier](https://github.com/FerdiKr/TIANE/blob/master/TIANE%20-%20Installationsanleitung.pdf) detailliert beschrieben.

### Docker
Um das System mithilfe von [Docker](https://www.docker.com/) auszusetzen, muss erst die nötige config mithilfe der setup-skripte erstellt werden.
Nachdem dies getan ist kann ein Docker-image mit `docker build . -t tiane_container` gebaut werden. Das Image kann nachdem es fertig gebaut ist mit `docker run tiane_container:latest` gestartet werden.



