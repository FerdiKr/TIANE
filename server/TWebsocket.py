import asyncio
import json
import time
import traceback
from threading import Thread
from typing import List, MutableMapping, Optional

import websockets

EVENT_LOOP = None
ACTIVE_CONNECTIONS: List[websockets.WebSocketServerProtocol] = []

ROOMS_TO_WS: MutableMapping[str, websockets.WebSocketServerProtocol] = {}
OUTPUT_TO_WS: MutableMapping[str, List[str]] = {}
SECURE_ROOMS: List[str] = []

AWAITING_USERS: List[str] = []  # Messages from those are not processed normally. Put them to queued_messages, someone is waiting.
QUEUED_MESSAGES: MutableMapping[str, str] = {}  # If added here remove user from awaiting_users
LISTEN_TIMEOUT: int = 0

def startWsServer(tiane, port: int, allowNonSecure: bool, listenTimeout: int):
    global EVENT_LOOP
    EVENT_LOOP = asyncio.get_event_loop()

    global LISTEN_TIMEOUT
    LISTEN_TIMEOUT = listenTimeout

    async def newConection(websocket: websockets.WebSocketServerProtocol, path):
        tiane.Log.write('INFO', 'Neue WebSocket-Verbindung mit {}'.format(str(websocket.remote_address)), show=True)

        ACTIVE_CONNECTIONS.append(websocket)

        async def receiveMsg() -> Optional[dict]:
            resp = await websocket.recv()
            if type(resp) == 'str' or str(type(resp)) == "<class 'str'>" or isinstance(resp, str):
                return json.loads(resp)
            else:
                return json.loads(str(resp, 'utf-8'))

        while True:
            try:
                message = await receiveMsg()
                print(message)
                action = message['action'].lower()
                if action == 'listen':
                    msg = message['msg']
                    user = message['user']
                    room = message['room']
                    explicit = message['explicit']
                    if 'role' in message and message['role'] is not None:
                        role = message['role']
                    else:
                        role = 'USER'

                    if user in AWAITING_USERS:
                        if not user in tiane.local_storage['rooms'][room]['users']:
                            for myRoom in tiane.local_storage['rooms']:
                                if user in tiane.local_storage['rooms'][myRoom]['users']:
                                    tiane.local_storage['rooms'][myRoom]['users'].remove(user)
                            tiane.local_storage['rooms'][room]['users'].append(user)
                            tiane.local_storage['users'][user]['room'] = room

                        AWAITING_USERS.remove(user)
                        QUEUED_MESSAGES[user] = msg
                    elif explicit:
                        if not user in tiane.Users.userlist:
                            tiane.Users.userlist.append(user)
                            if (' ' in user):
                                userdata = {
                                    'name': user,
                                    'first_name': user[:user.rindex(' ')],
                                    'last_name': user[user.rindex(' ') + 1:],
                                    'role': role,
                                    'uid': len(tiane.Users.userlist),
                                    'path': ''
                                }
                            else:
                                userdata = {
                                    'name': user,
                                    'first_name': user,
                                    'last_name': '',
                                    'role': role,
                                    'uid': len(tiane.Users.userlist),
                                    'path': ''
                                }
                            tiane.Users.userdict[user] = userdata
                            tiane.Modules.user_modules[user] = []

                        if not user in tiane.local_storage['rooms'][room]['users']:
                            for myRoom in tiane.local_storage['rooms']:
                                if user in tiane.local_storage['rooms'][myRoom]['users']:
                                    tiane.local_storage['rooms'][myRoom]['users'].remove(user)
                            tiane.local_storage['rooms'][room]['users'].append(user)
                            tiane.local_storage['users'][user]['room'] = room

                        if not tiane.route_query_modules(user, text = msg, direct = True, origin_room = room, must_be_secure = room in SECURE_ROOMS):
                            await websocket.send(json.dumps({
                                'action': 'say',
                                'msg': 'Entschuldige, das habe ich leider nicht verstanden.',
                                'ping': user,
                                'room': room
                            }))
                elif action == 'notify':
                    msg = message['msg']
                    user = message['user']
                    if 'output' in message and message['output'] is not None:
                        output = message['output']
                    else:
                        output = 'auto'
                    tiane.route_say('§nonexistent_websocket', msg, None, user, output)
                elif action == 'create_room':
                    room = message['room']
                    secure = message['secure']
                    if not room in tiane.room_list and (allowNonSecure or secure):
                        if (secure):
                            SECURE_ROOMS.append(room)
                        tiane.room_list.append(room)
                        tiane.local_storage['rooms'][room] = {
                            'name': room,
                            'users':[]
                        }
                        ROOMS_TO_WS[room] = websocket
                elif action == 'set_output':
                    output = message['output']
                    room = message['room']

                    if room in ROOMS_TO_WS:
                        if not output in OUTPUT_TO_WS:
                            OUTPUT_TO_WS[output] = []
                        if not room in OUTPUT_TO_WS[output]:
                            OUTPUT_TO_WS[output].append(room)
                elif action == 'set_user_to_room':
                    user = message['user']
                    room = message['room']
                    if not user in tiane.local_storage['rooms'][room]['users']:
                        for myRoom in tiane.local_storage['rooms']:
                            if user in tiane.local_storage['rooms'][myRoom]['users']:
                                tiane.local_storage['rooms'][myRoom]['users'].remove(user)
                        tiane.local_storage['rooms'][room]['users'].append(user)
                        tiane.local_storage['users'][user]['room'] = room
            except websockets.ConnectionClosed:
                if websocket in ACTIVE_CONNECTIONS:
                    ACTIVE_CONNECTIONS.remove(websocket)

                collectRooms = []
                for room in ROOMS_TO_WS:
                    if ROOMS_TO_WS[room] == websocket:
                        collectRooms.append(room)
                for room in collectRooms:
                    del ROOMS_TO_WS[room]
                    if room in SECURE_ROOMS:
                        SECURE_ROOMS.remove(room)

                for output in OUTPUT_TO_WS:
                    if websocket in OUTPUT_TO_WS[output]:
                        OUTPUT_TO_WS[output].remove(websocket)

                return
            except:
                traceback.print_exc()
                time.sleep(1)

    websocketServer = websockets.serve(newConection, "127.0.0.1", port)

    def runThread():
        tiane.Log.write('INFO', 'WebSocket gestartet', show=True)
        EVENT_LOOP.run_until_complete(websocketServer)
        EVENT_LOOP.run_forever()

    serverThread = Thread(target=runThread)
    serverThread.setDaemon(True)
    serverThread.start()

