# -*- coding: utf-8 -*-

#    SidebarList
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


from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import ListBox, ListBoxRow, Separator, Template
#from re import IGNORECASE, compile, escape, sub

from .entityselectable import EntitySelectable
from .page import Page
#from .property import Property
from .sidebarentity import SidebarEntity
#from .values import Values
from .util import MyThread, label_color

@Template.from_resource("/ml/prevete/Daty/gtk/sidebarlist.ui")
class SidebarList(ListBox):
    __gtype_name__ = "SidebarList"

    def __init__(self,
                 content_leaflet,
                 titlebar_leaflet,
                 stack, 
                 entity_label,
                 entity_description, 
                 entity_search_entry,
                 sidebar_search_entry,
                 autoselect=False,
                 load=None,
                 wikidata=None,
                 *args, **kwargs):
        """Sidebar ListBox
        
        Args:
            stack (Gtk.Stack): entities stack;
            entity_label (Gtk.Label): title of the visible entity;
            description_label (Gtk.Label): description of the visible entity;
            autoselect (bool): whether to select the first element
                by default.
           
        """
        ListBox.__init__(self, *args, **kwargs)

        # Set some inputs as attributes
        self.autoselect = autoselect
        self.stack = stack
        self.load = load
        self.wikidata = wikidata
        self.entity_search_entry = entity_search_entry
        self.sidebar_search_entry = sidebar_search_entry

        # Set "last" selected entities attribute
        self.last = []

        # Set separator as row header
        self.set_header_func(self.update_header)

        self.connect("row-selected", self.sidebar_row_selected_cb,
                                     content_leaflet,
                                     titlebar_leaflet,
                                     stack,
                                     entity_label,
                                     entity_description)

    def entity_search_entry_changed_cb(self, entry):
        text = entry.get_text()
        page = self.stack.get_visible_child()
        statements = page.statements
        i = 0
        row = lambda i,j: statements.get_child_at(j,i)
        while row(i,0):
            p_label = row(i,0).property_label.get_text()
            p_desc = row(i,0).property_label.get_tooltip_text()
            p_found = self.filter(text, p_label) or self.filter(text, p_desc)
            if p_found:
                label_color(row(i,0).property_label, text)
                row(i,0).set_visible(True)
                row(i,1).set_visible(True)
            else:
                label_color(row(i,0).property_label, color='')
                row(i,0).set_visible(False)
                row(i,1).set_visible(False)
            i = i + 1

    def filter(self, query, text):
        return query.lower() in text.lower()

    def sidebar_search_entry_changed_cb(self, entry):
        text = entry.get_text()
        for row in self.get_children():
            if row.get_children():
                child = row.child
                entity = child.entity
                if text.lower() in entity["Label"].lower() or text.lower() in entity["Description"].lower():
                    row.set_visible(True)
                    label_color(child.label, text)
                    label_color(child.description, text)
                else:
                    row.set_visible(False)
                   
    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())

    def set_selection_mode(self, value):
        """Set selection mode on or off

            Args:
                value (bool): whether to activate selection mode
        """
        #TODO: add custom titlebar
        #self.header_bar.add_custom_titlebar
        self.selected = []
        self.foreach(self.set_checkbutton, value)

    def set_checkbutton(self, row, value):
        """Add checkbutton to row

            Args:
                row (Gtk.ListBoxRow): selected row;
                value (bool): whether to add or remove checkbutton.
        """
        if row.get_children():
            child = row.child
            entity = child.entity
            if value:
                row.check = EntitySelectable(entity,
                                             widget=False,
                                             selected=self.selected)
                child.box.pack_start(row.check, False, False, 0)
                row.child.box.child_set_property(row.check, 'position', 0)
            else:
                row.check.destroy()
 
    def add(self, row, select=False):
        """Add widget to a new row

            Overrides Gtk.Container.add

            Args:
                widget (Gtk.Widget): the widget to add to the new row.
        """
        # If the list has rows
        if self.get_children():

            # Pick the last one
            last_row = self.get_children()[-1]

            # If it has no children, it is the ending separator, so remove it
            if not last_row.get_children():
                self.remove(last_row)

        super(SidebarList, self).add(row)

        # Select if 'autoselect'
        if (len(self.get_children()) >= 1 and self.autoselect) or select:
            self.select_row(row)

        # The final empty row that acts as separator
        row = ListBoxRow()
        row.props.activatable = False
        row.props.selectable = False
        super(SidebarList, self).add(row)

    def load_page_async(self, entity):
        entity = cp(entity)
        f = lambda : entity
        def do_call():
            idle_add(lambda: self.on_page_complete(entity))
        thread = MyThread(target = do_call)
        thread.start()

    def on_page_complete(self, entity):
        page = Page(entity['Data'], load=self.load)
        self.stack.add_titled(page, entity['URI'], entity['Label'])
        self.stack.set_visible_child_name(entity['URI'])
        self.entity_search_entry.connect("search-changed", self.entity_search_entry_changed_cb)
        self.sidebar_search_entry.connect("search-changed", self.sidebar_search_entry_changed_cb)
        return None

    def sidebar_row_selected_cb(self,
                                listbox, 
                                row,
                                content_leaflet, 
                                titlebar_leaflet,
                                stack, 
                                entity_label,
                                entity_description,
                                load=None):
        """Sidebar row selected callback

            If not existing, creates entity page and then
            switch to it in content_stack.

            Args:
                listbox (Gtk.ListBox): the listbox class, so self;
                row (Gtk.ListBoxRow): the selected row, which has 
                for only child a SidebarEntity object;
                stack (Gtk.Stack): the stack which has to switch
                visible child.
                entity_label (Gtk.Label): widget of entity title
                entity_description(Gtk.Label)
        """
        if not row:
            if len(self.last) >= 1:
                row = self.last[-1]
            #TODO: decide what to do when no entities are open
            #if len(self.last) == 0:
            else:
                row = self.get_row_at_index(0)
            print(self.last)
            self.select_row(row)
            return None

        # Set last
        self.last.append(row)

        # Set view for folded mode
        content_leaflet.set_visible_child_name("content_stack")
        titlebar_leaflet.set_visible_child_name("sub_header_bar")

        # Get entity from SidebarEntity child
        sidebar_entity = row.child
        entity = sidebar_entity.entity

        # Set titlebar
        def set_text(widget, label):
            widget.set_text(label)
            widget.set_tooltip_text(label)

        set_text(entity_label, entity["Label"])
        set_text(entity_description, entity["Description"])

        # If there is no corresponding child in stack, create one
        if not stack.get_child_by_name(entity['URI']):
            stack.set_visible_child_name("loading")
            children = stack.get_children()

            # Prune the cache
            if len(children) >= 10:
                print("more than 5 children")
                oldest = children[1]
                children.remove(oldest)
                oldest.destroy()
                del oldest
                print(len(children))

            # TODO: Implement a short timeout to make sure you explicitly wanted to load the row
            self.load_page_async(entity)
        else:
            stack.set_visible_child_name(entity['URI'])
            self.entity_search_entry.connect("search-changed", self.entity_search_entry_changed_cb)
            self.sidebar_search_entry.connect("search-changed", self.sidebar_search_entry_changed_cb)
