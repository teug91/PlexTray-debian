#!/usr/bin/python3

import requests, webbrowser, time, urllib
import xml.etree.ElementTree as ET
from PySide2.QtCore import Signal, QThread

class Plex(QThread):
    '''Communicates with PMS.'''

    available = Signal(bool)

    def __init__(self, host, token):
        '''Initializes Plex class.'''
        QThread.__init__(self)
        self._stop = False
        if not host.endswith("/"):
            host += "/"
        self._host = host
        self._token = "X-Plex-Token=" + token
        self._session = requests.Session()

    def run(self):
        """Runs Plex thread."""
        status = None
        while not self._stop:
            available = self._is_available()
            if status != available:
                self.available.emit(available)
            time.sleep(3)

    def stop(self):
        """Stops thread."""
        self._stop = True

    def open_media(self, file_path):
        """Open the Plex web site for the media in browser.
        
        Keyword arguments:
        media_name -- media name
        """
        print(file_path)
        libraries = self._get_libraries()
        base_media_url = self._get_base_media_url()
        if not libraries or not base_media_url:
            return
        i = 0
        while i < 10:
            for library in libraries:
                media_key = self._get_media_key(library[0], library[1], file_path)
                if media_key:
                    webbrowser.open(base_media_url + media_key)
                    return
            i += 1
            time.sleep(1)
        print("Did not find media")

    def open_plex(self):
        """Opens PMS in browser."""
        webbrowser.open(self._host)

    def update_libraries(self):
        """Updates all libraries. Takes a long time for large libraries and could break collections."""
        libraries = self._get_libraries()
        if not libraries:
            return
        for library in libraries:
            self._get("library/sections/" + library[0] + "/refresh?force=1&")
    
    def _is_available(self):
        """Returns True if the PMS is avalaible."""
        try:
            return self._get("system/?").ok
        except Exception as e:
            exception_type = type(e).__name__
            print(exception_type)
            print(e)
            return False

    def _get_libraries(self):
        """Returns list of library keys."""
        try:
            children = ET.fromstring(self._get("library/sections/?").text).getchildren()
            libraries = list()
            for child in children:
                try:
                    libraries.append([child.attrib["key"], child.attrib["type"]])
                except Exception:
                    pass
            return libraries
        except Exception as e:
            exception_type = type(e).__name__
            print(exception_type)
            print(e)
            return None

    def _get_media_key(self, library_key, library_type, file_path):
        try:
            if library_type == "movie":
                video = ET.fromstring(self._get("library/sections/" + library_key + "/all?file=" + file_path + "&").text).find("Video")
                if video:
                    return video.attrib["ratingKey"]
            elif library_type == "show":
                for tv_show in ET.fromstring(self._get("library/sections/" + library_key + "/all?").text):
                    path = ET.fromstring(self._get("library/metadata/" + tv_show.attrib["ratingKey"] + "?").text).find("Directory").find("Location").attrib["path"]
                    if path in file_path:
                        return tv_show.attrib["ratingKey"]
        except Exception as e:
            exception_type = type(e).__name__
            print(exception_type)
            print(e)
            return None

    def _get_base_media_url(self):
        """Returns base URL for PMS media items."""
        try:
            return self._host + "web/index.html#!/server/" + ET.fromstring(self._get("?").text).attrib["machineIdentifier"] + "/details?key=%2Flibrary%2Fmetadata%2F"
        except Exception:
            return None

    def _get(self, command):
        """Returns respons from PMS."""
        try:
            return self._session.get(self._host + command + self._token)
        except Exception as e:
            exception_type = type(e).__name__
            if exception_type == "ConnectionError":
                print("Host unreachable!")
            else:
                print(exception_type)
                print(e)
            return None
