#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 <Zane Swafford> <zane@zaneswafford.com>
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
### END LICENSE

from gi.repository import Gdk    
from gi.repository import Gtk
from gi.repository import Dee
_m = dir(Dee.SequenceModel)
from gi.repository import Unity
from gi.repository import Dbusmenu

class Launcher:
    """Adds a quicklist to the Ubuntu Unity Launcher item based on a notebook's 
        pages"""
    def __init__(self, window, notebook):
        self.window = window
        self.notebook = notebook
        # Get the unity launcher item
        self.launcher = Unity.LauncherEntry.get_for_desktop_id("spindl.desktop")
        # Create the quicklist menu
        quicklist = Dbusmenu.Menuitem.new()

        # For each of the notebook pages, we are going to add a section to
        # the dynamic Quicklist
        sections = []
        for page_number in xrange(self.notebook.get_n_pages()):
            sections.append((self.notebook.get_tab_label(self.notebook.get_nth_page(page_number)).get_text()))
        for tab_id, tab_name in enumerate(sections):
            # Create a new item for this section
            section_menu_item = Dbusmenu.Menuitem.new ()
            # Set the tab's name as the menu item's name
            section_menu_item.property_set(Dbusmenu.MENUITEM_PROP_LABEL, 
                                            tab_name)
            # Make the menu item visible
            section_menu_item.property_set_bool(Dbusmenu.MENUITEM_PROP_VISIBLE, 
                                                True)
            # When the menu item is clicked, make it call menu_item_activated
            # with the tab id, which is used to make that the active tab
            section_menu_item.connect('item_activated', 
                                        self.menu_item_activated, 
                                        tab_id)
            # Add the section's menu item to the Quicklist menu
            quicklist.child_append(section_menu_item)
        # Apply the quickist to the Launcher icon
        self.launcher.set_property('quicklist', quicklist)

    def menu_item_activated(self, menu_item, obj, page_id):
        """Called when a Quicklist menu item is selected"""
        # Set the active tab to the one corresponding to the menu item selected
        self.notebook.set_current_page(page_id)
        # Present the Spindl Window to the user
        self.window.present()