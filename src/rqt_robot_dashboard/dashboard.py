# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import roslib;roslib.load_manifest('rqt_robot_dashboard')
import rospy

from python_qt_binding import loadUi

from python_qt_binding.QtCore import QSize
from python_qt_binding.QtGui import QWidget, QHBoxLayout, QGroupBox, QToolBar
from qt_gui.plugin import Plugin

class Dashboard(Plugin):
    """
    Base class from which dashboards should inherit.

    :param context: the plugin context
    :type context: qt_gui.plugin.Plugin
    :param name: name of the dashboard widget
    :type name: str
    :param MaxIconSize: maximum size of a dashboard icon
    :type MaxIconSize: QSize
    """
    def __init__(self, context, name = None, MaxIconSize=QSize(80,80)):
        super(Dashboard, self).__init__(context)
        self.context = context
        self.setup(context)

        if not hasattr(self, 'name'):
            if not name:
                self.name = 'Dashboard'
            else:
                self.name = name
        self._max_icon_size = MaxIconSize
        self._main_widget = QToolBar()
        self._main_widget.setIconSize(MaxIconSize)
        self._main_widget.setObjectName(self.name)
        self._main_widget.setWindowTitle(self.name)
        widgets = self.get_widgets()

        layout = QHBoxLayout()

        self._widgets = []
        for v in widgets:
            for i in v:
                try:
                    self._main_widget.addWidget(i)
                    self._widgets.append(i)
                except:
                    raise(Exception("All widgets must be a subclass of QWidget!"))

            self._main_widget.addSeparator()

        # Display the dashboard
        context.add_toolbar(self._main_widget)

    def setup(self, context):
        """
        Called during ``__init__`` Subclasses should do initialization here.
        
        NOTE: When overriding this method you must call ``self.setObjectName()``
        to avoid object name conflicts

        :param context: The plugin context
        :type context: qt_gui.plugin.Plugin
        """
        pass

    def shutdown_plugin(self):
        """
        Called when the toolbar is closed by Qt.
        """
        for widget in self._widgets:
            if hasattr(widget, 'close'):
                widget.close()

        self.shutdown_dashboard()

    def shutdown_dashboard(self):
        """
        Called after shutdown plugin, subclasses should do cleanup here, not in shutdown_plugin
        """
        pass

    def get_widgets(self):
        """
        Most of the dashboard customization should be done here. 
        If this function is not overriden the dashboard will display nothing.

        :returns: List of lists containing dashboard widgets.
        """
        return []
