# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/match_books.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MatchBooks(object):
    def setupUi(self, MatchBooks):
        MatchBooks.setObjectName("MatchBooks")
        MatchBooks.resize(751, 342)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MatchBooks.sizePolicy().hasHeightForWidth())
        MatchBooks.setSizePolicy(sizePolicy)
        self.gridlayout = QtWidgets.QGridLayout(MatchBooks)
        self.gridlayout.setObjectName("gridlayout")
        self.search_text = HistoryLineEdit(MatchBooks)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_text.sizePolicy().hasHeightForWidth())
        self.search_text.setSizePolicy(sizePolicy)
        self.search_text.setMinimumSize(QtCore.QSize(350, 0))
        self.search_text.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.search_text.setMinimumContentsLength(30)
        self.search_text.setObjectName("search_text")
        self.gridlayout.addWidget(self.search_text, 0, 0, 1, 1)
        self.search_button = QtWidgets.QPushButton(MatchBooks)
        self.search_button.setObjectName("search_button")
        self.gridlayout.addWidget(self.search_button, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(MatchBooks)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 1, 0, 1, 2)
        self.books_table = QtWidgets.QTableWidget(MatchBooks)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.books_table.sizePolicy().hasHeightForWidth())
        self.books_table.setSizePolicy(sizePolicy)
        self.books_table.setRowCount(0)
        self.books_table.setColumnCount(0)
        self.books_table.setObjectName("books_table")
        self.gridlayout.addWidget(self.books_table, 2, 0, 1, 2)
        self.label1 = QtWidgets.QLabel(MatchBooks)
        self.label1.setWordWrap(True)
        self.label1.setObjectName("label1")
        self.gridlayout.addWidget(self.label1, 3, 0, 1, 2)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(MatchBooks)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.hboxlayout.addWidget(self.buttonBox)
        self.gridlayout.addLayout(self.hboxlayout, 4, 0, 1, 2)

        self.retranslateUi(MatchBooks)
        self.buttonBox.rejected.connect(MatchBooks.reject)
        QtCore.QMetaObject.connectSlotsByName(MatchBooks)

    def retranslateUi(self, MatchBooks):

        MatchBooks.setWindowTitle(_("Match books"))
        self.search_button.setText(_("Search"))
        self.label.setText(_("Do a search to find the book you want to match"))
        self.label1.setText(_("<p>Remember to update metadata on the device when you are done (Right click the device icon and select <i>Update cached metadata</i>)</p>"))

from calibre.gui2.widgets import HistoryLineEdit
