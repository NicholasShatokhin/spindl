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
import calendar
from time import strptime

def format_date(date):
    """Format the date from YYYY-MM-DD to a form of Month Day, 
        Year"""
    # Get the date a string.
    date = str(date)
    # Get the day, month, and year.
    day = date[8:10]
    month = calendar.month_name[int(date[5:7])]
    year = date[0:4]
    # Format the day, month, and year as Month Day, Year and return the date.     
    formatted_date = str(month) + " " + str(day) + ", " + str(year)
    return formatted_date

def tuple_time(date):
    """Unformat the date (string) from Month Day, Year  Hr:Mn:Ss to 
        (SS, MM, HH, DD, MO, YYYY) (tuple)"""
    # Get the second, minute, hour, day, month, year as ints.
    second = int(date[-2:].rstrip())
    minute = int(date[-5:-3])
    hour = int(date[-8:-6])
    day = int(date[-20:-18].lstrip())
    # To get the month we take the first three letters aof the month and use
    # strptime on it and get the .tm_mon, which is the month as an int.
    month = int(strptime(date[0:3],'%b').tm_mon)
    year = int(date[-16:-11])
    # Put the time elements in a tuple and return it.
    unformatted_date = (second, minute, hour, day, month, year)
    return unformatted_date

def unformat_time(time):
    """Unformat the time (tuple) from SS,MM,HH,DD,MO,YR to 
    	seconds"""
    # Get the year, month, day, hour, minute, and second as ints
    year = int(time[5])
    # Month is set to the days up to that given month
    month = 0
    for i in range (1, int(time[4])):
        # Add the days from every month up to the given month
        month += calendar.monthrange(year, i)[1]
    # If day is set to None 
    if time[3] == None:
        # Set day to the number of days in the month
        day = calendar.monthrange(year, int(time[4]))[1]
    else:
        day = int(time[3])
    hour = int(time[2])
    minute = int(time[1])
    second = int(time[0])
    # Turn the time into an int representing the number of seconds passed since
    # 0 A.D. and return the int.
    unformatted_time = (year*31557600 + month*86400 + day*86400 + 
                        hour*3600 + minute*60 + second) 
    return unformatted_time

def time_in_span(start_time, stop_time, minimum, maximum):
    """Checks if an activity is within a time span by checking its start and
        stop time against a maximum and minimum value"""
    # If both the start time and start time are in the range 
    if (start_time >= minimum and start_time < maximum and 
        stop_time <= maximum):
        # Total time is the difference between the stop and start times
        total_time = stop_time - start_time
    # If start time is outside the range but the stop time is in the range
    elif (stop_time <= maximum and stop_time > minimum and 
            start_time < minimum):
        # Total time is the difference between the stop and minimum times
        total_time = stop_time - minimum
    # If start time is inside the range but stop time is outside the range
    elif (start_time >= minimum and start_time < maximum and 
            stop_time > maximum):
        # Total time is the difference between the maximum and start times
        total_time = maximum - start_time
    else:
        # Else there is no time in the range
        total_time = 0
    return total_time