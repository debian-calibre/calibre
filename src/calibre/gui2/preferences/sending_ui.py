# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/preferences/sending.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(807, 331)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.mm_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mm_label.sizePolicy().hasHeightForWidth())
        self.mm_label.setSizePolicy(sizePolicy)
        self.mm_label.setObjectName("mm_label")
        self.gridLayout.addWidget(self.mm_label, 0, 0, 1, 1)
        self.opt_manage_device_metadata = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.opt_manage_device_metadata.sizePolicy().hasHeightForWidth())
        self.opt_manage_device_metadata.setSizePolicy(sizePolicy)
        self.opt_manage_device_metadata.setObjectName("opt_manage_device_metadata")
        self.opt_manage_device_metadata.addItem("")
        self.opt_manage_device_metadata.addItem("")
        self.opt_manage_device_metadata.addItem("")
        self.gridLayout.addWidget(self.opt_manage_device_metadata, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(457, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_41 = QtWidgets.QLabel(Form)
        self.label_41.setWordWrap(True)
        self.label_41.setObjectName("label_41")
        self.gridLayout.addWidget(self.label_41, 1, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.opt_send_timefmt = QtWidgets.QLineEdit(Form)
        self.opt_send_timefmt.setObjectName("opt_send_timefmt")
        self.gridLayout.addWidget(self.opt_send_timefmt, 2, 1, 1, 1)
        self.send_template = SaveTemplate(Form)
        self.send_template.setObjectName("send_template")
        self.gridLayout.addWidget(self.send_template, 3, 0, 1, 3)
        self.mm_label.setBuddy(self.opt_manage_device_metadata)
        self.label_2.setBuddy(self.opt_send_timefmt)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.mm_label.setText(_("Me&tadata management:"))
        self.opt_manage_device_metadata.setItemText(0, _("Manual management"))
        self.opt_manage_device_metadata.setItemText(1, _("Only on send"))
        self.opt_manage_device_metadata.setItemText(2, _("Automatic management"))
        self.label_41.setText(_("<li><b>Manual management</b>: calibre updates the metadata and adds collections only when a book is sent. With this option, calibre will never remove a collection.</li>\n"
"<li><b>Only on send</b>: calibre updates metadata and adds/removes collections for a book only when it is sent to the device. </li>\n"
"<li><b>Automatic management</b>: calibre automatically keeps metadata on the device in sync with the calibre library, on every connect</li></ul>"))
        self.label_2.setText(_("Format &dates as:"))

from calibre.gui2.preferences.save_template import SaveTemplate
