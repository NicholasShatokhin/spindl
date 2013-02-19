#!/usr/bin/python
from gi.repository import Gdk
import pango

def format_column(column, column_header_label, column_child_text, 
					second_column_child_text=None, column_child_pixbuf=None, 
					ellipsize=True):
	"""Used to format treeview columns to pre-specified colors and ellipsizes
		unless unneccesary"""
	# Format the treeview as a log or total treeview
	column.set_widget(column_header_label)
	column_child_text.set_property('cell-background-gdk', 
									Gdk.Color(62194, 61937, 61680))
	column_child_text.set_property('foreground-gdk', 
									Gdk.Color(34952, 35466, 34181))
	# If the column_child_pixbuf is set
	if not column_child_pixbuf == None:
		# Format the treeview as a color treeview
		column_child_pixbuf.set_property('cell-background-gdk', 
											Gdk.Color(63231, 62975, 62975)) 
		column_child_text.set_property('cell-background-gdk', 
										Gdk.Color(63231, 62975, 62975))
		column_child_text.set_property('foreground-gdk', 
										Gdk.Color(34952, 35466, 34181))
		second_column_child_text.set_property('cell-background-gdk', 
										Gdk.Color(63231, 62975, 62975))
		second_column_child_text.set_property('foreground-gdk', 
										Gdk.Color(34952, 35466, 34181))
	# If the column needs to be ellipsized
	if ellipsize:
		column_child_text.set_property('ellipsize', pango.ELLIPSIZE_END)
		column_child_text.set_property('ellipsize-set', True)