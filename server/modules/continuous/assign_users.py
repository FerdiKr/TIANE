PRIORITY = 1

def start(tiane, profile):
    profile['TIANE_voice_recognized_users'] = {}
    profile['TIANE_cam_recognized_users'] = {}

def assign(user, room, tiane, profile):
    # Erst den User aus allen Räumen entfernen...
    for raum in profile['rooms'].values():
        try:
            if user in raum['users']:
                raum['users'].remove(user)
        except KeyError:
            raum['users'] = []
            continue
    for raum in tiane.rooms.values():
        if user in raum.users:
            raum.users.remove(user)
    # ...Dann den User in den richtigen Raum schreiben...
    try:
        profile['rooms'][room]['users'].append(user)
    except KeyError:
        profile['rooms'][room]['users'] = [user]
    tiane.rooms[room].users.append(user)
    # ...Und den richtigen Raum in den User schreiben!
    profile['users'][user]['room'] = room


def run(tiane, profile):
    assigned_users = [] # Alle Nutzer, die in dieser Runde schon neu zugewiesen wurden, werden hierein geschrieben...
                        # Das heißt, die Zuweisungsmethoden sollten nach Aussagekraft sortiert werden, die besten zuerst.

    for room in tiane.rooms.copy().values():
        # Erst mal holen wir die relevanten Informationen ein, nämlich ob ein Raum ein Sprachkommando empfangen hat...
        # Dem entnehmen wir dann, was der Raum schätzt, welcher Nutzer das war.
        user = room.Clientconnection.readanddelete('TIANE_user_voice_recognized')
        if user is not None:
            profile['TIANE_voice_recognized_users'][room.name] = user

    for room, users in profile['TIANE_cam_recognized_users'].items():
        # Wenn die Gesichtserkennung einen Nutzer zweimal in einem Raum verortet, ist es wahrscheinlich,
        # dass mindestens eines der Gesichter wirklich zu diesem Nutzer gehört.
        # finds duplicates in lists
        seen = {}
        dupes = []
        for user in users:
            if user not in seen:
                seen[user] = 1
            else:
                if seen[user] == 1:
                    dupes.append(user)
                seen[user] += 1
        # Doppelt im Raum vorhandene Nutzer diesem Raum zuweisen
        if not dupes == []:
            for user in dupes:
                if not user == 'Unknown' and user not in assigned_users:
                    assign(user, room, tiane, profile)
                    assigned_users.append(user)
                    #print('{} {} wegen doppelt gesehen'.format(user, room))

    for room, users in profile['TIANE_cam_recognized_users'].items():
        # Wenn man nicht doppelt im Raum vorhanden ist, muss man doch wenigstens zweimal hintereinander
        # dort gesichtet worden sein, ohne zwischenzeitlich woanders aufzutauchen...
        for user in users:
            if not user == 'Unknown':
                try:
                    if profile['users'][user]['last_seen_room'] == room:
                        profile['users'][user]['last_seen_counter'] += 1
                        if profile['users'][user]['last_seen_counter'] >= 2 and user not in assigned_users:
                            assign(user, room, tiane, profile)
                            assigned_users.append(user)
                            #print('{} {} wegen oft gesehen'.format(user,room))
                    else:
                        profile['users'][user]['last_seen_room'] = room
                        profile['users'][user]['last_seen_counter'] = 0
                except KeyError:
                    profile['users'][user]['last_seen_room'] = room
                    profile['users'][user]['last_seen_counter'] = 0
                    continue

    for room, user in profile['TIANE_voice_recognized_users'].copy().items():
        # Und jetzt noch die Variante, bei der die Stimmerkennung was zu erkennen glaubt...
        # Die einzigen Sicherheit, die wir hier bieten können, ist leider, dass der Nutzer
        # nicht in dieser Runde bereits anderweitig zugewiesen worden sein darf...
        if not user == 'Unknown':
            if user not in assigned_users:
                assign(user, room, tiane, profile)
                assigned_users.append(user)
                #print('{} {} wegen Stimme erkannt'.format(user,room))


    for room, user in profile['TIANE_voice_recognized_users'].copy().items():
	# Am Ende vom ganzen Text teilen wir den Räumen, die angefragt haben, dann auch noch mit,
    	# welcher Nutzer es denn nach unserer Einschätzung "wirklich" war, damit der Raum fortfahren kann.
        if not profile['rooms'][room]['users'] == []:
            if user in profile['rooms'][room]['users'] and not user == 'Unknown':
                tiane.rooms.copy()[room].Clientconnection.send({'TIANE_user_server_guess':user})
            else:
                tiane.rooms.copy()[room].Clientconnection.send({'TIANE_user_server_guess':profile['rooms'][room]['users'][-1]})
        else:
            tiane.rooms.copy()[room].Clientconnection.send({'TIANE_user_server_guess':'Unknown'})
        del profile['TIANE_voice_recognized_users'][room]
