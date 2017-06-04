# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/store/web_store_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(962, 656)
        Dialog.setWindowTitle("")
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.view = NPWebView(self.frame)
        self.view.setUrl(QtCore.QUrl("about:blank"))
        self.view.setObjectName("view")
        self.verticalLayout.addWidget(self.view)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 5)
        self.home = QtWidgets.QPushButton(Dialog)
        self.home.setObjectName("home")
        self.gridLayout.addWidget(self.home, 1, 0, 1, 1)
        self.reload = QtWidgets.QPushButton(Dialog)
        self.reload.setObjectName("reload")
        self.gridLayout.addWidget(self.reload, 1, 1, 1, 1)
        self.progress = QtWidgets.QProgressBar(Dialog)
        self.progress.setProperty("value", 0)
        self.progress.setObjectName("progress")
        self.gridLayout.addWidget(self.progress, 1, 3, 1, 1)
        self.back = QtWidgets.QPushButton(Dialog)
        self.back.setObjectName("back")
        self.gridLayout.addWidget(self.back, 1, 2, 1, 1)
        self.close = QtWidgets.QPushButton(Dialog)
        self.close.setObjectName("close")
        self.gridLayout.addWidget(self.close, 1, 4, 1, 1)

        self.retranslateUi(Dialog)
        self.close.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        self.home.setText(_("Home"))
        self.reload.setText(_("Reload"))
        self.progress.setFormat(_("%p%"))
        self.back.setText(_("Back"))
        self.close.setText(_("&Close"))

from calibre.gui2.store.web_control import NPWebView
