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
import calendar
from timeFormat import *
import os
import operator
from datetime import timedelta
from math import ceil
from gi.repository import GLib

CONST_MAX_DATA_ENTRIES = 15
CONST_MAX_VERTICAL_ENTRIES = 20
CONST_COLOR_LIST = ('#729fcf', '#ef2929', '#fce94f', '#8ae234', '#ad7fa8', 
					'#fcaf3e',	'#3465a4', '#cc0000', '#edd400', '#73d216', 
					'#75507b', '#f57900', '#204a87', '#a40000', '#c4a000', 
					'#4e9a06', '#5c3566', '#ce5c00', '#d3d7cf')

class Charter:
	def __init__(self, font, filepath, webview, webview_window, 
					loading_spinner):
		self.font = font
		self.filepath = filepath
		self.webview = webview
		# Turn off the right click menu for the webview
		self.webview.props.settings.props.enable_default_context_menu = False
		self.webview_window = webview_window
		self.loading_spinner = loading_spinner
		self.loading_spinner.set_visible(False)
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
		self.visible = True

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

	def compound_other_data(self, data):
		"""Compounds smallest data entries into 'other' entry"""
		# This function is necessary to keep legend from growing larger than the 
		# widget it is contained in.
		# Get the sum of all values (the [1] index in the entries)
		sum_of_values = 0
		for entry in data:
			sum_of_values += entry[1]
		# Set the minimum amount to one percent of the total amount
		minimum_amount = 0.01 * sum_of_values
		# Create a list item 'other' and give it a value of 0 and the last color
		# in the CONST_COLOR_LIST.
		other = ['Other ', 0, len(CONST_COLOR_LIST)-1]
		entries_to_compound = []
		entries_compunded = False
		for entry in data:
			if entry[1] <= minimum_amount:
				other[1] += entry[1]
				entries_to_compound.append(entry)
				entries_compunded = True
		for entry in entries_to_compound:
			del data[data.index(entry)]	
		# If the data still has too many entries, compound the smallest into the
		# 'Other' entry
		if len(data) > CONST_MAX_DATA_ENTRIES:
			self.sort_data_by_size(data)
			entries_to_compound = []
			for entry in xrange((len(data) - CONST_MAX_DATA_ENTRIES)):
				other[1] += data[entry][1]
				entries_to_compound.append(data[entry])
				entries_compunded = True
			for entry in entries_to_compound:
				del data[data.index(entry)]
		if entries_compunded:
			data.append(other)

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
				color = log[3]
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
					chart_list.append([activity, log_time, color])
		else:
			# If span is not specified then the data are totals.
			# Set the chart_list equal to the total data.
			for total in data:
				chart_list.append((total[0], total[2], total[3]))
		# Add each entry is the chart_list to the chart	
		self.sort(chart_list)
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
		if not chart_list == []:
			for entry in chart_list:
				self.chart.add(entry[0], entry[1])

	def create_bar_chart(self, data, span):
		"""Creates a bar chart from the the data"""
		# Initialize the chart_list
		chart_list = []
		for log in data:
			activity_time = 0
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			color = log[3]
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
				chart_list.append([activity, activity_time, color])
		self.sort(chart_list)
		# Data must be organized for day, month, etc. before using
		# If size has been specified
		if not self.size == (None, None):
			self.chart = Bar(style=self.style, y_scale=60.0,
								print_values=False, include_x_axis=True,
								width=self.size[0], height=self.size[1])
		# If size has not already been specified
		else:
			# Let the graph dynamically resize within webview
			self.chart = Bar(style=self.style, print_values=False,
								include_x_axis=True, y_scale=60.0)
		self.set_y_labels(chart_list)
		## Add each entry is the chart_list to the chart	
		if not chart_list == []:
			for entry in chart_list:
				time = str(timedelta(seconds=entry[1]))
				if time[1] == ':':
					time = '0' + time
				self.chart.add(entry[0], [{'value':entry[1], 'label':time}])
		else:
			self.chart = Pie(style=self.style, width=self.size[0],
								height=self.size[1])

	def set_y_labels(self, chart_list):
		"""Sets the y labels on a bar chart"""
		# Set up the y axis
		maximum_time_in_seconds = 0
		for entry in chart_list:
			if entry[1] > maximum_time_in_seconds:
				maximum_time_in_seconds = entry[1]
		max_number_of_minutes = int(ceil(maximum_time_in_seconds/60))+2
		y_labels = []
		if max_number_of_minutes > 2:
			if max_number_of_minutes < 30:
				for minute in xrange(max_number_of_minutes+1):
					y_labels.append(minute*60)
			elif max_number_of_minutes >= 30 and max_number_of_minutes < 60:
				for minute in xrange((max_number_of_minutes/5)+1):
					y_labels.append(minute*60*5)
			elif max_number_of_minutes >= 60 and max_number_of_minutes < 120:
				for minute in xrange((max_number_of_minutes/10)+2):
					y_labels.append(minute*60*10)
			elif max_number_of_minutes >= 120 and max_number_of_minutes < 240:
				for minute in xrange((max_number_of_minutes/15)+1):
					y_labels.append(minute*60*15)
			elif max_number_of_minutes >= 240 and max_number_of_minutes < 480:
				for minute in xrange((max_number_of_minutes/20)+1):
					y_labels.append(minute*60*20)
			elif max_number_of_minutes >= 480 and max_number_of_minutes < 960:	
				for minute in xrange((max_number_of_minutes/30)+1):
					y_labels.append(minute*60*30)
			elif max_number_of_minutes >= 960:
				for minute in xrange((max_number_of_minutes/60)+1):
					y_labels.append(minute*3600)
		else:
			for second in xrange((maximum_time_in_seconds)+1):
					y_labels.append(second)
		self.chart.y_labels = y_labels

	def convert_y_axis_to_time(self, label):
		"""Converts y axis labels from seconds to minutes"""
		y_value_in_time = ''
		y_value_in_time = str(timedelta(seconds=int(label)))
		if y_value_in_time[1] == ':':
			y_value_in_time = '0' + y_value_in_time
		if not self.filepath == None:
			convert_y_axis = ("sed -i 's/class=\\\"\\\">%s.0/class=\\\"\\\"" + 
								">%s/g' " + self.filepath) % (str(label), 
																y_value_in_time)
			os.system(convert_y_axis)
			# Then convert the major y axises (The zeroeth and first amounts) to
			# a formatted time if the label is a major axis.
			convert_major_y_axis = ("sed -i 's/class=\\\"major\\\">%s.0/" + 
									"class=\\\"major\\\">%s/g' " + 
										self.filepath) % (str(label), 
															y_value_in_time)
			os.system(convert_major_y_axis)

	def fix_tooltip(self):
		"""Changes the SVG file's default mouseover tooltip to no longer contain 
			value for time in seconds"""
		if not self.filepath == None:
			os.system(("sed -i 's/<desc class=\"value\">[0-9]*<\/desc>//g' " + 
						self.filepath))

	def clear(self):
		"""Resets the data and chart"""
		self.data = []
		self.chart = None

	def sort_data_by_size(self, data):
		"""Used to sort the pie slices by time from largest to smallest."""
		# Make a duplicate of the data so it does not get tampered with
		sorted_data = data
		# Sort from smallest to largest based on time.
		sorted_data.sort(key=operator.itemgetter(1))
		# Make sure that the Other entry is at the end of the list if it exists
		for entry in sorted_data:
			if entry[0] == 'Other ':
				sorted_data.insert(0,sorted_data.pop(sorted_data.index(entry)))
		# Then set data as the sorted data.
		data = sorted_data#[::-1]

	def sort_colorlist(self, data):
		"""Used to make the order of the color_list match the order of the 
			pie_list's activity colors"""
		# Create an empty list to put the sorted colors in
		sorted_colorlist = []
		# Iterate through the chart data
		for entry in data:
			# Get the specified color from the chart data 
			color = int(entry[2])
			# Arrange the colorlist so that the given datum recieves that color
			if color < (len(CONST_COLOR_LIST)-1) or entry[0] == 'Other ':
				sorted_colorlist.append(CONST_COLOR_LIST[color])
			else:
				sorted_colorlist.append(CONST_COLOR_LIST[(color-(len(CONST_COLOR_LIST)-1))])
		# Set the colorlist to the sorted_colorlist
		self.colorlist = sorted_colorlist
		if not self.colorlist == []:
			self.style = Style(background='#F7F6F6',
						plot_background='#F7F6F6',
						foreground='#888a85',
						foreground_light='#888a85',
						foreground_dark='#555753',
						opacity='.6',
						opacity_hover='.9',
						transition='200ms ease-in',
							colors=(self.colorlist))

	def sort(self, data):
		"""Sort the data and colors"""
		if not data == []:
			self.compound_other_data(data)
			self.sort_data_by_size(data)
			self.sort_colorlist(data)

	def send_to_svg(self):
		"""Send the prepared pie graph to an SVG file"""
		self.chart.render_to_file(self.filepath)
		# Set the font in the svg file to the font specified during __init__ 
		self.fix_font()
		if hasattr(self.chart, 'y_labels'):
			self.fix_tooltip()	
			for label in self.chart.y_labels:
				self.convert_y_axis_to_time(label)

	def fix_font(self):
		"""Changes the SVG file's default font (monospace) to the font specified
			when the charter was initialized"""
		if not self.font == None:
			os.system(("sed -i 's/font-family:monospace/font-family:" + self.font 
						+ "/g' " + self.filepath))

	def start_loading_animation(self):      
        GLib.timeout_add(500, self.get_loading_animation)
	
	def get_loading_animation(self):
		if self.visible:
	        chart_loading = not (str(self.webview.get_load_status()) == '<enum WEBKIT_LOAD_FAILED of type WebKitLoadStatus>' 
	                    or str(self.webview.get_load_status()) == '<enum WEBKIT_LOAD_FINISHED of type WebKitLoadStatus>')
	        if not chart_loading:
	            self.loading_spinner.stop()
	            self.loading_spinner.set_visible(False)
	            self.webview_window.set_visible(True)
	        return chart_loading
	    else:
	    	return False       

	def load_into_webview(self, initial=False):
		"""Load the SVG file for the chart into the webview"""
		#self.sort()
		self.send_to_svg()
		if initial:
			self.webview.open(self.filepath)
		else:
			self.webview.reload()
			if self.visible:
				self.webview_window.set_visible(False)
				self.loading_spinner.set_visible(True)
				self.loading_spinner.start()
				self.start_loading_animation()

	def set_visible(self, visible=True):
		self.visible = visible
		self.webview_window.set_visible(visible)
		if not visible:
			self.loading_spinner.set_visible(False)