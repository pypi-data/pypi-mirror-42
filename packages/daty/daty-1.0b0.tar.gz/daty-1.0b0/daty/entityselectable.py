# -*- coding: utf-8 -*-

#    EntitySelectable
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

from gi.repository.Gtk import CheckButton, Template

@Template.from_resource("/ml/prevete/Daty/gtk/entityselectable.ui")
class EntitySelectable(CheckButton):
    __gtype_name__ = "EntitySelectable"

    widget = Template.Child("widget")
    label = Template.Child("label")
    description = Template.Child("description")
    URI = Template.Child("URI")

    def __init__(self, entity, *args,
                 widget=True, selected=None, open_button=None,
                 select_entities=None):
        """Search result widget in 'open new entity' dialog

            Args:
                entity (dict): havig keys "URI, "Label", "Description" and "Data".
                selected (list): keep track of entity's selected status
        """
        CheckButton.__init__(self, *args)
        
        self.entity = entity

        if widget:
            self.label.set_text(entity['Label'])
            self.description.set_text(entity['Description'])
            self.URI.set_text(entity['URI'])
        else:
            self.label.destroy()
            self.description.destroy()
            self.URI.destroy()

        #TODO: implement selected as signal in cointaining listbox
        if selected != None:
            if entity["URI"] in (v["URI"] for v in selected):
                self.set_active(True)
            args = [self.toggled_cb, selected]
            if open_button: args = args + [open_button]
            if select_entities: args = args + [select_entities]
            self.connect("toggled", *args)
        self.show_all()

    def toggled_cb(self, widget, selected, *args):
        """Toggled callback

            Args:
                widget (Gtk.Widget): toggled widget (so self);
                selected (list): add self's entity attribute to it to 
                keep track of parent listbox selected toggles.
        """
        if widget.get_active():
            selected.add(self.entity)
            try:
                args[0].set_sensitive(True)
                args[1].set_label(" ".join(["Selected",
                                            str(len(selected)),
                                            "entities"]))
            except Exception as e:
                raise e
                #pass
        else:
            selected.remove(self.entity)
            try:
                if not selected:
                    args[0].set_sensitive(False)
                    args[1].set_label("Click on entities to select them")
                else:
                    args[1].set_label(" ".join(["Selected",
                                                str(len(selected)),
                                                "entities"]))
            except:
                pass
