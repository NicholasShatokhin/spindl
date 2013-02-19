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

def format_analytics_combobox(show_combobox, for_combobox):
	"""Sets the entries in the analytics comboboxes"""
	# Get the liststores (models) from the comboboxes
	show_liststore = show_combobox.get_model()
	for_liststore = for_combobox.get_model()
	# Set the lists for the liststores to what we want them to be
	show_list = ['Totals', 'Average']
	for_list = ['All Time', 'Day', 'Month', 'Span of Time']
	# Iterate through the lists and add the entries to the liststores
	for entry in show_list:
		show_liststore.append([entry,])
	for entry in for_list:
		for_liststore.append([entry,])
	# Update the model for the comboboxes
	show_combobox.set_model(show_liststore)
	for_combobox.set_model(for_liststore)

def format_combobox_text(cellrenderertext):
	"""Modifies items in a combobox to the correct color and style"""
	# Set the text color to light grey 
	#cellrenderertext.set_property('foreground-gdk', 
	#								Gdk.Color(34952, 35466, 34181))
	pass