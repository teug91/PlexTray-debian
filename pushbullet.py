#!/usr/bin/python3

import requests, json, time
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
from PySide2.QtCore import Signal, QThread
#from PySide2.QtWebSockets import QWebSocket

class Pushbullet(QThread):
    """Communicates with Pushbullet."""

    media_received = Signal(list)
    update_timestamp = Signal(float)

    def __init__(self, token, timestamp=0.0):
        """Initializes Pushbullet class.

        Keyword arguments:
        token -- Pushbullet token
        timestamp -- UNIX timestamp for last shown new media push
        """
        QThread.__init__(self)
        self._stop = False
        self._token = token
        self._timestamp = timestamp
        self._session = requests.Session()

    def run(self):
        """Runs Pushbullet thread."""
        while not self._stop:
            self._get_pushes()
            time.sleep(5)
        print("Pusbullet stopped")

    def stop(self):
        """Stops thread."""
        self._stop = True

    def _get_pushes(self):
        """Gets and emits new media added."""
        data = json.loads(self._get().text)
        try:
            timestamp = data["pushes"][0]["modified"]
            if timestamp != self._timestamp:
                self.update_timestamp.emit(timestamp)
                self._timestamp = timestamp
            else:
                return
        except IndexError:
            return None
        except KeyError:
            self._stop = True
            return None
        except Exception as e:
            exception_type = type(e).__name__
            print(exception_type)
            print(e)
            return None
        for push in data["pushes"]:
            if push["type"] == "file":
                self.media_received.emit(self._get_file_path(push["file_url"]))

    def _get_file_path(self, url):
        """Returns name of media.

        Keyword arguments:
        url -- URL from push.
        """
        try:
            row = ET.fromstring(self._session.get(url, headers={"Access-Token":self._token}).text)[1][2][1]
            data = [row[1].text, row[1].text, row[2].text]
            if " - S" in data[0]:
                data[0] = data[0][0:data[1].rfind(" - S")]
            elif " (" in data[0]:
                data[0] = data[0][0:data[1].rfind(" (")]
            return data
        except Exception as e:
            exception_type = type(e).__name__
            print("Unable to get media name.")
            print(exception_type)
            print(e)
            return None

    def _get(self):
        """Gets pushes.
        
        Keyword arguments:
        timestamp -- limits to pushes created after UNIX time
        """
        try:
            return self._session.get("https://api.pushbullet.com/v2/pushes?modified_after=" + str(self._timestamp), headers={"Access-Token":self._token})
        except Exception as e:
            exception_type = type(e).__name__
            if exception_type == "ConnectionError":
                print("Host unreachable!")
            else:
                print(exception_type)
                print(e)
            return None
