#!/usr/bin/python
import calendar
from timeFormat import *

def format_entry_as_date(current_date, entry, entry_value, show_days=True):
        """Formats the value in a Gtk entry to a date of MM/DD/YYYY or 
        	MM/YYYY from a time formatted as a tuple of (DD, MM, YYYY)"""
        # Get the current date tuple
        day = current_date[0]
        month = current_date[1]
        year = current_date[2]
        # If set to show days and format date as MM/DD/YYYY
        if show_days:
            # Subtract the change in days from today
            day = day + entry_value
            # While change in days is greater than today
            while day < 1:
                # Decrement the month by 1
                month -= 1
                # If month is valid month (January-December)
                if month > 0:
                    # Add the number of days in the month to day
                    day += calendar.monthrange(year, month)[1]
                # Else the month is 0 (not a calendar month)
                else:
                    # Set month to December of the previous year
                    month = 13
                    year -= 1
            # Set the text in the spinbox to MM/DD/YYYY
            entry.set_text(str(month) + '/' + str(day) + '/' + str(year))
        # Else set to not show days and format date as MM/YYYY
        else:
            # Subtract the change in months from this month
            month = month + entry_value
            # While change in months is greater than this month
            while month < 1:
                # Decrement the year by 1
                year -= 1
                # Set the month to December
                month += 12
            # Set the text in the spinbox to MM/YYYY
            entry.set_text(str(month) + '/' + str(year))

def entry_day_is_valid(current_date, entry_value):
    """Checks whether the day formatted as MM/DD/YYYY in an entry is 
    	acceptable and returns a boolean to reflect that"""
    # If the entry value is set to the future
    if entry_value > 0:
        return False
    # Get the current date tuple
    day = current_date[0]
    month = current_date[1]
    year = current_date[2]
    # Subtract the change in days from today
    day = day + entry_value
    # While change in days is greater than today
    while day < 1:
        # Decrement the month by 1
        month -= 1
        # If month is valid month (January-December)
        if month >= 1:
            # Add the number of days in the month to day
            day += calendar.monthrange(year, month)[1]
        # Else the month is 0 (not a calendar month)
        else:
            # Set month to December of the previous year
            month += 13
            year -= 1
            # If year is set to before this app was published
            if year < 2013:
                # The date is incorrect
                return False
    return True

def entry_month_is_valid(current_date, entry_value):
    """Checks whether the month formatted as MM/YYYY in an entry is 
    	acceptable and returns a boolean to reflect that"""
    # If the entry value is set to the future
    if entry_value > 0:
        return False
    # Get the current date tuple
    month = current_date[1]
    year = current_date[2]
    # Subtract the change in months from this month
    month = month + entry_value
    # While change in months is greater than this month
    while month < 1:
        # Decrement the year by 1
        year -= 1
        # Set the month to December
        month += 13
        # If year is set to before this app was published
        if year < 2013:
           return False
    return True

def unformat_entry(current_date, entry, days_shown=True):
    """Unformats an entry containing a day formatted as either MM/DD/YYYY
    	or MM/YYYY to an integer describing days or months"""
    # Get the current date tuple
    current_day = current_date[0]
    current_month = current_date[1]
    current_year = current_date[2]
    # If days are set to be shown and date is formatted as MM/DD/YYYY
    if days_shown:
        # See if the date is full of valid integers for day, month, and year
        try:
            # Get the day, month, and year from the entry
            # If the month is only one digit long (month is 9 or less)
            if not entry.get_text()[1] == '/':
                month = int(entry.get_text()[0:2])
                # If the day is only one digit long (day is 9 or less)
                if not entry.get_text()[4] == '/':
                    day = int(entry.get_text()[3:5])
                # Else the day is longer than one digit (day is 10 or higher) 
                else:
                    day = int(entry.get_text()[3:4]) 
            # Else the month is longer than one digit (month is 10 or higher)
            else:
                month = int(entry.get_text()[0:1])
                # If the day is only one digit long (day is 9 or less)
                if not entry.get_text()[3] == '/':
                    day = int(entry.get_text()[2:4])
                # Else the day is longer than one digit (day is 10 or higher) 
                else:
                    day = int(entry.get_text()[2:3])
            # Make sure month is sane
            if month == 0:
                month = 1
            # Make sure day is sane
            if day == 0:
                day = 1
            # Get the year from the last 4 digits in the date
            year = int(entry.get_text()[-4:])
            # Convert the date in the entry to seconds
            date = unformat_time((0, 0, 0, day, month, year))
            # Convert the current date to seconds
            current_date = unformat_time((0, 0, 0, current_day, current_month, 
                                            current_year))
            # Set date to the difference of the entry date and the current 
            # date
            date = date - current_date
            # Return the difference of days in the entry and current day
            return int(date / 86400)
        # If the date is invalid
        except ValueError:
            return None
    # Else days are not set to be shown and date is formatted as MM/YYYY    
    else:
        # See if the date is full of valid integers for month and year
        try:
            # Get the month and year from the entry
            # If the month is only one digit long (month is 9 or less)
            if not entry.get_text()[1] == '/':
                month = int(entry.get_text()[0:2])
            # Else the month is longer than one digit (month is 10 or higher)
            else:
                month = int(entry.get_text()[0:1])
            year = int(entry.get_text()[-4:])
            date = month + year*12
            current_date = current_month + current_year*12
            date = date - current_date
            # Return the number of months in the entry 
            return int(date) 
        # If the date is invalid
        except ValueError:
            return None