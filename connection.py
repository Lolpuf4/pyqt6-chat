import socket
from protocol.protocol import *
from helpers import *
import time
import sys

HOST = "62.60.178.229" if len(sys.argv) > 1 else "127.0.0.1"
PORT = 10009

class Connection:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.connection = True

    def try_login(self, username, password):
        """Try to log in with server; return (success, message)."""
        try:
            send_text(self.socket, username)
            send_text(self.socket, password)

            information = recv(self.socket)
        except socket.timeout:
            return False, "Server did not respond (timeout)."
        except Exception as e:
            return False, f"Network error: {e}"

        if information[0] == "ERR":
            return False, "Invalid credentials"
        elif information[0] == "TXT":
            save_cookie(username, password)
            send_text(self.socket, "desktop")
            return True, "Login successful"
        return False, "Unexpected server response"

    def get_info(self):

        information = recv(self.socket)
        print(information)

        if information[0] == "TXT":
            return information[1]
        elif information[0] == "JSN":
            file = open(information[1], "r", encoding="UTF-8")
            data = json.load(file)
            file.close()
            return data
        elif information[0] == "DIC":
            return json.loads(information[1])
        else:

            raise ConnectionError("unknown type in get_info")


    def send_info(self, data, type):
        if type == "TXT":
            send_text(self.socket, data)
        elif type == "JSN":
            send_json(self.socket, data)

    def disconnect(self):
        try:

            self.connection = False

            send_error(self.socket, "1")
            time.sleep(1)

            self.socket.close()
        except Exception as e:
            print(e)