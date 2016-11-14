# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/shortcuts.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 170)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.default_shortcuts = QtWidgets.QRadioButton(Frame)
        self.default_shortcuts.setObjectName("default_shortcuts")
        self.gridLayout.addWidget(self.default_shortcuts, 1, 0, 1, 2)
        self.custom = QtWidgets.QRadioButton(Frame)
        self.custom.setObjectName("custom")
        self.gridLayout.addWidget(self.custom, 2, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(25, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QtWidgets.QLabel(Frame)
        self.label1.setObjectName("label1")
        self.horizontalLayout.addWidget(self.label1)
        self.button1 = QtWidgets.QPushButton(Frame)
        self.button1.setObjectName("button1")
        self.horizontalLayout.addWidget(self.button1)
        self.clear1 = QtWidgets.QToolButton(Frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("clear_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear1.setIcon(icon)
        self.clear1.setObjectName("clear1")
        self.horizontalLayout.addWidget(self.clear1)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(25, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label2 = QtWidgets.QLabel(Frame)
        self.label2.setObjectName("label2")
        self.horizontalLayout_3.addWidget(self.label2)
        self.button2 = QtWidgets.QPushButton(Frame)
        self.button2.setObjectName("button2")
        self.horizontalLayout_3.addWidget(self.button2)
        self.clear2 = QtWidgets.QToolButton(Frame)
        self.clear2.setIcon(icon)
        self.clear2.setObjectName("clear2")
        self.horizontalLayout_3.addWidget(self.clear2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 2)
        self.header = QtWidgets.QLabel(Frame)
        self.header.setText("")
        self.header.setWordWrap(True)
        self.header.setObjectName("header")
        self.gridLayout.addWidget(self.header, 0, 0, 1, 2)
        self.label1.setBuddy(self.button1)
        self.label2.setBuddy(self.button1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):

        Frame.setWindowTitle(_("Frame"))
        self.default_shortcuts.setText(_("&Default"))
        self.custom.setText(_("&Custom"))
        self.label1.setText(_("&Shortcut:"))
        self.button1.setToolTip(_("Click to change"))
        self.button1.setText(_("None"))
        self.clear1.setToolTip(_("Clear"))
        self.clear1.setText(_("..."))
        self.label2.setText(_("&Alternate shortcut:"))
        self.button2.setToolTip(_("Click to change"))
        self.button2.setText(_("None"))
        self.clear2.setToolTip(_("Clear"))
        self.clear2.setText(_("..."))


