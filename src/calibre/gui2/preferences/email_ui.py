# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/preferences/email.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(701, 494)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setWordWrap(True)
        self.label_22.setObjectName("label_22")
        self.verticalLayout.addWidget(self.label_22)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.email_view = QtWidgets.QTableView(Form)
        self.email_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.email_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.email_view.setObjectName("email_view")
        self.horizontalLayout_8.addWidget(self.email_view)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.email_add = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_add.sizePolicy().hasHeightForWidth())
        self.email_add.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.email_add.setIcon(icon)
        self.email_add.setIconSize(QtCore.QSize(24, 24))
        self.email_add.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.email_add.setObjectName("email_add")
        self.verticalLayout_8.addWidget(self.email_add)
        self.email_make_default = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_make_default.sizePolicy().hasHeightForWidth())
        self.email_make_default.setSizePolicy(sizePolicy)
        self.email_make_default.setObjectName("email_make_default")
        self.verticalLayout_8.addWidget(self.email_make_default)
        self.email_remove = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_remove.sizePolicy().hasHeightForWidth())
        self.email_remove.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.email_remove.setIcon(icon1)
        self.email_remove.setIconSize(QtCore.QSize(24, 24))
        self.email_remove.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.email_remove.setObjectName("email_remove")
        self.verticalLayout_8.addWidget(self.email_remove)
        self.horizontalLayout_8.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.opt_add_comments_to_email = QtWidgets.QCheckBox(Form)
        self.opt_add_comments_to_email.setObjectName("opt_add_comments_to_email")
        self.verticalLayout.addWidget(self.opt_add_comments_to_email)
        self.send_email_widget = SendEmail(Form)
        self.send_email_widget.setObjectName("send_email_widget")
        self.verticalLayout.addWidget(self.send_email_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label_22.setText(_("calibre can send your books to you (or your reader) by email. Emails will be automatically sent for downloaded news to all email addresses that have Auto-send checked."))
        self.email_add.setToolTip(_("Add an email address to which to send books"))
        self.email_add.setText(_("&Add email"))
        self.email_make_default.setText(_("Make &default"))
        self.email_remove.setText(_("&Remove email"))
        self.opt_add_comments_to_email.setToolTip(_("Add the comments from the book metadata to the email.\n"
"Useful to allow the recipient to see a summary of the\n"
"book before opening it."))
        self.opt_add_comments_to_email.setText(_("Add &comments metadata as text to the email"))

from calibre.gui2.wizard.send_email import SendEmail

