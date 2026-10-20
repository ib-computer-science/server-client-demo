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

from abc import ABC, abstractmethod

from application_window import ApplicationWindow


class Application(ABC):
    SERVER_PORT = 50500

    def __init__(self, starter, role):
        self.starter = starter
        self.role = role
        self.application_window = ApplicationWindow(self)

    def get_role(self):
        return self.role

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def send(self):
        ...

    @abstractmethod
    def receive(self):
        ...

    def set_status_text(self, txt):
        self.application_window.set_status_text(txt)

    def activate_buttons(self):
        self.application_window.set_buttons_enabled(True)

    def deactivate_buttons(self):
        self.application_window.set_buttons_enabled(False)

    def invoke_later(self, func):
        self.application_window.invoke_later(func)
