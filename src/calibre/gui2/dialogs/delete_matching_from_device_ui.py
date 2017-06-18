# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/delete_matching_from_device.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeleteMatchingFromDeviceDialog(object):
    def setupUi(self, DeleteMatchingFromDeviceDialog):
        DeleteMatchingFromDeviceDialog.setObjectName("DeleteMatchingFromDeviceDialog")
        DeleteMatchingFromDeviceDialog.resize(730, 342)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeleteMatchingFromDeviceDialog.sizePolicy().hasHeightForWidth())
        DeleteMatchingFromDeviceDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(DeleteMatchingFromDeviceDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.explanation = QtWidgets.QLabel(DeleteMatchingFromDeviceDialog)
        self.explanation.setObjectName("explanation")
        self.verticalLayout.addWidget(self.explanation)
        self.table = QtWidgets.QTableWidget(DeleteMatchingFromDeviceDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setColumnCount(0)
        self.table.setObjectName("table")
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.buttonBox = QtWidgets.QDialogButtonBox(DeleteMatchingFromDeviceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DeleteMatchingFromDeviceDialog)
        self.buttonBox.accepted.connect(DeleteMatchingFromDeviceDialog.accept)
        self.buttonBox.rejected.connect(DeleteMatchingFromDeviceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DeleteMatchingFromDeviceDialog)

    def retranslateUi(self, DeleteMatchingFromDeviceDialog):

        DeleteMatchingFromDeviceDialog.setWindowTitle(_("Delete from device"))

