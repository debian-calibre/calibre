# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/htmlz_output.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(438, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 246, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.opt_htmlz_class_style = QtWidgets.QComboBox(Form)
        self.opt_htmlz_class_style.setObjectName("opt_htmlz_class_style")
        self.gridLayout.addWidget(self.opt_htmlz_class_style, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.opt_htmlz_css_type = QtWidgets.QComboBox(Form)
        self.opt_htmlz_css_type.setMinimumContentsLength(20)
        self.opt_htmlz_css_type.setObjectName("opt_htmlz_css_type")
        self.gridLayout.addWidget(self.opt_htmlz_css_type, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.opt_htmlz_title_filename = QtWidgets.QCheckBox(Form)
        self.opt_htmlz_title_filename.setObjectName("opt_htmlz_title_filename")
        self.gridLayout.addWidget(self.opt_htmlz_title_filename, 2, 0, 1, 2)
        self.label.setBuddy(self.opt_htmlz_css_type)
        self.label_2.setBuddy(self.opt_htmlz_class_style)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("How to handle &CSS"))
        self.label_2.setText(_("How to handle class &based CSS"))
        self.opt_htmlz_title_filename.setText(_("Use book &title as the filename for the HTML file inside the archive"))

