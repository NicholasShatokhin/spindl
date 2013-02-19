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