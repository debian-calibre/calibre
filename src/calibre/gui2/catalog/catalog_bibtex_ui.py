# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/catalog/catalog_bibtex.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(579, 411)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.bibfile_enc = QtWidgets.QComboBox(Form)
        self.bibfile_enc.setObjectName("bibfile_enc")
        self.gridLayout.addWidget(self.bibfile_enc, 1, 0, 1, 1)
        self.db_fields = QtWidgets.QListWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.db_fields.sizePolicy().hasHeightForWidth())
        self.db_fields.setSizePolicy(sizePolicy)
        self.db_fields.setToolTip("")
        self.db_fields.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.db_fields.setObjectName("db_fields")
        self.gridLayout.addWidget(self.db_fields, 1, 1, 11, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.bibfile_enctag = QtWidgets.QComboBox(Form)
        self.bibfile_enctag.setObjectName("bibfile_enctag")
        self.gridLayout.addWidget(self.bibfile_enctag, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.bib_entry = QtWidgets.QComboBox(Form)
        self.bib_entry.setObjectName("bib_entry")
        self.gridLayout.addWidget(self.bib_entry, 6, 0, 1, 1)
        self.impcit = QtWidgets.QCheckBox(Form)
        self.impcit.setObjectName("impcit")
        self.gridLayout.addWidget(self.impcit, 7, 0, 1, 1)
        self.addfiles = QtWidgets.QCheckBox(Form)
        self.addfiles.setObjectName("addfiles")
        self.gridLayout.addWidget(self.addfiles, 8, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 9, 0, 1, 1)
        self.bib_cit = QtWidgets.QLineEdit(Form)
        self.bib_cit.setObjectName("bib_cit")
        self.gridLayout.addWidget(self.bib_cit, 10, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 11, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("Bib file encoding:"))
        self.label_5.setText(_("Fields to include in output:"))
        self.label_2.setText(_("Encoding configuration (change if you have errors):"))
        self.label_6.setText(_("BibTeX entry type:"))
        self.impcit.setText(_("Create a citation tag?"))
        self.addfiles.setText(_("Add file paths with formats?"))
        self.label_3.setText(_("Expression to form the BibTeX citation tag:"))
        self.label_4.setText(_("Some explanation about this template:\n"
" -The fields availables are \'author_sort\', \'authors\', \'id\',\n"
"    \'isbn\', \'pubdate\', \'publisher\', \'series_index\', \'series\',\n"
"   \'tags\', \'timestamp\', \'title\', \'uuid\', \'title_sort\'\n"
" -For list types ie authors and tags, only the first element\n"
"   will be selected.\n"
" -For time field, only the date will be used. "))

