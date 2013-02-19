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
from datetime import datetime
from gi.repository import GLib # switched from gobject to glib

class Timer:
    def __init__(self, label, indicator_label=None):
        self.time_elapsed = 0
        self.label = label
        self.indicator_label = indicator_label
        self.is_running = False
        self.start_times = []
        self.stop_times = []
        self.current_date = (datetime.now().day, datetime.now().month, 
                                datetime.now().year)

    def clear(self):
        """Set the timer to its initial value"""
        self.start_times = []
        self.stop_times = []
        self.time_elapsed = 0
        self.label.set_text(self.format_timer(self.time_elapsed))
        # If the indicator exists
        if not self.indicator_label == None:
            # Clear it as well
            self.indicator_label.set_label(self.format_timer(self.time_elapsed))

    def stop(self):
        """Stop the timer"""
        # If the timer was not already paused.
        if len(self.start_times) > len(self.stop_times):
            # Add the current time to the stop_times list.
            self.stop_times.append(datetime.now())    
            # Stop the timer from refreshing and running.    
            self.is_running = False
            # Update the time elapsed to reflect the new stop_times entry
            for entry in xrange(0, len(self.stop_times)):
                    delta = (self.stop_times[entry] - self.start_times[entry])
                    self.time_elapsed += delta.seconds + delta.days*86400

    def start(self):
        """Start the timer"""
        # Add the current time to the start time list
        self.start_times.append(datetime.now())
        # Start the timer by allowing it to refresh
        self.is_running = True
        # Start refreshing the timer at one second intervals
        GLib.timeout_add_seconds(1, self.refresh)       
    
    def refresh(self):
        """Callback used to set the time to the current time passed since last 
            starting the timer"""
        # If the timer is still running
        if self.is_running:
            # Clear time elapsed
            self.time_elapsed = 0
            # Get the delta (in seconds) between all of the stop and start times
            # and add them to time elapsed.
            for entry in xrange(0, len(self.stop_times)):
                delta = (self.stop_times[entry] - self.start_times[entry])
                self.time_elapsed += delta.seconds + delta.days*86400
            # Added these two lines to fix a weird bug that added an extra
            # second after resuming the timer.
            if len(self.stop_times) > 1:
                self.time_elapsed -= 1
            # Get the time delta between now and the last start time and
            # format it as an integer of seconds.
            delta = datetime.now() - self.start_times[-1]
            delta_in_seconds = delta.seconds + delta.days*86400
            # Add the time delta (in seconds) to time_elapsed.
            self.time_elapsed += delta_in_seconds
            self.label.set_text(self.format_timer(self.time_elapsed))
            # If the indicator exists, set it to the time elapsed as well
            if not self.indicator_label == None:
                formatted_time = self.format_timer(self.time_elapsed)
                self.indicator_label.set_label(formatted_time)
        # Return true if the timer is running to keep he callback going
        return self.is_running

    def format_timer(self, time):
        """Format the time from seconds to a form of HH:MM:SS"""
        # Get the number of hours minutes and seconds to be formatted
        hours = int(time / 3600)
        minutes = int((time % 3600.00) / 60.00)
        seconds = int(time % 60)
        # Format them as strings and prepend 0's if neccesary
        hours =  ("0" + str(hours)) if (hours < 10) else str(hours)
        minutes =  ("0" + str(minutes)) if (minutes < 10) else str(minutes)  
        seconds =  ("0" + str(seconds)) if (seconds < 10) else str(seconds) 
        # Append hours, minutes, and seconds in a string and return the string.
        formatted_timer = hours + ":" + minutes + ":" + seconds
        return formatted_timer

    def update_current_date(self):
        """Updates the current_date"""
        self.current_date = (datetime.now().day, datetime.now().month, 
                            datetime.now().year)