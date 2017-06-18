# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/epub_output.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(644, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.opt_preserve_cover_aspect_ratio = QtWidgets.QCheckBox(Form)
        self.opt_preserve_cover_aspect_ratio.setObjectName("opt_preserve_cover_aspect_ratio")
        self.gridLayout.addWidget(self.opt_preserve_cover_aspect_ratio, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.opt_flow_size = QtWidgets.QSpinBox(Form)
        self.opt_flow_size.setMinimum(0)
        self.opt_flow_size.setMaximum(1000000)
        self.opt_flow_size.setSingleStep(20)
        self.opt_flow_size.setObjectName("opt_flow_size")
        self.gridLayout.addWidget(self.opt_flow_size, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 262, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.opt_no_default_epub_cover = QtWidgets.QCheckBox(Form)
        self.opt_no_default_epub_cover.setObjectName("opt_no_default_epub_cover")
        self.gridLayout.addWidget(self.opt_no_default_epub_cover, 1, 0, 1, 1)
        self.opt_no_svg_cover = QtWidgets.QCheckBox(Form)
        self.opt_no_svg_cover.setObjectName("opt_no_svg_cover")
        self.gridLayout.addWidget(self.opt_no_svg_cover, 2, 0, 1, 1)
        self.opt_epub_inline_toc = QtWidgets.QCheckBox(Form)
        self.opt_epub_inline_toc.setObjectName("opt_epub_inline_toc")
        self.gridLayout.addWidget(self.opt_epub_inline_toc, 3, 0, 1, 1)
        self.opt_dont_split_on_page_breaks = QtWidgets.QCheckBox(Form)
        self.opt_dont_split_on_page_breaks.setObjectName("opt_dont_split_on_page_breaks")
        self.gridLayout.addWidget(self.opt_dont_split_on_page_breaks, 0, 0, 1, 2)
        self.opt_epub_toc_at_end = QtWidgets.QCheckBox(Form)
        self.opt_epub_toc_at_end.setObjectName("opt_epub_toc_at_end")
        self.gridLayout.addWidget(self.opt_epub_toc_at_end, 3, 1, 1, 1)
        self.opt_epub_flatten = QtWidgets.QCheckBox(Form)
        self.opt_epub_flatten.setObjectName("opt_epub_flatten")
        self.gridLayout.addWidget(self.opt_epub_flatten, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.opt_toc_title = QtWidgets.QLineEdit(Form)
        self.opt_toc_title.setObjectName("opt_toc_title")
        self.gridLayout.addWidget(self.opt_toc_title, 4, 1, 1, 1)
        self.label.setBuddy(self.opt_flow_size)
        self.label_2.setBuddy(self.opt_toc_title)

        self.retranslateUi(Form)
        self.opt_no_svg_cover.toggled['bool'].connect(self.opt_preserve_cover_aspect_ratio.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_preserve_cover_aspect_ratio.setText(_("Preserve cover &aspect ratio"))
        self.label.setText(_("Split files &larger than:"))
        self.opt_flow_size.setSpecialValueText(_("Disabled"))
        self.opt_flow_size.setSuffix(_(" KB"))
        self.opt_no_default_epub_cover.setText(_("No default &cover"))
        self.opt_no_svg_cover.setText(_("No &SVG cover"))
        self.opt_epub_inline_toc.setText(_("Insert inline &Table of Contents"))
        self.opt_dont_split_on_page_breaks.setText(_("Do not &split on page breaks"))
        self.opt_epub_toc_at_end.setText(_("Put inserted Table of Contents at the &end of the book"))
        self.opt_epub_flatten.setText(_("&Flatten EPUB file structure"))
        self.label_2.setText(_("&Title for inserted ToC:"))

