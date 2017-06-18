# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/smartdevice.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(612, 226)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("devices/tablet.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridlayout = QtWidgets.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")
        self.msg = QtWidgets.QLabel(Dialog)
        self.msg.setMinimumSize(QtCore.QSize(600, 0))
        self.msg.setStyleSheet("QLabel { margin-bottom: 1ex; }")
        self.msg.setWordWrap(True)
        self.msg.setOpenExternalLinks(True)
        self.msg.setObjectName("msg")
        self.gridlayout.addWidget(self.msg, 0, 0, 1, 3)
        self.label_23 = QtWidgets.QLabel(Dialog)
        self.label_23.setObjectName("label_23")
        self.gridlayout.addWidget(self.label_23, 1, 0, 1, 1)
        self.ip_addresses = QtWidgets.QLabel(Dialog)
        self.ip_addresses.setWordWrap(True)
        self.ip_addresses.setObjectName("ip_addresses")
        self.gridlayout.addWidget(self.ip_addresses, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.password_box = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_box.sizePolicy().hasHeightForWidth())
        self.password_box.setSizePolicy(sizePolicy)
        self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_box.setObjectName("password_box")
        self.gridlayout.addWidget(self.password_box, 2, 1, 1, 1)
        self.show_password = QtWidgets.QCheckBox(Dialog)
        self.show_password.setObjectName("show_password")
        self.gridlayout.addWidget(self.show_password, 2, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setObjectName("label_21")
        self.gridlayout.addWidget(self.label_21, 4, 0, 1, 1)
        self.fixed_port = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fixed_port.sizePolicy().hasHeightForWidth())
        self.fixed_port.setSizePolicy(sizePolicy)
        self.fixed_port.setObjectName("fixed_port")
        self.gridlayout.addWidget(self.fixed_port, 4, 1, 1, 1)
        self.use_fixed_port = QtWidgets.QCheckBox(Dialog)
        self.use_fixed_port.setObjectName("use_fixed_port")
        self.gridlayout.addWidget(self.use_fixed_port, 4, 2, 1, 1)
        self.autostart_box = QtWidgets.QCheckBox(Dialog)
        self.autostart_box.setObjectName("autostart_box")
        self.gridlayout.addWidget(self.autostart_box, 6, 0, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 10, 0, 1, 3)
        self.label_2.setBuddy(self.password_box)
        self.label_21.setBuddy(self.fixed_port)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Smart device control"))
        self.msg.setText(_("<p>Start wireless device connections. Currently used only\n"
"       by <a href=\"http://www.multipie.co.uk/calibre-companion/\">Calibre Companion</a>.\n"
"       <p>You may see some messages from your computer\'s firewall or anti-virus manager asking you if it is OK for calibre to connect to the network. <b>Please answer yes</b>. If you do not, wireless connections will not work."))
        self.label_23.setText(_("calibre IP addresses:"))
        self.ip_addresses.setText(_("Possibe IP addresses:"))
        self.label_2.setText(_("Optional &password:"))
        self.password_box.setPlaceholderText(_("Optional password for security"))
        self.show_password.setText(_("&Show password"))
        self.label_21.setText(_("Optional &fixed port:"))
        self.fixed_port.setPlaceholderText(_("Optional port number"))
        self.use_fixed_port.setText(_("&Use a fixed port"))
        self.autostart_box.setText(_("&Automatically allow connections at calibre startup"))


