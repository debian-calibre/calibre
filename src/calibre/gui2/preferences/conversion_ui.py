# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/preferences/conversion.ui'
#
# Created: Wed Nov  5 09:01:07 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(720, 603)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list = QtWidgets.QListView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list.sizePolicy().hasHeightForWidth())
        self.list.setSizePolicy(sizePolicy)
        self.list.setMinimumSize(QtCore.QSize(180, 0))
        self.list.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.list.setFont(font)
        self.list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list.setTabKeyNavigation(True)
        self.list.setProperty("showDropIndicator", False)
        self.list.setIconSize(QtCore.QSize(48, 48))
        self.list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.list.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.list.setFlow(QtWidgets.QListView.TopToBottom)
        self.list.setSpacing(10)
        self.list.setViewMode(QtWidgets.QListView.ListMode)
        self.list.setObjectName("list")
        self.horizontalLayout.addWidget(self.list)
        self.stack = QtWidgets.QStackedWidget(Form)
        self.stack.setObjectName("stack")
        self.horizontalLayout.addWidget(self.stack)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))

