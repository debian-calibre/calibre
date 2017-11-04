# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/jobs.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_JobsDialog(object):
    def setupUi(self, JobsDialog):
        JobsDialog.setObjectName("JobsDialog")
        JobsDialog.resize(633, 542)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("jobs.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        JobsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(JobsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search = SearchBox2(JobsDialog)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.search_button = QtWidgets.QToolButton(JobsDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon1)
        self.search_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.jobs_view = QtWidgets.QTableView(JobsDialog)
        self.jobs_view.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.jobs_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.jobs_view.setAlternatingRowColors(True)
        self.jobs_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.jobs_view.setIconSize(QtCore.QSize(32, 32))
        self.jobs_view.setObjectName("jobs_view")
        self.gridLayout.addWidget(self.jobs_view, 1, 0, 1, 2)
        self.kill_button = QtWidgets.QPushButton(JobsDialog)
        self.kill_button.setObjectName("kill_button")
        self.gridLayout.addWidget(self.kill_button, 2, 0, 1, 1)
        self.hide_button = QtWidgets.QPushButton(JobsDialog)
        self.hide_button.setObjectName("hide_button")
        self.gridLayout.addWidget(self.hide_button, 2, 1, 1, 1)
        self.details_button = QtWidgets.QPushButton(JobsDialog)
        self.details_button.setObjectName("details_button")
        self.gridLayout.addWidget(self.details_button, 3, 0, 1, 1)
        self.show_button = QtWidgets.QPushButton(JobsDialog)
        self.show_button.setObjectName("show_button")
        self.gridLayout.addWidget(self.show_button, 3, 1, 1, 1)
        self.stop_all_jobs_button = QtWidgets.QPushButton(JobsDialog)
        self.stop_all_jobs_button.setObjectName("stop_all_jobs_button")
        self.gridLayout.addWidget(self.stop_all_jobs_button, 4, 0, 1, 1)
        self.hide_all_button = QtWidgets.QPushButton(JobsDialog)
        self.hide_all_button.setObjectName("hide_all_button")
        self.gridLayout.addWidget(self.hide_all_button, 4, 1, 1, 1)

        self.retranslateUi(JobsDialog)
        QtCore.QMetaObject.connectSlotsByName(JobsDialog)

    def retranslateUi(self, JobsDialog):

        JobsDialog.setWindowTitle(_("Active jobs"))
        self.search_button.setToolTip(_("Find next match"))
        self.search_button.setText(_("&Search"))
        self.kill_button.setText(_("&Stop selected jobs"))
        self.hide_button.setText(_("&Hide selected jobs"))
        self.details_button.setText(_("Show job &details"))
        self.show_button.setText(_("Show &all jobs"))
        self.stop_all_jobs_button.setText(_("Stop &all non device jobs"))
        self.hide_all_button.setText(_("&Hide all jobs"))

from calibre.gui2.search_box import SearchBox2

