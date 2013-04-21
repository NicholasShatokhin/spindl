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

from gi.repository import Gdk    
from gi.repository import Gtk
from gi.repository import Dee
_m = dir(Dee.SequenceModel)
from gi.repository import AppIndicator3

# Path to the SVG icon for the app
ICON_PATH = "/home/zane/spindl/data/media/spindl.svg"

class Indicator:
    """Adds a section for integrating with Application Indicators"""
    def __init__(self, indicator_menu, activity_item, timer_item, icon):

        # Create the AppIndicator
        self.app_indicator = AppIndicator3.Indicator.new(
                            "Spindl",
                            icon,
                            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        # Set it to Active by default
        self.app_indicator.set_status (AppIndicator3.IndicatorStatus.ACTIVE)

        # Not displayed in the indicator, but used by HUD
        self.app_indicator.set_title(('Spindl'))

        # Indicator menu items 
        self.indicator_menu = indicator_menu
        self.activity_item = activity_item
        self.timer_item = timer_item
        
        # Make activity_item and timer_item not sensitive so they aren't 
        # highlighted orange when the mouse goes over them.
        self.activity_item.set_sensitive(False)
        self.timer_item.set_sensitive(False)
	    # Attach the menu to the indicator
        self.app_indicator.set_menu(self.indicator_menu)