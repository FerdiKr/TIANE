import googlemaps
import re

# Beschreibung
'''
Dieses Modul fragt die Distanz und Fahrzeit zwischen zwei Orten von Google Maps ab.
'''

# Python Client Library: https://github.com/googlemaps/google-maps-services-python
# Requirements: pip install -U googlemaps
# API Doc: https://developers.google.com/maps/documentation/distance-matrix/intro
# HTTP-Request: https://maps.googleapis.com/maps/api/distancematrix/json?origins=<>&destinations=<>&language=de&key=<>

def isValid(text):
    text = text.lower()
    if ('wie weit' in text or 'wie lang' in text) and ('von' in text and ('bis' in text or 'nach' in text)):
        return True
    else:
        return False

def handle(text, tiane, local_storage):
    text = text.lower()
    gmaps = googlemaps.Client(key='')

    origin = ''
    destination = ''

    directions_result = gmaps.distance_matrix(origin,destination)
