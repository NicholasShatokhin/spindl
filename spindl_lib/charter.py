#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
from pygal import *
from pygal.style import *
import os
import operator

CONST_MAX_DATA_ENTRIES = 18
CONST_MAX_VERTICAL_ENTRIES = 20
CONST_COLOR_LIST = '#729fcf', '#ef2929', '#fce94f', '#8ae234', '#ad7fa8', 
					'#fcaf3e',	'#3465a4', '#cc0000', '#edd400', '#73d216', 
					'#75507b', '#f57900', '#204a87', '#a40000', '#c4a000', 
					'#4e9a06', '#5c3566', '#ce5c00', '#d3d7cf']

class Charter:
	def __init__(self, font, filepath, webview):
		self.font = font
		self.filepath = filepath
		self.webview = webview
		self.data = []
		self.type = None
		self.chart = None
		self.colorlist = CONST_COLOR_LIST
		self.sort_colorlist()
		# The custom pygal style used for the pie graph.
		self.style = Style(background='#F7F6F6',
							plot_background='#F7F6F6',
							foreground='#888a85',
							foreground_light='#888a85',
							foreground_dark='#555753',
							opacity='.6',
							opacity_hover='.9',
							transition='200ms ease-in',
	  						colors=(self.color_list))

	def add_entry(self, label, time, color):
		"""Adds an entry to data and gives it a label, time, and color"""
		# If the color is not set
		if color == None:
			# Set the color to light grey
			color = len(self.colorlist)-1
		# If color is specified
		else:
			# Make sure it is a valid color from the colorlist
			while color >= len(self.colorlist)-1:
				color -= len(self.colorlist)-1
		# add the entry to the data
		self.data.append((label, time, color))

	def compound_other_data(self):
		"""Compounds smallest data entries into 'other' entry"""
		# This function is necessary to keep legend from growing larger than the 
		# widget it is contained in.
		if len(self.data) > CONST_MAXIMUM_DATA_ENTRIES:
			# Make a copy of the data
			sorted_data = self.data
			# Organize the copy from smallest to largest
			sorted_data.sort(key=operator.itemgetter(1))
			# Add entry ("Other", 0, max_color) to data
			self.add_entry("Other", 0, max_color)
			# While there are more data entries than CONST_MAXIMUM_DATA_ENTRIES
			while len(sorted_data) > CONST_MAXIMUM_DATA_ENTRIES:
				# Add the smallest entry to data the "Other" entry.
				sorted_data[-1][1] += sorted_data[0][1] 
				# Remove the smallest entry
				sorted_data = sorted_data[1:]
			# Set original data equal to the modified copy
			self.data = sorted_data

	def clear(self):
		"""Resets the data and chart"""
		self.data = []
		self.type = None
		self.chart = None

	def sort_data_by_size(self, data):
		"""Used to sort the pie slices by time from largest to smallest."""
		# Make a duplicate of the data so it does not get tampered with
		sorted_data = self.data
		# Sort from smallest to largest based on time.
		sorted_data.sort(key=operator.itemgetter(1))
		# Then set data as the reverse the sorted data.
		self.data = sorted_data[::-1]

	def sort_color_list(self):
		"""Used to make the order of the color_list match the order pf the 
			pie_list's activity colors"""
		sorted_colorlist = [] * len(self.colorlist) 
		for index in xrange (0, len(self.data)):
			color = self.data[index][2]
			sorted_colorlist[index] = self.colorlist[color]
		self

	def send_to_svg(self):
		"""Send the prepared pie graph to an SVG file"""
		self.chart.render_to_file(self.filepath)
		# Set the font in the cvg file to the font specified during __init__ 
		os.system("sed -i 's/font-family:monospace/font-family:%(font)s/g' %(filepath)s") % {'font':self.font, 'filepath': self.filepath}

	def load_into_webview(self):
		"""Load the SVG file for the chart into the webview"""
		self.webview.open(filepath)