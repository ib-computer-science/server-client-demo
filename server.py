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


class Server(Application):
    NUM_CLIENTS = 2

    def __init__(self, starter, my_ip):
        super().__init__(starter, Role.SERVER)
        self.my_ip = my_ip
        self.server_socket = None
        self.client_sockets = [None] * self.NUM_CLIENTS
        self.cur_num_clients = 0
        self.cur_client = 0

    def run(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", self.SERVER_PORT))
            self.server_socket.listen()
        except Exception as e:
            print(f"unable to open server socket, exception [ {e} ]")
            os._exit(1)
        self.deactivate_buttons()
        self._accept_client()

    def send(self):
        try:
            self.client_sockets[self.cur_client].sendall(pickle.dumps(Data(0)))
        except Exception as e:
            print(f"unable to send data, exception [ {e} ]")
            os._exit(1)

        self.set_status_text(f"sent data to client [ {self.cur_client} ], waiting for reply")
        self.deactivate_buttons()
        self.invoke_later(self.receive)

    def receive(self):
        try:
            data = pickle.loads(self.client_sockets[self.cur_client].recv(4096))
        except Exception as e:
            print(f"unable to receive data, exception [ {e} ]")
            os._exit(1)
        self.set_status_text(f"received data from client [ {self.cur_client} ]")
        self.cur_client = (self.cur_client + 1) % self.NUM_CLIENTS
        self._ready_to_send()

    def _accept_client(self):
        assert self.cur_num_clients < self.NUM_CLIENTS
        self.set_status_text(
            f"accepting [ {self.NUM_CLIENTS - self.cur_num_clients} ] clients at {self.my_ip}"
        )
        self.invoke_later(self._accept)

    def _accept(self):
        try:
            client_socket, _ = self.server_socket.accept()
            self.client_sockets[self.cur_num_clients] = client_socket
            self.cur_num_clients += 1
        except Exception as e:
            print(f"unable to accept connections, exception [ {e} ]")
            os._exit(1)
        if self.cur_num_clients < self.NUM_CLIENTS:
            self._accept_client()
        else:
            self.cur_client = 0
            self._ready_to_send()

    def _ready_to_send(self):
        self.set_status_text(f"ready to send data to client [ {self.cur_client} ]")
        self.activate_buttons()
