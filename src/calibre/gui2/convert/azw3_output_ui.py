# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/azw3_output.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(724, 342)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.opt_prefer_author_sort = QtWidgets.QCheckBox(Form)
        self.opt_prefer_author_sort.setObjectName("opt_prefer_author_sort")
        self.gridLayout.addWidget(self.opt_prefer_author_sort, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.opt_share_not_sync = QtWidgets.QCheckBox(Form)
        self.opt_share_not_sync.setObjectName("opt_share_not_sync")
        self.gridLayout.addWidget(self.opt_share_not_sync, 5, 0, 1, 1)
        self.opt_no_inline_toc = QtWidgets.QCheckBox(Form)
        self.opt_no_inline_toc.setObjectName("opt_no_inline_toc")
        self.gridLayout.addWidget(self.opt_no_inline_toc, 0, 0, 1, 1)
        self.opt_mobi_toc_at_start = QtWidgets.QCheckBox(Form)
        self.opt_mobi_toc_at_start.setObjectName("opt_mobi_toc_at_start")
        self.gridLayout.addWidget(self.opt_mobi_toc_at_start, 2, 0, 1, 2)
        self.opt_toc_title = QtWidgets.QLineEdit(Form)
        self.opt_toc_title.setObjectName("opt_toc_title")
        self.gridLayout.addWidget(self.opt_toc_title, 1, 1, 1, 1)
        self.opt_dont_compress = QtWidgets.QCheckBox(Form)
        self.opt_dont_compress.setObjectName("opt_dont_compress")
        self.gridLayout.addWidget(self.opt_dont_compress, 4, 0, 1, 1)
        self.label.setBuddy(self.opt_toc_title)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_prefer_author_sort.setText(_("Use author &sort for author"))
        self.label.setText(_("&Title for Table of Contents:"))
        self.opt_share_not_sync.setText(_("Enable &sharing of book content via Facebook, etc. WARNING: Disables last read syncing"))
        self.opt_no_inline_toc.setText(_("Do not add &Table of Contents to book"))
        self.opt_mobi_toc_at_start.setText(_("Put generated Table of Contents at &start of book instead of end"))
        self.opt_dont_compress.setText(_("Disable &compression of the file contents"))

