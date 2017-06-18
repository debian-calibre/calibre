# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/convert/xpath_wizard.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 381)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tag = QtWidgets.QComboBox(Form)
        self.tag.setEditable(True)
        self.tag.setObjectName("tag")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.tag.addItem("")
        self.verticalLayout.addWidget(self.tag)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.attribute = QtWidgets.QLineEdit(Form)
        self.attribute.setObjectName("attribute")
        self.verticalLayout.addWidget(self.attribute)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.value = QtWidgets.QLineEdit(Form)
        self.value.setObjectName("value")
        self.verticalLayout.addWidget(self.value)
        self.example_label = QtWidgets.QLabel(Form)
        self.example_label.setWordWrap(True)
        self.example_label.setOpenExternalLinks(True)
        self.example_label.setObjectName("example_label")
        self.verticalLayout.addWidget(self.example_label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label.setBuddy(self.tag)
        self.label_2.setBuddy(self.attribute)
        self.label_3.setBuddy(self.value)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.label.setText(_("Match HTML &tags with tag name:"))
        self.tag.setItemText(0, _("*"))
        self.tag.setItemText(1, _("a"))
        self.tag.setItemText(2, _("br"))
        self.tag.setItemText(3, _("div"))
        self.tag.setItemText(4, _("h1"))
        self.tag.setItemText(5, _("h2"))
        self.tag.setItemText(6, _("h3"))
        self.tag.setItemText(7, _("h4"))
        self.tag.setItemText(8, _("h5"))
        self.tag.setItemText(9, _("h6"))
        self.tag.setItemText(10, _("hr"))
        self.tag.setItemText(11, _("span"))
        self.label_2.setText(_("Having the &attribute:"))
        self.label_3.setText(_("With &value:"))
        self.label_4.setText(_("(A regular expression)"))
        self.example_label.setText(_("<p>For example, to match all h2 tags that have class=\"chapter\", set tag to <i>h2</i>, attribute to <i>class</i> and value to <i>chapter</i>.</p><p>Leaving attribute blank will match any attribute and leaving value blank will match any value. Setting tag to * will match any tag.</p><p>To learn more advanced usage of XPath see the <a href=\"%s\">XPath Tutorial</a>."))

