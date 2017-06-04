# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/mobi_output.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(588, 416)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.opt_no_inline_toc = QtWidgets.QCheckBox(Form)
        self.opt_no_inline_toc.setObjectName("opt_no_inline_toc")
        self.gridLayout.addWidget(self.opt_no_inline_toc, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.opt_toc_title = QtWidgets.QLineEdit(Form)
        self.opt_toc_title.setObjectName("opt_toc_title")
        self.gridLayout.addWidget(self.opt_toc_title, 1, 1, 1, 1)
        self.opt_mobi_toc_at_start = QtWidgets.QCheckBox(Form)
        self.opt_mobi_toc_at_start.setObjectName("opt_mobi_toc_at_start")
        self.gridLayout.addWidget(self.opt_mobi_toc_at_start, 2, 0, 1, 2)
        self.opt_mobi_ignore_margins = QtWidgets.QCheckBox(Form)
        self.opt_mobi_ignore_margins.setObjectName("opt_mobi_ignore_margins")
        self.gridLayout.addWidget(self.opt_mobi_ignore_margins, 3, 0, 1, 1)
        self.opt_prefer_author_sort = QtWidgets.QCheckBox(Form)
        self.opt_prefer_author_sort.setObjectName("opt_prefer_author_sort")
        self.gridLayout.addWidget(self.opt_prefer_author_sort, 4, 0, 1, 1)
        self.opt_mobi_keep_original_images = QtWidgets.QCheckBox(Form)
        self.opt_mobi_keep_original_images.setObjectName("opt_mobi_keep_original_images")
        self.gridLayout.addWidget(self.opt_mobi_keep_original_images, 5, 0, 1, 2)
        self.opt_dont_compress = QtWidgets.QCheckBox(Form)
        self.opt_dont_compress.setObjectName("opt_dont_compress")
        self.gridLayout.addWidget(self.opt_dont_compress, 6, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.opt_mobi_file_type = QtWidgets.QComboBox(self.groupBox)
        self.opt_mobi_file_type.setObjectName("opt_mobi_file_type")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.opt_mobi_file_type)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.opt_personal_doc = QtWidgets.QLineEdit(self.groupBox)
        self.opt_personal_doc.setObjectName("opt_personal_doc")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.opt_personal_doc)
        self.opt_share_not_sync = QtWidgets.QCheckBox(self.groupBox)
        self.opt_share_not_sync.setObjectName("opt_share_not_sync")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.opt_share_not_sync)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label_4)
        self.gridLayout.addWidget(self.groupBox, 7, 0, 1, 2)
        self.label.setBuddy(self.opt_toc_title)
        self.label_2.setBuddy(self.opt_mobi_file_type)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_no_inline_toc.setText(_("Do not add &Table of Contents to book"))
        self.label.setText(_("&Title for Table of Contents:"))
        self.opt_mobi_toc_at_start.setText(_("Put generated Table of Contents at &start of book instead of end"))
        self.opt_mobi_ignore_margins.setText(_("Ignore &margins"))
        self.opt_prefer_author_sort.setText(_("Use author &sort for author"))
        self.opt_mobi_keep_original_images.setText(_("Do not convert all images to &JPEG (may result in images not working in older viewers)"))
        self.opt_dont_compress.setText(_("Disable &compression of the file contents"))
        self.groupBox.setTitle(_("Kindle options"))
        self.label_2.setText(_("MOBI file &type:"))
        self.label_3.setText(_("Personal Doc tag:"))
        self.opt_share_not_sync.setText(_("Enable &sharing of book content via Facebook, etc. WARNING: Disables last read syncing"))
        self.label_4.setText(_("<b>WARNING:</b> Various Kindle devices have trouble displaying the new or both MOBI filetypes. If you wish to use the new format on your device, convert to AZW3 instead of MOBI."))

