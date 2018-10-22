#!/usr/bin/python

import time # REMOVE
from shared import resource_path
from PySide2.QtWidgets import (QWidget, QLineEdit, QPushButton, QApplication, QFormLayout, QVBoxLayout, QGridLayout, QDialog, QComboBox, QLabel, QCheckBox, QPushButton, QSizePolicy, QGroupBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, Qt

class Settings_Window(QDialog):
    """Settings window."""

    save_clicked = Signal(list)

    def __init__(self, plex_host, plex_token, pushbullet_token):
        """Initiates SettingsWindow.

        Keyword arguments:
        plex_host -- PMS host
        plex_token -- PMS token
        pushbullet_token -- Pushbullet token
        """
        super(Settings_Window, self).__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.plex_host = QLineEdit()
        if plex_host:
            self.plex_host.setText(plex_host)
        self.plex_host.setToolTip("Example: http://192.168.1.100:32400")
        self.plex_token = QLineEdit()
        if plex_token:
            self.plex_token.setText(plex_token)
        self.plex_token.setToolTip("Plex token")
        self.pushbullet_token = QLineEdit()
        if pushbullet_token:
            self.pushbullet_token.setText(pushbullet_token)
        self.pushbullet_token.setToolTip("Pushbullet token")

        plex_layout = QFormLayout()
        plex_layout.addRow("Host:", self.plex_host)
        plex_layout.addRow("Token:", self.plex_token)
        plex_box = QGroupBox("Plex")
        plex_box.setLayout(plex_layout)

        pushbullet_layout = QFormLayout()
        pushbullet_layout.addRow("Token:", self.pushbullet_token)
        pushbullet_box = QGroupBox("Pushbullet")
        pushbullet_box.setLayout(pushbullet_layout)

        bottom_grid_layout = QGridLayout()
        bottom_grid_layout.setRowMinimumHeight(0, 60)
        bottom_grid_layout.setColumnMinimumWidth(0, 300)
        bottom_grid_layout.setColumnStretch(1, 1)

        bottom_grid_layout.addWidget(QWidget(), 1, 0)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self._save_click)
        bottom_grid_layout.addWidget(save_button, 1, 2)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self._cancel_click)
        bottom_grid_layout.addWidget(cancel_button, 1, 3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(plex_box)
        space = QGridLayout()
        space.setRowMinimumHeight(0, 20)
        main_layout.addLayout(space)
        main_layout.addWidget(pushbullet_box)
        main_layout.addStretch(2)
        main_layout.addLayout(bottom_grid_layout)

        self.setLayout(main_layout)
        self.setWindowIcon(QIcon(resource_path("plex.png")))
        self.setWindowTitle("PlexTray settings")
        self.show()

    def _cancel_click(self):
        """When cancel has been clicked."""
        self.hide()
        self.close()

    def _save_click(self):
        """When save has been clicked."""
        values = [self.plex_host.text(), self.plex_token.text(), self.pushbullet_token.text()]
        self.save_clicked.emit(values)
        self.hide()
        self.close()
