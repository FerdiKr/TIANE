#!/usr/bin/env python3

from spacex_py import launches


def isValid(text):
    hit_list = ["rakete", "spacex"]
    if any((hit for hit in hit_list if hit in text.lower())) == True:
        return True
    else:
        return False

def handle(text, tiane, local_storage):

    if tiane.telegram_call == False:
        tiane.say("Das kann jetzt einiges an text werden, willst du das wirklich alles hören?")
        antwort = tiane.listen()

        if antwort == 'TIMEOUT_OR_INVALID':
            tiane.say("Fehler")

        hit_list = ["Ja", "Yes"]
        else if any((hit for hit in hit_list if hit in text.lower())) == True:
            


    text_lower = text.lower()

    ################################################################################ 
    # Wann (nächster Start)
    ################################################################################ 

    # Define hits
    hit_list = ["wann", "when"]

    if any((hit for hit in hit_list if hit in text.lower())) == True:
        # Get the launches launch 
        got_launches, header = launches.get_launches()


        if tiane.telegram_call == True:
            return_string = ""
            return_string += f"Time (UTC): " + got_launches[-1]["launch_date_utc"] + "\n"
            tiane.say(return_string)
            return

        else:
            day = got_launches[-1]["launch_date_utc"][8:10]
            month = got_launches[-1]["launch_date_utc"][5:7]
            minute = got_launches[-1]["launch_date_utc"][15:16]
            hour = got_launches[-1]["launch_date_utc"][11:13]

            speech_dict = {
                    "01": "ersten",
                    "02": "zweiten",
                    "03": "dritten",
                    "04": "vierten",
                    "05": "fünften",
                    "06": "sechsten",
                    "07": "siebten",
                    "08": "achten",
                    "09": "neunten",
                    "10": "zehnten",
                    "11": "elften",
                    "12": "zwölten",
                    "13": "dreizehnten",
                    "14": "vierzehnten",
                    "15": "fünfzehnten",
                    "16": "sechzehnten",
                    "17": "siebzehnten",
                    "18": "achtzehnten",
                    "19": "neunzehnten",
                    "20": "zwanzigsten",
                    "21": "einundzwanzigsten",
                    "22": "zweiundzwanzigsten",
                    "23": "dreiundzwanzigsten",
                    "24": "vierundzwanzigsten",
                    "25": "fünfundzwanzigsten",
                    "26": "sechsundzwanzigsten",
                    "27": "siebenundzwanzigsten",
                    "28": "achtundzwanzigsten",
                    "29": "neunundzwanzigsten",
                    "30": "dreißigsten",
                    "31": "einunddreißigsten",
                    }

            return_string = ""
            return_string += f"Der nächste Start ist am {speech_dict[day]} {speech_dict[month]} "
            return_string += f"um {speech_dict[hour]} Uhr {speech_dict[minute]} U T C\n"
            tiane.say(return_string)

    ################################################################################ 
    # Infos zum nächstem Start 
    ################################################################################ 

    # Define hits
    hit_list1 = ["info", "info", "information"]
    hit1 = any((hit for hit in hit_list if hit in text.lower())) 

    hit_list2 = ["nächster", "next"]
    hit2 = any((hit for hit in hit_list if hit in text.lower())) 

    if hit1 == True and hit2 == True:
        # Get the launches
        got_launches, header = launches.get_launches()

        return_string = ""

        return_string += "Nächster launch: \n"
        return_string += f"Mission ID: " + got_launches[-1]["mission_id"][0] + "\n"
        return_string += f"Launch site: " + got_launches[-1]["launch_site"]["site_name_long"] + "\n"
        return_string += got_launches[-1]["rocket"]["rocket_name"] + "\n"
        return_string += f"Time (UTC): " + got_launches[-1]["launch_date_utc"] + "\n"
        return_string += f"Telemetry: " + got_launches[-1]["telemetry"]["flight_club"] + "\n"

        return_string += "\n\nDetails:\n"
        return_string += got_launches[-1]["details"] + "\n"

        return_string += "\n\nLinks:\n"
        return_string += got_launches[-1]["links"]["wikipedia"] + "\n"

        tiane.say(return_string)
        return

    ################################################################################ 
    # Links zum nächsten Start
    ################################################################################ 

    # Define hits
    hit_list = ["link", "links", "artikel"]
    hit1 = any((hit for hit in hit_list if hit in text.lower())) 

    hit_list2 = ["nächster", "next"]
    hit2 = any((hit for hit in hit_list if hit in text.lower())) 

    if hit1 == True and hit2 == True:
        # Get the launches launch 
        got_launches, header = launches.get_launches()

        # Get the dict containing the links
        links = got_launches[-1]["links"]

        # Iterate over all the items in the dict appending the links to the return string
        return_string = ""
        for key, value in links.items():
            return_string += f"{value}\n"

        tiane.say(return_string)
        return
