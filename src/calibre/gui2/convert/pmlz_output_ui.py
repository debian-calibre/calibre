# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/pmlz_output.ui'
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
        spacerItem = QtWidgets.QSpacerItem(20, 246, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.opt_inline_toc = QtWidgets.QCheckBox(Form)
        self.opt_inline_toc.setObjectName("opt_inline_toc")
        self.gridLayout.addWidget(self.opt_inline_toc, 2, 0, 1, 1)
        self.opt_full_image_depth = QtWidgets.QCheckBox(Form)
        self.opt_full_image_depth.setObjectName("opt_full_image_depth")
        self.gridLayout.addWidget(self.opt_full_image_depth, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.opt_pml_output_encoding = EncodingComboBox(Form)
        self.opt_pml_output_encoding.setEditable(True)
        self.opt_pml_output_encoding.setObjectName("opt_pml_output_encoding")
        self.horizontalLayout.addWidget(self.opt_pml_output_encoding)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.label.setBuddy(self.opt_pml_output_encoding)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_inline_toc.setText(_("&Inline TOC"))
        self.opt_full_image_depth.setText(_("Do not &reduce image size and depth"))
        self.label.setText(_("Output &encoding:"))

from calibre.gui2.widgets import EncodingComboBox
