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

	def compound_other_data(self):
		"""Compounds smallest data entries into 'other' entry"""
		# This function is necessary to keep legend from growing larger than the 
		# widget it is contained in.
		if len(self.data) > CONST_MAX_DATA_ENTRIES:
			# Make a copy of the data
			sorted_data = self.data
			# Organize the copy from smallest to largest
			sorted_data.sort(key=operator.itemgetter(1))
			# Add entry ("Other", 0, max_color) to data
			self.add_entry("Other", 0, max_color)
			# While there are more data entries than CONST_MAX_DATA_ENTRIES
			while len(sorted_data) > CONST_MAX_DATA_ENTRIES:
				# Add the smallest entry to data the "Other" entry.
				sorted_data[-1][1] += sorted_data[0][1] 
				# Remove the smallest entry
				sorted_data = sorted_data[1:]
			# Set original data equal to the modified copy
			self.data = sorted_data

	def create_chart(self, chart_type=None, span=None):
		"""Creates a chart of the given type based the data"""
		if not chart_type == None:
			self.type = chart_type
		if self.type == 'line':
			self.create_line_chart(self.data, span)
		elif self.type == 'pie':
			self.create_pie_chart(self.data, span)
		elif self.type == 'bar':
			self.create_bar_chart(self.data, span)

	def create_line_chart(self, data, span):
		"""Creates a line chart from the the data"""
		# Data must be organized for day, month, etc. before using
		# If size has been specified
		if not self.size == (None, None):
			self.chart =  XY(style=self.style, 
								width=self.size[0], 
								height=self.size[1],
								fill=True,
								#print_zeroes=False,
								print_values=False,
								human_readable=True,
								include_x_axis=True)#,
								#show_points=False)
		# If size has not already been specified
		else:
			# Let the graph dynamically resize within webview
			self.chart = XY(style=self.style, fill=True)
		# Set the X-Axis labels for the line graph
		#if span[0] == 'day':
		#	timespan = map(str, range(25))
		#elif span[0] == 'month':
		#	timespan = map(str, range(0, 31))
		# Else span[0] == 'year'
		#else:
		#	timespan = map(str, range(0, 12))
		#self.chart.x_labels = timespan
		
		frequencies = []
		# Iterate through logs
		for log in data:
				# Get information from the log
				activity = log[0]
				print '\n\n LOG IS: ' + str(log[1])
				start_time = tuple_time(log[1])
				stop_time = tuple_time(log[2])

				# Get the difference in days from start and stop times
				difference_in_days = ((unformat_time(stop_time) - 
										unformat_time(start_time)) / 86400)
				# Get the frequency from the given log
				activity_frequency = []
				for hour in xrange(25):
					hour_frequency = 0
					if start_time[2] == hour and stop_time[2] == hour:
						hour_frequency = ((stop_time[1] + stop_time[0]/60) - 
											(start_time[1] + start_time[0]/60))
					elif start_time[2] == hour and not stop_time[2] == hour:
						hour_frequency = (60 - (start_time[1] + 
												start_time[0]/60))
					elif (start_time[2] < hour and stop_time[2] > hour and 
							difference_in_days == 0):
							hour_frequency = 1
					activity_frequency.append([hour, hour_frequency])
				# Check if activity is already in frequencies list
				activity_in_frequencies = False
				for frequency in frequencies:
					# If the activity is in the frequencies list
					if frequency[0] == activity:
						# Add the activity's frequency to the existing list item
						frequency[1] += activity_frequency
						activity_in_frequencies = True
				# If the activity is not in the frequencies list		
				if not activity_in_frequencies:
					# Append the activity to the frequencies list
					frequencies.append([activity, activity_frequency])
		# Change the frequencies in the frequencies list to percentages
	
		for frequency in frequencies:
			# Get the sum of all frequencies for the activity
			sum_of_activity_frequencies = 0
			for hour in frequency[1]:
				sum_of_activity_frequencies += hour[1]
			# Change the value to a percentage
			for hour in frequency[1]:
				hour[1] = (hour[1]*100.00) / (sum_of_activity_frequencies*1.00)

		for entry in frequencies:
				self.chart.add(entry[0], entry[1])
		

	def create_pie_chart(self, data=None, span='all', no=None):
		"""Creates a pie chart from the the data"""
		# Data must be organized for day, month, etc. before using
		# If size has been specified
		if not self.size == (None, None):
			self.chart = Pie(style=self.style,
								print_values=False,
								width=self.size[0], 
								height=self.size[1])
		# If size has not already been specified
		else:
			# Let the graph dynamically resize within webview
			self.chart = Pie(style=self.style, print_values=False)
		# Create the list of objects to be added to the chart
		chart_list = []
		# If the span has been specified, then get the logs only for that time
		if not span == None and not span == 'all':
			#print 'Data is: ' + str(data)
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
		if not chart_list == None:
			for entry in chart_list:
				self.chart.add(entry[0], entry[1])

	def create_bar_chart(self, data, span):
		"""Creates a bar chart from the the data"""
		pass

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
		"""Used to make the order of the color_list match the order pf the 
			pie_list's activity colors"""
		sorted_colorlist = [] * len(self.colorlist) 
		for index in xrange (0, len(self.data)):
			color = self.data[index][2]
			sorted_colorlist[index] = self.colorlist[color]
		self.colorlist = sorted_colorlist

	def sort(self):
		"""Sort the data and colors"""
		self.sort_data_by_size()
		#self.sort_colorlist()

	def send_to_svg(self):
		"""Send the prepared pie graph to an SVG file"""
		self.chart.render_to_file(self.filepath)
		# Set the font in the svg file to the font specified during __init__ 
		os.system("sed -i 's/font-family:monospace/font-family:ubuntu/g' /home/zane/.spindl/chart.svg")
		if self.type == 'line':
			self.fix_tooltip()
		#print "OK"

	def fix_font(self):
		os.system(("sed -i 's/font-family:monospace/font-family:" + self.font 
					+ "/g' " + self.filepath))

	def fix_tooltip(self):
		print "FILEPATH = " + str(self.filepath)
		os.system("sed -i 's/<desc class=\"value\">x=[0-9]*,/<desc class=\"value\">/g' /home/zane/.spindl/chart.svg")
		#print "OK1"
		os.system("sed -i 's/<desc class=\"value\"> y=/<desc class=\"value\">/g' /home/zane/.spindl/chart.svg")
		print "OK2"
		os.system("sed -i 's/<\/desc>/%<\/desc>/g' /home/zane/.spindl/chart.svg")
		print "OK3"

	def load_into_webview(self, initial=False):
		"""Load the SVG file for the chart into the webview"""
		self.sort()
		self.send_to_svg()
		if initial:
			self.webview.open(self.filepath)
		else:
			self.webview.reload()