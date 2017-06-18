# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/edit_authors_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditAuthorsDialog(object):
    def setupUi(self, EditAuthorsDialog):
        EditAuthorsDialog.setObjectName("EditAuthorsDialog")
        EditAuthorsDialog.resize(768, 342)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditAuthorsDialog.sizePolicy().hasHeightForWidth())
        EditAuthorsDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditAuthorsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = QtWidgets.QLabel(EditAuthorsDialog)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.find_box = HistoryLineEdit(EditAuthorsDialog)
        self.find_box.setMinimumSize(QtCore.QSize(200, 0))
        self.find_box.setObjectName("find_box")
        self.hboxlayout.addWidget(self.find_box)
        self.find_button = QtWidgets.QPushButton(EditAuthorsDialog)
        self.find_button.setObjectName("find_button")
        self.hboxlayout.addWidget(self.find_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.table = QtWidgets.QTableWidget(EditAuthorsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setColumnCount(0)
        self.table.setObjectName("table")
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.sort_by_author = QtWidgets.QPushButton(EditAuthorsDialog)
        self.sort_by_author.setObjectName("sort_by_author")
        self.gridlayout.addWidget(self.sort_by_author, 0, 0, 1, 1)
        self.sort_by_author_sort = QtWidgets.QPushButton(EditAuthorsDialog)
        self.sort_by_author_sort.setObjectName("sort_by_author_sort")
        self.gridlayout.addWidget(self.sort_by_author_sort, 0, 1, 1, 1)
        self.recalc_author_sort = QtWidgets.QPushButton(EditAuthorsDialog)
        self.recalc_author_sort.setObjectName("recalc_author_sort")
        self.gridlayout.addWidget(self.recalc_author_sort, 1, 0, 1, 1)
        self.auth_sort_to_author = QtWidgets.QPushButton(EditAuthorsDialog)
        self.auth_sort_to_author.setObjectName("auth_sort_to_author")
        self.gridlayout.addWidget(self.auth_sort_to_author, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EditAuthorsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridlayout)
        self.label.setBuddy(self.find_box)

        self.retranslateUi(EditAuthorsDialog)
        self.buttonBox.accepted.connect(EditAuthorsDialog.accept)
        self.buttonBox.rejected.connect(EditAuthorsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditAuthorsDialog)

    def retranslateUi(self, EditAuthorsDialog):

        EditAuthorsDialog.setWindowTitle(_("Manage authors"))
        self.label.setText(_("&Search for:"))
        self.find_button.setText(_("F&ind"))
        self.sort_by_author.setText(_("Sort by &author"))
        self.sort_by_author_sort.setText(_("Sort by author &sort"))
        self.recalc_author_sort.setToolTip(_("Reset all the author sort values to a value automatically\n"
"generated from the author. Exactly how this value is automatically\n"
"generated can be controlled via Preferences->Advanced->Tweaks"))
        self.recalc_author_sort.setText(_("&Recalculate all author sort values"))
        self.auth_sort_to_author.setToolTip(_("Copy author sort to author for every author. You typically use this button\n"
"after changing Preferences->Advanced->Tweaks->Author sort name algorithm"))
        self.auth_sort_to_author.setText(_("&Copy all author sort values to author"))

from calibre.gui2.widgets import HistoryLineEdit
