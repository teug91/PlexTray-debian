#!/usr/bin/python

#import sys, os
from shared import resource_path
from PySide2.QtWidgets import QSystemTrayIcon, QMenu
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal

class TrayIcon(QSystemTrayIcon):
    """System tray icon."""

    settings_clicked = Signal()
    update_clicked = Signal()
    webui_clicked = Signal()
    exit_clicked = Signal()
    icon_clicked = Signal()

    def __init__(self, parentApp):
        """Initiates TrayIcon"""
        self._icon_plex = QIcon(resource_path("plex.png"))
        self._icon_dc = QIcon(resource_path("dc.png"))
        super(TrayIcon, self).__init__(self._icon_dc, parent=parentApp)
        self.setToolTip("PlexTray")
        menu = QMenu()
        menu.addAction("WebUI").triggered.connect(self._emit_webui)
        menu.addAction("Update libraries").triggered.connect(self._emit_update)
        menu.addAction("Settings").triggered.connect(self._emit_settings)
        menu.addAction("Exit").triggered.connect(self._emit_exit)
        self.setContextMenu(menu)
        if QSystemTrayIcon.supportsMessages():
            self.activated.connect(self._icon_clicked)
        self.show()

    def set_icon(self, available):
        """Sets icon.

        Keyword arguments:
        available -- True if PMS is available
        """
        if available:
            self.setIcon(self._icon_plex)
        else:
            self.setIcon(self._icon_dc)

    def media_added_message(self, media_name):
        """Displays tray message.

        Keyword arguments:
        media_name -- media name
        """
        self.showMessage("Media added", media_name, self._icon_plex)

    def _icon_clicked(self, reason):
        """Emits signal if tray icon was clicked."""
        if reason == QSystemTrayIcon.Trigger:
            self.icon_clicked.emit()

    def _emit_settings(self):
        """Emits settings clicked signal."""
        self.settings_clicked.emit()

    def _emit_update(self):
        """Emits update clicked signal."""
        self.update_clicked.emit()

    def _emit_webui(self):
        """Emits WebUI clicked signal."""
        self.webui_clicked.emit()

    def _emit_exit(self):
        """Emits exit clicked signal."""
        self.exit_clicked.emit()
