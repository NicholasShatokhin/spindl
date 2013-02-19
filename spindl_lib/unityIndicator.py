# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
#from gettext import gettext as _
from gi.repository import Gdk    
from gi.repository import Gtk
from gi.repository import Dee
_m = dir(Dee.SequenceModel)
from gi.repository import AppIndicator3

ICON_PATH = "/home/zane/timelog.svg"

class Indicator:
    """Adds a section for integrating with Application Indicators"""
    def __init__(self, indicator_menu, activity_item, timer_item, 
                    start_item, pause_item, hide_item, quit_item):

        # Create the AppIndicator
        self.app_indicator = AppIndicator3.Indicator.new(
                            "Timelog",
                            ICON_PATH,
                            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        # Set it to Active by default
        self.app_indicator.set_status (AppIndicator3.IndicatorStatus.ACTIVE)

        # Not displayed in the indicator, but used by HUD
        self.app_indicator.set_title(('Timelog'))

        # Indicator menu items 
        self.indicator_menu = indicator_menu
        self.activity_item = activity_item
        self.timer_item = timer_item
        #self.start_item = start_item
        #self.pause_item = pause_item
        #self.hide_item = hide_item
        #self.quit_item = quit_item
        
        # Make activity_item and timer_item not sensitive so they aren't 
        # highlighted orange when the mouse goes over them.
        self.activity_item.set_sensitive(False)
        self.timer_item.set_sensitive(False)
	    # Attach the menu to the indicator
        self.app_indicator.set_menu(self.indicator_menu)