# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/toc.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(596, 493)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.opt_toc_threshold = QtWidgets.QSpinBox(Form)
        self.opt_toc_threshold.setMaximum(10000)
        self.opt_toc_threshold.setObjectName("opt_toc_threshold")
        self.gridLayout.addWidget(self.opt_toc_threshold, 7, 1, 1, 1)
        self.opt_use_auto_toc = QtWidgets.QCheckBox(Form)
        self.opt_use_auto_toc.setObjectName("opt_use_auto_toc")
        self.gridLayout.addWidget(self.opt_use_auto_toc, 1, 0, 1, 2)
        self.opt_no_chapters_in_toc = QtWidgets.QCheckBox(Form)
        self.opt_no_chapters_in_toc.setObjectName("opt_no_chapters_in_toc")
        self.gridLayout.addWidget(self.opt_no_chapters_in_toc, 2, 0, 1, 2)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 8, 0, 1, 1)
        self.opt_level3_toc = XPathEdit(Form)
        self.opt_level3_toc.setObjectName("opt_level3_toc")
        self.gridLayout.addWidget(self.opt_level3_toc, 11, 0, 1, 2)
        self.opt_max_toc_links = QtWidgets.QSpinBox(Form)
        self.opt_max_toc_links.setMaximum(10000)
        self.opt_max_toc_links.setObjectName("opt_max_toc_links")
        self.gridLayout.addWidget(self.opt_max_toc_links, 6, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 13, 0, 1, 1)
        self.opt_duplicate_links_in_toc = QtWidgets.QCheckBox(Form)
        self.opt_duplicate_links_in_toc.setObjectName("opt_duplicate_links_in_toc")
        self.gridLayout.addWidget(self.opt_duplicate_links_in_toc, 3, 0, 1, 2)
        self.opt_level2_toc = XPathEdit(Form)
        self.opt_level2_toc.setObjectName("opt_level2_toc")
        self.gridLayout.addWidget(self.opt_level2_toc, 10, 0, 1, 2)
        self.opt_toc_filter = QtWidgets.QLineEdit(Form)
        self.opt_toc_filter.setObjectName("opt_toc_filter")
        self.gridLayout.addWidget(self.opt_toc_filter, 8, 1, 1, 1)
        self.opt_level1_toc = XPathEdit(Form)
        self.opt_level1_toc.setObjectName("opt_level1_toc")
        self.gridLayout.addWidget(self.opt_level1_toc, 9, 0, 1, 2)
        self.help_label = QtWidgets.QLabel(Form)
        self.help_label.setWordWrap(True)
        self.help_label.setOpenExternalLinks(True)
        self.help_label.setObjectName("help_label")
        self.gridLayout.addWidget(self.help_label, 0, 0, 1, 2)
        self.manually_fine_tune_toc = QtWidgets.QCheckBox(Form)
        self.manually_fine_tune_toc.setObjectName("manually_fine_tune_toc")
        self.gridLayout.addWidget(self.manually_fine_tune_toc, 12, 0, 1, 2)
        self.label_10.setBuddy(self.opt_max_toc_links)
        self.label.setBuddy(self.opt_toc_filter)
        self.label_16.setBuddy(self.opt_toc_threshold)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_use_auto_toc.setText(_("&Force use of auto-generated Table of Contents"))
        self.opt_no_chapters_in_toc.setText(_("Do not add &detected chapters to the Table of Contents"))
        self.label_10.setText(_("Number of &links to add to Table of Contents:"))
        self.label.setText(_("TOC &filter:"))
        self.label_16.setText(_("Chapter &threshold:"))
        self.opt_duplicate_links_in_toc.setText(_("Allow &duplicate links when creating the Table of Contents"))
        self.help_label.setText(_("<a href=\"%s\">Help with using these options to generate a Table of Contents</a>"))
        self.manually_fine_tune_toc.setToolTip(_("This option will cause calibre to popup the Table of Contents Editor tool,\n"
" which will allow you to manually edit the Table of Contents, to fix any errors\n"
" caused by automatic generation."))
        self.manually_fine_tune_toc.setText(_("&Manually fine-tune the ToC after conversion is completed"))

from calibre.gui2.convert.xpath_wizard import XPathEdit
