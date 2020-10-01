
from bs4 import BeautifulSoup
from pathlib import Path
import requests
from urllib.parse import urlparse
import subprocess
from pathlib import Path
import wave
import os

SECURE = False

#PRIORITY = 6

TAGESSCHAU_URL = "https://www.tagesschau.de/100sekunden/"

def isValid(text):
    text = text.lower()
    if 'was' in text and ("gibt's" in text or 'gibts' in text) and 'neues' in text:
        return True
    if ('sage' in text or 'erzähl' in text or 'sprich' in text) and 'nachrichten' in text:
        return True

def handle(text, tiane, profile):
    
    DOWNLOAD_PATH = Path(tiane.path + "/modules/resources")
    try:
        print(f"Hole Video-URL von {TAGESSCHAU_URL} ...")
        url = get_video_url()
        print(f"Lade Video von {url} herunter ...")
        path = download_video(url, DOWNLOAD_PATH)
        print(f"Video wurde gespeichert unter {path}")
        print(f"Konvertiere Video in Audio ...")
        convert_to_wav(tiane)
        print(f"Video kovertiert")
        pfad = tiane.path + "/modules/resources/tagesschau_100sec.wav"
        tiane.play(path=pfad)
        os.remove(pfad)
    except Exception as e:
        print(f"Abbruch durch Fehler: {e}")
        
def get_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content
    
def get_video_url():
    print('filtere Video-URL heraus')
    soup = BeautifulSoup(get_content(TAGESSCHAU_URL), "html.parser")
    meta = soup.find("meta", {"name": "twitter:player:stream"})
    if not meta or not meta.has_attr("content"):
        raise ValueError("Konnte keine Infos zur Video-URL finden")
    return meta["content"]

def download_video(url, DOWNLOAD_PATH):
    print('lade Video herunter')
    filename = 'tagesschau_100sec.mp4'
    path = DOWNLOAD_PATH / filename
    path.write_bytes(get_content(url))
    return path

def convert_to_wav(tiane):
    print('convert_to_wav')
    pfad = tiane.path + "/modules/resources/"
    print('Pfad wurde festgelegt. Er lautet wie folgt: ')
    print(pfad)
    command = "ffmpeg -i " + pfad + "tagesschau_100sec.mp4" + " -ab 160k -ac 2 -ar 44100 -vn " + pfad + "tagesschau_100sec.wav -y"
    print('command wurde festgelegt')
    print(command)
    subprocess.call(command, shell=True)
    print('subprocess wurde ausgeführt')
