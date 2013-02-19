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
from gi.repository import Gtk

def format_toolbar(toolbar):
	"""Formats a Gtk Toolbar to have the slick ubuntu-black style"""
	context = toolbar.get_style_context()
	context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
	context = toolbar

def add_toolitem(widget, toolbar, position, set_expand=False):
	"""Adds Gtk Widgets to a Gtk Toolbar as Gtk ToolItems"""
	# Adding toolitems to the toolbar must be done manually (as of December 
    # 2012) since Glade cannot add these items to the toolbar correctly.
    # Create a new Gtk ToolItem     
	toolitem = Gtk.ToolItem()
	toolitem.set_expand(set_expand)
	# Add the widget into the ToolItem
	toolitem.add(widget)
	# Show the ToolItem
	toolitem.show()
	# Insert the ToolItem into the toolbar at the specified position
	toolbar.insert(toolitem, position)