import spotipy
import spotipy.util as util
import json
import re

# Beschreibung
'''
Spotify Steuerung
Für genauere Infos siehe ReadMe in server/resources/spotify

Entwickelt von Peter Elsen und Simon Tebeck
'''

def isValid(text):
    text = text.lower()

    triggers = ["play", "fortsetzen", "pause", "nächstes lied", "weiter", "vorheriges lied", "zurück", "spotify", "shuffle", "zufall"]
    for trigger in triggers:
        if trigger in text:
            return True

    return False

def handle(text, tiane, profile):
    text = text.lower()
    length = len(text)

    # Spotify Authentifizierung
    cachepath = tiane.local_storage["TIANE_PATH"] + "/resources/spotify/spotify-auth"
    token = util.prompt_for_user_token('your-username',
                           'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-library-read user-read-currently-playing',
                           client_id='',
                           client_secret='',
                           redirect_uri='https://oskar.pw/',
                           cache_path=cachepath)

    access_token = json.loads(open(cachepath, "r").readlines()[0])["access_token"]
    sp = spotipy.Spotify(auth=access_token)

    # prüfen, ob ein Gerät aktiv ist
    devices = sp.devices()["devices"]
    devicesCount = len(devices)

    activeDevice = False

    for i in range(devicesCount):
        if devices[i]["is_active"]:
            activeDevice = True
            break

    if not activeDevice:
        tiane.say("Bitte starte Spotify auf deinem Gerät")
        return

    # Steuerbefehle ausführen
    if ("play" in text and "playlist" not in text) or "fortsetzen" in text or "pause" in text:
        # kontrolliere start / stop
        is_playing = sp.current_playback()['is_playing']

        #tiane.say("Verstanden")

        if is_playing:
            sp.pause_playback()
        else:
            sp.start_playback()

    elif "nächstes lied" in text or "weiter" in text:
        # nächstes lied
        #tiane.say("Verstanden")
        sp.next_track()

    elif "vorheriges lied" in text or "zurück" in text:
        # vorheriges lied
        #tiane.say("Verstanden")
        sp.previous_track()

    elif "spotify" in text and "spiele" in text:
        # Künstler, Playlist oder Lied abspielen
        if "künstler" in text or "artist" in text or "interpret" in text:
            match = re.search('(künstler|artist|interpret)', text)
            if match != None:
                startName = match.end() + 1
                artistname = text[startName:length]
                artist_uri = sp.search(artistname, limit=1, offset=0, type='artist', market=None)["artists"]["items"][0]["uri"]
                #tiane.say("Verstanden")
                sp.start_playback(context_uri=artist_uri)

        elif "playlist" in text:
            match = re.search('playlist', text)
            if match != None:
                startName = match.end() + 1
                playlistname = text[startName:length]
                playlist_uri = sp.search(playlistname, limit=1, offset=0, type='playlist', market=None)["playlists"]["items"][0]["uri"]
                #tiane.say("Verstanden")
                sp.start_playback(context_uri=playlist_uri)

        else:
            if "lied" in text:
                match = re.search('lied', text)
            else:
                match = re.search('spiele', text)

            if match != None:
                startName = match.end() + 1
                trackname = text[startName:length]
                tracks = sp.search(trackname, limit=10, offset=0, type='track', market=None)["tracks"]["items"]

                #tiane.say("Verstanden")
                trackuris = []
                for i in range(10):
                    trackuris.append(tracks[i]["uri"])

                sp.start_playback(uris=trackuris)

    elif "spotify" in text and "warteschlange" in text:
        # Lied in die Warteschlange
        match = re.search('(füge|setze)', text)
        if match != None:
            startName = match.end() + 1

            matchEnd = re.search('(zur|in)', text)
            if matchEnd != None:
                startEnd = matchEnd.start() - 1

        trackname = text[startName:startEnd]
        track_uri = sp.search(trackname, limit=1, offset=0, type='track', market=None)["tracks"]["items"][0]["uri"]
        #tiane.say("Verstanden")
        sp.add_to_queue(track_uri)

    elif "spotify" in text and ("lauter" in text or "leiser" in text):
        # lauter oder leiser
        current_volume = sp.current_playback()['device']['volume_percent']
        if "lauter" in text:
            new_volume = current_volume + 10
        else:
            new_volume = current_volume - 10
        sp.volume(new_volume)

    elif "spotify" in text and "lautstärke" in text:
        # Laustärle auf festen Wert
        if "volle" in text and ("kanne" in text or "möhre" in text or "power" in text or "energie"):
            sp.volume(100)

        else:
            match = re.search('auf', text)
            if match != None:
                start = match.end() + 1
                volume_str = text[start:length]
                new_volume = int(volume_str)

                sp.volume(new_volume)

    elif "shuffle" in text or "zufall" in text:
        # Shuffle-Modus
        if "beende" in text or "stoppe" in text or "aus" in text:
            sp.shuffle(False)
        else:
            sp.shuffle(True)
