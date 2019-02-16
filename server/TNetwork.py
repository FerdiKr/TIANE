from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random

from threading import Thread
import traceback
import binascii
import pickle
import socket
import time

class TNetwork_Connection_Server:
    def __init__(self):
        self.sock = None
        self.dict_append = {}
        self.dict_remove = {}
        self.dict_buffer = {}
        self.dict_read = {}
        self.dict_send = {}
        self.connected = False
        self.stopped = False

        self.key = b"YOU CAN GET A KEY BY CALLING Crypto.Random.get_random_bytes(32)"

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def connect(self, conn, addr):
        # Client und Server tauschen eine kleine Begrüßung aus, um sich gegenseitig zu identifizieren
        try:
            length = self.recvall(conn,16)
            greeting = self.recvall(conn, int(length))
            #print('Server hat empfangen: {}'.format(greeting))
            if not greeting == b'Hallo Server':
                print('[ERROR] Client {} konnte sich nicht korrekt identifizieren'.format(addr))
                raise ConnectionAbortedError('Client konnte sich nicht korrekt identifizieren!')
            greeting = 'Hallo Geraet'
            lenstring = str(len(greeting)).ljust(16)
            conn.send(lenstring.encode('utf-8'))
            conn.send(greeting.encode('utf-8'))
        except:
            print('[ERROR] Verbindung mit Client {} fehlgeschlagen'.format(addr))
            conn.close()
            raise
            return
        # Begrüßung vorbei, ab jetzt wird richtig (verschlüsselt?) übertragen
        self.sock = conn
        self.connected = True
        self.start()
        return

    def start(self):
        snt = Thread(target=self.run)
        snt.daemon = True
        snt.start()
        #return self

    def read(self,key):
        try:
            return self.dict_read[key]
        except KeyError:
            return None

    def readanddelete(self,key):
        data = self.dict_read.pop(key, None)
        return data

    def send(self, data_dict):
        self.dict_append.update(data_dict)

    def send_buffer(self, data_dict):
        # Gebaut vor allem mit Blick auf Audio-Buffer...
        # Ist aber auch für andere Anwendungen gut:
        # Es ergänzt einfach eine schon im Netzwerk vorhandene Liste
        for key in data_dict:
            if type(data_dict[key]) is not list:
                continue
            if key in self.dict_buffer:
                for i in data_dict[key]:
                    self.dict_buffer[key].append(i)
            else:
                self.dict_buffer[key] = data_dict[key]

    def encrypt(self, key, plaintext):
        assert len(key) == 32

        # Choose a random, 16-byte IV.
        iv = Random.new().read(AES.block_size)

        # Convert the IV to a Python integer.
        iv_int = int(binascii.hexlify(iv), 16)

        # Create a new Counter object with IV = iv_int.
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

        # Create AES-CTR cipher.
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)

        # Encrypt and return IV and ciphertext.
        ciphertext = aes.encrypt(plaintext)
        return (iv, ciphertext)

    def decrypt(self, key, iv, ciphertext):
        assert len(key) == 32

        # Initialize counter for decryption. iv should be the same as the output of
        # encrypt().
        iv_int = int(binascii.hexlify(iv), 16)
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

        # Create AES-CTR cipher.
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)

        # Decrypt and return the plaintext.
        plaintext = aes.decrypt(ciphertext)
        return plaintext

    def run(self):
        conn = self.sock
        try:
            while True:
                #time.sleep(0.01)
                # Initialization_vector empfangen
                length = self.recvall(conn,16)
                iv = self.recvall(conn, int(length))
                # Dictionary empfangen
                length = self.recvall(self.sock,16)
                ciphertext = self.recvall(self.sock, int(length))
                dict_recieve = pickle.loads(self.decrypt(self.key, iv, ciphertext))
                #print('Server recieves: {}'.format(dict_recieve))
                # Dictionaries ergänzen/aufräumen
                try:
                    for key,value in dict_recieve['TIANE_send_buffer'].items():
                        if key in self.dict_read:
                            for i in value:
                                self.dict_read[key].append(i)
                        else:
                            self.dict_read[key] = value
                    del dict_recieve['TIANE_send_buffer']
                except KeyError:
                    pass
                self.dict_read.update(dict_recieve)
                self.dict_send = self.dict_append.copy()
                self.dict_send['TIANE_send_buffer'] = self.dict_buffer.copy()
                self.dict_append = {}
                self.dict_buffer = {}
                # Dictionary senden
                #print('Server sends: {}'.format(self.dict_send))
                (iv, ciphertext) = self.encrypt(self.key, pickle.dumps(self.dict_send, -1))
                lenstring = str(len(iv)).ljust(16)
                conn.send(lenstring.encode('utf-8'))
                conn.send(iv)
                lenstring = str(len(ciphertext)).ljust(16)
                conn.send(lenstring.encode('utf-8'))
                conn.send(ciphertext)
                self.dict_send = {}
                # Ende?
                if self.stopped == True:
                    self.sock.close()
                    break
        except Exception as e:
            #print(e)
            #traceback.print_exc()
            self.sock.close()
            self.connected = False

    def stop(self):
        self.stopped = True

