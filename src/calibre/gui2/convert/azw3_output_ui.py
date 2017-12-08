# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/azw3_output.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(724, 342)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.opt_no_inline_toc = QtWidgets.QCheckBox(Form)
        self.opt_no_inline_toc.setObjectName("opt_no_inline_toc")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.opt_no_inline_toc)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.opt_toc_title = QtWidgets.QLineEdit(Form)
        self.opt_toc_title.setObjectName("opt_toc_title")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_toc_title)
        self.opt_mobi_toc_at_start = QtWidgets.QCheckBox(Form)
        self.opt_mobi_toc_at_start.setObjectName("opt_mobi_toc_at_start")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.opt_mobi_toc_at_start)
        self.opt_prefer_author_sort = QtWidgets.QCheckBox(Form)
        self.opt_prefer_author_sort.setObjectName("opt_prefer_author_sort")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.opt_prefer_author_sort)
        self.opt_dont_compress = QtWidgets.QCheckBox(Form)
        self.opt_dont_compress.setObjectName("opt_dont_compress")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.opt_dont_compress)
        self.opt_share_not_sync = QtWidgets.QCheckBox(Form)
        self.opt_share_not_sync.setObjectName("opt_share_not_sync")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.opt_share_not_sync)
        self.label.setBuddy(self.opt_toc_title)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_no_inline_toc.setText(_("Do not add &Table of Contents to book"))
        self.label.setText(_("&Title for Table of Contents:"))
        self.opt_mobi_toc_at_start.setText(_("Put generated Table of Contents at &start of book instead of end"))
        self.opt_prefer_author_sort.setText(_("Use author &sort for author"))
        self.opt_dont_compress.setText(_("Disable &compression of the file contents"))
        self.opt_share_not_sync.setText(_("Enable &sharing of book content via Facebook, etc. WARNING: Disables last read syncing"))

