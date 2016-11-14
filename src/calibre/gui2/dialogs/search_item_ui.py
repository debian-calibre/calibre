# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/search_item.ui'
#
# Created: Wed Nov  5 09:01:06 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 39)
        self.hboxlayout = QtWidgets.QHBoxLayout(Form)
        self.hboxlayout.setObjectName("hboxlayout")
        self.field = QtWidgets.QComboBox(Form)
        self.field.setObjectName("field")
        self.hboxlayout.addWidget(self.field)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.text = QtWidgets.QLineEdit(Form)
        self.text.setObjectName("text")
        self.hboxlayout.addWidget(self.text)
        self.negate = QtWidgets.QCheckBox(Form)
        self.negate.setObjectName("negate")
        self.hboxlayout.addWidget(self.negate)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("contains"))
        self.text.setToolTip(_("The text to search for. It is interpreted as a regular expression."))
        self.negate.setToolTip(_("<p>Negate this match. That is, only return results that <b>do not</b> match this query."))
        self.negate.setText(_("Negate"))

