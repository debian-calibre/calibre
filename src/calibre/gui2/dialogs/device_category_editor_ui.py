# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/device_category_editor.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceCategoryEditor(object):
    def setupUi(self, DeviceCategoryEditor):
        DeviceCategoryEditor.setObjectName("DeviceCategoryEditor")
        DeviceCategoryEditor.resize(397, 335)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("chapters.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DeviceCategoryEditor.setWindowIcon(icon)
        self.gridlayout = QtWidgets.QGridLayout(DeviceCategoryEditor)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = QtWidgets.QLabel(DeviceCategoryEditor)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.delete_button = QtWidgets.QToolButton(DeviceCategoryEditor)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("trash.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon1)
        self.delete_button.setIconSize(QtCore.QSize(32, 32))
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout_2.addWidget(self.delete_button)
        self.rename_button = QtWidgets.QToolButton(DeviceCategoryEditor)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(I("edit_input.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rename_button.setIcon(icon2)
        self.rename_button.setIconSize(QtCore.QSize(32, 32))
        self.rename_button.setObjectName("rename_button")
        self.verticalLayout_2.addWidget(self.rename_button)
        self.hboxlayout1.addLayout(self.verticalLayout_2)
        self.available_tags = QtWidgets.QListWidget(DeviceCategoryEditor)
        self.available_tags.setAlternatingRowColors(True)
        self.available_tags.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.available_tags.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.available_tags.setObjectName("available_tags")
        self.hboxlayout1.addWidget(self.available_tags)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.gridlayout.addLayout(self.vboxlayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DeviceCategoryEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.label.setBuddy(self.available_tags)

        self.retranslateUi(DeviceCategoryEditor)
        self.buttonBox.accepted.connect(DeviceCategoryEditor.accept)
        self.buttonBox.rejected.connect(DeviceCategoryEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(DeviceCategoryEditor)

    def retranslateUi(self, DeviceCategoryEditor):

        DeviceCategoryEditor.setWindowTitle(_("Category Editor"))
        self.label.setText(_("Items in use"))
        self.delete_button.setToolTip(_("Delete item from database. This will unapply the item from all books and then remove it from the database."))
        self.delete_button.setText(_("..."))
        self.rename_button.setToolTip(_("Rename the item in every book where it is used."))
        self.rename_button.setText(_("..."))
        self.rename_button.setShortcut(_("Ctrl+S"))

