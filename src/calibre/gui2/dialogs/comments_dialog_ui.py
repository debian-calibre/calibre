# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/comments_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CommentsDialog(object):
    def setupUi(self, CommentsDialog):
        CommentsDialog.setObjectName("CommentsDialog")
        CommentsDialog.resize(400, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CommentsDialog.sizePolicy().hasHeightForWidth())
        CommentsDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(CommentsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textbox = Editor(CommentsDialog)
        self.textbox.setObjectName("textbox")
        self.verticalLayout.addWidget(self.textbox)
        self.buttonBox = QtWidgets.QDialogButtonBox(CommentsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CommentsDialog)
        self.buttonBox.accepted.connect(CommentsDialog.accept)
        self.buttonBox.rejected.connect(CommentsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CommentsDialog)

    def retranslateUi(self, CommentsDialog):

        CommentsDialog.setWindowTitle(_("Edit comments"))

from calibre.gui2.comments_editor import Editor
