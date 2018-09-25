#!/usr/bin/python3

import base64
from PySide2.QtCore import (Signal, QSettings, QObject)

class SettingsManager(QObject):
    """Handles settings."""

    def __init__(self):
        """Initiates SettingsManager"""
        super().__init__()
        self._settings = QSettings("/etc/PlexTray/config.ini", QSettings.IniFormat)
    
    def get_plex_host(self):
        """Returns Plex host"""
        return self._get_setting("plex_host")

    def get_plex_token(self):
        """Returns Plex token"""
        return self._get_setting("plex_token", True)

    def get_pushbullet_token(self):
        """Returns Pushbullet token"""
        return self._get_setting("pushbullet_token", True)

    def get_timestamp(self):
        """Returns Pushbullet timestamp"""
        return self._get_setting("timestamp")

    def set_plex_host(self, plex_host):
        """Sets Plex host"""
        self._set_setting(plex_host, "plex_host")

    def set_plex_token(self, plex_token):
        """Sets Plex token"""
        self._set_setting(plex_token, "plex_token", True)

    def set_pushbullet_token(self, pushbullet_token):
        """Sets Pushbullet token"""
        self._set_setting(pushbullet_token, "pushbullet_token", True)

    def set_timestamp(self, timestamp):
        """Sets Pushbullet timestamp"""
        self._set_setting(timestamp, "timestamp")

    def _get_setting(self, key, decode=False):
        """Gets setting.

        Keyword arguments:
        key -- which setting
        decode -- True if decoding is necessary
        """
        try:
            value = self._settings.value(key)
            if decode:
                value = base64.b64decode(bytearray([int(i) for i in value])).decode()
            return value
        except Exception as e:
            print("Failed to get " + key)
            exception_type = type(e).__name__
            print(exception_type)
            print(e)
            return None

    def _set_setting(self, value, key, encode=False):
        """Sets setting.

        Keyword arguments:
        value -- new value
        key -- which setting
        decode -- True if encoding for obscurity
        """
        try:
            if encode:
                value = base64.b64encode(value.encode())
            self._settings.setValue(key, value)
        except Exception as e:
            print("Failed to set " + key)
            exception_type = type(e).__name__
            print(exception_type)
            print(e)
            return None
