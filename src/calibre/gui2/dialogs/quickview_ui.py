# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/quickview.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Quickview(object):
    def setupUi(self, Quickview):
        Quickview.setObjectName("Quickview")
        Quickview.resize(768, 342)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Quickview.sizePolicy().hasHeightForWidth())
        Quickview.setSizePolicy(sizePolicy)
        self.gridlayout = QtWidgets.QGridLayout(Quickview)
        self.gridlayout.setObjectName("gridlayout")
        self.items_label = QtWidgets.QLabel(Quickview)
        self.items_label.setObjectName("items_label")
        self.gridlayout.addWidget(self.items_label, 0, 0, 1, 1)
        self.items = QtWidgets.QListWidget(Quickview)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.items.sizePolicy().hasHeightForWidth())
        self.items.setSizePolicy(sizePolicy)
        self.items.setObjectName("items")
        self.gridlayout.addWidget(self.items, 1, 0, 1, 1)
        self.books_label = QtWidgets.QLabel(Quickview)
        self.books_label.setObjectName("books_label")
        self.gridlayout.addWidget(self.books_label, 0, 1, 1, 1)
        self.books_table = QtWidgets.QTableWidget(Quickview)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.books_table.sizePolicy().hasHeightForWidth())
        self.books_table.setSizePolicy(sizePolicy)
        self.books_table.setColumnCount(0)
        self.books_table.setRowCount(0)
        self.books_table.setObjectName("books_table")
        self.gridlayout.addWidget(self.books_table, 1, 1, 1, 1)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.lock_qv = QtWidgets.QCheckBox(Quickview)
        self.lock_qv.setObjectName("lock_qv")
        self.hboxlayout.addWidget(self.lock_qv)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.dock_button = QtWidgets.QPushButton(Quickview)
        self.dock_button.setAutoDefault(False)
        self.dock_button.setObjectName("dock_button")
        self.hboxlayout.addWidget(self.dock_button)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.search_button = QtWidgets.QPushButton(Quickview)
        self.search_button.setAutoDefault(False)
        self.search_button.setObjectName("search_button")
        self.hboxlayout.addWidget(self.search_button)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Quickview)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.hboxlayout.addWidget(self.buttonBox)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 2)
        self.items_label.setBuddy(self.items)
        self.books_label.setBuddy(self.books_table)

        self.retranslateUi(Quickview)
        self.buttonBox.rejected.connect(Quickview.reject)
        QtCore.QMetaObject.connectSlotsByName(Quickview)

    def retranslateUi(self, Quickview):

        Quickview.setWindowTitle(_("Quickview"))
        self.lock_qv.setText(_("&Lock Quickview contents"))
        self.lock_qv.setToolTip(_("<p>Select to prevent Quickview from changing content when the\n"
"        selection on the library view is changed</p>"))
        self.dock_button.setText(_("&Dock"))
        self.search_button.setText(_("&Search"))
        self.search_button.setToolTip(_("Search in the library view for the currently highlighted selection"))

