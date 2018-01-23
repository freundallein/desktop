# -*- coding: utf-8 -*-
import sys
import PyQt5.Qt as Qt
from PyQt5.QtCore import pyqtSignal, QRect, QSize
from PyQt5.QtGui import QPixmap, QFont, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, \
    QVBoxLayout, QGridLayout, QGroupBox, QFormLayout, QScrollArea, QMainWindow, \
    QLineEdit

from remote.service import RemoteService
from utils import Configurator


class Application(QMainWindow):
    DEBUG = False
    send_data = pyqtSignal(dict)
    get_data = pyqtSignal(dict)
    MACHINE_STATUS = False

    def __init__(self, config):
        super().__init__()
        self.DEBUG = config.debug
        self.start()

    def setup_UI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        self.layout = QGridLayout(self)
        widget.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        oImage = QImage("static/main_background.jpg")
        palette = QPalette()
        palette.setBrush(10, QBrush(oImage))  # 10 = Windowrole
        self.setPalette(palette)
        self.show()

    def clean_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def start(self):
        self.setup_UI()
        # self.start_standby_screen()
        # self.start_services()

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
        self.get_data.emit({'data': 'types'})

    def start_standby_screen(self):
        self.clean_layout()
        self.setWindowTitle('Loading Screen')
        image = QPixmap('static/standby.jpg')
        background_pic = QLabel()
        background_pic.setPixmap(image)
        self.layout.addWidget(background_pic)
        self.show()

    def draw_form(self, data):
        self.clean_layout()
        form_widget = QWidget(self)
        self.setCentralWidget(form_widget)

        fields = data.get('fields')
        listBox = QVBoxLayout(self)
        form_widget.setLayout(listBox)

        scroll = QScrollArea(self)
        listBox.addWidget(scroll)
        listBox.addWidget(QPushButton('Back'))
        listBox.addWidget(QPushButton('Forward'))
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QFormLayout(scrollContent)
        for field in fields:
            scrollLayout.addRow(QLabel(field), QLineEdit())
        scrollContent.setLayout(scrollLayout)
        scroll.setWidget(scrollContent)

    def draw_card_types(self, data):
        types = data.get('types', [])
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(3, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(len(types) + 2, 1)
        self.layout.setSpacing(1)
        font = QFont("Times")
        font.setPixelSize(28)
        header = QLabel('Choose card type:')
        header.setFont(font)
        header.setAlignment(Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        header.setStyleSheet("padding-left: 350px; padding-right: 350px;"
                             "padding-top: 30px; padding-bottom: 30px;")
        self.layout.addWidget(header, 1, 1)
        for n, card_type in enumerate(types):
            button = QPushButton()
            button.setText(card_type)
            button.setFont(font)
            button.setStyleSheet("padding-left: 350px; padding-right: 350px;"
                                 "padding-top: 30px; padding-bottom: 30px;"
                                 "background-color: grey")
            button.clicked.connect(self.type_button_clicked)
            self.layout.addWidget(button, n + 2, 1)

    def type_button_clicked(self):
        card_type = self.sender().text()
        self.get_data.emit({'data': 'form',
                            'card_type': card_type})

    def on_data_received(self, data):
        if data.get('types'):
            self.draw_card_types(data)
        if data.get('fields'):
            self.draw_form(data)

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
