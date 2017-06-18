# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/device_drivers/configwidget.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConfigWidget(object):
    def setupUi(self, ConfigWidget):
        ConfigWidget.setObjectName("ConfigWidget")
        ConfigWidget.resize(442, 332)
        self.gridLayout = QtWidgets.QGridLayout(ConfigWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(ConfigWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.columns = QtWidgets.QListWidget(self.groupBox)
        self.columns.setAlternatingRowColors(True)
        self.columns.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.columns.setObjectName("columns")
        self.horizontalLayout_3.addWidget(self.columns)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.column_up = QtWidgets.QToolButton(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("arrow-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.column_up.setIcon(icon)
        self.column_up.setObjectName("column_up")
        self.verticalLayout_3.addWidget(self.column_up)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.column_down = QtWidgets.QToolButton(self.groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("arrow-down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.column_down.setIcon(icon1)
        self.column_down.setObjectName("column_down")
        self.verticalLayout_3.addWidget(self.column_down)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.opt_read_metadata = QtWidgets.QCheckBox(ConfigWidget)
        self.opt_read_metadata.setObjectName("opt_read_metadata")
        self.gridLayout.addWidget(self.opt_read_metadata, 1, 0, 1, 1)
        self.opt_use_subdirs = QtWidgets.QCheckBox(ConfigWidget)
        self.opt_use_subdirs.setObjectName("opt_use_subdirs")
        self.gridLayout.addWidget(self.opt_use_subdirs, 2, 0, 1, 1)
        self.opt_use_author_sort = QtWidgets.QCheckBox(ConfigWidget)
        self.opt_use_author_sort.setObjectName("opt_use_author_sort")
        self.gridLayout.addWidget(self.opt_use_author_sort, 3, 0, 1, 1)
        self.extra_layout = QtWidgets.QGridLayout()
        self.extra_layout.setObjectName("extra_layout")
        self.gridLayout.addLayout(self.extra_layout, 6, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.label = QtWidgets.QLabel(ConfigWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.opt_save_template = QtWidgets.QLineEdit(ConfigWidget)
        self.opt_save_template.setObjectName("opt_save_template")
        self.gridLayout.addWidget(self.opt_save_template, 5, 0, 1, 1)
        self.label.setBuddy(self.opt_save_template)

        self.retranslateUi(ConfigWidget)
        QtCore.QMetaObject.connectSlotsByName(ConfigWidget)

    def retranslateUi(self, ConfigWidget):

        ConfigWidget.setWindowTitle(_("Form"))
        self.groupBox.setTitle(_("Select available formats and their order for this device"))
        self.column_up.setText(_("..."))
        self.column_down.setText(_("..."))
        self.opt_read_metadata.setText(_("Read metadata from files on device"))
        self.opt_use_subdirs.setToolTip(_("If checked, books are placed into sub-directories based on their metadata on the device. If unchecked, books are all put into the top level directory."))
        self.opt_use_subdirs.setText(_("Use sub-directories"))
        self.opt_use_author_sort.setText(_("Use author sort for author"))
        self.label.setText(_("Save &template:"))


