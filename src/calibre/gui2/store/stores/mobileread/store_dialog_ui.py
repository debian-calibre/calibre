# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/store/stores/mobileread/store_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(691, 614)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.adv_search_button = QtWidgets.QToolButton(Dialog)
        self.adv_search_button.setObjectName("adv_search_button")
        self.horizontalLayout_2.addWidget(self.adv_search_button)
        self.search_query = HistoryLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_query.sizePolicy().hasHeightForWidth())
        self.search_query.setSizePolicy(sizePolicy)
        self.search_query.setObjectName("search_query")
        self.horizontalLayout_2.addWidget(self.search_query)
        self.search_button = QtWidgets.QPushButton(Dialog)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_2.addWidget(self.search_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.results_view = QtWidgets.QTreeView(Dialog)
        self.results_view.setAlternatingRowColors(True)
        self.results_view.setRootIsDecorated(False)
        self.results_view.setItemsExpandable(False)
        self.results_view.setSortingEnabled(True)
        self.results_view.setExpandsOnDoubleClick(False)
        self.results_view.setObjectName("results_view")
        self.results_view.header().setCascadingSectionResizes(False)
        self.verticalLayout.addWidget(self.results_view)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.total = QtWidgets.QLabel(Dialog)
        self.total.setObjectName("total")
        self.horizontalLayout.addWidget(self.total)
        spacerItem = QtWidgets.QSpacerItem(308, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_button = QtWidgets.QPushButton(Dialog)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label.setBuddy(self.search_query)

        self.retranslateUi(Dialog)
        self.close_button.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Dialog"))
        self.label.setText(_("&Query:"))
        self.adv_search_button.setText(_("..."))
        self.search_button.setText(_("Search"))
        self.label_2.setText(_("Books:"))
        self.total.setText(_("0"))
        self.close_button.setText(_("&Close"))

from calibre.gui2.widgets import HistoryLineEdit