class TNetwork_Connection_Client:
    def __init__(self):
        self.ip = ''
        self.port = 50000
        self.sock = socket.socket()
        self.dict_append = {}
        self.dict_remove = {}
        self.dict_buffer = {}
        self.dict_read = {}
        self.dict_send = {}
        self.connected = False
        self.stopped = False

        self.key = b"YOU CAN GET A KEY BY CALLING Crypto.Random.new_random_bytes(32)"

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def connect(self,server_ip):
        while True:
            # Verbindet sich mit dem nächsten offenen Port des Servers und findet heraus,
            # ob es der richtige ist.
            try:
                self.sock.connect((server_ip, self.port))
            except:
                self.port += 1
                continue
            try:
                greeting = 'Hallo Server'
                lenstring = str(len(greeting)).ljust(16)
                self.sock.send(lenstring.encode('utf-8'))
                self.sock.send(greeting.encode('utf-8'))
                length = self.recvall(self.sock,16)
                greeting = self.recvall(self.sock,int(length))
                if not greeting == b'Hallo Geraet':
                    print('[ERROR] Server {}:{} konnte sich nicht korrekt identifizieren'.format(server_ip, self.port))
                    continue
            except:
                print('[ERROR] Verbindung mit Server {}:{} fehlgeschlagen'.format(server_ip, self.port))
                continue
            break
        self.ip = server_ip
        # Begrüßung vorbei, ab jetzt wird richtig (verschlüsselt?) übertragen
        self.connected = True
        self.start()

    def start(self):
        cnt = Thread(target=self.run)
        cnt.daemon = True
        cnt.start()
        #return self

    def read(self,key):
        try:
            return self.dict_read[key]
        except KeyError:
            return None

    def readanddelete(self,key):
        data = self.dict_read.pop(key, None)
        return data

    def send(self, data_dict):
        self.dict_append.update(data_dict)

    def send_buffer(self, data_dict):
        # Gebaut vor allem mit Blick auf Audio-Buffer...
        # Ist aber auch für andere Anwendungen gut:
        # Es ergänzt einfach eine schon im Netzwerk vorhandene Liste
        for key in data_dict:
            if type(data_dict[key]) is not list:
                continue
            if key in self.dict_buffer:
                for i in data_dict[key]:
                    self.dict_buffer[key].append(i)
            else:
                self.dict_buffer[key] = data_dict[key]

    def encrypt(self, key, plaintext):
        assert len(key) == 32

        # Choose a random, 16-byte IV.
        iv = Random.new().read(AES.block_size)

        # Convert the IV to a Python integer.
        iv_int = int(binascii.hexlify(iv), 16)

        # Create a new Counter object with IV = iv_int.
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

        # Create AES-CTR cipher.
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)

        # Encrypt and return IV and ciphertext.
        ciphertext = aes.encrypt(plaintext)
        return (iv, ciphertext)

    def decrypt(self, key, iv, ciphertext):
        assert len(key) == 32

        # Initialize counter for decryption. iv should be the same as the output of
        # encrypt().
        iv_int = int(binascii.hexlify(iv), 16)
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

        # Create AES-CTR cipher.
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)

        # Decrypt and return the plaintext.
        plaintext = aes.decrypt(ciphertext)
        return plaintext

    def run(self):
        conn = self.sock
        dict_recieve = {}
        try:
            while True:
                # Dictionaries ergänzen/aufräumen
                try:
                    for key,value in dict_recieve['TIANE_send_buffer'].items():
                        if key in self.dict_read:
                            for i in value:
                                self.dict_read[key].append(i)
                        else:
                            self.dict_read[key] = value
                    del dict_recieve['TIANE_send_buffer']
                except KeyError:
                    pass
                self.dict_read.update(dict_recieve)
                self.dict_send = self.dict_append.copy()
                self.dict_send['TIANE_send_buffer'] = self.dict_buffer.copy()
                self.dict_append = {}
                self.dict_buffer = {}
                # Dictionary senden
                #print('Client sends: {}'.format(self.dict_send))
                (iv, ciphertext) = self.encrypt(self.key, pickle.dumps(self.dict_send, -1))
                lenstring = str(len(iv)).ljust(16)
                conn.send(lenstring.encode('utf-8'))
                conn.send(iv)
                lenstring = str(len(ciphertext)).ljust(16)
                conn.send(lenstring.encode('utf-8'))
                conn.send(ciphertext)
                self.dict_send = {}
                #time.sleep(0.01)
                # Initialization_vector empfangen
                length = self.recvall(conn,16)
                iv = self.recvall(conn, int(length))
                # Dictionary empfangen
                length = self.recvall(self.sock,16)
                ciphertext = self.recvall(self.sock, int(length))
                dict_recieve = pickle.loads(self.decrypt(self.key, iv, ciphertext))
                #print('Client recieves: {}'.format(dict_recieve))
                # Ende?
                if self.stopped == True:
                    self.sock.close()
                    break
        except Exception as e:
            #print(e)
            #traceback.print_exc()
            self.sock.close()
            self.connected = False

    def stop(self):
        self.stopped = True
