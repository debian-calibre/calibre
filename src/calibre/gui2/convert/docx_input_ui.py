# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/docx_input.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(518, 353)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.opt_docx_no_cover = QtWidgets.QCheckBox(Form)
        self.opt_docx_no_cover.setObjectName("opt_docx_no_cover")
        self.verticalLayout_3.addWidget(self.opt_docx_no_cover)
        self.opt_docx_no_pagebreaks_between_notes = QtWidgets.QCheckBox(Form)
        self.opt_docx_no_pagebreaks_between_notes.setObjectName("opt_docx_no_pagebreaks_between_notes")
        self.verticalLayout_3.addWidget(self.opt_docx_no_pagebreaks_between_notes)
        self.opt_docx_inline_subsup = QtWidgets.QCheckBox(Form)
        self.opt_docx_inline_subsup.setObjectName("opt_docx_inline_subsup")
        self.verticalLayout_3.addWidget(self.opt_docx_inline_subsup)
        spacerItem = QtWidgets.QSpacerItem(20, 213, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_docx_no_cover.setText(_("Do not try to autodetect a &cover from images in the document"))
        self.opt_docx_no_pagebreaks_between_notes.setText(_("Do not add a page after every &endnote"))
        self.opt_docx_inline_subsup.setText(_("Render &superscripts and subscripts so that they do not affect the line height."))

