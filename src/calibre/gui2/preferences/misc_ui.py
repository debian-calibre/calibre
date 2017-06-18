# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/preferences/misc.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(502, 314)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.opt_worker_limit = QtWidgets.QSpinBox(Form)
        self.opt_worker_limit.setMinimum(1)
        self.opt_worker_limit.setObjectName("opt_worker_limit")
        self.gridLayout.addWidget(self.opt_worker_limit, 0, 1, 1, 1)
        self.opt_enforce_cpu_limit = QtWidgets.QCheckBox(Form)
        self.opt_enforce_cpu_limit.setObjectName("opt_enforce_cpu_limit")
        self.gridLayout.addWidget(self.opt_enforce_cpu_limit, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.device_detection_button = QtWidgets.QPushButton(Form)
        self.device_detection_button.setObjectName("device_detection_button")
        self.gridLayout.addWidget(self.device_detection_button, 4, 0, 1, 2)
        self.user_defined_device_button = QtWidgets.QPushButton(Form)
        self.user_defined_device_button.setObjectName("user_defined_device_button")
        self.gridLayout.addWidget(self.user_defined_device_button, 5, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 10, 0, 1, 1)
        self.button_open_config_dir = QtWidgets.QPushButton(Form)
        self.button_open_config_dir.setObjectName("button_open_config_dir")
        self.gridLayout.addWidget(self.button_open_config_dir, 9, 0, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 1000, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 22, 0, 1, 1)
        self.proxies = QtWidgets.QLabel(Form)
        self.proxies.setText("")
        self.proxies.setObjectName("proxies")
        self.gridLayout.addWidget(self.proxies, 11, 0, 1, 2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.opt_worker_max_time = QtWidgets.QSpinBox(Form)
        self.opt_worker_max_time.setMaximum(100000)
        self.opt_worker_max_time.setSingleStep(10)
        self.opt_worker_max_time.setObjectName("opt_worker_max_time")
        self.gridLayout.addWidget(self.opt_worker_max_time, 3, 1, 1, 1)
        self.icon_theme_button = QtWidgets.QPushButton(Form)
        self.icon_theme_button.setObjectName("icon_theme_button")
        self.gridLayout.addWidget(self.icon_theme_button, 8, 0, 1, 2)
        self.label_5.setBuddy(self.opt_worker_limit)
        self.label.setBuddy(self.opt_worker_max_time)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label_5.setText(_("Max. simultaneous conversion/&news download/plugin jobs:"))
        self.opt_enforce_cpu_limit.setText(_("Limit the max. simultaneous jobs to the available CPU &cores"))
        self.device_detection_button.setText(_("Debug &device detection"))
        self.user_defined_device_button.setText(_("Get information to setup the &user defined device"))
        self.button_open_config_dir.setText(_("Open calibre &configuration directory"))
        self.label.setText(_("Abort &jobs that take more than:"))
        self.opt_worker_max_time.setSpecialValueText(_("Never abort"))
        self.opt_worker_max_time.setSuffix(_(" minutes"))
        self.icon_theme_button.setText(_("Create a calibre &icon theme"))

