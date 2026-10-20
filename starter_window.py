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
from tkinter import ttk

from role import Role


class StarterWindow:
    IP_ADDRESS_MAX_LENGTH = 15

    def __init__(self, root, starter):
        self.root = root
        self.starter = starter
        root.title("Select program role")

        self.role_var = tk.StringVar()
        self.role_combo = ttk.Combobox(
            root,
            textvariable=self.role_var,
            values=[str(role) for role in Role],
            state="readonly",
        )
        self.role_combo.pack(side=tk.LEFT)
        self.role_combo.bind("<<ComboboxSelected>>", self._on_role_selected)

        self.ip_var = tk.StringVar()
        ip_entry = tk.Entry(root, textvariable=self.ip_var, width=self.IP_ADDRESS_MAX_LENGTH)
        ip_entry.pack(side=tk.LEFT)

        ok_button = tk.Button(root, text="OK", command=starter.run_application)
        ok_button.pack(side=tk.LEFT)

        cancel_button = tk.Button(root, text="Cancel", command=lambda: os._exit(0))
        cancel_button.pack(side=tk.LEFT)

    def _on_role_selected(self, event):
        self.starter.set_role(Role(self.role_var.get()))

    def show_role(self, role):
        self.role_var.set(str(role))
        self.ip_var.set(self.starter.get_my_ip() if role == Role.SERVER else self.starter.get_local_ip())

    def get_server_ip(self):
        return self.ip_var.get()

    def set_visible(self, visible):
        if visible:
            self.root.deiconify()
        else:
            self.root.withdraw()
