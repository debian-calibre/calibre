# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/store/config/chooser/chooser_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(610, 553)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.query = HistoryLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.query.sizePolicy().hasHeightForWidth())
        self.query.setSizePolicy(sizePolicy)
        self.query.setClearButtonEnabled(True)
        self.query.setObjectName("query")
        self.horizontalLayout.addWidget(self.query)
        self.search = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search.setIcon(icon)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.results_view = ResultsView(Form)
        self.results_view.setAlternatingRowColors(True)
        self.results_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.results_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.results_view.setRootIsDecorated(False)
        self.results_view.setUniformRowHeights(True)
        self.results_view.setItemsExpandable(False)
        self.results_view.setSortingEnabled(True)
        self.results_view.setExpandsOnDoubleClick(False)
        self.results_view.setObjectName("results_view")
        self.results_view.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.results_view)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.enable_all = QtWidgets.QPushButton(Form)
        self.enable_all.setObjectName("enable_all")
        self.horizontalLayout_2.addWidget(self.enable_all)
        self.enable_none = QtWidgets.QPushButton(Form)
        self.enable_none.setObjectName("enable_none")
        self.horizontalLayout_2.addWidget(self.enable_none)
        self.enable_invert = QtWidgets.QPushButton(Form)
        self.enable_invert.setObjectName("enable_invert")
        self.horizontalLayout_2.addWidget(self.enable_invert)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.query.setPlaceholderText(_("Query"))
        self.search.setText(_("Search"))
        self.label_2.setText(_("Enable:"))
        self.enable_all.setText(_("&All"))
        self.enable_none.setText(_("&None"))
        self.enable_invert.setText(_("&Invert"))

from calibre.gui2.widgets import HistoryLineEdit
from results_view import ResultsView

