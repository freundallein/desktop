# -*- coding: utf-8 -*-
from PyQt5.QtCore import QStringListModel, QObject, QRegExp
from PyQt5.QtGui import QFont, QDoubleValidator, QValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QLabel, QScrollArea, QFormLayout, QLineEdit, QCompleter
from PyQt5.Qt import Qt


class WidgetCaptain(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def get_completer(self, fieldname):
        completer = QCompleter()
        model = QStringListModel()
        model.setStringList(["any", "word", "you", "want", "here"])
        completer.setModel(model)
        return completer

    def get_validator(self, fieldname):
        if fieldname == 'phone':
            regexp = QRegExp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
            return QRegExpValidator(regexp)
        elif fieldname == 'email':
            regexp = QRegExp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.['
                             'a-zA-Z0-9-.]+we$')
            return QRegExpValidator(regexp)
        else:
            pass

    def check_state(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        if validator:
            state = validator.validate(sender.text(), 0)[0]
            if state == QValidator.Acceptable:
                color = '#c4df9b'  # green
            elif state == QValidator.Intermediate:
                color = '#fff79a'  # yellow
            else:
                color = '#f6989d'  # red
            sender.setStyleSheet("background-image: url(0);"
                                   "background-color: %s;"
                                   "padding: 0 0 0 0" % color)

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
        layout.setSpacing(3)
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
                                 "border-radius: 15px; border-style: outset;"
                                 "border-width: 2px; border-color: grey;"
                                 "background-color: grey;"
                                 "background-image: url(0)")
            button.clicked.connect(self.view.type_button_clicked)
            layout.addWidget(button, n + 2, 1)
        return widget

    def get_form_screen(self, data):
        form = data.get('form', {})
        fields = form.get('fields')
        mandatory = form.get('mandatory')

        widget = QWidget(self.view)
        widget.setStyleSheet("background-image: url("
                             "static/main_background.jpg);")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        font = QFont("Times")
        font.setPixelSize(38)
        title = QLabel('Fill that form to achieve card:')
        title.setFont(font)
        title.setAlignment(Qt.AlignBottom)
        title.setStyleSheet("background-image: url(0);"
                            "padding: 100 0 0 50;")
        layout.addWidget(title, 0, 1)

        back_button = QPushButton()
        back_button.setText('Back')
        back_button.setFont(font)
        back_button.setStyleSheet("background-image: url(0);"
                                  "margin-left: 5px;"
                                  "padding: 100 30 100 30;"
                                  "background-color: grey;")
        back_button.clicked.connect(
            lambda: self.view.switch_screen('CARD_TYPE'))
        forward_button = QPushButton()
        forward_button.setFont(font)
        forward_button.setText('Confirm')
        forward_button.setStyleSheet("background-image: url(0);"
                                     "padding: 50 50 50 50;"
                                     "background-color: grey;")

        layout.addWidget(back_button, 1, 0)
        layout.addWidget(forward_button, 2, 2, 1, 3)

        scroll = QScrollArea(self.view)
        scroll.setStyleSheet("background-image: url(0);"
                             "background-color: rgba(0,0,0,0);"
                             "padding: 50 50 50 50;")
        layout.addWidget(scroll, 1, 1, 1, 6)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QFormLayout(scrollContent)
        for field in fields:
            font = QFont("Times")
            font.setPixelSize(48)
            label = QLabel(field)
            label.setFont(font)
            label.setStyleSheet("background-image: url(0);"
                                # "background-color: rgba(0,0,0,0);"
                                "padding: 0 0 0 0")
            edit = QLineEdit()
            completer = self.get_completer(field)
            validator = self.get_validator(field)
            edit.setCompleter(completer)
            edit.setValidator(validator)
            edit.setFont(font)
            edit.setStyleSheet("background-image: url(0);"
                               "background-color: white;"
                               "padding: 0 0 0 0")
            edit.textChanged.connect(self.check_state)
            scrollLayout.addRow(label, edit)
        scrollLayout.setAlignment(Qt.AlignCenter)
        scrollLayout.setSpacing(20)
        scrollContent.setLayout(scrollLayout)
        scroll.setWidget(scrollContent)

        widget.setLayout(layout)
        return widget

    def get_wait_screen(self, data):
        pass

    def get_thanks_screen(self, data):
        pass
