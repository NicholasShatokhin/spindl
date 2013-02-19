# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
import sqlite3 
#import sys
from math import floor
from timeFormat import *

class Filer:
    def __init__(self, filepath):
        # Connect to database
        self.connection = sqlite3.connect(filepath)
        with self.connection:        
            # Setup cursor
            self.cursor = self.connection.cursor()
            # Setup table
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Logs(Activity TEXT, Start TEXT, Stop TEXT, Color INT)")
    
    def write_log(self, data): 
        """Commit an activity log to the database file"""
        # Data must be a tuple with Activity, Start Time, and stop Time
        activity = data[0]
        start_time = data[1]
        stop_time = data[2]
        # If the log is sane to write
        if not start_time == None and not stop_time == None:
            # If the activity already exists in the logs
            if not self.read_log(activity) == []:
                # Get the color for the log's activity
                color = self.read_log(activity)[0][3]
            # If this is a new activity
            else:
                # Set a new color for the activity
                color = self.highest_color()+1
            # Prepare and write the log 
            data = (activity[0].upper() + activity[1:].lower(), 
                    start_time[:-7], stop_time[:-7], color) 
            self.cursor.execute("INSERT INTO Logs VALUES(?,?,?,?)", data)
            self.connection.commit()

    def read_log(self, activity):
        """Return an activity log from the database file"""  
        # If the function was called to read all logs using the wildcard '*'
        if activity == "*":
            # Select all the logs in the database.
            self.cursor.execute("SELECT * FROM Logs")
            self.connection.commit()
            data = self.cursor.fetchall()
        # Else if the function was called to read a specific log
        else:       
            # Select that specific log based on what its activity is.
            self.cursor.execute("SELECT * FROM Logs WHERE Activity = ?", 
                                (activity,))
            self.connection.commit()
            data = self.cursor.fetchall()
        # Return the selected logs
        return data 
    
    def read_total(self, current_date, span=None):
        """Extrapolates a set of totals based on information in the logs and 
         returns as a list of tuples"""
        totals_list = []
        # Iterate through the logs
        for entry in self.read_log("*"):
            # Get the activity from the entry
            activity = entry[0] 
            # Get the entry's start time
            start_time = tuple_time(entry[1])
            # Get the entry's stop time
            stop_time = tuple_time(entry[2])
            # Get the entry's color
            color = entry[3]
            # Get the time elapsed by the entry and round to the lowest nearby
            # whole integer and subtract 1
            day = current_date[0]
            month = current_date[1]
            year = current_date[2]
            stop_time = unformat_time(stop_time) 
            start_time = unformat_time(start_time)
            minimum = unformat_time((0, 0, 0, 0, 0, 0))
            maximum = unformat_time((59, 59, 23, day, month, year))
            total_time = time_in_span(start_time, stop_time, minimum, maximum)
            if not total_time == 0:
                minimum = unformat_time((0, 0, 0, day, month, year))
                time_today = time_in_span(start_time, stop_time, minimum, maximum)
                is_new_activity = True
                for total in totals_list:
                    if total[0] == entry[0]:
                        updated_total = (entry[0], total[1]+time_today, total[2]+total_time, color)
                        totals_list[totals_list.index(total)] = updated_total
                        is_new_activity = False
                # If the entry is a new activity
                if is_new_activity:
                    # Append it to the day_totals
                    totals_list.append((activity, time_today, total_time, color))
        # Return totals_list
        return totals_list

    def highest_color(self):
        """Returns the highest color integer in the logs"""
        highest_color = -1
        for log in self.read_log('*'):
            color = log[3]
            if color > highest_color:
                highest_color = color
        return highest_color

    def edit_log(self, data, new_activity_text):
        """Modifies a log's, or set of logs', activity"""
        # Iterate through the logs provided
        for entry in data:
            # If the activity already exists
            if not self.read_log(new_activity_text) == []:
                # Use the pre-specified color
                color = self.read_log(new_activity_text)[0][3]
                # Update the activity text and color in the database and commit
                self.cursor.execute("UPDATE Logs SET Activity = ? WHERE Start = ? AND Stop = ? AND Color = ?", 
                                    (new_activity_text, 
                                        entry[1], 
                                        entry[2], 
                                        color)) 
            # If the activity is being changed to a new activity
            else:
                # Update the activity text in the database and commit
                self.cursor.execute("UPDATE Logs SET Activity = ? WHERE Start = ? AND Stop = ? ", 
                                    (new_activity_text, entry[1], entry[2]))       
            self.connection.commit()

    def delete_log(self, activity, start_time = None, stop_time = None):
        """Removes an activity log from the database file"""
        # If the function call only specified an activity
        if start_time == None and stop_time == None:
            # Delete ll logs that match that activity and commit to the database
            self.cursor.execute("DELETE FROM Logs WHERE Activity = ?", 
                                (activity,))
            self.connection.commit()
        # Else if the function call supplied the activity, start, and stop time
        else:
            # Delete that specific log and commit to the database
            self.cursor.execute("DELETE FROM Logs WHERE Activity = ? AND Start = ? AND Stop = ?", 
                                (activity, start_time, stop_time))
            self.connection.commit()
    
    def compound_logs(self):
        """Remove logs with 'None' entries"""
        self.cursor.execute("DELETE FROM Logs WHERE Start = ? OR Stop = ?", 
                            ('None', 'None'))
        self.cursor.execute("DELETE FROM Logs WHERE Start = ? OR Stop = ?", 
                            ('', ''))
        self.connection.commit()