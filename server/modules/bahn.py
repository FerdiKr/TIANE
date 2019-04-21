#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import random
import requests
import json
import datetime
from bs4 import BeautifulSoup # needs html5lib
import time
import traceback

__author__     = "olagino"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"
"""
Wann fährt die nächste Bahn?
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
        t_a = time.time()
        sp0 = parse.split("[",1)
        front = sp0[0]
        sp1 = sp0[1].split("]",1)
        middle = sp1[0].split("|",1)
        end = sp1[1]
        t_b = time.time()
        parse = front + random.choice(middle) + end
    return parse

def sayAsync(tiane, text):
    try:
        tiane.end_Conversation()
        tiane.start_module(name="justsaysomethin", text=text)
    except AttributeError:
        print("ASYNC>" + text)

########## bahn_external.py ###########################
"""
WARNING: Handle and use with care.
This "libary" uses a wild mixture of several parsers scraping db-reiseauskunft and marudor.de
these "APIs" may or may not be depracted instantly when deutschebahn or marudor change something in their online-page-structure
"""

class MainBlock(object):
    """Main Class to handle everything."""
    def __init__(self, start='', end=''):
        self.time = datetime.datetime.now()
        if len(start) > 0 and len(end) > 0:
            self.setTrainStationsByString(start, end, self.time)

    def setTrainStationsByString(self, start, end, time):
        self.start = TrainStation(start)
        self.end = TrainStation(end)
        self.time = time

    def interactive(self):
        startRaw = input("Bitte geben Sie Ihren Startbahnhof ein: ")
        self.start = TrainStation(startRaw)
        print("Folgender Startbahnhof wurde ausgefäwhlt:", self.start.name, '\n')
        endRaw = input("Bitte geben Sie Ihren Zielbahnhof ein:  ")
        self.end = TrainStation(endRaw)
        print("Folgender Zielbahnhof wurde ausgewählt:", self.end.name, '\n')
        types = input("Nah oder Fernverkehr? (N/V)")
        print("\nDie Verbindungen werden berechnet.")
        if types == "N":
            self.getConnections("0011111111")
        else:
            self.getConnections("1111111111")
        print("\nEs wurden " + str(len(self.data.connections)) + " Verbindungen gefunden:\n")
        count = 0
        for connection in self.data.connections:
            count += 1
            print('VERBINDUNG', count, str(connection.price))
            for train in connection.trainList:
                print('  ', train.startTime, "+" + str(train.startDelay), train.startStation, '\t', train.startTrack)
                print('   |', str(train.duration) + 'min')
                print('   ->', train.endTime, train.endStation, '\t', train.endTrack)
                print('     (', train.trainNumber, ')')
            print('\n')

    def getConnections(self, trafficType="1111111111"):
        self.data = ConnectionGroup(self.time, self.start.id, self.end.id)
        self.data.requestConnections(trafficType)
        return self.data


class TrainStation(object):
    """The TrainStation-class stores information about a station of Deutsche Bahn."""
    def __init__(self, string):
        self.station = self.idFromName(string)
        self.type = self.station['stationType']
        self.id = self.station['stationID']
        self.name = self.station['stationName']
        self.lat, self.long = self.station['lat'], self.station['long']

    def idFromName(self, search):
        url = "https://reiseauskunft.bahn.de/bin/ajax-getstop.exe/dn"
        param = {
            'encoding': 'utf-8',
            'L': 'vs_test_fsugg_getstop',
            'start': 1,
            'tpl': 'sls',
            'getstop': 1,
            'noSession': 'yes',
            'iER': 'yes',
            'S': search + '?',
            'json': 'true'
        }
        data = getRequest(url, param).replace('SLs.sls=', '').replace(";SLs.showSuggestion();", "")
        self.rawData = data
        data = json.loads(data)
        if 'suggestions' in data and len(data['suggestions']) >= 1:
            dict_out = {
                'stationID': str(data['suggestions'][0]['extId']),
                'stationName': str(data['suggestions'][0]['value']),
                'stationType': str(data['suggestions'][0]['typeStr']),
                'lat': int(data['suggestions'][0]['xcoord'])/1000000,
                'long': int(data['suggestions'][0]['ycoord'])/1000000
            }
            return dict_out
        else:
            return -1

    def nextDepartures(self):
        url = "https://marudor.de/api/ownAbfahrten/" + self.id + "?lookahead=150&lookbehind=0"
        data = getRequest(url, {})
        for train in json.loads(data)["departures"]:
            if "departure" in train:
                data = {
                    "name": train["train"],
                    "destination": train["destination"],
                    "departure": train["departure"] / 1000,
                    "departure_rel": round(train["departure"] / 1000 - time.time())
                }
                return data


class ConnectionGroup(object):
    def __init__(self, dateStart, startName, endName):
        self.date = dateStart
        self.start = startName
        self.end = endName
        self.connections = []

    def requestConnections(self, trafficType='1111111111'):
        if len(trafficType) == 10:
            types = trafficType
        else:
            types = '1111111111'
        time = self.date.strftime('%H:%M')
        date = self.date.strftime('%d.%m.%Y')
        weekday = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'][int(self.date.strftime('%w'))]
        start = self.start.replace(' ', '+')
        end = self.end.replace(' ', '+')
        url = "https://reiseauskunft.bahn.de/bin/query.exe/dn"
        param = {
            'advancedProductMode': 'yes',
            'existIntermodalDep_enable': 'yes',
            'existIntermodalDest_enable': 'yes',
            'existOptimizePrice': '1',
            'existOptionBits': 'yes',
            'existProductAutoReturn': 'yes',
            'existProductNahverkehr': '1',
            'HWAI=JS!ajax': 'yes',
            'HWAI=JS!js': 'yes',
            'HWAI=QUERY!displayed': 'yes',
            'HWAI=QUERY!hideExtInt': 'no',
            'HWAI=QUERY!prodAdvanced': '0',
            'HWAI=QUERY!rit': 'no',
            # 'HWAI=QUERY$PRODUCTS$0_0!show': '{…}''
            'HWAI=QUERY$via$0!number': '0',
            'HWAI=QUERY$via$1!number': '0',
            'ignoreTypeCheck': 'yes',
            'queryPageDisplayed': 'yes',
            'REQ0HafasChangeTime': '0:1',
            'REQ0HafasOptimize1': '0:1',
            'REQ0HafasSearchForw': '1',
            'REQ0JourneyDate': weekday + ',+' + date,
            'REQ0JourneyDep__enable': 'Foot',
            'REQ0JourneyDep_Bike_maxDist': '5000',
            'REQ0JourneyDep_Bike_minDist': '0',
            'REQ0JourneyDep_Foot_maxDist': '2000',
            'REQ0JourneyDep_Foot_minDist': '0',
            'REQ0JourneyDep_KissRide_maxDist': '50000',
            'REQ0JourneyDep_KissRide_minDist': '2000',
            'REQ0JourneyDest__enable': 'Foot',
            'REQ0JourneyDest_Bike_maxDist': '5000',
            'REQ0JourneyDest_Bike_minDist': '0',
            'REQ0JourneyDest_Foot_maxDist': '2000',
            'REQ0JourneyDest_Foot_minDist': '0',
            'REQ0JourneyDest_KissRide_maxDist': '50000',
            'REQ0JourneyDest_KissRide_minDist': '2000',
            'REQ0JourneyProduct_opt_section_0_list': '0:0000',
            'REQ0JourneyProduct_prod_section_0_0': types[0],
            'REQ0JourneyProduct_prod_section_0_1': types[1],
            'REQ0JourneyProduct_prod_section_0_2': types[2],
            'REQ0JourneyProduct_prod_section_0_3': types[3],
            'REQ0JourneyProduct_prod_section_0_4': types[4],
            'REQ0JourneyProduct_prod_section_0_5': types[5],
            'REQ0JourneyProduct_prod_section_0_6': types[6],
            'REQ0JourneyProduct_prod_section_0_7': types[7],
            'REQ0JourneyProduct_prod_section_0_8': types[8],
            'REQ0JourneyProduct_prod_section_0_9': types[9],
            'REQ0JourneyRevia': 'yes',
            'REQ0JourneyStops1ID': '',
            'REQ0JourneyStops2ID': '',
            'REQ0JourneyStopsS0A': '255',
            'REQ0JourneyStopsS0a': '131072',
            'REQ0JourneyStopsS0G': start,
            'REQ0JourneyStopsS0ID': '',
            'REQ0JourneyStopsS0o': '8',
            'REQ0JourneyStopsZ0A': '255',
            'REQ0JourneyStopsZ0a': '131072',
            'REQ0JourneyStopsZ0G': end,
            'REQ0JourneyStopsZ0o': '8',
            'REQ0JourneyTime': time,
            'REQ0Tariff_Class': '2',
            'REQ0Tariff_TravellerAge.1': '',
            'REQ0Tariff_TravellerReductionClass.1': '0',
            'REQ0Tariff_TravellerType.1': 'E',
            'REQ1HafasSearchForw': '1',
            'REQ1JourneyDate': '',
            'REQ1JourneyStops1ID': '',
            'REQ1JourneyStops2ID': '',
            'REQ1JourneyTime': '',
            'rtMode': '12',
            'start': 'Suchen',
            'traveller_Nr': '1',
            'travelProfile': ''
        }
        data = getRequest(url, param)
        data = BeautifulSoup(data, 'html5lib')
        dataRows = data.find_all('tbody', {'class': 'scheduledCon'})
        normalLen = len(dataRows)
        dataRows = dataRows + data.find_all("tbody", {'class': 'liveCon'})
        if len(dataRows) >= 1:
            oCnt = 0
            for rowInfo in dataRows:
                oCnt += 1
                # setup of connection
                moreInformation = rowInfo.find_all('a', {'title': 'Details einblenden'})
                if len(moreInformation) > 0:
                    detailUrl = moreInformation[0]['href']
                    tID = moreInformation[0]['rel'][0].split('HWAI:CONNECTION{')[1].split('}')[0]
                    conn = Connection(detailUrl, tID, self.date)
                    # get price information
                    price = []
                    if len(rowInfo.find_all('a', {'class': 'layer_nofares'})) == 0:
                        for t in rowInfo.find_all('span', {'class': 'fareOutput'}):
                            price.append(float(t.text.replace('EUR', '').replace(',', '.').strip()))
                    else:
                        price.append(0)
                    conn.price = price
                    conn.type = "schedule" if oCnt <= normalLen else "live"
                    # get duration information
                    duration = rowInfo.find_all('td', {'class': 'duration'})[0].text.split(':')
                    conn.duration = int(duration[0]) * 60 + int(duration[1])
                    # get start time
                    startTime = rowInfo.find_all('td', {'class': 'time'})[0]
                    conn.startTime = refineTime(startTime.text, self.date)
                    # print all fetched informations
                    # print(conn.price, conn.duration, conn.startTime)
                    # fetch other information
                    conn.fetchDetailsFromUrl()
                    # append Class to the list
                    self.connections.append(conn)


class Connection(object):
    """Single Train Connection"""
    def __init__(self, detailUrl, tID, mainTime):
        self.ident = detailUrl.split("ident=")[1].split("&")[0]
        self.ld = detailUrl.split("ld=")[1].split("&")[0]
        self.tId = tID
        self.seqnr = detailUrl.split("seqnr=")[1].split("&")[0]
        self.price = 0
        self.startTime = ''
        self.mainTime = mainTime
        self.trainList = []  # list of station-ids where a train stops
        self.duration = 0
        # TODO calculated properties
        # self.hopList = []  # list of station-ids where the user has to change trains

    @property
    def hopList(self):
        hopList = []
        oldTrain = self.trainList[0]
        for train in self.trainList:
            changeTime = (train.startTime - oldTrain.endTime).seconds // 60
            hop = {
                'startStation': oldTrain.endStation,
                'startTrack': oldTrain.startTrack,
                'startNumber': oldTrain.trainNumber,
                'time': changeTime,
                'endStation': train.startStation,
                'endTrack': train.startTrack,
                'endNumber': train.trainNumber
            }
            oldTrain = train
            hopList.append(hop)
        hopList.pop(0)  # remove first element because of useless information ("difference" within the same change)
        return hopList

    def fetchDetailsFromUrl(self):
        url = "https://reiseauskunft.bahn.de/bin/query.exe/dn"
        param = {
            'ld': self.ld,
            'protocol': 'https:',
            'seqnr': int(self.seqnr) + 0,
            'ident': self.ident,
            'rt': 1,
            'rememberSortType': 'minDeparture',
            'ajax': 1,
            'HWAI': 'CONNECTION$' + self.tId + '!id=' + self.tId + '!HwaiConId=' + self.tId + '!HwaiDetailStatus=journeyGuide!'
        }
        data = getRequest(url, param)
        data = BeautifulSoup(data, 'html5lib')
        data = data.find_all('table', {'class': 'result'})
        if len(data) >= 1:
            data = data[0]
            stopTable = data.find_all('tr')
            train = None
            for row in stopTable:
                if 'class' in row.attrs:
                    rowClass = row.attrs['class']
                    if 'first' in rowClass:
                        # initialize TrainLane class
                        trainNumber = row.find_all('td', {'class': 'products'})[0].text.strip()
                        train = TrainLane(trainNumber, self.mainTime)
                        train.startStation = row.find_all('td', {'class': 'station'})[0].text.strip()
                        train.startTime = row.find_all('td', {'class': 'time'})[0].text.strip()
                        train.startTrack = row.find_all('td', {'class': 'platform'})[0].text.strip()
                        train.description = row.find_all('td', {'class': 'lastrow'})[0].text.strip()
                    elif 'intermediate' in rowClass:
                        pass
                    elif 'intermediateStationRow' in rowClass:
                        stationName = row.find_all('td', {'class': 'intermediateStation'})[0].text.strip()
                        stationTime = row.find_all('td', {'class': 'intermeadiateTime'})[0].text.strip()
                        platformList = row.find_all('td', {'class': 'platform'})
                        if len(platformList) == 1:
                            stationTrack = platformList[0].text.strip()
                        else:
                            stationTrack = ''
                        train.newStop(stationName, stationTrack, stationTime)
                    elif 'last' in rowClass:
                        train.endStation = row.find_all('td', {'class': 'station'})[0].text.strip()
                        tEndTime = row.find_all('td', {'class': 'time'})
                        if len(tEndTime) == 1:
                            train.endTime = tEndTime[0].text.strip()
                        else:
                            train.endTime = ''
                        try:
                            train.endTrack = row.find_all('td', {'class': 'platform'})[0].text.strip()
                        except IndexError:
                            train.endTrack = ""
                        self.trainList.append(train)


class TrainLane(object):
    def __init__(self, number, mainTime):
        self.trainNumber = ' '.join(number.split())
        self.startStation = ''
        self.startTrack = ''
        self._startTime = ''
        self._startTimeLive = ''
        self.endStation = ''
        self.endTrack = ''
        self._endTime = ''
        self._endTimeLive = ''
        self.trainDescription = ''
        self.stops = []
        self._duration = 0
        self._stopCount = 0
        self.mainTime = mainTime

    @property
    def duration(self):
        try:
            diffTime = (self.endTime - self.startTime).seconds // 60
        except TypeError:
            diffTime = None
        return diffTime

    @property
    def startDelay(self):
        try:
            diffTime = (self._startTimeLive - self._startTime).seconds // 60
        except TypeError:
            diffTime = 0
        return diffTime

    @property
    def endDelay(self):
        try:
            diffTime = (self._endTimeLive - self._endTime).seconds // 60
        except TypeError:
            diffTime = 0
        return diffTime

    @property
    def startTime(self):
        return self._startTime

    @property
    def startTimeLive(self):
        return self._startTimeLive

    @startTime.setter
    def startTime(self, startTime):
        self._startTime, self._startTimeLive = self.refineTime(startTime)

    @property
    def endTime(self):
        return self._endTime

    @property
    def endTimeLive(self):
        return self._endTimeLive

    @endTime.setter
    def endTime(self, endTime):
        self._endTime, self._endTimeLive = self.refineTime(endTime)

    def refineTime(self, timeRaw):
        timeFine = timeRaw.replace("ab", "").replace("an", "").strip()
        # check if reiseauskunf has real-time-data and use these timestamps
        timeFineSplit = timeFine.split()
        if len(timeFineSplit) > 1:
            timeFine = timeFineSplit[0]
            timeFineLive = timeFineSplit[-1]
        else:
            timeFineLive = timeFine
        try:
            timeFine = datetime.datetime.strptime(timeFine, "%H:%M")
            timeFineLive = datetime.datetime.strptime(timeFineLive, "%H:%M")
            # merge the two times together
            timeFine = datetime.datetime(self.mainTime.year, self.mainTime.month, self.mainTime.day, timeFine.hour, timeFine.minute, 0)
            timeFineLive = datetime.datetime(self.mainTime.year, self.mainTime.month, self.mainTime.day, timeFineLive.hour, timeFineLive.minute, 0)
        except ValueError:
            pass
        return timeFine, timeFineLive

    def newStop(self, name, track, time):
        data = {
            'name': name,
            'track': track,
            'time': time
        }
        self.stops.append(data)


def getRequest(url, param):
    data = requests.get(url, params=param)
    return data.text


def refineTime(timeRaw, mainTime):
    timeFine = timeRaw.strip()
    # check if reiseauskunf has real-time-data and use these timestamps
    timeFineSplit = timeFine.split()
    if len(timeFineSplit) > 1:
        timeFine = timeFineSplit[-1]
    timeFine = datetime.datetime.strptime(timeFine, "%H:%M")
    # merge the two times together
    timeFine = datetime.datetime(mainTime.year, mainTime.month, mainTime.day, timeFine.hour, timeFine.minute, 0)
    return timeFine

#######################################################
###### Main bahn-module ###############################

def handle(text, tiane, profile):
    text = text.lower().replace("ß", "ss")
    journey = False
    try:
        start = tiane.analysis["town"]
        if start is 'None':
            tiane.say(speechVariation("Ich weiß noch gar nicht, wo [wir hier gerade sind|es losgehen soll]."))
            tiane.say(speechVariation("An welche[m Bahnhof|r Station] [willst|möchtest] du [|denn] [|gerne] [ab|los]fahren?"))
            start = tiane.listen().strip()
        startB = TrainStation(start)
        if "nach " in text:
            tiane.say(speechVariation(["Mal sehen, was so auf den Schienen los ist.", "Einen Augenblick bitte."]))
            ziel = text.split("nach ")[1]
            journey = True
        if "planen" in text or "reise" in text:
            tiane.say(speechVariation([
                "[So,|] und wohin soll [die|deine] Reise gehen?",
                "Was ist denn dein Reiseziel?",
                "Wohin soll es denn gehen?"
            ]))
            ziel = tiane.listen().strip()
            journey = True
        if journey:
            zielB = TrainStation(ziel)
            DeltaLat = abs(startB.lat - zielB.lat) * 111.11
            DeltaLong = abs(startB.long - zielB.long) * 111.11
            airdist = round((DeltaLat**2 + DeltaLong**2)**0.5)
            time = datetime.datetime.now()
            bridgeText = "Gut, dann schau[|e] ich mal, was ich für [Optionen|Möglichkeiten] finde."
            if airdist > 150:
                bridgeText += " Oh, da hast du dir aber eine lange Reise[strecke|route] ausgesucht."
            else:
                bridgeText += " Bitte [gedulde ich noch ein wenig|habe einen Moment Geduld]."
            sayAsync(tiane, speechVariation(bridgeText))
            # check nahverkehr
            cGNV = ConnectionGroup(time, startB.id, zielB.id)
            cGNV.requestConnections("0011111111")
            cNV = cGNV.connections
            print("cNV", len(cNV))
            cNV = cNV[0]
            ttnNV = abs((time - cNV.startTime).total_seconds()) / 60
            durNV = cNV.duration
            try:
                priNV = min(cNV.price)
            except ValueError:
                priNV = -1
            hopsNV = len(cNV.trainList)
            # only check Fernverkehr if distance over 150km
            if airdist > 150:
                foo = False
                try:
                    # check fernverkehr
                    cGFV = ConnectionGroup(time, startB.id, zielB.id)
                    cGFV.requestConnections("1111111111")
                    cFV = cGFV.connections[0]
                    ttnFV = abs((cFV.startTime - time).total_seconds()) / 60
                    durFV = cFV.duration
                    try:
                        priFV = min(cFV.price)
                    except ValueError:
                        priFV = -1
                    hopsFV = len(cFV.trainList)
                except IndexError:
                    foo = True
            else:
                foo = True
            if foo:
                cFV = cNV
                ttnFV = ttnNV
                durFV = durNV
                priFV = priNV
                hopsFV = hopsNV

            timespan = ttnFV
            timespanRaw = timespan
            timespan = str(round(timespan)) + " Minuten" if timespan < 60 else str(round(timespan//60)) + " Stunden und " + str(round(timespan%60)) + " Minuten"
            dur = durFV
            duration = str(round(dur)) + " Minuten" if dur < 60 else str(round(dur//60)) + " Stunden und " + str(round(dur%60)) + " Minuten"

            durdiff = durNV-durFV
            durdiffRaw = durdiff
            durdiff = str(round(durdiff)) + " Minuten" if durdiff < 60 else str(round(durdiff//60)) + " Stunden und " + str(round(durdiff%60)) + " Minuten"
            text = "Die nächste Verbindung [fährt|kommt] in " + timespan + " und dauert bei "
            text += str(hopsFV-1) + " Zugwechsel ungefähr " + duration + "."

            if priNV < priFV:
                text += " Wenn du [Fernzüge ausschliesst|nur den Nahverkehr nutzt], sparst du " + str(round(priFV-priNV)) + " Euro " + (str(round(((priFV-priNV)-round(priFV-priNV))*100)) + "." if ((priFV-priNV)-round(priFV-priNV))*100 > 0 else ".")
                if durFV < durNV:
                    if durdiffRaw < 10:
                        text += " Und du bist nichteimal zehn minuten länger [auf der Reise|unterwegs]"
                    if durdiffRaw/timespanRaw > 0.8:
                        text += "Dafür bist du mehr als doppelt so lange unterwegs"
                    else:
                        text += "Dafür bist du " + str(durdiff) + " Minuten länger unterwegs"
                if ttnNV > ttnFV:
                    text += " und wartest " + str(round(ttnNV-ttnFV)) + " Minuten [länger|mehr] am Startbahnhof."
                else:
                    text += "."
            elif priNV > 0 or priFV > 0:
                text += " Das Ticket [dafür|für diese Strecke] kostet [vorraussichtlich|im Moment] " + str(round(priFV)) + " Euro " + (str(round(((priFV)-round(priFV))*100)) if ((priFV)-round(priFV))*100 > 0 else "")
            else:
                text += ""
            tiane.say(speechVariation(text))
            text = " Soll ich dir mehr Details über die schnellste Verbindung erzählen?"
            tiane.say(speechVariation(text))
            instr = tiane.listen()
            if batchMatch("[ja|ja gerne|gern]", instr):
                text = "Okay, [aufgepasst|dann hol dir am besten einen Zettel zum mitschreiben]. "
                first = True
                for t in cNV.trainList:
                    track = " [am Bahnsteig|an Gleis] " + str(t.startTrack) if len(str(t.startTrack).strip()) >= 1 else ""
                    pronoun = "die " if "S " in t.trainNumber else "den "
                    pronoun2 = "sie " if "S " in t.trainNumber else "Der [|Zug]"
                    if first and len(cNV.trainList) > 1:
                        text += "Als erstes steigst du in " + pronoun + t.trainNumber + track + " ein. "
                    elif not first and len(cNV.trainList) > 1:
                        varA = "[Nach deiner Ankunft|] in " + t.startStation
                        varA += " [wechselst|steigst] du [als nächstes|dann] in " + pronoun + t.trainNumber + " nach " + t.endStation + ". "
                        varA += pronoun2 + " fährt um " + t.startTime.strftime("%-H Uhr %-M ") + track + " [los|ab]. "
                        if len(str(t.startTrack).strip()) >= 1:
                            varB = "[Wenn du in " + t.startStation + " angekommen bist,| Nach deiner Ankunf in " + t.startStation + "] "
                            varB += "[gehst|läufst] du dann zum " + " ".join(track.split(" ")[2:]).strip() + " "
                            varB += "und steigst [kurz vor|um] " + t.startTime.strftime("%-H Uhr %-M ") + "in " + pronoun + t.trainNumber + " ein. "
                        else:
                            varB = "Spätestens um " + t.startTime.strftime("%-H Uhr %-M ") + "solltest du in " + t.startStation + "sein, damit"
                            varB += " du noch " + pronoun + t.trainNumber + " nach " + t.endStation +" [erreichst|bekommst|erwischst]. "
                        text += random.choice([varA, varB, varB])
                    first = False
                text += " Vorraussichtlich kommst du dann um " + t.endTime.strftime("%-H Uhr %-M ") + " an."
                text = text.replace("Hbf", "[|Hauptbahnhof]").replace("(", " ").replace(")", " ").replace("  ", " ")
                tiane.say(speechVariation(text))
            else:
                tiane.say("[Okay|Kein Problem|keine Ursache]")

        else:
            deps = startB.nextDepartures()
            try:
                dest = deps["destination"].replace("Hbf", "").replace("(", "").replace(")", "")
                text = "[Der nächste Zug, der|Die nächste Bahn, die] in " + startB.name + " abfährt, heißt "
                text += deps["name"] + ", [fährt nach|hat als Fahrziel] " + dest
                text += " und fährt planmäßig in " + str(round(deps["departure_rel"]/60))
                text += " Minuten ab."
            except TypeError:
                text = "Im Moment konnte ich keine [passenden|] Abfahrten finden. [Vielleicht|Eventuell] schaust du mal im Bahn Navigator nach?"
            tiane.say(speechVariation(text))
    except IndexError as e:
        print(e)
        traceback.print_exc()
        tiane.say(speechVariation("[ooh je|ups], irgend[et|]was ist da [schiefgegangen|nicht nach plan gelaufen]. Wie wäre es, wenn du es einfach [später|noch einmal] versuchst?"))

def isValid(text):
    text = text.lower()
    batch = [
        "wann [fährt|kommt] [der|die] nächste [Zug|Bahn]",
        "Wann [fährt|gibt es] [die nächste|eine] [bahn|]verbindung [von|ab|nach]",
        "Welche[|r] [Zug|Bahn] [fährt|kommt] [als nächstes|demnächst|bald|gleich]"
        ]
    if batchMatch(batch, text) or ("reise" in text and "planen" in text):
        return True
    else:
        return False

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '10', 'hour': '10', 'year': '2018', 'minute': '00', 'day': '09'}, 'town': 'None'}

    def say(self, text):
        print(text)
    def listen(self):
        neuertext = input()
        return neuertext

def test():
    profile = {}
    tiane = Tiane()
    print("FRAGE eingeben")
    handle(input(), tiane, profile)

if __name__ == "__main__":
    test()
