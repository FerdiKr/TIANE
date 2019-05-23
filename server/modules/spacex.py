#!/usr/bin/env python3

from spacex_py import launches


def isValid(text):
    hit_list = ["rakete", "spacex"]
    if any((hit for hit in hit_list if hit in text.lower())) == True:
        return True
    else:
        return False

def handle(text, tiane, local_storage):

    text_lower = text.lower()

    ################################################################################ 
    # Wann (nächster Start)
    ################################################################################ 

    # Define hits
    hit_list = ["wann", "when"]

    if any((hit for hit in hit_list if hit in text.lower())) == True:
        # Get the launches launch 
        got_launches, header = launches.get_launches()

        return_string = ""
        return_string += f"Time (UTC): " + got_launches[-1]["launch_date_utc"] + "\n"
        tiane.say(return_string)
        return

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
