# -*- coding: utf-8 -*-

import sys

import gtk
import gobject
import pango
import re
import gtkgui_helpers

from common import gajim
from plugins import GajimPlugin
from plugins.helpers import log, log_calls

class RaisetabsPlugin(GajimPlugin):
    @log_calls('RaisetabsPlugin')
    def init(self):
        self.config_dialog = None
        self.gui_extension_points = {'chat_control_base' : (self.connect_with_chat_control, self.disconnect_from_chat_control)}
        self.config_default_values = {}
        self.chat_control = None
        self.controls = []

    @log_calls('RaisetabsPlugin')
    def activate(self):
        pass

    @log_calls('RaisetabsPlugin')
    def deactivate(self):
        pass

    @log_calls('RaisetabsPlugin')
    def connect_with_chat_control(self, chat_control):
        self.chat_control = chat_control
        control = Base(self, self.chat_control)
        self.controls.append(control)

    @log_calls('RaisetabsPlugin')
    def disconnect_from_chat_control(self, chat_control):
        for control in self.controls:
            control.disconnect_from_chat_control()
        self.controls = []

class Base(object):
    def __init__(self, plugin, chat_control):
        self.plugin = plugin
        self.chat_control = chat_control

        self.id_ = self.chat_control.msg_textview.connect('key_press_event', self.mykeypress_event)
        self.chat_control.handlers[self.id_] = self.chat_control.msg_textview

    def mykeypress_event(self, widget, event):
        if event.is_modifier:
            return
        notebook = self.chat_control.parent_win.notebook
        current_page = notebook.get_nth_page(notebook.get_current_page())
        notebook.reorder_child(current_page, 0);
