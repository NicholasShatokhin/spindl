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
from locale import gettext as _
from gi.repository import Gtk, WebKit# pylint: disable=E0611
from gi.repository import Gdk
import pango
import logging
import os
logger = logging.getLogger('spindl')
from spindl_lib.filer import Filer
from spindl_lib.timer import Timer
from spindl_lib.charter import Charter
from spindl_lib.unityIndicator import Indicator
from spindl_lib.toolbarFormat import *
from spindl_lib.comboboxFormat import *
from spindl_lib.timeFormat import *
from spindl_lib.treeviewFormat import *
from spindl_lib.entryFormat import *
from spindl_lib.menuFormat import *
from spindl_lib import Window
from spindl.AboutSpindlDialog import AboutSpindlDialog
from spindl.PreferencesSpindlDialog import PreferencesSpindlDialog

# Make sure the ./spindl directory exists. If not, create it.
user_home = os.getenv('HOME')
spindl_directory = user_home + '/.spindl/'
if not os.path.isdir(spindl_directory):
    os.makedirs(spindl_directory)
# Location of the activity database
CONST_DB_FILE_PATH = spindl_directory + 'spindl.db'
CONST_CHART_PATH = spindl_directory + 'chart.svg'

# See spindl_lib.Window.py for more details about how this class works
class SpindlWindow(Window):
    __gtype_name__ = "SpindlWindow"
    
    def finish_initializing(self, builder): 
        """Set up the main window"""
        print CONST_DB_FILE_PATH
        super(SpindlWindow, self).finish_initializing(builder)
        self.AboutDialog = AboutSpindlDialog
        self.PreferencesDialog = PreferencesSpindlDialog
        # Code for initialization of gtk objects to be used.
        # Initialize the main window componenets.
        self.spindl_window = self.builder.get_object("spindl_window")
        self.timer_box = self.builder.get_object("timer_box")
        self.current_activity_label = self.builder.get_object("current_activity_label") 
        self.timer_label = self.builder.get_object("timer_label")   
        self.timer_button_box = self.builder.get_object("timer_button_box")
        self.timer_start_button = self.builder.get_object("timer_start_button")
        self.timer_pause_button = self.builder.get_object("timer_pause_button")
        self.activity_entry = self.builder.get_object("activity_entry")
        self.total_treeview = self.builder.get_object("total_treeview")
        self.log_treeview = self.builder.get_object("log_treeview")   
        self.total_treestore = self.builder.get_object("total_treestore")
        self.log_treestore = self.builder.get_object("log_treestore")
        self.total_treeview_right_click_menu = self.builder.get_object("total_treeview_right_click_menu")
        self.log_treeview_right_click_menu = self.builder.get_object("log_treeview_right_click_menu")
        self.timer_toolbar = self.builder.get_object("timer_toolbar")
        self.entrycompletion1 = self.builder.get_object("entrycompletion1")
        # Initialize the total_treeview and its subwidgets.
        self.total_activity_column = self.builder.get_object("total_activity_column")        
        self.total_activity_column_header_label = self.builder.get_object("total_activity_column_header_label")
        self.total_activity_column_child_text = self.builder.get_object("total_activity_column_child_text")
        self.time_today_column = self.builder.get_object("time_today_column")        
        self.time_today_column_header_label = self.builder.get_object("time_today_column_header_label")
        self.time_today_column_child_text = self.builder.get_object("time_today_column_child_text")
        self.time_total_column = self.builder.get_object("time_total_column")        
        self.time_total_column_header_label = self.builder.get_object("time_total_column_header_label")
        self.time_total_column_child_text = self.builder.get_object("time_total_column_child_text")
        # Initialize the log_treeview and its subwidgets.
        self.log_activity_column = self.builder.get_object("log_activity_column") 
        self.log_activity_column_header_label = self.builder.get_object("log_activity_column_header_label")       
        self.log_activity_column_child_text = self.builder.get_object("log_activity_column_child_text")
        self.start_time_column = self.builder.get_object("start_time_column")        
        self.start_time_column_header_label = self.builder.get_object("start_time_column_header_label")
        self.start_time_column_child_text = self.builder.get_object("start_time_column_child_text")
        self.stop_time_column = self.builder.get_object("stop_time_column")        
        self.stop_time_column_header_label = self.builder.get_object("stop_time_column_header_label")
        self.stop_time_column_child_text = self.builder.get_object("stop_time_column_child_text")
        # Initialize widgets in the Analytics tab
        # Initialize the color_liststore and the color_treeview 
        self.color_liststore = self.builder.get_object("color_liststore")
        self.color_column = self.builder.get_object("color_column")        
        self.color_column_child_pixbuf = self.builder.get_object("color_column_child_pixbuf")
        self.value_column_child_text = self.builder.get_object("value_column_child_text")
        self.activity_column_child_text = self.builder.get_object("activity_column_child_text")


        self.webview_scrolledwindow = self.builder.get_object("webview_scrolledwindow")
        self.webview = WebKit.WebView()
        self.webview_scrolledwindow.add(self.webview)
        self.webview.show()

        # Initialize the GtkBoxes that contain the date entries for analytics.
        self.analytics_day_box = self.builder.get_object("analytics_day_box")
        self.analytics_month_box = self.builder.get_object("analytics_month_box")
        self.analytics_from_box = self.builder.get_object("analytics_from_box")
        self.analytics_to_box = self.builder.get_object("analytics_to_box")
        self.analytics_for_box = self.builder.get_object("analytics_for_box")
        self.analytics_radio_box = self.builder.get_object("analytics_radio_box")
        # Initialize all of the date entries and plus/minus buttons 
        # for analytics
        self.show_combobox = self.builder.get_object("show_combobox")
        self.show_combobox_text = self.builder.get_object("show_combobox_text")
        self.for_combobox = self.builder.get_object("for_combobox") 
        self.for_combobox_text = self.builder.get_object("for_combobox_text")
        self.day_entry = self.builder.get_object("day_entry")
        self.month_entry = self.builder.get_object("month_entry")
        self.from_entry = self.builder.get_object("from_entry")
        self.to_entry = self.builder.get_object("to_entry")
        self.percentages_radiobutton = self.builder.get_object("percentages_radiobutton")
        self.time_radiobutton = self.builder.get_object("time_radiobutton")
        self.minus_day_button = self.builder.get_object("minus_day_button")
        self.minus_month_button = self.builder.get_object("minus_month_button")
        self.minus_from_button = self.builder.get_object("minus_from_button")
        self.minus_to_button = self.builder.get_object("minus_to_button")
        self.plus_day_button = self.builder.get_object("plus_day_button")
        self.plus_month_button = self.builder.get_object("plus_month_button")
        self.plus_from_button = self.builder.get_object("plus_from_button")
        self.plus_to_button = self.builder.get_object("plus_to_button")
        self.day_entry = self.builder.get_object("day_entry")
        self.month_entry = self.builder.get_object("month_entry")
        self.from_entry = self.builder.get_object("from_entry")
        self.to_entry = self.builder.get_object("to_entry")
        # Initialize the Set Activity Window and its components
        self.set_activity_window = self.builder.get_object("set_activity_window")
        self.set_activity_box = self.builder.get_object("set_activity_box")
        self.set_activity_entry = self.builder.get_object("set_activity_entry")
        self.set_activity_toolbar = self.builder.get_object("set_activity_toolbar")
        self.entrycompletion2 = self.builder.get_object("entrycompletion2")
        # Initialize the widgets used in the indicator and indicator menu.
        self.indicator_menu = self.builder.get_object("indicator_menu")
        self.current_activity_indicator = self.builder.get_object("current_activity_indicator")
        self.alternative_new_activity_indicator = self.builder.get_object("alternative_new_activity_indicator")
        self.set_activity_indicator = self.builder.get_object("set_activity_indicator")
        self.activity_menuitem1 = self.builder.get_object("activity_menuitem1")
        self.activity_menuitem2 = self.builder.get_object("activity_menuitem2")
        self.activity_menuitem3 = self.builder.get_object("activity_menuitem3")
        self.activity_menuitem4 = self.builder.get_object("activity_menuitem4")
        self.activity_menuitem5 = self.builder.get_object("activity_menuitem5")
        self.timer_indicator = self.builder.get_object("timer_indicator")
        self.start_timer_indicator = self.builder.get_object("start_timer_indicator")
        self.pause_timer_indicator = self.builder.get_object("pause_timer_indicator")
        self.indicator_set_activity = self.builder.get_object("indicator_set_activity")
        self.hide_window_indicator = self.builder.get_object("hide_window_indicator")
        self.quit_indicator = self.builder.get_object("quit_indicator")
        # Formatting for various widgets that could not otherwise be performed 
        # in Glade3
        # Formatting for the timer_toolbar
        format_toolbar(self.timer_toolbar)
        add_toolitem(self.timer_box, self.timer_toolbar, 0, set_expand=True)
        add_toolitem(self.timer_button_box, self.timer_toolbar, 1)
        # Set the activity and timer indicator to unsensitive so it cannot be
        # interacted with.
        self.current_activity_indicator.set_sensitive(False)
        self.timer_indicator.set_sensitive(False)
        # Connect the window's delete event to it's hide event so it is not 
        # destroyed upon being closed.
        self.set_activity_window.connect('delete-event', 
                                            self.on_set_activity_window_hide)
        # Format for the Set Activity toolbar
        format_toolbar(self.set_activity_toolbar)
        # Add the set activity box to a toolitem and add that toolitem to the
        # set activity toolbar.
        add_toolitem(self.set_activity_box, 
                        self.set_activity_toolbar, 
                        0, set_expand=True)
        # Activity column on total_treeview's formatting   
        format_column(self.total_activity_column, 
                        self.total_activity_column_header_label, 
                        self.total_activity_column_child_text)
        # Time today column on total_treeview's formatting       
        format_column(self.time_today_column, 
                        self.time_today_column_header_label, 
                        self.time_today_column_child_text)
        # Total time column on total_treeview's formatting   
        format_column(self.time_total_column, 
                        self.time_total_column_header_label, 
                        self.time_total_column_child_text)
        # Activity column on log_treeview's formatting   
        format_column(self.log_activity_column, 
                        self.log_activity_column_header_label, 
                        self.log_activity_column_child_text)
        # Start time column on log_treeview's formatting   
        format_column(self.start_time_column, 
                        self.start_time_column_header_label, 
                        self.start_time_column_child_text, 
                        ellipsize=False)
        # Stop time column on log_treeview's formatting.
        format_column(self.stop_time_column, 
                        self.stop_time_column_header_label, 
                        self.stop_time_column_child_text, 
                        ellipsize=False)
        format_combobox_text(self.show_combobox_text)
        format_combobox_text(self.for_combobox_text)
        # Set the "Show Percentages" and "Show Time" radiobutton's labels
        self.percentages_radiobutton.modify_fg(0,Gdk.Color(34952, 35466, 34181))
        self.time_radiobutton.modify_fg(0,Gdk.Color(34952, 35466, 34181))
        # Set the analytics boxes to invisible until told otherwise
        self.analytics_day_box.set_visible(False)
        self.analytics_month_box.set_visible(False)
        self.analytics_from_box.set_visible(False)
        self.analytics_to_box.set_visible(False)
        self.analytics_for_box.set_visible(False)
        self.analytics_radio_box.set_visible(False)
        # Set the initial values for day/month/from/to values. These are used
        # to determine what time period the graph should be drawn to. They
        # begin at 0 for current day and go backwards (negative) in time.
        self.day_value = 0
        self.month_value = 0
        self.from_value = 0
        self.to_value = 0
        # Set the activity text to its default value
        self.current_activity_text = "No Activity"
        # Initialize the timer, filer, pieGrapher, and indicator objects
        self.timer = Timer(self.timer_label, self.timer_indicator) 
        self.filer = Filer(CONST_DB_FILE_PATH)
        self.charter = Charter('ubuntu', CONST_CHART_PATH, self.webview)
        # Set the data
        self.charter.data = []#('Activity', 100, 0), ('Things', 25, 1), ('Stuff', 25, 2), ('Cool', 10, 3)]
        # Create the chart of type pie
        self.charter.create_chart('pie')
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview(initial=True)
        self.indicator = Indicator(self.indicator_menu, 
                                    self.current_activity_indicator,
                                    self.timer_indicator, 
                                    self.start_timer_indicator,
                                    self.pause_timer_indicator, 
                                    self.hide_window_indicator,
                                    self.quit_indicator)
        # Load the previous logs from the database
        for entry in self.filer.read_log("*"):
            self.log_treestore.prepend(None, (entry[0], entry[1], entry[2]))
        # Load the previous totals from the database
        self.timer.update_current_date()
        for entry in self.filer.read_total(self.timer.current_date):
            self.total_treestore.prepend(None, 
                                        (entry[0], 
                                        self.timer.format_timer(entry[1]), 
                                        self.timer.format_timer(entry[2])))
        self.charter.data = []
        # Create the chart of type pie
        self.charter.create_chart('pie')
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        # format all of the date entry widgets
        format_entry_as_date(self.timer.current_date, 
                                self.day_entry, self.day_value)
        format_entry_as_date(self.timer.current_date, 
                                self.month_entry, 
                                self.month_value, 
                                show_days=False)
        format_entry_as_date(self.timer.current_date, 
                                self.from_entry, 
                                self.from_value)
        format_entry_as_date(self.timer.current_date, 
                                self.to_entry, 
                                self.to_value)
        # Set the set_activity_menu_list to the items in the set_activity_menu
        self.set_activity_menu_list = [self.activity_menuitem1, 
                                        self.activity_menuitem2,
                                        self.activity_menuitem3, 
                                        self.activity_menuitem4,
                                        self.activity_menuitem5]
        # format the set_activity_menu based on the activitties in the totals
        format_menu_from_totals(self.filer.read_total(self.timer.current_date), 
                                self.set_activity_menu_list,
                                self.set_activity_indicator, 
                                self.alternative_new_activity_indicator)

    def start_time(self):
        """Starts the timer"""
        # Start the timer
        self.timer.start()

    def stop_time(self):
        """Stops the timer"""
        # Check if the timer was paused before stopping.
        if self.timer.is_running:
            was_paused = False
        else:
            was_paused = True
        # Stop the timer and set the activity's stop time.
        self.timer.stop()
        # If the timer was not paused before stopping
        if not was_paused:
            # Format the start date and time so they are ready to write to file.
            start_time = self.timer.start_times[-1]
            start_date = format_date(self.timer.start_times[-1])
            # Format the stop date and time so they are ready to write to file.
            stop_time = self.timer.stop_times[-1]
            stop_date = format_date(self.timer.stop_times[-1])
            # Append and join a list of strings to form a formatted start time. 
            start_time_list = []
            start_time_list.append(start_date)
            start_time_list.append("    ")
            start_time_list.append(str(start_time)[-15:])
            formatted_start_time =  "".join(start_time_list)
            # Append and join a list of strings to form a formatted start time. 
            stop_time_list = []
            stop_time_list.append(stop_date)
            stop_time_list.append("    ")
            stop_time_list.append(str(stop_time)[-15:])
            formatted_stop_time = "".join(stop_time_list)
            # Write the activity text, start time, and stop time to the log
            # table in the database
            self.filer.write_log((self.current_activity_text, 
                                    formatted_start_time, 
                                    formatted_stop_time))
        # Clear the treestores and graph
        self.filer.compound_logs()
        self.log_treestore.clear()
        self.total_treestore.clear()
        self.charter.clear()
        # Reload the information in the log treestore
        for entry in self.filer.read_log("*"):
            self.log_treestore.prepend(None, (entry[0], entry[1], entry[2]))
        # Reload the information in the total treestore
        self.timer.update_current_date()
        for entry in self.filer.read_total(self.timer.current_date):
            self.total_treestore.prepend(None, 
                                        (entry[0], 
                                        self.timer.format_timer(entry[1]), 
                                        self.timer.format_timer(entry[2])))
        self.charter.data = self.filer.read_total(self.timer.current_date)
        # Create the chart of type pie
        self.charter.create_chart()
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        #### CUT AND SPLICE HERE
        model = self.for_combobox.get_model()
        index = self.for_combobox.get_active()
        active_item = model[index][0]
        # Update the current date
        self.timer.update_current_date()
        if active_item == 'All Time':
            # Refresh the graph to reflect the totals
            self.refresh_totals_graph()
        elif active_item == 'Day':
            # Format the day entry as a date
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                self.day_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_day_graph()
        elif active_item == 'Month':
            # Format the month entry as a date
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                self.month_value, show_days=False)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_month_graph()
        elif active_item == 'Span of Time':
            # Format the span entries as a date
            format_entry_as_date(self.timer.current_date, self.from_entry, self.from_value)
            format_entry_as_date(self.timer.current_date, self.to_entry, self.to_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_span_graph()
        ####
        # Load the new activity information into the set_activity_menu
        format_menu_from_totals(self.filer.read_total(self.timer.current_date), 
                                self.set_activity_menu_list,
                                self.set_activity_indicator, 
                                self.alternative_new_activity_indicator)
        # Reset the current activity
        self.current_activity_text = 'No Activity'
        # Clear the timer
        self.timer.clear()
        
    def pause_time(self):
        """Pauses the timer"""
        # Pause the timer and record the time in the current activity
        self.timer.stop()         
        # Set the start time to either the activity's start time or its resume 
        # time, whichever is more recent
        start_time = str(self.timer.start_times[-1])[-15:]
        start_date = format_date(self.timer.start_times[-1])
        pause_time = str(self.timer.stop_times[-1])[-15:]
        pause_date = format_date(self.timer.stop_times[-1])
        # Append and join a list of strings to form a formatted start time.
        start_time_list = []
        start_time_list.append(start_date)
        start_time_list.append("    ")
        start_time_list.append(start_time)
        formatted_start_time =  "".join(start_time_list)
        # Append and join a list of strings to form a formatted pause time.
        pause_time_list = []
        pause_time_list.append(pause_date)
        pause_time_list.append("    ")
        pause_time_list.append(pause_time)
        formatted_pause_time = "".join(pause_time_list)
        # Write the activity text, start time, and stop time to the log table
        # in the database
        self.filer.write_log((self.current_activity_text, formatted_start_time, 
                                formatted_pause_time))
        # Remove any dupliactes from the database
        self.filer.compound_logs() 
        # Clear the treestores and graph
        self.log_treestore.clear()
        self.total_treestore.clear()
        self.charter.clear()
        # Reload the information in the log treestore
        for entry in self.filer.read_log("*"):
            self.log_treestore.prepend(None, (entry[0], entry[1], entry[2]))
         # Reload the information in the total treestore
        self.timer.update_current_date()
        for entry in self.filer.read_total(self.timer.current_date):
            self.total_treestore.prepend(None, 
                                        (entry[0], 
                                        self.timer.format_timer(entry[1]), 
                                        self.timer.format_timer(entry[2])))
        self.charter.data = self.filer.read_total(self.timer.current_date)
        # Create the chart of type pie
        self.charter.create_chart()
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        #### CUT AND SPLICE HERE
        model = self.for_combobox.get_model()
        index = self.for_combobox.get_active()
        active_item = model[index][0]
        # Update the current date
        self.timer.update_current_date()
        if active_item == 'All Time':
            # Refresh the graph to reflect the totals
            self.refresh_totals_graph()
        elif active_item == 'Day':
            # Format the day entry as a date
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                self.day_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_day_graph()
        elif active_item == 'Month':
            # Format the month entry as a date
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                self.month_value, show_days=False)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_month_graph()
        elif active_item == 'Span of Time':
            # Format the span entries as a date
            format_entry_as_date(self.timer.current_date, self.from_entry, self.from_value)
            format_entry_as_date(self.timer.current_date, self.to_entry, self.to_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_span_graph()
        ####
        # Load the new activity information into the set_activity_menu
        format_menu_from_totals(self.filer.read_total(self.timer.current_date), 
                                self.set_activity_menu_list,
                                self.set_activity_indicator, 
                                self.alternative_new_activity_indicator)

    def resume_time(self):
        """Resumes the timer from a pause"""
        self.timer.start() 

    def set_current_activity(self, activity_text, keep_running=False):
        """Adds an activity object to the database and sets to current"""
        # Stop the current activity if it is running.
	    if self.timer.is_running and not keep_running:
		    self.stop_time()
            # Make sure the start and pause buttons are set to their defaults
            self.timer_start_button.set_active(False)
            self.timer_pause_button.set_active(False)
        # If the entry has a valid activity            
        if (not activity_text.isspace() and not (activity_text == "No Activity")
            and not (activity_text == None) and not (activity_text == "")):
            # Format the entry's text by capitalizing the first letter and 
            # putting the rest in lower-case.
            formatted_activity_text = (activity_text[0].upper() + 
                                        activity_text[1:].lower())
            # Set the current activity's text to the formatted text 
            self.current_activity_text = formatted_activity_text               
            self.current_activity_label.set_text(formatted_activity_text)  
            self.current_activity_indicator.set_label(formatted_activity_text)
        # Clear the activity entry
        self.activity_entry.set_text("")
        # If the indicator exists
        if not self.activity_entry == None:
            # Clear it as well
            self.set_activity_entry.set_text("")

    def refresh_totals_graph(self):
        """Called when the user selects 'Totals' show combobox"""
        # Clear the pieGraph
        self.charter.clear()
        # Update the current date in the timer
        self.timer.update_current_date()
        # Set the chart data to reflect the current data
        #self.charter.data = self.filer.read_total(self.timer.current_date)
        self.charter.data = self.filer.read_log('*')
        # Create the chart of type pie
        self.charter.create_chart()
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        # Set the proper entry box as visible 
        self.analytics_day_box.set_visible(False)
        self.analytics_month_box.set_visible(False)
        self.analytics_from_box.set_visible(False)
        self.analytics_to_box.set_visible(False)
        self.analytics_radio_box.set_visible(True)

    def refresh_day_graph(self):
        """Called to get the date from the day_entry and redraw the graph to 
            reflect that date"""
        # Initialize the totals for the day selected
        day_totals = []
        #self.pieGrapher.clear()
        self.charter.clear()
        # Refresh all entries in the Pie Graph from the database
        for entry in self.filer.read_log("*"): 
            # Get the activity
            activity = entry[0]
            # Get the color
            color = entry[3]
            # Get the month and day selected in entries
            month = self.day_entry.get_text()[0:2]
            if month[1] == '/':
                month = month[0]
                day = self.day_entry.get_text()[2:4]
                if day[1] == '/':
                    day = day[0]
            else:
                day = self.day_entry.get_text()[3:5]
                if day[1] == '/':
                        day = day[0]
            # Get the year selected in the entry
            year = self.day_entry.get_text()[-4:]
            # Get the start time of the log entry
            start_time = unformat_time(tuple_time(entry[1]))
            # Get the stop time of the log entry
            stop_time = unformat_time(tuple_time(entry[2]))
            # Get the minimum and maximum allowed times from the entries
            minimum = unformat_time((0, 0, 0, day, month, year))
            maximum = unformat_time((59, 59, 23, day, month, year))
            # Get the total_time the log entry coincides with the allowed 
            # minimum and maximum values from the entries
            total_time = time_in_span(start_time, stop_time, minimum, maximum)
            # If time in the log coincides with the span in the entry
            if not total_time == 0:
                # By default, the log entry is a new activity
                is_new_activity = True
                # Iterate through the day_totals if entries exist
                for total in day_totals:
                    # If the entry in day_totals has the same activity as the 
                    # log entry.
                    if total[0] == entry[0]:
                        # Update the total_time in the day_total to include the
                        # time from the log entry.
                        updated_total = (entry[0], total[1]+total_time, color)
                        day_totals[day_totals.index(total)] = updated_total
                        # The activity exists in the logs and is not new
                        is_new_activity = False
                # If the entry is a new activity
                if is_new_activity:
                    # Append it to the day_totals
                    day_totals.append((activity, total_time, color))
        # Set the data in the chart equal to the day's total times
        self.charter.data = day_totals
        # Create the chart of type pie
        self.charter.create_chart()
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        # Set the proper time selection boxes as visible
        self.analytics_day_box.set_visible(True)
        self.analytics_month_box.set_visible(False)
        self.analytics_from_box.set_visible(False)
        self.analytics_to_box.set_visible(False)
        self.analytics_radio_box.set_visible(True)

    def refresh_month_graph(self):
        """Called to get the date from the month_entry and redraw the graph to 
            reflect that date"""
        # Initialize the totals for the month selected
        month_totals = []
        self.charter.clear()
        # Refresh all entries in the Pie Graph from the database
        for entry in self.filer.read_log("*"):
            # Get the activity
            activity = entry[0]
            # Get the color
            color = entry[3]
            # Get the month selected in entry
            month = self.month_entry.get_text()[0:2]
            if month[1] == '/':
                month = month[0]
            # Get the year selected in the entry
            year = self.month_entry.get_text()[-4:]
            # Get the start time of the log entry
            start_time = unformat_time(tuple_time(entry[1]))
            # Get the stop time of the log entry
            stop_time = unformat_time(tuple_time(entry[2]))
            # Get the minimum and maximum allowed times from the entries
            minimum = unformat_time((0, 0, 0, 0, month, year))
            maximum = unformat_time((59, 59, 23, None, month, year))
            # Get the total_time the log entry coincides with the allowed 
            # minimum and maximum values from the entries
            total_time = time_in_span(start_time, stop_time, minimum, maximum)
            # If time in the log coincides with the span in the entry
            if (int(month) == tuple_time(entry[1])[4] 
                and int(year) == tuple_time(entry[1])[5]):
                is_new_activity = True
                for total in month_totals:
                    # If the entry in month_totals has the same activity as the 
                    # log entry.
                    if total[0] == entry[0]:
                        # Update the total_time in the month_total to include the
                        # time from the log entry.
                        updated_total = (entry[0], total[1]+total_time, color)
                        month_totals[month_totals.index(total)] = updated_total
                        # The activity exists in the logs and is not new
                        is_new_activity = False
                # If the entry is a new activity
                if is_new_activity:
                    # Append it to the month_totals
                    month_totals.append((activity, total_time, color))
        # Set the data in the chart equal to the month's total times
        self.charter.data = month_totals
        # Create the chart of type pie
        self.charter.create_chart()
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        # Set the proper time selection boxes as visible
        self.analytics_day_box.set_visible(False)
        self.analytics_month_box.set_visible(True)
        self.analytics_from_box.set_visible(False)
        self.analytics_to_box.set_visible(False)
        self.analytics_radio_box.set_visible(True)

    def refresh_span_graph(self):
        """Called to get the date from the span_entry and redraw the graph to 
        reflect that date"""
        span_totals = []
        self.charter.clear()
        # Refresh all entries in the Pie Graph from the database
        for entry in self.filer.read_log("*"):
            # Get the activity
            activity = entry[0]
            # Get the color
            color = entry[3]
            # Get the month and day selected in the from entry
            from_month = self.from_entry.get_text()[0:2]
            if from_month[1] == '/':
                from_month = from_month[0]
                from_day = self.from_entry.get_text()[2:4]
                if from_day[1] == '/':
                    from_day = from_day[0]
            else:
                from_day = self.from_entry.get_text()[3:5]
                if from_day[1] == '/':
                        from_day = from_day[0]
            # Get the year selected in the from entry
            from_year = self.from_entry.get_text()[-4:]
            # Get the month and day selected in the to entry
            to_month = self.to_entry.get_text()[0:2]
            if to_month[1] == '/':
                to_month = to_month[0]
                to_day = self.to_entry.get_text()[2:4]
                if to_day[1] == '/':
                    to_day = to_day[0]
            else:
                to_day = self.to_entry.get_text()[3:5]
                if to_day[1] == '/':
                        to_day = to_day[0]
            # Get the year selected in the to entry
            to_year = self.to_entry.get_text()[-4:]
            # Get the start time of the log entry
            start_time = unformat_time(tuple_time(entry[1]))
            # Get the stop time of the log entry
            stop_time = unformat_time(tuple_time(entry[2]))
            # Get the minimum and maximum allowed times from the entries
            minimum = unformat_time((0, 0, 0, from_day, from_month, from_year))
            maximum = unformat_time((59, 59, 23, to_day, to_month, to_year))
            # Get the total_time the log entry coincides with the allowed 
            # minimum and maximum values from the entries
            total_time = time_in_span(start_time, stop_time, minimum, maximum)
            # If time in the log coincides with the span in the entry
            if not total_time == 0:
                is_new_activity = True
                for total in span_totals:
                    # If the entry in month_totals has the same activity as the 
                    # log entry.
                    if total[0] == entry[0]:
                        updated_total = (entry[0], total[1]+total_time, color)
                        span_totals[span_totals.index(total)] = updated_total
                        is_new_activity = False
                # If the entry is a new activity
                if is_new_activity:
                    # Append it to the span_totals
                    span_totals.append((activity, total_time, color))
        # Set the data in the chart equal to the span's total times
        self.charter.data = span_totals
        # Create the chart of type pie
        self.charter.create_chart()
        # Compound data
        self.charter.compound_other_data()
        # Load the chart into the webview
        self.charter.load_into_webview()
        # Set the proper time selection boxes as visible
        self.analytics_day_box.set_visible(False)
        self.analytics_month_box.set_visible(False)
        self.analytics_from_box.set_visible(True)
        self.analytics_to_box.set_visible(True)
        self.analytics_radio_box.set_visible(True)

################# Functions for Gtk signals begin here ##################

    def on_timer_start_button_toggled(self, user_data):
        """Called when the user toggles the start/stop button from the timer 
            toolbar"""  
        # If an activity has been set
        if not self.current_activity_label.get_text() == "No Activity": 
            # And the start button is active after being pressed.         
            if self.timer_start_button.get_active(): 
                # Start the timer.
                self.start_time() 
                # Set the start button's and indicator's labels to display Stop.
                self.timer_start_button.set_label("Stop")
                self.start_timer_indicator.set_label("Stop")
            # Else if the start button is not active after being pressed                              
            else:
                self.stop_time()
                # Reset the start button's, indicator's, and current 
                # activity's labels.
                self.timer_start_button.set_label("Start")
                self.start_timer_indicator.set_label("Start")
                self.current_activity_label.set_text("No Activity")
                self.current_activity_indicator.set_label("No Activity")
                # Reset the pause button if it was active before stopping.     
                self.timer_pause_button.set_active(False)
                self.timer_pause_button.set_label("Pause")
                self.pause_timer_indicator.set_label("Pause")   
        else:
            self.timer_start_button.set_active(False)
  
    def on_timer_pause_button_toggled(self, user_data):
        """Called when the user toggles the pause button from the timer 
            toolbar"""
        # If an activity is currently running
        if self.timer_start_button.get_active():
            # And the pause button is active after being pressed
            if self.timer_pause_button.get_active():
                # Pause the timer.
                self.pause_time()
                # Set the pause button label and indicator to display "Resume"
                self.timer_pause_button.set_label("Resume")
                self.pause_timer_indicator.set_label("Resume")
            # Else if the pause button is not active after being pressed.
            else:
                # Resume the timer.
                self.resume_time()
                # Set the pause button label and indicator to display "Pause" 
                self.timer_pause_button.set_label("Pause")
                self.pause_timer_indicator.set_label("Pause")
        # Else if no activity is running
        else:
            self.timer_pause_button.set_active(False)

    def on_set_button_clicked(self, user_data):
        """Called when the user clicks the set button"""
        # Disable all entrycompletion until the activity is set; otherwise, it
        # will leave behind artifacts from the total_treestore for some unknown
        # reason.
        self.entrycompletion1.set_inline_selection(False)
        self.entrycompletion1.set_inline_completion(False)
        self.entrycompletion2.set_inline_selection(True)
        self.entrycompletion2.set_inline_completion(True)
        # Set the activity label as the text from the text entry
        self.set_current_activity(self.activity_entry.get_text())
        # Clear the text entry
        self.activity_entry.set_text("")
        # If the indicator exists
        if not self.activity_entry == None:
            # Clear it as well
            self.set_activity_entry.set_text("")
        # Re-enable all entry completion
        self.entrycompletion1.set_inline_selection(True)
        self.entrycompletion1.set_inline_completion(True)
        self.entrycompletion2.set_inline_selection(True)
        self.entrycompletion2.set_inline_completion(True)

    def on_edit_activity_activate(self, user_data):
        """Called when the user selects 'Edit Activity' from the 
            total_treeview's right-click menu"""
        # Set the activity text column as editable.
        self.total_activity_column_child_text.set_property('editable', True)
        # Iterate through the treeview and get the selected cell for the 
        # activity text and set the cursor on it.
        selection = self.total_treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            self.total_treeview.set_cursor(path, self.total_activity_column, 
                                            True)
        self.total_activity_column_child_text.set_property('editable', False)
        
    def on_set_as_current_activity_activate(self, user_data):
        """Called when the user selects 'Set as Current Activity' from the 
            total_treeview's right-click menu"""
        # Iterate through the  treeview and get the selected cell for the
        # activity text and set the cursor on it.
        selection = self.total_treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            iter = model.get_iter(path)
            # Set the activity in the selected cell as the current activity.
            self.set_current_activity(model.get_value(iter, 0))

    def on_delete_activity_activate(self, user_data):
        """Called when the user selects 'Delete Activity' from the 
            total_treeview's right-click menu"""
        # Iterate through the  treeview and get the selected cell for the
        # activity text and set the cursor on it.
        selection = self.total_treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            iter = model.get_iter(path)
            # Delete the log and total entry for the selected activity cell.
            self.filer.delete_log(model.get_value(iter, 0))
        self.log_treestore.clear()
        self.total_treestore.clear()
        # Refresh all entries in the log treestore from the database
        for entry in self.filer.read_log("*"):
            self.log_treestore.prepend(None, (entry[0], entry[1], entry[2]))
        self.charter.clear()
        # Refresh all entries in the total treestore from the database
        self.timer.update_current_date()
        for entry in self.filer.read_total(self.timer.current_date):
            self.total_treestore.prepend(None, 
                                        (entry[0], 
                                        self.timer.format_timer(entry[1]), 
                                        self.timer.format_timer(entry[2])))
        format_menu_from_totals(self.filer.read_total(self.timer.current_date), 
                                self.set_activity_menu_list, 
                                self.set_activity_indicator, 
                                self.alternative_new_activity_indicator)
    
    def on_total_treeview_row_activated(self, path, column, user_data):
        """Called when the user double-clicks a row in the total_treeview"""
        # Get the selection for the total treeview
        tree_selection = self.total_treeview.get_selection()
        # Get the row that is selected as model, pathlist
        model, pathlist = tree_selection.get_selected_rows()
        # Iterate through the selected pathlist
        for path in pathlist:
            # Get the selected TreeIter
            tree_iter = model.get_iter(path)
            # Get the text from the activity column from the selected model
            activity = str(model.get_value(tree_iter,0))
            # If the selected activity is not currently set
            if not activity == self.current_activity_text:
                # Set tthe selected activity as the current activity
                self.set_current_activity(activity) 

    def on_total_activity_column_child_text_edited(self, path, user_data, new_activity_text):
        """Called when the user is done editing activity text in the totals
            treeview."""
        # Get the activity_text before it was edited
        activity = self.total_activity_column_child_text.get_property("text")
        if self.current_activity_text == activity:
            self.set_current_activity(new_activity_text, True)
        # Format the activity text by capitalizing the first letter and 
        # putting the rest in lower-case.
        new_activity_text = (new_activity_text[0].upper() + 
                                new_activity_text[1:].lower())
        # Edit the entries in the totals table in the database to have the new 
        # activity text
        data = self.filer.read_log(activity)    
        self.filer.edit_log(data, new_activity_text) 
        # Edit the entries in the logs table in the database to have the new 
        # activity text
        data = self.filer.read_log(activity)
        self.filer.edit_log(data, new_activity_text) 
        # Delete duplicates in the database and clean it up
        self.filer.compound_logs() 
        # Clear the total and log treestores 
        self.total_treestore.clear()
        self.log_treestore.clear()
        # Refresh all entries in the log treestore from the database
        for entry in self.filer.read_log("*"):
            self.log_treestore.prepend(None, (entry[0], entry[1], entry[2]))
        self.charter.clear()
        # Refresh all entries in the total treestore from the database
        self.timer.update_current_date()
        for entry in self.filer.read_total(self.timer.current_date):
            self.total_treestore.prepend(None, 
                                        (entry[0], 
                                        self.timer.format_timer(entry[1]), 
                                        self.timer.format_timer(entry[2])))

    def on_delete_log_activate(self, user_data):
        """Called when the user selects 'Delete Log' from the log_treeview's 
            right-click menu"""
        # Iterate through the  treeview and get the selected cell for the
        # activity text and set the cursor on it.
        selection = self.log_treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            iter = model.get_iter(path)
            # Delete the selected activity from the log table in the database.
            self.filer.delete_log(model.get_value(iter, 0), 
                                    model.get_value(iter, 1), 
                                    model.get_value(iter, 2))
        # Clear the treestores and graph
        self.filer.compound_logs()
        self.total_treestore.clear()
        self.log_treestore.clear()
        self.charter.clear()
        # Refresh all entries in the log treestore from the database
        for entry in self.filer.read_log("*"):
            self.log_treestore.prepend(None, (entry[0], entry[1], entry[2]))
        # Reload the information in the total treestore and graph
        self.timer.update_current_date()
        for entry in self.filer.read_total(self.timer.current_date):
            self.total_treestore.prepend(None, 
                                        (entry[0], 
                                        self.timer.format_timer(entry[1]), 
                                        self.timer.format_timer(entry[2])))
        # Format the indicator menu from data in the totals
        format_menu_from_totals(self.filer.read_total(self.timer.current_date), 
                                self.set_activity_menu_list,
                                self.set_activity_indicator, 
                                self.alternative_new_activity_indicator)

    def on_total_treeview_button_press_event(self, widget, event):
        """Called when a user clicks within the total treeview"""
        # event.button 3 is a right-click
        if event.button == 3:
            self.total_treeview_right_click_menu.popup(None, None, None, None,
                                                        0, 0)    
    
    def on_log_treeview_button_press_event(self, widget, event):
        """Called when a user clicks within the log treeview"""
        # event.button 3 is a right-click
        if event.button == 3:
            self.log_treeview_right_click_menu.popup(None, None, None, None,
                                                        0, 0)    

    def on_show_combobox_changed(self, user_data):
        """Called when the user specifies what analytics they would like to view
            from the show combobox"""
        model = self.show_combobox.get_model()
        index = self.show_combobox.get_active()
        active_item = model[index][0]
        print '\n\nYou have selected: ' + str(active_item) + '\n\n'
        if active_item == 'Percent of Time Spent':
            self.charter.type = 'pie'
            self.analytics_for_box.set_visible(True)
            self.refresh_totals_graph()
        elif active_item == 'Total Time Spent':
            self.charter.type = 'bar'
            self.analytics_for_box.set_visible(True)
        elif active_item == 'Activity Frequency':
            self.charter.type = 'line'
            self.analytics_for_box.set_visible(True)
        else:
            self.analytics_for_box.set_visible(True)

    def on_for_combobox_changed(self, user_data):
        """Called when the user specifies a time for analytics in the 'For'
            combobox"""
        model = self.for_combobox.get_model()
        index = self.for_combobox.get_active()
        active_item = model[index][0]
        # Update the current date
        self.timer.update_current_date()
        if active_item == 'All Time':
            # Refresh the graph to reflect the totals
            self.refresh_totals_graph()
        elif active_item == 'Day':
            # Format the day entry as a date
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                self.day_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_day_graph()
        elif active_item == 'Month':
            # Format the month entry as a date
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                self.month_value, show_days=False)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_month_graph()
        elif active_item == 'Span of Time':
            # Format the span entries as a date
            format_entry_as_date(self.timer.current_date, self.from_entry, self.from_value)
            format_entry_as_date(self.timer.current_date, self.to_entry, self.to_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_span_graph()

    def on_minus_day_button_pressed(self, user_data):
        """Called when the user presses the minus day button to decrement the 
        date in the day entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if entry_day_is_valid(self.timer.current_date, self.day_value-1):
            self.day_value -= 1
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                    self.day_value)
        # Refresh the graph to reflect the changes
        self.refresh_day_graph()

    def on_plus_day_button_pressed(self, user_data):
        """Called when the user presses the plus day button to increment the 
        date in the day entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if entry_day_is_valid(self.timer.current_date, self.day_value+1):
            self.day_value += 1
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                    self.day_value)
        # Refresh the graph to reflect the changes
        self.refresh_day_graph()

    def on_day_entry_activate(self, user_data):
        """Called when the user manually changes the date in the day entry"""
        # Update the current date
        self.timer.update_current_date()
        # Get the date to be set from the entry
        days = unformat_entry(self.timer.current_date, self.day_entry)
        # Check if the date to be changed to is valid before changing it
        if (not days == None and 
            entry_day_is_valid(self.timer.current_date, days)):
            self.day_value = days
        format_entry_as_date(self.timer.current_date, 
                                self.day_entry, 
                                self.day_value)
        # Refresh the graph to reflect the changes
        self.refresh_day_graph()

    def on_minus_month_button_pressed(self, user_data):
        """Called when the user presses the minus month button to decrement the 
        date in the month entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if entry_month_is_valid(self.timer.current_date, self.month_value-1):
            self.month_value -= 1
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                    self.month_value, show_days=False)
        # Refresh the graph to reflect the changes
        self.refresh_month_graph()

    def on_plus_month_button_pressed(self, user_data):
        """Called when the user presses the plus month button to increment the 
        date in the month entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if entry_month_is_valid(self.timer.current_date, self.month_value+1):
            self.month_value += 1
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                    self.month_value, show_days=False)
        # Refresh the graph to reflect the changes
        self.refresh_month_graph()

    def on_month_entry_activate(self, user_data):
        """Called when the user manually changes the date in the month entry"""
        # Update the current date
        self.timer.update_current_date()
        # Get the date to be set from the entry
        months = unformat_entry(self.timer.current_date, 
                                self.month_entry, 
                                days_shown=False)
        # Check if the date to be changed to is valid before changing it
        if (not months == None and 
            entry_month_is_valid(self.timer.current_date, months)):
            self.month_value = months
        format_entry_as_date(self.timer.current_date, self.month_entry, 
                                self.month_value, show_days=False)
        # Refresh the graph to reflect the changes
        self.refresh_month_graph()

    def on_minus_from_button_pressed(self, user_data):
        """Called when the user presses the minus from button to decrement the 
        date in the from entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if entry_day_is_valid(self.timer.current_date, self.from_value-1):
            self.from_value -= 1
            format_entry_as_date(self.timer.current_date, 
                                    self.from_entry, 
                                    self.from_value)
        # Refresh the graph to reflect the changes
        self.refresh_span_graph()

    def on_plus_from_button_pressed(self, user_data):
        """Called when the user presses the plus from button to increment the 
        date in the from entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if (entry_day_is_valid(self.timer.current_date, self.from_value+1) 
            and self.from_value < self.to_value):
            self.from_value += 1
            format_entry_as_date(self.timer.current_date, 
                                    self.from_entry, 
                                    self.from_value)
        # Refresh the graph to reflect the changes
        self.refresh_span_graph()

    def on_from_entry_activate(self, user_data):
        """Called when the user manually changes the date in the from entry"""
        # Update the current date
        self.timer.update_current_date()
        # Get the date to be set from the entry
        days = unformat_entry(self.timer.current_date, self.from_entry)
        # Check if the date to be changed to is valid before changing it
        if (not days == None and 
            entry_day_is_valid(self.timer.current_date, days) 
            and days < self.to_value):
            self.from_value = days
        format_entry_as_date(self.timer.current_date, 
                                self.from_entry, 
                                self.from_value)
        # Refresh the graph to reflect the changes
        self.refresh_span_graph()

    def on_minus_to_button_pressed(self, user_data):
        """Called when the user presses the minus to button to decrement the 
        date in the to entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if (entry_day_is_valid(self.timer.current_date, self.to_value-1) 
            and self.from_value < self.to_value):
            self.to_value -= 1
            format_entry_as_date(self.timer.current_date, 
                                    self.to_entry, 
                                    self.to_value)
        # Refresh the graph to reflect the changes
        self.refresh_span_graph()

    def on_plus_to_button_pressed(self, user_data):
        """Called when the user presses the plus to button to increment the 
        date in the to entry"""
        # Update the current date
        self.timer.update_current_date()
        # Check if the date to be changed to is valid before changing it
        if entry_day_is_valid(self.timer.current_date, self.to_value+1):
            self.to_value += 1
            format_entry_as_date(self.timer.current_date, 
                                    self.to_entry, 
                                    self.to_value)
        # Refresh the graph to reflect the changes
        self.refresh_span_graph()

    def on_to_entry_activate(self, user_data):
        """Called when the user manually changes the date in the to entry"""
        # Update the current date
        self.timer.update_current_date()
        # Get the date to be set from the entry
        days = unformat_entry(self.timer.current_date, self.to_entry)
        # Check if the date to be changed to is valid before changing it
        if (not days == None and 
            entry_day_is_valid(self.timer.current_date, days) 
            and self.from_value < days):
            self.to_value = days
        format_entry_as_date(self.timer.current_date, 
                                self.to_entry, 
                                self.to_value)
        # Refresh the graph to reflect the changes
        self.refresh_span_graph()

    def on_percentages_radiobutton_toggled(self, user_data):
        """Called when the user selects to see data in terms of percent"""
        #self.pieGrapher.liststore_mode = 'percent'
        model = self.for_combobox.get_model()
        index = self.for_combobox.get_active()
        active_item = model[index][0]
        # Update the current date
        self.timer.update_current_date()
        if active_item == 'All Time':
            # Refresh the graph to reflect the totals
            self.refresh_totals_graph()
        elif active_item == 'Day':
            # Format the day entry as a date
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                self.day_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_day_graph()
        elif active_item == 'Month':
            # Format the month entry as a date
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                self.month_value, show_days=False)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_month_graph()
        elif active_item == 'Span of Time':
            # Format the span entries as a date
            format_entry_as_date(self.timer.current_date, self.from_entry, self.from_value)
            format_entry_as_date(self.timer.current_date, self.to_entry, self.to_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_span_graph()

    def on_time_radiobutton_toggled(self, user_data):
        """Called when the user selects to see data in terms of time"""
        #self.pieGrapher.liststore_mode = 'time'
        model = self.for_combobox.get_model()
        index = self.for_combobox.get_active()
        active_item = model[index][0]
        # Update the current date
        self.timer.update_current_date()
        if active_item == 'All Time':
            # Refresh the graph to reflect the totals
            self.refresh_totals_graph()
        elif active_item == 'Day':
            # Format the day entry as a date
            format_entry_as_date(self.timer.current_date, self.day_entry, 
                                self.day_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_day_graph()
        elif active_item == 'Month':
            # Format the month entry as a date
            format_entry_as_date(self.timer.current_date, self.month_entry, 
                                self.month_value, show_days=False)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_month_graph()
        elif active_item == 'Span of Time':
            # Format the span entries as a date
            format_entry_as_date(self.timer.current_date, self.from_entry, self.from_value)
            format_entry_as_date(self.timer.current_date, self.to_entry, self.to_value)
            # Refresh the graph to reflect changes in the day entry
            self.refresh_span_graph()

    def on_spindl_window_configure_event(self, event, user_data):
        """Called when the window is resized and resizes the graph image"""
        #self.pieGrapher.update_size()

############### Functions for Unity indicator signals begin here ###############

    def on_start_timer_indicator_activate(self, user_data):
        """Called when the user toggles the start/stop button from the timer 
            toolbar"""        
        # If an activity is set 
        if not self.current_activity_label.get_text() == "No Activity":  
            # And the indicator button is set to start the timer 
            if self.start_timer_indicator.get_label() == "Start": 
                # Toggle the start button on the main window, which starts the 
                # timer
                self.timer_start_button.set_active(True) 
            # Else the indicator button is set to stop the timer                               
            else:
                # Toggle the stop button on the main window, which stops the 
                # timer
                self.timer_start_button.set_active(False)
        # Else do nothing and make sure the indicator start button isn't active.
        else:
            self.timer_start_button.set_active(False)
  
    def on_pause_timer_indicator_activate(self, user_data):
        """Called when the user toggles the pause item from the indicator"""
        # If an activity is set 
        if not self.current_activity_label.get_text() == "No Activity":
            # And the indicator button is set to pause the timer
            if self.pause_timer_indicator.get_label() == "Pause":
                # Toggle the pause button on the main window, which pauses the 
                # timer
                self.timer_pause_button.set_active(True)
            # Else the indicator button is set to resume the timer 
            else:
                # Toggle the resume button on the main window, which resumes the 
                # timer
                self.timer_pause_button.set_active(False)
        # Else do nothing and make sure the indicator pause button isn't active.
        else:
            self.timer_pause_button.set_active(False)

    def on_new_activity_indicator_activate(self, user_data):
        """Called when the user selects the Set Activity item from the 
            indicator"""
        self.set_activity_window.set_visible(True)

    def on_activity_menuitem_activate (self, activity_menuitem):
        """Called when the user selects the activity from the set_activity sub
            menu"""
        if activity_menuitem.get_label() == self.current_activity_text:
            self.set_current_activity(activity_menuitem.get_label(), 
                                        keep_running=True)
        else:
            self.set_current_activity(activity_menuitem.get_label())

    def on_hide_window_indicator_activate(self, user_data):
        """Called when the user toggles the hide item from the indicator"""
        # If the indicator hide button is set to hide mode
        if self.hide_window_indicator.get_label() == "Hide Spindl":
            # Make the main window invisible
            self.spindl_window.set_visible(False)
            # Hide the main window from any pager or taskbar
            self.spindl_window.set_skip_taskbar_hint(True)
            self.spindl_window.set_skip_pager_hint(True)
            # Switch the indicator hide button to show mode
            self.hide_window_indicator.set_label("Show Spindl")
        # If the indicator hide button is set to show mode
        else:
            # Make the main window visible
            self.spindl_window.set_visible(True)
            # Show the main window from any pager or taskbar
            self.spindl_window.set_skip_taskbar_hint(False)
            self.spindl_window.set_skip_pager_hint(False)
            # Switch the indicator show button to hide mode
            self.hide_window_indicator.set_label("Hide Spindl")

    def on_quit_indicator_activate(self, user_data):
        """Called when the user clicks the quit item from the indicator"""
        self.spindl_window.destroy()

############# Functions for Set Activity Window signals begin here #############

    def on_set_activity_window_hide(self, event, user_data):
        """Called when the Set Activity Window is hidden"""
        # Hide the window and return True to keep it hidden
        self.set_activity_window.set_visible(False)
        return True

    def on_set_activity_window_delete_event(self, unknown, user_data):
        """Called when the user clicks the close button on the Set Activity
            Window"""
        # Just used to keep gtk from throwing errors
        # No function here
        pass

    def on_set_activity_button_activate(self, user_data):
        """Called when the user clicks the set button on the Set Activity 
            Window"""
        # Set the activity label as the text from the text entry
        self.set_current_activity(self.set_activity_entry.get_text())
        # Clear the text entry
        self.set_activity_entry.set_text("")
        # Hide the window once finised setting
        self.set_activity_window.set_visible(False)