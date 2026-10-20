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
import socket

from role import Role
from starter_window import StarterWindow


class Starter:
    def __init__(self, root):
        self.starter_window = StarterWindow(root, self)
        self.role = Role.SERVER
        self.starter_window.show_role(self.role)

    def get_my_ip(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception as e:
            print(f"unable to get IP address, exception [ {e} ]")
            os._exit(1)

    def get_local_ip(self):
        return "127.0.0.1"

    def set_role(self, role):
        self.role = role
        self.starter_window.show_role(role)

    def get_role(self):
        return self.role

    def run_application(self):
        self.starter_window.set_visible(False)
        server_ip = self.starter_window.get_server_ip()
        if self.role == Role.SERVER:
            from server import Server

            application = Server(self, server_ip)
        else:
            from client import Client

            application = Client(self, server_ip)
        application.run()
