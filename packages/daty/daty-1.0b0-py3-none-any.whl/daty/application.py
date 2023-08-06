#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    Daty
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from gi import require_version
require_version('Gdk', '3.0')
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.Gdk import CURRENT_TIME
from gi.repository.GLib import OptionArg, OptionFlags
from gi.repository.Gio import ApplicationFlags, SimpleAction
from gi.repository.Gtk import Application, Builder, show_uri
from platform import system
from sys import argv

#from .aboutdaty import AboutDaty
name = "ml.prevete.Daty"

class Daty(Application):
    def __init__(self, *args, new_session=True, entities=[], **kwargs):
        super().__init__(*args, application_id=name,
                         flags=ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.entities=entities
        self.window = None
        self.add_main_option("test", ord("t"), OptionFlags.NONE,
                             OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Application.do_startup(self)

        # Set app menu
        action = SimpleAction.new("help", None)
        action.connect("activate", self.on_help)
        self.add_action(action)

        # Set app menu
        action = SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        #builder = Builder()
        #builder.add_from_resource("/ml/prevete/Daty/gtk/menus.ui")
        #self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self, new_session=True, **kwargs):
        if not self.window:
            from .editor import Editor
            self.window = Editor(application=self, title="Daty", quit_cb=self.quit, entities=self.entities)
        #self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "test" in options:
            print("Test argument received: %s" % options["test"])

        self.activate()
        return 0

    def on_help(self, action, param):
        if system() == 'Linux':
            show_uri (None, "help:daty", CURRENT_TIME)
        if system() == 'Windows':
            from webbrowser import open
            open('http://daty.prevete.ml')

    def on_about(self, action, param):
        from .aboutdaty import AboutDaty
        about_dialog = AboutDaty(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

if __name__ == "__main__":
    app = Daty()
    app.run(argv)
