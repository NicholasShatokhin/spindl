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
			self.chart =  XY(style=self.style, width=self.size[0], 
								height=self.size[1], fill=True, 
								print_values=False, human_readable=True,
								include_x_axis=True)
		# If size has not already been specified
		else:
			# Let the graph dynamically resize within webview
			self.chart = XY(style=self.style, fill=True, print_values=False,
								human_readable=True, include_x_axis=True)
		frequencies = []
		# Iterate through logs
		for log in data:
			# Get information from the log
			activity = log[0]
			start_time_tuple = tuple_time(log[1])
			stop_time_tuple = tuple_time(log[2])
			# Get the difference in days from start and stop times
			difference_in_days = ((unformat_time(stop_time_tuple) - 
									unformat_time(start_time_tuple)) / 86400)
			# Init a list to get the frequency from the given activity
			activity_frequency = []
			# Set the timespan based on the span[0]
			if span[0] == 'day':
				# There is a max of 24 hours in a day (25 since for + xrange 
				# does not include the last item)
				timespan = 25
				# The index for hours in a time tuple is 2
				timeindex = 2
				# Get the Start and Stop times for the log as an int 
				# representing number of seconds
				start_time_int = (start_time_tuple[1] + 
									1.0*start_time_tuple[0]/60)
				stop_time_int = stop_time_tuple[1] + 1.0*stop_time_tuple[0]/60
				# Get the number of seconds in a given time unit (hour, day,...)
				seconds_per_unit = 60
			elif span[0] == 'month':
				# There is a max of 31 days in a month (32 since for + xrange 
				# does not include the last item)
				timespan = 32
				# The index for days in a time tuple is 3
				timeindex = 3
				# Get the Start and Stop times for the log as an int 
				# representing number of seconds
				start_time_int = (start_time_tuple[2] + 
									1.0*start_time_tuple[1]/60 + 
									1.0*start_time_tuple[0]/3600)
				stop_time_int = (stop_time_tuple[2] + 1.0*stop_time_tuple[1]/60 
									+ 1.0*stop_time_tuple[0]/3600)
				# Get the number of seconds in a given time unit (hour, day,...)
				seconds_per_unit = 24
			#Else span[0] is set to 'year'
			else:
				# There is a max of 12 months in a year (13 since for + xrange 
				# does not include the last item)
				timespan = 13
				# The index for months in a time tuple is 4
				timeindex = 4
				# Get the Start and Stop times for the log as an int 
				# representing number of seconds
				start_time_int = (start_time_tuple[3] + 
									1.0*start_time_tuple[2]/24 + 
									1.0*start_time_tuple[1]/60 + 
									1.0*start_time_tuple[0]/3600)
				stop_time_int = (stop_time_tuple[3]
									+ 1.0*stop_time_tuple[2]/24 
									+ 1.0*stop_time_tuple[1]/60
									+ 1.0*stop_time_tuple[0]/3600)
				# Get the number of seconds in a given time unit (hour, day,...)
				seconds_per_unit = calendar.monthrange(start_time_tuple[5], 
														start_time_tuple[4])[1]
			# Iterate through 
			for interval in xrange(timespan):
				occurances = self.get_occurances_in_span(interval, timeindex, 
															seconds_per_unit,
															start_time_tuple, 
															stop_time_tuple, 
															start_time_int, 
															stop_time_int, 
															difference_in_days)
				activity_frequency.append([interval, occurances])
			self.get_activity_frequency(frequencies, activity, 
										activity_frequency, timespan)
		self.get_percent_frequency(frequencies)
		if not frequencies == []:
			# Add the frequencies to the line chart
			for entry in frequencies:
				self.chart.add(entry[0], entry[1])
		else:
			self.chart = Pie(style=self.style, width=self.size[0],
								height=self.size[1])

	def get_occurances_in_span(self, interval, timeindex, seconds_per_unit,
								start_time_tuple, stop_time_tuple, 
								start_time_int, stop_time_int, 
								difference_in_days):
		"""Gets the occurences of a given activity in an interval based on its
			stop and start time and returns the occurences as a decimal"""
		# 1.0 = the activity occured over the entire time interval,
		# 0.5 = the activity occured over half the interval and so on. 
		occurances = 0
		if (start_time_tuple[timeindex] == interval 
			and stop_time_tuple[timeindex] == interval):
			occurances = stop_time_int - start_time_int
		elif (start_time_tuple[timeindex] == interval 
				and not stop_time_tuple[timeindex] == interval):
			occurances = seconds_per_unit - start_time_int
		elif (not start_time_tuple[timeindex] == interval 
				and stop_time_tuple[timeindex] == interval):
			occurances = stop_time_int
		elif (start_time_tuple[timeindex] < interval 
				and stop_time_tuple[timeindex] > interval):
			occurances = seconds_per_unit
		# If the span is set to days log spans one or more days
		if timeindex == 2 and difference_in_days > 0:
			# The frequency is equal to the number of times the log
			# spans over the given interval.
			occurances = difference_in_days * seconds_per_unit
		return occurances

	def get_activity_frequency(self, frequencies, activity, activity_frequency, 
								timespan):
		"""Gets the number of occurances and adds or appends them to a 
			frequencies list"""
		# Check if activity is already in frequencies list
		activity_in_frequencies = False
		for frequency in frequencies:
			# If the activity is in the frequencies list
			if frequency[0] == activity:
				# Add the activity's frequency to the existing list item
				for interval in xrange(timespan):
					frequency[1][interval][1] += activity_frequency[interval][1]
				# Note that the activity is already in the frequencies
				activity_in_frequencies = True
		# If the activity is not in the frequencies list		
		if not activity_in_frequencies:
			# Append the activity to the frequencies list
			frequencies.append([activity, activity_frequency])
	

	def get_percent_frequency(self, frequencies):
		"""Changes a list of occurances into a list of percent frequencies"""
		# Change the frequencies in the frequencies list to percentages
		for frequency in frequencies:
			# Get the sum of all frequencies for the activity
			sum_of_activity_frequencies = 0
			for interval in frequency[1]:
				sum_of_activity_frequencies += interval[1]
			# Change the value to a percentage
			for interval in frequency[1]:
				if not sum_of_activity_frequencies == 0:
					interval[1] = ((interval[1]*100.00) / 
									(sum_of_activity_frequencies*1.00))
				else:
					interval[1] = 0

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
		# If the chart type is a line chart, fix the tooltip accordingly.
		if self.type == 'line':
			self.fix_tooltip()

	def fix_font(self):
		"""Changes the SVG file's default font (monospace) to the font specified
			when the charter was initialized"""
		if not self.font == None:
			os.system(("sed -i 's/font-family:monospace/font-family:" + self.font 
						+ "/g' " + self.filepath))

	def fix_tooltip(self):
		""" Use sed and regular expressions to replace the SVG tooltip normal
			mouseover (x=?, y=?) to a nicely formatted frequency of ?%"""
		## Only to be used with line charts
		os.system(("sed -i 's/<desc class=\"value\">x=[0-9]*,/" + 
					"<desc class=\"value\">/g' " + self.filepath))
		os.system(("sed -i 's/<desc class=\"value\"> y=/" + 
					"<desc class=\"value\">/g' " + self.filepath))
		os.system(("sed -i 's/<\/desc>/%<\/desc>/g' " + self.filepath))

	def load_into_webview(self, initial=False):
		"""Load the SVG file for the chart into the webview"""
		self.sort()
		self.send_to_svg()
		if initial:
			self.webview.open(self.filepath)
		else:
			self.webview.reload()