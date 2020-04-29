# Spotify Steuerung durch TIANE

## Einrichtung:

1. Registriere dich als Spotify-Entwickler und erstelle im [Dashboard](https://developer.spotify.com/dashboard/applications) eine neue App.
2. Trage in der App die Redirect-URL _https://oskar.pw/_ ein.
3. Trage im _spotify_-Modul UND in der Datei `get-spotify-auth.py` in diesem Ordner an den entsprechenden Stellen deinen **Benutzernamen**, deine **Client-ID** (der in 1. erstellten App) und dein **Client-Secret** ein.
4. Du musst einmalig manuell auf einem Gerät mit grafischer Oberfläche und Webbrowser den Zugriff der in 1. erstellten App auf deinen Spotify-Account genehmigen. Anschließend wird der Token automatisch erneuert.
  * Führe dazu das Skript `get-spotify-auth.py` aus. Dies musst nicht unbedingt auf dem TIANE-Server geschehen; du musst nur später die generierte Datei _spotify-auth_ in diesen Ordner (`server/resources/spotify`) kopieren.
  * Es öffnet sich ein Webbrowser. Dort genehmigst du den Zugriff. Anschließend erhältst du einen _Refresh-Token_, den du im Eingabeprompt des Skripts einfügst.
  * Nun wird automatisch der _acces_token_ abgefragt und in der Datei _spotify-auth_ gespeichert sowie zur Kontrolle ausgegeben.
  * Stelle sicher, dass die Datei `spotify-auth` in diesem Ordner liegt.

#### FERTIG
Du kannst nun die Wiedergabe steuern sowie Lieder und Playlists abspielen. Beachte jedoch, dass bereits ein Abspielgerät aktiv ist.
