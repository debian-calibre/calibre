# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/catalog/catalog_csv_xml.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(579, 411)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.db_fields = QtWidgets.QListWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.db_fields.sizePolicy().hasHeightForWidth())
        self.db_fields.setSizePolicy(sizePolicy)
        self.db_fields.setToolTip("")
        self.db_fields.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.db_fields.setObjectName("db_fields")
        self.gridLayout.addWidget(self.db_fields, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label_6.setText(_("Fields to include in output:"))

