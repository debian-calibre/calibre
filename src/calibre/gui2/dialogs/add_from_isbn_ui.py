# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/add_from_isbn.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(678, 430)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("add_book.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.isbn_box = QtWidgets.QPlainTextEdit(Dialog)
        self.isbn_box.setObjectName("isbn_box")
        self.verticalLayout_2.addWidget(self.isbn_box)
        self.paste_button = QtWidgets.QPushButton(Dialog)
        self.paste_button.setObjectName("paste_button")
        self.verticalLayout_2.addWidget(self.paste_button)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 2, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.add_tags = QtWidgets.QLineEdit(Dialog)
        self.add_tags.setObjectName("add_tags")
        self.verticalLayout.addWidget(self.add_tags)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.label_2.setBuddy(self.add_tags)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Add books by ISBN"))
        self.paste_button.setText(_("&Paste from clipboard"))
        self.label.setText(_("<p>Enter a list of ISBNs in the box to the left, one per line. calibre will automatically create entries for books based on the ISBN and download metadata and covers for them.</p>\n"
"<p>Any invalid ISBNs in the list will be ignored.</p>\n"
"<p>You can also specify a file that will be added with each ISBN. To do this enter the full path to the file after a <code>>></code>.  For example:</p>\n"
"<p><code>9788842915232 >> %s</code></p>"))
        self.label_2.setText(_("&Tags to set on created book entries:"))


