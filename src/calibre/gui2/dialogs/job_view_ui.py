# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/job_view.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(664, 462)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("view.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.log = QtWidgets.QPlainTextEdit(Dialog)
        self.log.setUndoRedoEnabled(False)
        self.log.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.gridLayout.addWidget(self.log, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.tb = QtWidgets.QTextBrowser(Dialog)
        self.tb.setObjectName("tb")
        self.gridLayout.addWidget(self.tb, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Details of job"))


