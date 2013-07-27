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
from gi.repository import GdkPixbuf
from spindl_lib.treeviewFormat import format_column
from timeFormat import time_in_span, tuple_time, unformat_time
from math import ceil

class TrendView:
	def __init__(self, treeview_window, treestore, activity_cellrenderedtext, 
					trend_pixbuf, percent_change_cellrenderedtext, image_directory):
		self.treeview_window = treeview_window
		self.treestore = treestore
		self.activity_cellrenderedtext = activity_cellrenderedtext
		self.trend_pixbuf = trend_pixbuf
		self.percent_change_cellrenderedtext = percent_change_cellrenderedtext
		self.data = []
		# Make the trendview visible by default
		self.visible = True
		# Load up the pixbufs
		self.image_directory = image_directory
		self.up_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.image_directory + 'up.png')
		self.same_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.image_directory + 'same.png')
		self.down_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.image_directory + 'down.png')
		# Format the treeview_window
		format_column(None, None, self.activity_cellrenderedtext, 
					self.percent_change_cellrenderedtext, self.trend_pixbuf)

	def generate_day_trends(self, date):
		"""Takes logs from self.data and changes them to activity trends for 
		since the previous day based on a given date tuple"""
		day_activity_list = []
		previous_day_activity_list = []
		trends = []
		# Iterate through the log data.
		for log in self.data:
			# Get and format the information we need from the log.
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			minimum = unformat_time((0,0,0,date[0],date[1],date[2]))
			maximum = unformat_time((59,59,23,date[0],date[1],date[2]))
			# Add the time and activity to the chart_list.
			log_time = time_in_span(log_start, log_end, minimum, maximum)
			# Check if the activity has already been added to chart_list.
			in_day_activity_list = False
			for entry in day_activity_list:
				# If the activity is in the chart_list, make a note and add.
				# its time to the existing list item.
				if entry[0] == activity:
					entry[1] += log_time
					in_day_activity_list = True
			# If the log is not in the chart_list and it is in the span, add
			# it to the chart_list.
			if not in_day_activity_list and log_time > 0:
				day_activity_list.append([activity, log_time])
		# Iterate through the log data.
		for log in self.data:
			# Get and format the information we need from the log.
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			minimum = unformat_time((0,0,0,date[0],date[1],date[2]))
			minimum -= unformat_time((0,0,0,1,0,0))
			maximum = unformat_time((59,59,23,date[0],date[1],date[2]))
			maximum -= unformat_time((0,0,0,1,0,0))
			# Add the time and activity to the chart_list.
			log_time = time_in_span(log_start, log_end, minimum, maximum)
			# Check if the activity has already been added to chart_list.
			in_previous_day_activity_list = False
			for entry in previous_day_activity_list:
				# If the activity is in the chart_list, make a note and add.
				# its time to the existing list item.
				if entry[0] == activity:
					entry[1] += log_time
					in_previous_day_activity_list = True
			# If the log is not in the chart_list and it is in the span, add
			# it to the chart_list.
			if not in_previous_day_activity_list and log_time > 0:
				previous_day_activity_list.append([activity, log_time])
		# Search through the day_activity_list and previous_day_activity_list 
		# for matching activities
		for activity in day_activity_list:
			for previous_activity in previous_day_activity_list:
				if activity[0] == previous_activity[0]:
					# Get the percent change between the two activities' times
					# as a string in the form of 100.00%
					percent_change = (((activity[1]-previous_activity[1])*1.00)
										/(previous_activity[1]*1.00))
					percent_change = str((ceil(percent_change*10000.00))/100.00)
					if percent_change[-2] == '.':
						percent_change += '0'
					percent_change += '%'
					# Add this activity and it's percent change to trends list 
					trends.append([activity[0], percent_change])
		# Set data as trends
		self.data = trends

	def generate_month_trends(self, date):
		"""Takes logs from self.data and changes them to activity trends for 
		since the previous month based on a given date tuple"""
		month_activity_list = []
		previous_month_activity_list = []
		trends = []
		# Iterate through the log data.
		for log in self.data:
			# Get and format the information we need from the log.
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			minimum = unformat_time((0,0,0,1,date[1],date[2]))
			maximum = unformat_time((59,59,23,date[0],date[1],date[2]))
			# Add the time and activity to the chart_list.
			log_time = time_in_span(log_start, log_end, minimum, maximum)
			# Check if the activity has already been added to chart_list.
			in_month_activity_list = False
			for entry in month_activity_list:
				# If the activity is in the chart_list, make a note and add.
				# its time to the existing list item.
				if entry[0] == activity:
					entry[1] += log_time
					in_month_activity_list = True
			# If the log is not in the chart_list and it is in the span, add
			# it to the chart_list.
			if not in_month_activity_list and log_time > 0:
				month_activity_list.append([activity, log_time])
		# Iterate through the log data.
		for log in self.data:
			# Get and format the information we need from the log.
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			if date[1] > 1:
				minimum = unformat_time((0,0,0,1,date[1]-1,date[2]))
			else:
				minimum = unformat_time((0,0,0,1,12,date[2]-1))
			maximum = unformat_time((59,59,23,1,date[1],date[2]))
			maximum -= unformat_time((0,0,0,1,0,0))
			# Add the time and activity to the chart_list.
			log_time = time_in_span(log_start, log_end, minimum, maximum)
			# Check if the activity has already been added to chart_list.
			in_previous_month_activity_list = False
			for entry in previous_month_activity_list:
				# If the activity is in the chart_list, make a note and add.
				# its time to the existing list item.
				if entry[0] == activity:
					entry[1] += log_time
					in_previous_month_activity_list = True
			# If the log is not in the chart_list and it is in the span, add
			# it to the chart_list.
			if not in_previous_month_activity_list and log_time > 0:
				previous_month_activity_list.append([activity, log_time])
		# Search through the month_activity_list and 
		# previous_month_activity_list for matching activities
		for activity in month_activity_list:
			for previous_activity in previous_month_activity_list:
				if activity[0] == previous_activity[0]:
					# Get the percent change between the two activities' times
					# as a string in the form of 100.00%
					percent_change = (((activity[1]-previous_activity[1])*1.00)
										/(previous_activity[1]*1.00))
					percent_change = str((ceil(percent_change*10000.00))/100.00)
					if percent_change[-2] == '.':
						percent_change += '0'
					percent_change += '%'
					# Add this activity and it's percent change to trends list 
					trends.append([activity[0], percent_change])
		# Set data as trends
		self.data = trends

	def generate_span_trends(self, from_date, to_date):
		"""Takes logs from self.data and changes them to activity trends for 
		since the previous day based on a given date tuple"""
		activity_list = []
		# Iterate through the log data.
		for log in self.data:
			# Get and format the information we need from the log.
			activity = log[0]
			log_start = unformat_time(tuple_time(log[1]))
			log_end = unformat_time(tuple_time(log[2]))
			minimum = unformat_time((0, 0, 0, from_date[0], from_date[1],
										from_date[2]))
			maximum = unformat_time((59, 59, 23, to_date[0], to_date[1],
										to_date[2]))
			log_time = time_in_span(log_start, log_end, minimum, maximum)
			# If the log exists in the span
			if log_time > 0:
				in_activity_list = False
				# Iterate through the activity list to check for duplicates
				for entry in activity_list:
					if entry[0] == activity:
						# Then the entry is in the activity list
						in_activity_list = True
						# Set the maximum of the span to check as the end of the
						# from_date
						maximum = unformat_time((59, 59, 23, from_date[0],
													from_date[1], from_date[2]))
						# If the log did not happen on the from date 
						if not (time_in_span(log_start, log_end, 
												minimum, maximum) == 0):
							# add the log's time in the span to the activity's
							# start trend time.
							entry[1] += time_in_span(log_start, log_end, 
														minimum, maximum)
						else:
							# Else add it the activity's end trend time
							entry[2] += log_time
				# If the log is not already in the activity list, add it.
				if not in_activity_list:
					activity_list.append([activity, log_time, 0])
		# Make a list of the activities and their respective trends
		trends_list = []
		# Iterate through the activity list
		for entry in activity_list:
			# If the end trend time of the activity exists (I.E. not zero)
			if not entry[2] == 0:
				# Get the trend and convert it to a string with a percent symbol
				percent_change = (((entry[2] - entry[1])*1.00)/(entry[1]*1.00))
				percent_change = str((ceil(percent_change*10000.00))/100.00)
				if percent_change[-2] == '.':
					percent_change += '0'
				percent_change += '%'
				trends_list.append([entry[0], str(percent_change)])
		# Set data as trends
		self.data = trends_list

	def load_into_treeview_window(self):
		"""Load the treeviews data into the treestore widget"""
		for trend in self.data:
			# Get which pixbuf we will be using based on whether or not the
			# trend is positive.
			if float(trend[1][:-1]) > 0:
				pixbuf = self.up_pixbuf
			elif float(trend[1][:-1]) < 0:
				pixbuf = self.down_pixbuf
				trend[1] = trend[1][1:]
			else:
				pixbuf = self.same_pixbuf
			# append the data to the treestore
			self.treestore.append(None, (trend[0], pixbuf, trend[1]))

	def set_visible(self, visible=True):
		"""Used to make loading animation work correctly, need to remove"""
		self.treeview_window.set_visible(visible)
		self.visible = visible

	def clear(self):
		"""Clears the TrendView"""
		self.data = []
		self.treestore.clear()