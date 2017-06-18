# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/choose_format_device.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChooseFormatDeviceDialog(object):
    def setupUi(self, ChooseFormatDeviceDialog):
        ChooseFormatDeviceDialog.setObjectName("ChooseFormatDeviceDialog")
        ChooseFormatDeviceDialog.resize(507, 377)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("mimetypes/unknown.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ChooseFormatDeviceDialog.setWindowIcon(icon)
        self.vboxlayout = QtWidgets.QVBoxLayout(ChooseFormatDeviceDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.msg = QtWidgets.QLabel(ChooseFormatDeviceDialog)
        self.msg.setText("")
        self.msg.setObjectName("msg")
        self.vboxlayout.addWidget(self.msg)
        self.formats = QtWidgets.QTreeWidget(ChooseFormatDeviceDialog)
        self.formats.setAlternatingRowColors(True)
        self.formats.setIconSize(QtCore.QSize(64, 64))
        self.formats.setAllColumnsShowFocus(True)
        self.formats.setObjectName("formats")
        self.formats.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.vboxlayout.addWidget(self.formats)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChooseFormatDeviceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ChooseFormatDeviceDialog)
        self.buttonBox.accepted.connect(ChooseFormatDeviceDialog.accept)
        self.buttonBox.rejected.connect(ChooseFormatDeviceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChooseFormatDeviceDialog)

    def retranslateUi(self, ChooseFormatDeviceDialog):

        ChooseFormatDeviceDialog.setWindowTitle(_("Choose format"))
        self.formats.headerItem().setText(0, _("Format"))
        self.formats.headerItem().setText(1, _("Existing"))
        self.formats.headerItem().setText(2, _("Convertible"))


