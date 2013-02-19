#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
from pygal import *
from pygal.style import *
from gi.repository import Gdk, GdkPixbuf
import os
import operator

import math

class PieGrapher:
	def __init__(self, image_widget, 
					container_widget, liststore_widget, 
					chart_path, color_dir, 
					CONST_WIDTH=None, CONST_HEIGHT=None):
		self.image_widget = image_widget
		self.container_widget = container_widget
		self.liststore_widget = liststore_widget
		self.chart_path = chart_path
		self.color_dir = color_dir
		self.CONST_WIDTH = CONST_WIDTH
		self.CONST_HEIGHT = CONST_HEIGHT
		# Set the default liststore mode
		self.liststore_mode = 'percent'
		# The list of activities to be put in the pie graph.
		self.pie_list = []
		# The list of activities from the previous pie graph.
		#self.previous_pie_list = []
		# Set the list of colors for pie slices.
		self.color_list = ['#EF2929', '#729FCF', '#AD7FA8', '#8AE234', 
							'#FCAF3E', '#A40000', '#204A87', 
							'#5C3566', '#4E9A06', '#CE5C00', '#2E3436', '#D3D7CF']
		# Create the list of colors to be sorted at a later time.
		self.sorted_color_list = [None, None, None, None, None, None, 
									None, None, None, None, None, None] 
		self.sort_color_list()
		# The custom pygal style used for the pie graph.
		self.custom_style = Style(background='#F7F6F6', 
									plot_background='#F7F6F6', 
									foreground='#F7F6F6', 
									foreground_light='#53A0E8', 
									foreground_dark='#630C0D',
	  								colors=(self.sorted_color_list))
		# Setup the global width and height of the graph's SVG image.
		self.width = 0
		self.height = 0
		# The custom pygal chart for the pie graph.
		self.pie_chart = Pie(style=self.custom_style, 
								show_legend=False, 
								label_font_size=1, 
								value_font_size=1, 
								no_data_text=" ", 
								stroke=False,
								print_values=False, 
								disable_xml_declaration=True)

	def add_entry(self, label, value, color):
		"""Add an entry to the pie_list and give it a color"""
		# Add the activity with it's initial color
		if color == None:
			color = 11
		else:
			while color >= len(self.color_list)-1:
				color -= len(self.color_list)-1
		self.pie_list.append([label, value, color])

	def remove_entry(self, label, value, color):
		"""Remove an entry from the pie_list"""
		self.pie_list.remove([label, value, color])	

	def clear(self):
		"""Reset the pie chart and remove entries"""
		#
		# Iterate through pie_list and append all entries to previous_pie_list
		#for entry in self.pie_list:
		#	self.previous_pie_list.append(entry[0])
		#
		# Clear the pie_list and liststore_widget
		self.pie_list = []
		self.liststore_widget.clear()
		# Reset the pie chart to it's initial state
		self.pie_chart = Pie(style=self.custom_style, show_legend=False, 
								label_font_size=1, value_font_size=1, 
								no_data_text=" ", stroke=False,
								print_values=False, width=self.width, 
								height=self.height)
		# Delete the previous pie chart SVG file if it exists
		if os.path.exists(self.chart_path):
			os.remove(self.chart_path)

	def update_size(self, width=None, height=None):
		"""Resizes the pie graph and loads it into the image_widget"""
		# Set the width of the pie graph based on the size of it's container.
		self.width = (self.container_widget.get_size()[0] - 430)
		self.width -= int(self.width/10) 
		# If the pie graph is not wide enough
		if self.width < 250:
			# Correct it to be atleast 250px wide.
			self.width = 250
		# Set the height of the pie graph based on the size of it's container.
		self.height = (self.container_widget.get_size()[1] - 235)
		self.height -= int(self.height/10) 
		# If the pie graph is not tall enough
		if self.height < 250:
			# Correct it to be atleast 250px high.
			self.height = 250
		# Set height and width equal to the smalles of the two to make the pie
		# graph square in proportions.
		if self.height < self.width:
			self.width = self.height
		else:
			self.height = self.width
		# If width and height were specified in the function call
		if not width == None and not height == None:
			# Set the pie graph's height and width equal to the dimensions 
			# specified.
			self.width = width
			self.height = height
		# Reset the pie graph's appereance, but not dimensions.
		self.pie_chart = Pie(style=self.custom_style, show_legend=False, 
								label_font_size=1, value_font_size=1, 
								no_data_text=" ", stroke=False,
								print_values=False, width=self.width, 
								height=self.height)
		# Clear the liststore widget.
		self.liststore_widget.clear()
		# Load the pie graph into the image widget.
		self.load_into_image()

	def sort_data(self, initial_sort=False):
		"""Sort the data in the pie graph"""
		self.pie_list = self.data_by_size(self.pie_list)
		self.sort_color_list()

	def data_by_size(self, data):
		"""Used to sort the pie slices by time from largest to smallest."""
		# Make a duplicate of the data so it does not get tampered with
		sorted_data = data
		# Sort from smallest to largest based on time.
		sorted_data.sort(key=operator.itemgetter(1))
		# Then reverse and return the list.
		return sorted_data[::-1]

	def sort_color_list(self):
		"""Used to make the order of the color_list match the order pf the 
			pie_list's activity colors"""
		for index in xrange (0, len(self.pie_list)):
			color = self.pie_list[index][2]
			self.sorted_color_list[index] = self.color_list[color]

	def send_to_svg(self):
		"""Send the prepared pie graph to an SVG file"""
		total_time = 0
		for entry in self.pie_list:
			total_time += entry[1]
		# Iterate through the pie_list sorted by color.
		for entry in self.pie_list:
			# Add the entries in the pie list to the pie_chart.
			self.pie_chart.add(entry[0], entry[1])
			# Color path points to PNG file containing a swatch of the
			# activity's color.
			color = entry[2]
			color_path = self.color_dir + str(color) + ".png"
			# Create a new 16px by 16px pixbuf for the activity's color swatch
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(color_path, 16, 16)
			# Add the activity with it's color swatch to the liststore_widget
			# 
			#
			# NEED TO SLIM THIS DOWN AND OFFLOAD TO TIMEFORMAT AND LISTSTOREFORMAT
			if self.liststore_mode == 'percent': 
				percent = round(((float(entry[1])/float(total_time))*100), 1)
				if percent == 100:
					percent = ''
				else:
					percent = str(percent) + '%'
				value = percent
			elif self.liststore_mode == 'time':
				hours = int(math.floor(entry[1] / 3600))
				minutes = int(math.floor((entry[1] / 60) - hours*60))
				seconds = int(math.floor(((entry[1] - minutes*60) - hours*3600)))
				if hours < 10:
					hours = '0' + str(hours)
				else:
					hours = str(hours)
				if minutes < 10:
					minutes = '0' + str(minutes)
				else:
					minutes = str(minutes)
				if seconds < 10:
					seconds = '0' + str(seconds)
				else:
					seconds = str(seconds)
				value = str(hours) + ":" + str(minutes) + ":" + str(seconds)
			else:
				value = ''
			self.liststore_widget.append([pixbuf, entry[0], value])
			# Increment on to the next color
			color += 1
		# Render the pie chart to an SVG file
		self.pie_chart.render_to_file(self.chart_path)

	def load_into_image(self, width=None, height=None):
		"""Load the SVG file for the pie graph into the image widget"""
		# Create the SVG file.
		self.send_to_svg()
		# If dimensions are not specified by the CONST_HEIGHT and CONST_WIDTH
		if (not width == None and not height == None 
			and self.CONST_WIDTH == None and self.CONST_HEIGHT == None):
			# Create a pixbuf of specified dimensions from the svg file
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(CONST_CHART_PATH, 
															width, height)
			# Crop the extra space off of the pie graph
			cropped_pixbuf = pixbuf.new_subpixbuf(25, 0, width-50, height)
		# Else if dimensions are specified by the function call
		elif not self.CONST_WIDTH == None and not self.CONST_HEIGHT == None:
			# Create a pixbuf of CONSTANT dimensions from the svg file
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(self.chart_path,
															self.CONST_WIDTH,
															self.CONST_HEIGHT)
			# Crop the extra space off of the pie graph
			cropped_pixbuf = pixbuf.new_subpixbuf(25, 0, self.CONST_WIDTH-50,
													self.CONST_HEIGHT)
		# Else no dimenstions are specified
		else:
			# Create a pixbuf with no specific dimensions
			pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.chart_path)
			# Crop the extra space off the pie_graph
			height = pixbuf.get_height()
			width = pixbuf.get_width()
			cropped_pixbuf = pixbuf.new_subpixbuf(25, 0, width-50, height)
		# Set the cropped_pixbuf in the image_widget
		self.image_widget.set_from_pixbuf(cropped_pixbuf)