# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/catalog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(674, 660)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("lt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.count = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.count.setFont(font)
        self.count.setObjectName("count")
        self.verticalLayout.addWidget(self.count)
        self.tabs = QtWidgets.QTabWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setMinimumSize(QtCore.QSize(650, 575))
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.format = QtWidgets.QComboBox(self.tab)
        self.format.setObjectName("format")
        self.gridLayout_2.addWidget(self.format, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.title = QtWidgets.QLineEdit(self.tab)
        self.title.setObjectName("title")
        self.gridLayout_2.addWidget(self.title, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 1, 1, 1)
        self.sync = QtWidgets.QCheckBox(self.tab)
        self.sync.setObjectName("sync")
        self.gridLayout_2.addWidget(self.sync, 2, 0, 1, 2)
        self.add_to_library = QtWidgets.QCheckBox(self.tab)
        self.add_to_library.setObjectName("add_to_library")
        self.gridLayout_2.addWidget(self.add_to_library, 3, 0, 1, 3)
        self.tabs.addTab(self.tab, "")
        self.verticalLayout.addWidget(self.tabs)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.format)
        self.label_2.setBuddy(self.title)

        self.retranslateUi(Dialog)
        self.tabs.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Generate catalog"))
        self.count.setText(_("Generate catalog for {0} books"))
        self.label.setText(_("Catalo&g format:"))
        self.label_2.setText(_("Catalog &title (existing catalog with the same title will be replaced):"))
        self.sync.setText(_("&Send catalog to device automatically"))
        self.add_to_library.setToolTip(_("Add the catalog to your calibre library after it is generated.\n"
"Note that if you disable adding of the catalog to the library\n"
"automatic sending of the catalog to the device will not work."))
        self.add_to_library.setText(_("&Add catalog to library"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _("Catalog options"))


