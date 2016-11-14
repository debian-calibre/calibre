# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/message_box.ui'
#
# Created: Sun Nov 16 11:57:57 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(497, 235)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.icon_label = QtWidgets.QLabel(Dialog)
        self.icon_label.setMaximumSize(QtCore.QSize(68, 68))
        self.icon_label.setText("")
        self.icon_label.setPixmap(QtGui.QPixmap(I("dialog_warning.png")))
        self.icon_label.setScaledContents(True)
        self.icon_label.setObjectName("icon_label")
        self.gridLayout.addWidget(self.icon_label, 0, 0, 1, 1)
        self.msg = QtWidgets.QLabel(Dialog)
        self.msg.setText("")
        self.msg.setWordWrap(True)
        self.msg.setOpenExternalLinks(True)
        self.msg.setObjectName("msg")
        self.gridLayout.addWidget(self.msg, 0, 1, 1, 1)
        self.det_msg = QtWidgets.QPlainTextEdit(Dialog)
        self.det_msg.setReadOnly(True)
        self.det_msg.setObjectName("det_msg")
        self.gridLayout.addWidget(self.det_msg, 1, 0, 1, 2)
        self.bb = QtWidgets.QDialogButtonBox(Dialog)
        self.bb.setOrientation(QtCore.Qt.Horizontal)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.gridLayout.addWidget(self.bb, 3, 0, 1, 2)
        self.toggle_checkbox = QtWidgets.QCheckBox(Dialog)
        self.toggle_checkbox.setText("")
        self.toggle_checkbox.setObjectName("toggle_checkbox")
        self.gridLayout.addWidget(self.toggle_checkbox, 2, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.bb.accepted.connect(Dialog.accept)
        self.bb.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Dialog"))


