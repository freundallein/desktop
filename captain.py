# -*- coding: utf-8 -*-
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QDesktopWidget, \
    QLabel

from custom_types import PicButton


class WidgetCaptain:
    def __init__(self, view):
        self.view = view

    def get_screen(self, screen_type, data=None):
        if screen_type == 'STANDBY':
            return self.get_standby_screen()
        if screen_type == 'CARD_TYPE':
            return self.get_type_screen(data)
        if screen_type == 'FORM':
            return self.get_form_screen(data)
        if screen_type == 'WAIT':
            return self.get_wait_screen(data)
        if screen_type == 'THANKS':
            return self.get_wait_screen(data)

    def get_standby_screen(self):
        widget = QWidget(self.view)
        widget.setStyleSheet("background-image: url(static/standby.jpg);")
        # layout = QGridLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        # image = QPixmap('static/standby.jpg')
        # background_pic = QLabel()
        # background_pic.setPixmap(image)
        # layout.addWidget(background_pic)
        # widget.setLayout(layout)
        return widget

    def get_type_screen(self, data):
        types = data.get('types', [])

        widget = QWidget(self.view)
        widget.setStyleSheet("background-image: url("
                             "static/main_background.jpg);")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(3, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(len(types) + 2, 1)
        layout.setSpacing(1)
        font = QFont("Times")
        font.setPixelSize(28)
        header = QLabel('Choose card type:')
        header.setFont(font)
        header.setStyleSheet("padding-left: 350px; padding-right: 350px;"
                             "padding-top: 30px; padding-bottom: 30px;"
                             "background-image: url(0)")
        header.autoFillBackground()
        layout.addWidget(header, 1, 1)
        for n, card_type in enumerate(types):
            button = QPushButton()
            button.setText(card_type)
            button.setFont(font)
            button.setStyleSheet("padding-left: 350px; padding-right: 350px;"
                                 "padding-top: 30px; padding-bottom: 30px;"
                                 "background-color: rgba(0, 0, 0, 0);"
                                 "border-image: url(static/button.png)")
            button.clicked.connect(self.view.type_button_clicked)
            layout.addWidget(button, n + 2, 1)
        return widget

    def get_form_screen(self, data):
        print(data)

    def get_wait_screen(self, data):
        pass

    def get_thanks_screen(self, data):
        pass
