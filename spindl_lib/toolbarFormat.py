#!/usr/bin/python
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