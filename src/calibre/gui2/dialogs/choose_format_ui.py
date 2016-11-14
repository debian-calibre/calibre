# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/choose_format.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChooseFormatDialog(object):
    def setupUi(self, ChooseFormatDialog):
        ChooseFormatDialog.setObjectName("ChooseFormatDialog")
        ChooseFormatDialog.resize(507, 377)
        icon = QtGui.QIcon()
        icon.addFile(I("mimetypes/unknown.png"))
        ChooseFormatDialog.setWindowIcon(icon)
        self.vboxlayout = QtWidgets.QVBoxLayout(ChooseFormatDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.msg = QtWidgets.QLabel(ChooseFormatDialog)
        self.msg.setObjectName("msg")
        self.vboxlayout.addWidget(self.msg)
        self.formats = QtWidgets.QListWidget(ChooseFormatDialog)
        self.formats.setIconSize(QtCore.QSize(64, 64))
        self.formats.setObjectName("formats")
        self.vboxlayout.addWidget(self.formats)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChooseFormatDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ChooseFormatDialog)
        self.buttonBox.accepted.connect(ChooseFormatDialog.accept)
        self.buttonBox.rejected.connect(ChooseFormatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChooseFormatDialog)

    def retranslateUi(self, ChooseFormatDialog):

        ChooseFormatDialog.setWindowTitle(_("Choose Format"))
        self.msg.setText(_("TextLabel"))


