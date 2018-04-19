# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/xexp_edit.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(430, 74)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.msg = QtWidgets.QLabel(Form)
        self.msg.setWordWrap(True)
        self.msg.setObjectName("msg")
        self.verticalLayout.addWidget(self.msg)
        self.edit = HistoryLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit.sizePolicy().hasHeightForWidth())
        self.edit.setSizePolicy(sizePolicy)
        self.edit.setMinimumSize(QtCore.QSize(350, 0))
        self.edit.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.edit.setMinimumContentsLength(30)
        self.edit.setObjectName("edit")
        self.verticalLayout.addWidget(self.edit)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.button = QtWidgets.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("wizard.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon)
        self.button.setIconSize(QtCore.QSize(40, 40))
        self.button.setObjectName("button")
        self.gridLayout.addWidget(self.button, 0, 1, 1, 1)
        self.msg.setBuddy(self.edit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.msg.setText(_("TextLabel"))
        self.button.setToolTip(_("Use a wizard to help construct the Regular expression"))
        self.button.setText(_("..."))

from calibre.gui2.widgets import HistoryLineEdit

