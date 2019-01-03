#!/usr/bin/python3

import sys
from plex import Plex
from pushbullet import Pushbullet
from settings_manager import SettingsManager
from tray import TrayIcon
from settings_window import Settings_Window
from qtsingleapplication import QtSingleApplication
from shared import open_browser

class Application():
    """Application."""

    def __init__(self):
        """Initiates Application."""
        self._app = QtSingleApplication()
        if self._app.is_running() or not TrayIcon.isSystemTrayAvailable():
            sys.exit(0)
        self._tray_message_available = TrayIcon.supportsMessages()
        self._new_media = None
        self._app.setQuitOnLastWindowClosed(False)
        self._settings_manager = SettingsManager()
        self._plex_host = self._settings_manager.get_plex_host()
        self._plex_token = self._settings_manager.get_plex_token()
        self._pushbullet_token = self._settings_manager.get_pushbullet_token()
        self._timestamp = self._settings_manager.get_timestamp()
        self._new_plex_settings = True
        self._new_pushbullet_settings = True
        self._tray = TrayIcon(self._app)
        self._tray.settings_clicked.connect(self._on_settings_clicked)
        self._tray.update_clicked.connect(self._on_update_clicked)
        self._tray.webui_clicked.connect(self._on_webui_clicked)
        self._tray.exit_clicked.connect(sys.exit)
        self._tray.icon_clicked.connect(self._icon_clicked)
        if self._plex_host and self._plex_token:
            self._init_plex()
        if self._pushbullet_token and self._tray_message_available:
            self._init_pushbullet()
        sys.exit(self._app.exec_())

    def _init_plex(self):
        """Initiates PMS communicator."""
        if not self._new_plex_settings:
            return
        self._new_plex_settings = False
        self._plex = Plex(self._plex_host, self._plex_token)
        self._plex.available.connect(self._set_icon)
        self._plex.finished.connect(self._init_plex)
        self._plex.start()

    def _init_pushbullet(self):
        """Initiates Pushbullet communicator."""
        if not self._new_pushbullet_settings:
            return
        self._new_pushbullet_settings = False
        self._pushbullet = Pushbullet(self._pushbullet_token, self._timestamp)
        self._pushbullet.update_timestamp.connect(self._on_timestamp)
        self._pushbullet.media_received.connect(self._on_media_received)
        self._pushbullet.finished.connect(self._init_pushbullet)
        self._pushbullet.start()

    def _on_timestamp(self, timestamp):
        """Updates timestamp for last push.

        Keyword arguments:
        timestamp -- timestamp of last push
        """
        self._settings_manager.set_timestamp(timestamp)
        self._timestamp = timestamp

    def _on_media_received(self, new_media):
        """Shows message when new media has been added.

        Keyword arguments:
        media_name -- name of new media
        """
        self._new_media = new_media
        self._tray.media_added_message(new_media[0])

    def _icon_clicked(self):
        """Opens PMS page in browser of latest media added during runtime."""
        if self._plex and self._new_media:
            self._plex.open_media(self._new_media[2] + "/" + self._new_media[1])
            self._new_media = None

    def _on_webui_clicked(self):
        """Opens PMS page in browser."""
        if self._plex_host:
            open_browser(self._plex_host)

    def _on_update_clicked(self):
        """Updates all PMS libraries."""
        if self._plex:
            self._plex.update_libraries()

    def _on_settings_clicked(self):
        """Displays settings window."""
        self.settings_window = Settings_Window(self._plex_host, self._plex_token, self._pushbullet_token)
        self.settings_window.save_clicked.connect(self._on_settings_saved)

    def _on_settings_saved(self, settings):
        """(Re)initializes PMS/Pushbullet with new settings.

        Keyword arguments:
        settings -- list containing PMS host, PMS token, Pushbullet token.
        """
        plex_host = settings[0]
        plex_token = settings[1]
        pushbullet_token = settings[2]
        if plex_host != self._plex_host or plex_token != self._plex_token:
            if plex_host != self._plex_host:
                self._settings_manager.set_plex_host(plex_host)
                self._plex_host = plex_host
            if plex_token != self._plex_token:
                self._settings_manager.set_plex_token(plex_token)
                self._plex_token = plex_host
            self._new_plex_settings = True
            try:
                if not self._plex.isRunning():
                    self._init_plex()
                else:
                    self._plex.stop()
            except Exception:
                self._init_plex()
        if pushbullet_token != self._pushbullet_token and self._tray_message_available:
            self._settings_manager.set_pushbullet_token(pushbullet_token)
            self._pushbullet_token = pushbullet_token
            self._new_pushbullet_settings = True
            try:
                if not self._pushbullet.isRunning():
                    self._init_pushbullet()
                else:
                    self._pushbullet.stop()
            except Exception:
                self._init_pushbullet()

    def _set_icon(self, available):
        """Sets appropriate tray icon based on PMS availability
        
        Keyword arguments:
        available - True if PMS is available
        """
        self._tray.set_icon(available)

if __name__ == "__main__":
    Application()
