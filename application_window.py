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
import tkinter as tk


class ApplicationWindow:
    def __init__(self, application):
        self.application = application
        self.window = tk.Toplevel()
        self.window.title(str(application.get_role()))

        self.status_var = tk.StringVar()
        status_label = tk.Label(
            self.window,
            textvariable=self.status_var,
            width=50,
            height=6,
            wraplength=380,
            justify=tk.LEFT,
            anchor="nw",
        )
        status_label.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.window, text="Send", command=application.send)
        self.send_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(self.window, text="Quit", command=lambda: os._exit(0))
        self.quit_button.pack(side=tk.LEFT)

    def set_buttons_enabled(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.send_button.config(state=state)
        self.quit_button.config(state=state)

    def set_status_text(self, txt):
        self.status_var.set(txt)

    def invoke_later(self, func):
        self.window.after(0, func)
