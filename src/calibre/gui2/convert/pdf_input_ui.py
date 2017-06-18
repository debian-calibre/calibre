# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/pdf_input.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 213, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.opt_unwrap_factor = QtWidgets.QDoubleSpinBox(Form)
        self.opt_unwrap_factor.setMaximum(1.0)
        self.opt_unwrap_factor.setSingleStep(0.01)
        self.opt_unwrap_factor.setProperty("value", 0.45)
        self.opt_unwrap_factor.setObjectName("opt_unwrap_factor")
        self.gridLayout.addWidget(self.opt_unwrap_factor, 0, 1, 1, 1)
        self.opt_no_images = QtWidgets.QCheckBox(Form)
        self.opt_no_images.setObjectName("opt_no_images")
        self.gridLayout.addWidget(self.opt_no_images, 1, 0, 1, 1)
        self.label_2.setBuddy(self.opt_unwrap_factor)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label_2.setText(_("Line &un-wrapping factor:"))
        self.opt_no_images.setText(_("No &images"))

