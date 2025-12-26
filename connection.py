import socket
from protocol import *
from helpers import *
import time

HOST = "127.0.0.1"
PORT = 10008

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
            return True, "Login successful"
        return False, "Unexpected server response"

    def get_info(self):
        information = recv(self.socket)
        if information[0] == "TXT":
            return information[1]
        elif information[0] == "JSN":
            file = open(information[1], "r", encoding="UTF-8")
            data = json.load(file)
            file.close()
            return data


    def send_info(self, data, type):
        if type == "TXT":
            send_text(self.socket, data)

    def disconnect(self):
        try:
            self.connection = False
            time.sleep(0.2)
            send_error(self.socket, "1")
            self.socket.close()
        except Exception as e:
            print(e)