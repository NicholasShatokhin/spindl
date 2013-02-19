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
#import timeFormat
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
		# Size is a tuple of (width, height)
		self.size = (None, None)
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

	def create_chart(self, type, span=None):
		"""Creates a chart of the given type based the data"""
		if self.type == 'line':
			self.create_line_chart(self.data, span)
		elif self.type == 'pie':
			self.create_pie_chart(self.data, span)
		elif self.type == 'bar':
			self.create_bar_chart(self.data, span)

	def create_line_chart(self, logs, span):
		"""Creates a line chart from the the data"""
		# data must be set to logs before using
		# If size has been specified
		if self.size != (None, None)
			self.chart = pygal.Line(style=self.style, width=self.size[0], height=self.size[1]) # ,label_font_size=11, legend_font_size=11)
		else:
			self.chart = pygal.Line(style=self.style)
		# init 2Darray
		frequencies = []
		for log in logs:
			in_frequencies = False
			# fill 2Darray	
			for entry in frequencies:
				if log[0] == entry[0]:
					 in_frequencies = True
					 entry[1] += self.get_frequency(log[1], span)
			if not in_frequencies:
				frequencies.append(log[0], self.get_frequency(log[1]), span)
		# iterate through 2D array
		for entry in frequencies:
			# add each item to the chart
			self.chart.add(entry[0], entry[1])

	def get_frequency(self, log, span):
		frequencies = []
		if span = 'day':
			for hour in xrange(0,23):
				log_time = int(log[-9:-7])
				if log_time == hour:
					frequencies[hour] = 1
		elif span = 'week':
			for day in xrange(0,6):
				# Get the log date
				log_month = time.strptime(log[0:3],'%b').tm_mon
				log_day = int(log[-20:-18])
				log_year = int(log[-16:-12])
				# Set the log date as a datetime
				log_date = datetime.date(log_year, log_month, log_day)
				# Set the day of the week as an integer between 0 and 6
				log_day_of_week = log_date.strftime("%w")
				if log_day_of_week == day:
					frequencies[day] = 1
		elif span = 'year':
			for month in xrange(0,11):
				log_month = time.strptime(log[0:3],'%b').tm_mon
				if log_month == month:
					frequencies[month] = 1
		return frequencies

	def create_pie_chart(self, totals, span=None):
		"""Creates a pie chart from the the data"""
		# data must be set to totals before using
		# If size has been specified
		if self.size != (None, None)
			self.chart = pygal.Pie(style=self.style, width=self.size[0], height=self.size[1]) # ,label_font_size=11, legend_font_size=11)
		else:
			self.chart = pygal.pie(style=self.style)
		# If span is not specified
		if span == None:
			# Add up totals for all time
			for entry in totals:
				self.chart.add(entry[0], entry[1])
		elif span[0] == 'day':
			pass
		elif span[0] == 'month':
			pass
		elif span[0] == 'year':
			pass

	def create_bar_chart(self, span):
		"""Creates a bar chart from the the data"""
		self.chart = pygal.Bar(style=self.style)
		pass

	def clear(self):
		"""Resets the data and chart"""
		self.data = []
		self.type = None
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
		self.sort_colorlist()

	def send_to_svg(self):
		"""Send the prepared pie graph to an SVG file"""
		self.chart.render_to_file(self.filepath)
		# Set the font in the cvg file to the font specified during __init__ 
		os.system("sed -i 's/font-family:monospace/font-family:%(font)s/g' %(filepath)s") % {'font':self.font, 'filepath': self.filepath}

	def load_into_webview(self):
		"""Load the SVG file for the chart into the webview"""
		self.sort()
		self.send_to_svg()
		self.webview.open(self.filepath)

	def refresh(self):
		"""Refreshes the webview and updates the size of the chart"""
		self.load_into_webview()
		self.webview.refresh()