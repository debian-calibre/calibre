# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/confirm_delete_location.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(459, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("dialog_warning.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setPixmap(QtGui.QPixmap(I("dialog_warning.png")))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.msg = QtWidgets.QLabel(Dialog)
        self.msg.setText("")
        self.msg.setWordWrap(True)
        self.msg.setObjectName("msg")
        self.horizontalLayout.addWidget(self.msg)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_lib = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("lt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_lib.setIcon(icon1)
        self.button_lib.setObjectName("button_lib")
        self.horizontalLayout_2.addWidget(self.button_lib)
        self.button_device = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(I("reader.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_device.setIcon(icon2)
        self.button_device.setObjectName("button_device")
        self.horizontalLayout_2.addWidget(self.button_device)
        self.button_both = QtWidgets.QPushButton(Dialog)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(I("trash.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_both.setIcon(icon3)
        self.button_both.setObjectName("button_both")
        self.horizontalLayout_2.addWidget(self.button_both)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Where do you want to delete from?"))
        self.button_lib.setText(_("Library"))
        self.button_device.setText(_("Device"))
        self.button_both.setText(_("Library and device"))


