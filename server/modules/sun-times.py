#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import math
import requests
import json
import datetime
import random

__author__     = "olagino"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"
"""
Wann geht die Sonne auf bzw. unter?
Der Ortsname wird via Nominatim von OpenStreetMap zu Koordinaten übersetzt,
die genaue Berechnung erfolgt dann offline.
"""

########## speechHelper.py ############################
def batchGen(batch):
    """
    With the batchGen-function you can generate fuzzed compare-strings
    with the help of a easy syntax:
        "Wann [fährt|kommt] [der|die|das] nächst[e,er,es] [Bahn|Zug]"
    is compiled to a list of sentences, each of them combining the words
    in the brackets in all different combinations.
    This list can then fox example be used by the batchMatch-function to
    detect special sentences.
    """
    outlist = []
    ct = 0
    while len(batch) > 0:
        piece = batch.pop()
        if "[" not in piece and "]" not in piece:
            outlist.append(piece)
        else:
            frontpiece = piece.split("]")[0]
            inpiece = frontpiece.split("[")[1]
            inoptns = inpiece.split("|")
            for optn in inoptns:
                rebuild = frontpiece.split("[")[0] + optn
                rebuild += "]".join(piece.split("]")[1:])
                batch.append(rebuild)
    return outlist

def batchMatch(batch, match):
    t = False
    if isinstance(batch, str):
        batch = [batch]
    for piece in batchGen(batch):
        if piece.lower() in match.lower():
            t = True
    return t

def speechVariation(input):
    """
    This function is the counterpiece to the batchGen-function. It compiles the same
    sentence-format as given there but it only picks one random variant and directly
    pushes it into tiane. It returns the generated sentence.
    """
    if not isinstance(input, str):
        parse = random.choice(input)
    else:
        parse = input
    while "[" in parse and "]" in parse:
        sp0 = parse.split("[",1)
        front = sp0[0]
        sp1 = sp0[1].split("]",1)
        middle = sp1[0].split("|",1)
        end = sp1[1]
        parse = front + random.choice(middle) + end
    return parse

def sayAsync(tiane, text):
    try:
        tiane.end_Conversation()
        tiane.start_module(name="justsaysomethin", text=text)
    except AttributeError:
        print("ASYNC>" + text)

####################### Calculation-Functions ##################################
# Source https://github.com/diego-80/solar_calc

class sunsetTimes(object):
    def __init__(self, lat_d, lon_d, day_of_year, time_zone=0):
        """
        lat_d: float
        Latitude in degrees
        lon_d: float
        Longitude in degrees
        date: int
        Day of the year
        time_zone: int
        Offset to the UTC-Timezone
        """
        lat = math.radians(lat_d)
        lon = math.radians(lon_d)
        frac_year = ((math.pi*2)/(365))*(day_of_year-1) #radians
        eq_time = 229.18*(0.000075+(0.001868*math.cos(frac_year))\
        -(0.032077*math.sin(frac_year))-(0.014615*math.cos(2*frac_year))\
        -(0.040849*math.sin(2*frac_year))) #minutes
        decl = 0.006918-(0.399912*math.cos(frac_year))+(0.070257*math.sin(frac_year))\
        -(0.006758*math.cos(2*frac_year))+(0.000907*math.sin(2*frac_year))\
        -(0.002697*math.cos(3*frac_year))+(0.00148*math.sin(3*frac_year)) #radians
        hour_angle = math.degrees(math.acos(\
        math.cos(math.radians(90.833))/(math.cos(lat)*math.cos(decl))\
        -(math.tan(lat)*math.tan(decl)))) #degrees

        times = self.utc_times(lon_d, hour_angle, eq_time)
        self.converted = ((times[0]+time_zone*60), (times[1]+time_zone*60))

    def utc_times(self, lon, hour_angle, eq_time):
    	"""returns utc sunrise and sunset times based on parameters"""
    	sunrise = 720-4*(lon+hour_angle)-eq_time
    	sunset = 720-4*(lon-hour_angle)-eq_time
    	return (sunrise, sunset)

    def is_leap(self, year):
    	"""checks if the date occurs in a leap year"""
    	year=int(year)
    	if (year%4==0 and year%100!=0) or (year%400==0):
    		return True
    	else:
    		return False

##################### Main Code ################################################
def handle(text, tiane, profile):
    text = text.lower()
    if tiane.analysis["town"] == "None" or tiane.analysis["town"] == None:
        textOut = [
            "Von welchem Ort möchtest du denn die Sonnenzeiten wissen?",
            "Welchen Ort soll ich denn für meine Berechnungen annehmen?"
        ]
        tiane.say(speechVariation(textOut))
        if "in " in text:
            place = text.split("in ")[1].strip("?").strip()
        else:
            place = tiane.listen().replace("von").strip()
    else:
        place = tiane.analysis["town"]

    # Call Nominatim-API
    place = place.replace(" ", "+")
    r = requests.get("https://nominatim.openstreetmap.org/search?q={0}&format=json".format(place))
    if r.status_code == 200:
        try:
            response = json.loads(r.text)
            placeData = response[0]

            placeName = placeData["display_name"].split(", ")[0]
            lat = float(placeData["lat"])
            lon = float(placeData["lon"])

            if lat > 66.5 or lat < -66.5:
                tiane.say(speechVariation(
                    "Es ist mir etwas peinlich, aber für diesen Ort kann ich " \
                    "leider den Sonnen auf beziehungsweise Untergang nicht " \
                    "berechnen. Dafür ist mein hinterlegter Algorithmus nicht " \
                    "ausgelegt worden."
                ))
            else:
                datetimeTemp = tiane.analysis["datetime"]

                datestr = datetimeTemp.strftime("%Y%m%d")
                day_of_year = int(datetimeTemp.strftime("%j"))
                if day_of_year > 88 and day_of_year < 298:
                    timezone = 2
                else:
                    timezone = 1
                sT = sunsetTimes(lat, lon, day_of_year, timezone)
                sunrise, sunset  = sT.converted
                tiane.say(speechVariation(
                    "In {0} geht die Sonne [nach meinen Berechnungen|] um " \
                    " {1} Uhr {2} auf und um {3} Uhr {4} wieder unter. Du " \
                    "kannst also volle {5} Stunden und {6} Minuten " \
                    "Tageslicht genießen.".format(
                        placeName,
                        round(sunrise//60),
                        round(sunrise%60),
                        round(sunset//60),
                        round(sunrise%60),
                        round((sunset-sunrise)//60),
                        round((sunset-sunrise)%60)
                    )
                ))
        except IndexError:
            tiane.say(speechVariation(
                "Oh je, ich konnte zu [deinem angefragten Ort|] {0} leider keine" \
                "Position[sdaten|] finden. Vielleicht willst du es mit einer" \
                "anderen Aussprache-Variante ausprobieren?".format(place)
            ))
    else:
        tiane.say(speechVariation(
            "Oh, ich habe gerade [Probleme|Schwierigkeiten], " \
            "[an die Koordinaten zu kommen|die Koordinaten zu übersetzen]. " \
            "Vielleicht probierst du es einfach später nochmal[, okay|]?"
            ))


def isValid(text):
    text = text.lower()
    if "sonne" in text and ("auf" in text or "unter" in text):
        return True
    else:
        return False
