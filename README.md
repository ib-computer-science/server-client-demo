# Server-client networking example with a GUI (Python port)

This is a Python/Tkinter port of
[ib-cs-server-client](https://github.com/hurrja/ib-cs-server-client), a
Java/Swing example. The class structure, method names, and behavior are
kept as close to the original as the two languages/toolkits allow.

## The purpose of this repository

This repository contains an example of a server-client application.
It serves multiple purposes:

1. To show how a server can accept connections, and how clients can
   take a connection to the server.
2. To show how data can be passed between the server and the clients
   using serialization (here, `pickle`).
3. To demonstrate how the server can interact with multiple clients
   in a round robin manner.
4. To show how server and client functionality can be achieved in a
   program with a GUI.

## Running the server and the clients

The application works as follows:

1. First a startup window opens, and the user has to select whether
   the program is run as the server or the client. The first instance
   should be run as the server. The following instances should be run
   as clients.
2. In the startup window the user has the possibility to specify the
   IP address of the server. For the server instance, the default
   address is obtained from the network configuration of the
   computer. To run the application locally, on only one computer,
   you should specify `127.0.0.1` as the IP address of the server.
   This is also the default server IP address for the client
   instances.
3. Once the server has been started, it will wait for `NUM_CLIENTS`
   (default 2) clients to connect to it. The server will be listening
   for incoming connections at port `SERVER_PORT` (default 50500),
   and the clients will automatically connect to the correct port.
4. After `NUM_CLIENTS` have connected to the server, they will engage
   in a round robin data exchange of requests and replies as follows:
   1. The clients wait for a data request from the server. During
      this time, their user interfaces are inactive (no buttons can
      be pressed).
   2. The server sets the first client to be its current client.
   3. By pressing the send button in the server window, the server
      sends a data request to the current client, and then waits for
      a reply. While waiting, the user interface is inactive.
   4. Upon reading the data request from the server, the user
      interface of the current client becomes active, providing the
      user with the possibility to send a reply to the server.
   5. When the user presses send in the client window, a reply is
      sent to the server. The client then waits for another request.
   6. When the server receives a reply from the current client, it
      sets the next client as its current client, and returns to
      step 3.

## Running multiple instances

Just run `python3 main.py` once per instance (once as the server,
then once per client), each in its own terminal/process. Unlike a
single-process IDE "run configuration", separate OS processes don't
need any special "allow multiple instances" setting.

## Blocking network operations, GUI and `update_idletasks()`

Network operations, such as the server accepting (listening for) a
connection taken by a client, are blocking: the program will not
resume until the operation is completed. In a GUI program, this has
two significant implications:

1. None of the GUI components are responsive during blocking. In this
   application, this is indicated by inactivating the buttons.
2. If something - such as a piece of text, or the activity of a
   button - is changed in the GUI just prior to the blocking
   operation, this change will become visible to the user *after* the
   blocking operation is completed, unless the GUI is explicitly told
   to flush pending changes to the display first. Unlike Swing, whose
   `invokeLater()` reliably defers a callback until after already
   pending GUI work (including painting) has been handled, Tkinter's
   `after(0, func)` and `after_idle(func)` do *not* guarantee that a
   window just created or just updated has actually reached the
   display before `func` runs - testing against the real X server
   confirms the window can still be completely unmapped at that
   point.

To modify a GUI just prior to blocking, the GUI must be modified and
allowed to show this modification, before the blocking operation.
Calling `widget.update_idletasks()` makes this possible:

1. Modify the GUI.
2. Call `update_idletasks()`. This forces Tkinter to process pending
   layout and redraw work and flush it to the display immediately,
   instead of leaving it queued.
3. Only then call the blocking operation.

An example of this can be found in method `invoke_later()` of class
`ApplicationWindow`, used by e.g. `_accept_client()` of class
`Server`.

## Installation

1. Clone the repository.
2. Run `python3 main.py`.

Requires Python 3 with Tkinter (bundled with most standard CPython
installs).

## License

Copyright (C) 2026 Jarmo Hurri

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
