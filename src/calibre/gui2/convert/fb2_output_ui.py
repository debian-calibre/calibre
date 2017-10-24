# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/fb2_output.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 246, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.opt_sectionize = QtWidgets.QComboBox(Form)
        self.opt_sectionize.setMinimumContentsLength(20)
        self.opt_sectionize.setObjectName("opt_sectionize")
        self.gridLayout.addWidget(self.opt_sectionize, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.opt_fb2_genre = QtWidgets.QComboBox(Form)
        self.opt_fb2_genre.setObjectName("opt_fb2_genre")
        self.gridLayout.addWidget(self.opt_fb2_genre, 1, 1, 1, 1)
        self.label.setBuddy(self.opt_sectionize)
        self.label_2.setBuddy(self.opt_fb2_genre)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("&Sectionize:"))
        self.label_2.setText(_("&Genre:"))

