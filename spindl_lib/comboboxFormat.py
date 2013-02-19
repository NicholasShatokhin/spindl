#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
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