def sendEvent(name: str, data: dict):
    for ws in ACTIVE_CONNECTIONS:
        asyncio.new_event_loop().run_until_complete(ws.send(json.dumps({
            'action': 'event',
            'name': name,
            'data': data
        })))

def tellUserInRoom(user: Optional[str], room: str, msg: str) -> bool:
    if room in ROOMS_TO_WS:
        print({
            'action': 'say',
            'msg': msg,
            'ping': user,
            'room': room
        })
        asyncio.new_event_loop().run_until_complete(ROOMS_TO_WS[room].send(json.dumps({
            'action': 'say',
            'msg': msg,
            'ping': user,
            'room': room
        })))
        return True
    else:
        return False

def tellUser(user: str, msg: str, local_storage) -> bool:
    for myRoom in local_storage['rooms']:
        if myRoom in ROOMS_TO_WS and user in local_storage['rooms'][myRoom]['users']:
            tellUserInRoom(user, myRoom, msg)
            return True

def tellUserVia(user: Optional[str], output: str, msg: str) -> bool:
    if output in OUTPUT_TO_WS:
        if (len(OUTPUT_TO_WS[output]) == 0):
            return False
        for room in OUTPUT_TO_WS[output]:
            tellUserInRoom(user, room, msg)
        return True
    else:
        return False

def listen(user: str, local_storage) -> Optional[str]:
    if user is None:
        return 'TIMEOUT_OR_INVALID'

    is_ws_room = False
    for myRoom in local_storage['rooms']:
        if myRoom in ROOMS_TO_WS and user in local_storage['rooms'][myRoom]['users']:
            is_ws_room = True
    if not is_ws_room:
        return None

    AWAITING_USERS.append(user)

    answer: Optional[str] = None
    timeout = time.time() + LISTEN_TIMEOUT
    while answer is None and timeout >= time.time():
        if user in QUEUED_MESSAGES:
            answer = QUEUED_MESSAGES[user]
            del QUEUED_MESSAGES[user]
        else:
            time.sleep(0.01)
    if answer is None:
        if user in AWAITING_USERS:
            AWAITING_USERS.remove(user)
        return 'TIMEOUT_OR_INVALID'
    else:
        return answer