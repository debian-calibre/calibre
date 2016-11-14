# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/confirm_delete.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(439, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("dialog_warning.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setPixmap(QtGui.QPixmap(I("dialog_warning.png")))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.msg = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msg.sizePolicy().hasHeightForWidth())
        self.msg.setSizePolicy(sizePolicy)
        self.msg.setMinimumSize(QtCore.QSize(300, 0))
        self.msg.setWordWrap(True)
        self.msg.setObjectName("msg")
        self.horizontalLayout.addWidget(self.msg)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.again = QtWidgets.QCheckBox(Dialog)
        self.again.setChecked(True)
        self.again.setObjectName("again")
        self.gridLayout.addWidget(self.again, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Are you sure?"))
        self.msg.setText(_("TextLabel"))
        self.again.setText(_("&Show this warning again"))


