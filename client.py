# Copyright (C) 2026 Jarmo Hurri

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

import os
import pickle
import socket

from application import Application
from data import Data
from role import Role


class Client(Application):
    def __init__(self, starter, server_ip):
        super().__init__(starter, Role.CLIENT)
        self.server_ip = server_ip
        self.socket = None

    def run(self):
        self.set_status_text(f"connecting to server at {self.server_ip}")
        self.deactivate_buttons()
        self.invoke_later(self.connect)

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.SERVER_PORT))
        except Exception as e:
            print(f"unable to open socket, exception [ {e} ]")
            os._exit(1)

        self.set_status_text("made connection, waiting for request")
        self.invoke_later(self.receive)

    def send(self):
        try:
            self.socket.sendall(pickle.dumps(Data(1)))
        except Exception as e:
            print(f"unable to send data, exception [ {e} ]")
            os._exit(1)

        self.set_status_text("sent reply to server, waiting for more requests")
        self.deactivate_buttons()
        self.invoke_later(self.receive)

    def receive(self):
        try:
            data = pickle.loads(self.socket.recv(4096))
        except Exception as e:
            print(f"unable to receive data, exception [ {e} ]")
            os._exit(1)
        self.set_status_text("received request from server, ready to reply")
        self.activate_buttons()
