# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/snb_output.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.opt_snb_hide_chapter_name = QtWidgets.QCheckBox(Form)
        self.opt_snb_hide_chapter_name.setObjectName("opt_snb_hide_chapter_name")
        self.gridLayout.addWidget(self.opt_snb_hide_chapter_name, 3, 0, 1, 1)
        self.opt_snb_dont_indent_first_line = QtWidgets.QCheckBox(Form)
        self.opt_snb_dont_indent_first_line.setObjectName("opt_snb_dont_indent_first_line")
        self.gridLayout.addWidget(self.opt_snb_dont_indent_first_line, 2, 0, 1, 1)
        self.opt_snb_insert_empty_line = QtWidgets.QCheckBox(Form)
        self.opt_snb_insert_empty_line.setObjectName("opt_snb_insert_empty_line")
        self.gridLayout.addWidget(self.opt_snb_insert_empty_line, 1, 0, 1, 1)
        self.opt_snb_full_screen = QtWidgets.QCheckBox(Form)
        self.opt_snb_full_screen.setObjectName("opt_snb_full_screen")
        self.gridLayout.addWidget(self.opt_snb_full_screen, 4, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_snb_hide_chapter_name.setText(_("Hide &chapter name"))
        self.opt_snb_dont_indent_first_line.setText(_("Don\'t indent the &first line for each paragraph"))
        self.opt_snb_insert_empty_line.setText(_("Insert &empty line between paragraphs"))
        self.opt_snb_full_screen.setText(_("Optimize for full-&screen view "))

