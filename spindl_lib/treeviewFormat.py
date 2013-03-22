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
import pango

def format_column(column, column_header_label, column_child_text, 
					second_column_child_text=None, column_child_pixbuf=None, 
					ellipsize=True):
	"""Used to format treeview columns to pre-specified colors and ellipsizes
		unless unneccesary"""
	# Format the treeview as a log or total treeview
	if not column == None and not column_header_label == None:
		column.set_widget(column_header_label)
	column_child_text.set_property('cell-background-gdk', 
									Gdk.Color(62194, 61937, 61680))
	column_child_text.set_property('foreground-gdk', 
									Gdk.Color(34952, 35466, 34181))
	# If the column_child_pixbuf is set
	if not column_child_pixbuf == None:
		# Format the treeview as a trend treeview
		column_child_pixbuf.set_property('cell-background-gdk', 
											Gdk.Color(62194, 61937, 61680)) 
		column_child_text.set_property('cell-background-gdk', 
										Gdk.Color(62194, 61937, 61680))
		column_child_text.set_property('foreground-gdk', 
										Gdk.Color(34952, 35466, 34181))
		second_column_child_text.set_property('cell-background-gdk', 
										Gdk.Color(62194, 61937, 61680))
		second_column_child_text.set_property('foreground-gdk', 
										Gdk.Color(34952, 35466, 34181))
	# If the column needs to be ellipsized
	if ellipsize:
		column_child_text.set_property('ellipsize', pango.ELLIPSIZE_END)
		column_child_text.set_property('ellipsize-set', True)