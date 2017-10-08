# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/preferences/saving.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(707, 340)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.opt_save_cover = QtWidgets.QCheckBox(Form)
        self.opt_save_cover.setObjectName("opt_save_cover")
        self.gridLayout.addWidget(self.opt_save_cover, 1, 0, 1, 1)
        self.opt_replace_whitespace = QtWidgets.QCheckBox(Form)
        self.opt_replace_whitespace.setObjectName("opt_replace_whitespace")
        self.gridLayout.addWidget(self.opt_replace_whitespace, 1, 1, 1, 1)
        self.opt_update_metadata = QtWidgets.QCheckBox(Form)
        self.opt_update_metadata.setObjectName("opt_update_metadata")
        self.gridLayout.addWidget(self.opt_update_metadata, 2, 0, 1, 1)
        self.opt_to_lowercase = QtWidgets.QCheckBox(Form)
        self.opt_to_lowercase.setObjectName("opt_to_lowercase")
        self.gridLayout.addWidget(self.opt_to_lowercase, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.opt_timefmt = QtWidgets.QLineEdit(Form)
        self.opt_timefmt.setObjectName("opt_timefmt")
        self.gridLayout.addWidget(self.opt_timefmt, 6, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)
        self.opt_formats = QtWidgets.QLineEdit(Form)
        self.opt_formats.setObjectName("opt_formats")
        self.gridLayout.addWidget(self.opt_formats, 7, 1, 1, 1)
        self.save_template = SaveTemplate(Form)
        self.save_template.setObjectName("save_template")
        self.gridLayout.addWidget(self.save_template, 8, 0, 1, 2)
        self.opt_asciiize = QtWidgets.QCheckBox(Form)
        self.opt_asciiize.setObjectName("opt_asciiize")
        self.gridLayout.addWidget(self.opt_asciiize, 3, 1, 1, 1)
        self.opt_write_opf = QtWidgets.QCheckBox(Form)
        self.opt_write_opf.setObjectName("opt_write_opf")
        self.gridLayout.addWidget(self.opt_write_opf, 3, 0, 1, 1)
        self.opt_show_files_after_save = QtWidgets.QCheckBox(Form)
        self.opt_show_files_after_save.setObjectName("opt_show_files_after_save")
        self.gridLayout.addWidget(self.opt_show_files_after_save, 4, 0, 1, 2)
        self.label_2.setBuddy(self.opt_timefmt)
        self.label_3.setBuddy(self.opt_formats)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("Here you can control how calibre will save your books when you click the \"Save to disk\" button:"))
        self.opt_save_cover.setText(_("Save &cover separately"))
        self.opt_replace_whitespace.setText(_("Replace space with &underscores"))
        self.opt_update_metadata.setText(_("Update &metadata in saved copies"))
        self.opt_to_lowercase.setText(_("Change paths to &lowercase"))
        self.label_2.setText(_("Format &dates as:"))
        self.label_3.setText(_("File &formats to save:"))
        self.opt_asciiize.setText(_("Convert non-English characters to &English equivalents"))
        self.opt_write_opf.setText(_("Save metadata in a separate &OPF file"))
        self.opt_show_files_after_save.setText(_("&Show files in the file browser after saving to disk"))

from calibre.gui2.preferences.save_template import SaveTemplate
