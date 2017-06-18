# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/choose_library.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(602, 245)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("lt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.old_location = QtWidgets.QLabel(Dialog)
        self.old_location.setWordWrap(True)
        self.old_location.setObjectName("old_location")
        self.gridLayout.addWidget(self.old_location, 0, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.existing_library = QtWidgets.QRadioButton(Dialog)
        self.existing_library.setChecked(True)
        self.existing_library.setObjectName("existing_library")
        self.gridLayout.addWidget(self.existing_library, 4, 0, 1, 4)
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.setObjectName("hbox1")
        self.empty_library = QtWidgets.QRadioButton(Dialog)
        self.empty_library.setObjectName("empty_library")
        self.hbox1.addWidget(self.empty_library)
        self.copy_structure = QtWidgets.QCheckBox(Dialog)
        self.copy_structure.setObjectName("copy_structure")
        self.hbox1.addWidget(self.copy_structure)
        self.gridLayout.addLayout(self.hbox1, 5, 0, 1, 3)
        self.move_library = QtWidgets.QRadioButton(Dialog)
        self.move_library.setObjectName("move_library")
        self.gridLayout.addWidget(self.move_library, 6, 0, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.browse_button = QtWidgets.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("document_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browse_button.setIcon(icon1)
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 2, 3, 1, 1)
        self.location = HistoryLineEdit(Dialog)
        self.location.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.location.setMinimumContentsLength(40)
        self.location.setObjectName("location")
        self.gridLayout.addWidget(self.location, 2, 1, 1, 2)
        self.label_2.setBuddy(self.location)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Choose your calibre library"))
        self.old_location.setText(_("Your calibre library is currently located at {0}"))
        self.label_2.setText(_("New &Location:"))
        self.existing_library.setText(_("Use the previously &existing library at the new location"))
        self.empty_library.setText(_("&Create an empty library at the new location"))
        self.copy_structure.setToolTip(_("Copy the custom columns, saved searches, column widths, plugboards,\n"
"user categories, and other information from the old to the new library"))
        self.copy_structure.setText(_("&Copy structure from the current library"))
        self.move_library.setText(_("&Move current library to new location"))
        self.browse_button.setText(_("..."))

from calibre.gui2.widgets import HistoryLineEdit

