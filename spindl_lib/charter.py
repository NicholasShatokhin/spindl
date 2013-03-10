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
from pygal import *
from pygal.style import *
import time
import calendar
from timeFormat import *
import os
import operator

CONST_MAX_DATA_ENTRIES = 18
CONST_MAX_VERTICAL_ENTRIES = 20
CONST_COLOR_LIST = ['#729fcf', '#ef2929', '#fce94f', '#8ae234', '#ad7fa8', 
					'#fcaf3e',	'#3465a4', '#cc0000', '#edd400', '#73d216', 
					'#75507b', '#f57900', '#204a87', '#a40000', '#c4a000', 
					'#4e9a06', '#5c3566', '#ce5c00', '#d3d7cf']

class Charter:
	def __init__(self, font, filepath, webview):
		self.font = font
		self.filepath = filepath
		self.webview = webview
		# Turn off the right click menu for the webview
		self.webview.props.settings.props.enable_default_context_menu = False
		self.data = []
		self.type = None
		# Size is a tuple of (width, height)
		self.size = (450, 350)
		self.chart = None
		self.colorlist = ['#729fcf', '#ef2929', '#fce94f', '#8ae234', '#ad7fa8', 
							'#fcaf3e',	'#3465a4', '#cc0000', '#edd400', '#73d216', 
							'#75507b', '#f57900', '#204a87', '#a40000', '#c4a000', 
							'#4e9a06', '#5c3566', '#ce5c00', '#d3d7cf']
		#self.sort_colorlist()
		# The custom pygal style used for the pie graph.
		self.style = Style(background='#F7F6F6',
							plot_background='#F7F6F6',
							foreground='#888a85',
							foreground_light='#888a85',
							foreground_dark='#555753',
							opacity='.6',
							opacity_hover='.9',
							transition='200ms ease-in',
	  						colors=(self.colorlist))

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

	def compound_other_data(self):#, data):
		"""Compounds smallest data entries into 'other' entry"""
		# This function is necessary to keep legend from growing larger than the 
		# widget it is contained in.
		#if len(data) > CONST_MAX_DATA_ENTRIES:
		#	# Make a copy of the data
		#	sorted_data = self.data
		#	# Organize the copy from smallest to largest
		#	sorted_data.sort(key=operator.itemgetter(1))
		#	# Add entry ("Other", 0, max_color) to data
		#	max_color = len(CONST_COLOR_LIST)-1
		#	data.append("Other", 0, max_color)
		#	# While there are more data entries than CONST_MAX_DATA_ENTRIES
		#	while len(sorted_data) > CONST_MAX_DATA_ENTRIES:
		#		# Add the smallest entry to data the "Other" entry.
		#		sorted_data[-1][1] += int(sorted_data[0][1])
		#		# Remove the smallest entry
		#		sorted_data = sorted_data[1:]
		#	# Set original data equal to the modified copy
		#	data = sorted_data
		pass

	def create_chart(self, chart_type=None, span=None):
		"""Creates a chart of the given type based the data"""
		if not chart_type == None:
			self.type = chart_type
		if self.type == 'pie':
			self.create_pie_chart(self.data, span)
		elif self.type == 'bar':
			self.create_bar_chart(self.data, span)
	
	def create_pie_chart(self, data=None, span='all', no=None):
		"""Creates a pie chart from the the data"""
		# Data must be organized for day, month, etc. before using
		# If size has been specified
		if not self.size == (None, None):
			self.chart = Pie(style=self.style,
								print_values=False,
								fill=True,
								human_readable=True,
								include_x_axis=True,
								width=self.size[0], 
								height=self.size[1])
		# If size has not already been specified
		else:
			# Let the graph dynamically resize within webview
			self.chart = Pie(style=self.style, print_values=False, fill=True,
								human_readable=True, include_x_axis=True)
		# Create the list of objects to be added to the chart
		chart_list = []
		# If the span has been specified, then get the logs only for that time
		if not span == None and not span == 'all':
			# Iterate through the log data.
			for log in self.data:
				# Get and format the information we need from the log.
				activity = log[0]
				log_start = unformat_time(tuple_time(log[1]))
				log_end = unformat_time(tuple_time(log[2]))
				minimum = unformat_time(span[1])
				maximum = unformat_time(span[2])
				# Add the time and activity to the chart_list.
				log_time = time_in_span(log_start, log_end, minimum, maximum)
				# Check if the activity has already been added to chart_list.
				in_chart_list = False
				for entry in chart_list:
					# If the activity is in the chart_list, make a note and add.
					# its time to the existing list item.
					if entry[0] == activity:
						entry[1] += log_time
						in_chart_list = True
				# If the log is not in the chart_list and it is in the span, add
				# it to the chart_list.
				if not in_chart_list and log_time > 0:
					chart_list.append([activity, log_time])
		else:
			# If span is not specified then the data are totals.
			# Set the chart_list equal to the total data.
			for total in data:
				chart_list.append((total[0], total[2]))
		# Add each entry is the chart_list to the chart	
		if not chart_list == []:
			for entry in chart_list:
				self.chart.add(entry[0], entry[1])

	def create_bar_chart(self, data, span):
		"""Creates a bar chart from the the data"""
		# Data must be organized for day, month, etc. before using
		# If size has been specified
		if not self.size == (None, None):
			self.chart = Bar(style=self.style,
								#print_values=False,
								width=self.size[0], 
								height=self.size[1])
		# If size has not already been specified
		else:
			# Let the graph dynamically resize within webview
			self.chart = Bar(style=self.style)#, print_values=False)
		# Initialize some dummy values for chart_list
		chart_list = []#[('Working', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1]),
				#('Cleaning',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3]),
				#('Studying',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])]
		for log in data:
			activity_time = 0
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			minimum = span[1]
			maximum = span[2]	
			minimum = unformat_time(minimum)
			maximum = unformat_time(maximum)
			activity_time += time_in_span(log_start, log_end, minimum, maximum)
			in_chart_list = False
			for entry in chart_list:
				if entry[0] == activity:
					entry[1] += activity_time
					in_chart_list = True
			if not in_chart_list and activity_time > 0:
				chart_list.append([activity, activity_time])
		## Add each entry is the chart_list to the chart	
		if not chart_list == []:
			for entry in chart_list:
				self.chart.add(entry[0], entry[1])
		else:
			self.chart = Pie(style=self.style, width=self.size[0],
								height=self.size[1])

	def clear(self):
		"""Resets the data and chart"""
		self.data = []
		self.chart = None

	def sort_data_by_size(self):
		"""Used to sort the pie slices by time from largest to smallest."""
		# Make a duplicate of the data so it does not get tampered with
		sorted_data = self.data
		# Sort from smallest to largest based on time.
		sorted_data.sort(key=operator.itemgetter(1))
		# Then set data as the reverse the sorted data.
		self.data = sorted_data[::-1]

	def sort_colorlist(self):
		"""Used to make the order of the color_list match the order of the 
			pie_list's activity colors"""
		# Create an empty list to put the sorted colors in
		sorted_colorlist = []
		# Iterate through the chart data
		for index in xrange (len(self.data)):
			# Get the specified color from the chart data 
			color = int(self.data[index][3])
			# Arrange the colorlist so that the given datum recieves that color
			sorted_colorlist.append(CONST_COLOR_LIST[color])
		# Set the colorlist to the sorted_colorlist
		self.colorlist = sorted_colorlist

	def sort(self):
		"""Sort the data and colors"""
		self.sort_data_by_size()
		self.sort_colorlist()

	def send_to_svg(self):
		"""Send the prepared pie graph to an SVG file"""
		self.chart.render_to_file(self.filepath)
		# Set the font in the svg file to the font specified during __init__ 
		self.fix_font()

	def fix_font(self):
		"""Changes the SVG file's default font (monospace) to the font specified
			when the charter was initialized"""
		if not self.font == None:
			os.system(("sed -i 's/font-family:monospace/font-family:" + self.font 
						+ "/g' " + self.filepath))
	def load_into_webview(self, initial=False):
		"""Load the SVG file for the chart into the webview"""
		self.sort()
		self.send_to_svg()
		if initial:
			self.webview.open(self.filepath)
		else:
			self.webview.reload()