#!/usr/bin/python3

########################################################################################################################################################
#   From user user763305, Stackoverflow. See https://stackoverflow.com/questions/12712360/qtsingleapplication-for-pyside-or-pyqt
#
#   Note: This license has also been called the "Simplified BSD License" and the "FreeBSD License". See also the 3-clause BSD License.
#   
#   Copyright <YEAR> <COPYRIGHT HOLDER>
#   
#   Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#   
#   1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#   
#   2.  Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#   
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#   INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY
#   OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
#   OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################################################################################################

from PySide2.QtNetwork import QLocalSocket, QLocalServer
from PySide2.QtWidgets import QApplication

class QtSingleApplication(QApplication):

    def __init__(self):
        super(QtSingleApplication, self).__init__()
        self._id = "/etc/PlexTray/socket"
        self._out_socket = QLocalSocket()
        self._out_socket.connectToServer(self._id)
        self._is_running = self._out_socket.waitForConnected()
        if not self._is_running:
            self._out_socket = None
            QLocalServer.removeServer(self._id)
            self._server = QLocalServer()
            self._server.listen(self._id)

    def is_running(self):
        return self._is_running
