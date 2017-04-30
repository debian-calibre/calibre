# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/docx_output.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(638, 588)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.opt_docx_page_size = QtWidgets.QComboBox(Form)
        self.opt_docx_page_size.setObjectName("opt_docx_page_size")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.opt_docx_page_size)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.opt_docx_custom_page_size = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.opt_docx_custom_page_size.sizePolicy().hasHeightForWidth())
        self.opt_docx_custom_page_size.setSizePolicy(sizePolicy)
        self.opt_docx_custom_page_size.setObjectName("opt_docx_custom_page_size")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_docx_custom_page_size)
        self.opt_docx_no_cover = QtWidgets.QCheckBox(Form)
        self.opt_docx_no_cover.setObjectName("opt_docx_no_cover")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.opt_docx_no_cover)
        self.opt_docx_no_toc = QtWidgets.QCheckBox(Form)
        self.opt_docx_no_toc.setObjectName("opt_docx_no_toc")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.opt_docx_no_toc)
        self.label.setBuddy(self.opt_docx_page_size)
        self.label_3.setBuddy(self.opt_docx_custom_page_size)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("Paper Si&ze:"))
        self.label_3.setText(_("&Custom size:"))
        self.opt_docx_no_cover.setText(_("Do not insert &cover as image at start of document"))
        self.opt_docx_no_toc.setText(_("Do not insert the &Table of Contents as a page at the start of the document"))

