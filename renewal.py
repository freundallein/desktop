# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from remote.service import RemoteService
from captain import WidgetCaptain
from utils import Configurator


class Application(QMainWindow):
    get_from_server = pyqtSignal(dict)
    post_to_server = pyqtSignal(dict)
    status = pyqtSignal(str)
    MACHINE_STATUS = False

    def __init__(self, config):
        super().__init__()
        self.DEBUG = config.debug
        self.widget_captain = WidgetCaptain(self)
        self.data = {}
        self.setup_ui()
        self.start_remote_service()

    def get_screen_resolution(self):
        screen = QDesktopWidget().screenGeometry()
        return screen.width(), screen.height()

    def setup_ui(self):
        self.setWindowTitle('Main Screen')
        self.width, self.height = self.get_screen_resolution()
        self.resize(self.width, self.height)
        self.switch_screen('STANDBY')

    def on_status_change(self, status):
        if status == 'STANDBY':
            self.MACHINE_STATUS = False
            self.switch_screen('STANDBY')
        else:
            if not self.MACHINE_STATUS:
                self.MACHINE_STATUS = True
                self.get_from_server.emit({'data': 'types'})
                self.switch_screen('CARD_TYPE')

    def type_button_clicked(self):
        card_type = self.sender().text()
        self.get_from_server.emit({'data': 'form',
                                   'card_type': card_type})

    def on_data_received(self, data):
        self.data.update(data)
        datatype = list(data.keys())[0]
        if datatype == 'types':
            self.switch_screen('CARD_TYPE')
        if datatype == 'form':
            self.switch_screen('FORM')

    def switch_screen(self, screen_type):
        screen = self.widget_captain.get_screen(screen_type, self.data)
        self.setCentralWidget(screen)
        # self.current_screen = screen_type

    def start_remote_service(self):
        self.remote_thread = RemoteService(self, config)
        self.get_from_server.connect(self.remote_thread.get_data)
        self.post_to_server.connect(self.remote_thread.send_data)
        self.remote_thread.data_received.connect(self.on_data_received)
        self.remote_thread.status_changed.connect(self.on_status_change)
        self.remote_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = Configurator().get_config()
    main = Application(config)
    if config.debug:
        main.show()
    else:
        main.showFullScreen()
    sys.exit(app.exec_())
