# -*- coding: utf-8 -*-
import sys
import PyQt5.Qt as Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, \
    QGridLayout, QButtonGroup, QAbstractButton, QPushButton, QVBoxLayout

from remote.service import RemoteService
from utils import Configurator


class Application(QWidget):
    DEBUG = False
    send_data = pyqtSignal(dict)
    get_data = pyqtSignal(str)
    MACHINE_STATUS = False

    def __init__(self, config):
        super().__init__()
        self.DEBUG = config.debug
        self.start()

    def setup_UI(self):
        # self.setFixedSize(1920, 1080)
        self.layout = QVBoxLayout(self)
        # self.layout.setFixedWidth(80)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def clean_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    def start(self):
        self.setup_UI()
        self.start_standby_screen()
        self.start_services()

    def start_services(self):
        self.remote_thread = RemoteService(self, config)
        self.send_data.connect(self.remote_thread.send_data)
        self.get_data.connect(self.remote_thread.get_data)
        self.remote_thread.data_received.connect(self.on_data_received)
        self.remote_thread.statusOK.connect(self.on_status_OK)
        self.remote_thread.statusSTANDBY.connect(self.on_status_STANDBY)
        self.remote_thread.start()

    def start_GUI(self):
        self.clean_layout()
        self.setWindowTitle('Main Screen')
        self.setStyleSheet("""
            color: white; 
            background-image: url(./static/main_background.jpg);
            background-attachment: scroll;
        """)
        self.get_data.emit('types')

    def start_standby_screen(self):
        self.clean_layout()
        self.setWindowTitle('Loading Screen')
        image = QPixmap('static/standby.jpg')
        background_pic = QLabel()
        background_pic.setPixmap(image)
        self.layout.addWidget(background_pic)
        self.show()

    def draw_card_types(self, data):
        header = QLabel('Choose card type:')
        self.layout.addWidget(header)
        # self.layout.setSpacing(5)
        for card_type in data.get('types'):
            button = QPushButton()
            button.setText(card_type)
            self.layout.addWidget(button)

    def on_data_received(self, data):
        if data.get('types'):
            self.draw_card_types(data)

    def on_status_OK(self):
        if not self.MACHINE_STATUS:
            self.MACHINE_STATUS = True
            self.start_GUI()
        else:
            pass

    def on_status_STANDBY(self):
        self.MACHINE_STATUS = False
        self.start_standby_screen()

    def show(self):
        if self.DEBUG:
            # qtRectangle = QDesktopWidget().screenGeometry()
            # centerPoint = QDesktopWidget().availableGeometry().center()
            # qtRectangle.moveCenter(centerPoint)
            # self.move(qtRectangle.topLeft())
            # self.resize(qtRectangle.width(), qtRectangle.height())
            super().show()
        else:
            super().showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = Configurator().get_config()
    main = Application(config)
    sys.exit(app.exec_())
