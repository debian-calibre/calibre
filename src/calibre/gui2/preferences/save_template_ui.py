# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/preferences/save_template.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(477, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.help_label = QtWidgets.QLabel(self.groupBox)
        self.help_label.setWordWrap(True)
        self.help_label.setObjectName("help_label")
        self.gridLayout_2.addWidget(self.help_label, 0, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 2)
        self.template_variables = QtWidgets.QTextBrowser(self.groupBox)
        self.template_variables.setObjectName("template_variables")
        self.gridLayout_2.addWidget(self.template_variables, 3, 0, 1, 2)
        self.opt_template = HistoryBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.opt_template.sizePolicy().hasHeightForWidth())
        self.opt_template.setSizePolicy(sizePolicy)
        self.opt_template.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.opt_template.setMinimumContentsLength(40)
        self.opt_template.setObjectName("opt_template")
        self.gridLayout_2.addWidget(self.opt_template, 1, 0, 1, 1)
        self.open_editor = QtWidgets.QPushButton(self.groupBox)
        self.open_editor.setObjectName("open_editor")
        self.gridLayout_2.addWidget(self.open_editor, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.groupBox.setTitle(_("Save template"))
        self.help_label.setText(_("By adjusting the template below, you can control what folders the files are saved in and what filenames they are given. You can use the / character to indicate sub-folders. Available metadata variables are described below. If a particular book does not have some metadata, the variable will be replaced by the empty string."))
        self.label_5.setText(_("Available variables:"))
        self.open_editor.setText(_("Template &editor"))

from calibre.gui2.preferences.history import HistoryBox
