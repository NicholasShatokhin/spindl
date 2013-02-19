#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
def format_menu_from_totals(total_list, menu_list, 
							parent_widget, alternate_widget):
	"""Sets the menuitems for the menulist as visible or invisible and sets 
		their label based on info from the total_list"""
	# Iterate through the totals list starting at the most recent
	for entry in reversed(total_list):
		# Set index to the index of the entry in the reversed total_list
		index = (len(total_list)-1) - total_list.index(entry)
		# If index is within the number of menu items
		if index <= (len(menu_list)-1):
			# Set the menulist item at index to visible and set it's label to
			# the total_list entry
			menu_list[index].set_visible(True)
			menu_list[index].set_label(entry[0])
	# If there are less total_list items than the allowed menu_list items
	if len(total_list) < len(menu_list):
		# Iterate through the remaining menulist items and set them invisible
		for index in xrange(len(total_list), len(menu_list)):
			menu_list[index].set_visible(False)
	# If there are no activities in the total_list
	if total_list == []:
		# Set the parent widget as invisible and make the alternate visible
		parent_widget.set_visible(False)
		alternate_widget.set_visible(True)
	# If there are activities to make menuitems for
	else:
		# Set the parent widget as visible and make the alternate invisible
		parent_widget.set_visible(True)
		alternate_widget.set_visible(False)