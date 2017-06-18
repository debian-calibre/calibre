# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/lrf_renderer/config.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ViewerConfig(object):
    def setupUi(self, ViewerConfig):
        ViewerConfig.setObjectName("ViewerConfig")
        ViewerConfig.resize(373, 264)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("config.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewerConfig.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ViewerConfig)
        self.gridLayout.setObjectName("gridLayout")
        self.white_background = QtWidgets.QCheckBox(ViewerConfig)
        self.white_background.setObjectName("white_background")
        self.gridLayout.addWidget(self.white_background, 0, 0, 1, 1)
        self.hyphenate = QtWidgets.QCheckBox(ViewerConfig)
        self.hyphenate.setChecked(True)
        self.hyphenate.setObjectName("hyphenate")
        self.gridLayout.addWidget(self.hyphenate, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(ViewerConfig)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ViewerConfig)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(ViewerConfig)
        self.buttonBox.accepted.connect(ViewerConfig.accept)
        self.buttonBox.rejected.connect(ViewerConfig.reject)
        QtCore.QMetaObject.connectSlotsByName(ViewerConfig)

    def retranslateUi(self, ViewerConfig):

        ViewerConfig.setWindowTitle(_("Configure Viewer"))
        self.white_background.setText(_("Use white background"))
        self.hyphenate.setText(_("Hyphenate"))
        self.label.setText(_("<b>Changes will only take effect after a restart.</b>"))


