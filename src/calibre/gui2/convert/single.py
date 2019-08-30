#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
# License: GPLv3 Copyright: 2009, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

import shutil

from PyQt5.Qt import (
    QAbstractListModel, QCheckBox, QComboBox, QCoreApplication, QDialog,
    QDialogButtonBox, QFont, QFrame, QGridLayout, QHBoxLayout, QIcon, QLabel,
    QListView, QModelIndex, QRect, QScrollArea, QSize, QSizePolicy, QSpacerItem,
    QStackedWidget, Qt, QTextEdit, QVBoxLayout, QWidget
)

from calibre.customize.conversion import OptionRecommendation
from calibre.ebooks.conversion.config import (
    GuiRecommendations, delete_specifics, get_input_format_for_book,
    get_output_formats, save_specifics, sort_formats_by_preference
)
from calibre.ebooks.conversion.plumber import create_dummy_plumber
from calibre.gui2 import gprefs
from calibre.gui2.convert.debug import DebugWidget
from calibre.gui2.convert.heuristics import HeuristicsWidget
from calibre.gui2.convert.look_and_feel import LookAndFeelWidget
from calibre.gui2.convert.metadata import MetadataWidget
from calibre.gui2.convert.page_setup import PageSetupWidget
from calibre.gui2.convert.search_and_replace import SearchAndReplaceWidget
from calibre.gui2.convert.structure_detection import StructureDetectionWidget
from calibre.gui2.convert.toc import TOCWidget
from calibre.utils.config import prefs
from polyglot.builtins import native_string_type, range, unicode_type


class GroupModel(QAbstractListModel):

    def __init__(self, widgets):
        self.widgets = widgets
        QAbstractListModel.__init__(self)

    def rowCount(self, *args):
        return len(self.widgets)

    def data(self, index, role):
        try:
            widget = self.widgets[index.row()]
        except:
            return None
        if role == Qt.DisplayRole:
            return (widget.config_title())
        if role == Qt.DecorationRole:
            return (widget.config_icon())
        if role == Qt.FontRole:
            f = QFont()
            f.setBold(True)
            return (f)
        return None


class Config(QDialog):
    '''
    Configuration dialog for single book conversion. If accepted, has the
    following important attributes

    output_format - Output format (without a leading .)
    input_format  - Input format (without a leading .)
    opf_path - Path to OPF file with user specified metadata
    cover_path - Path to user specified cover (can be None)
    recommendations - A pickled list of 3 tuples in the same format as the
    recommendations member of the Input/Output plugins.
    '''

    def __init__(self, parent, db, book_id,
            preferred_input_format=None, preferred_output_format=None):
        QDialog.__init__(self, parent)
        self.setupUi()
        self.opt_individual_saved_settings.setVisible(False)
        self.db, self.book_id = db, book_id

        self.setup_input_output_formats(self.db, self.book_id, preferred_input_format,
                preferred_output_format)
        self.setup_pipeline()

        self.input_formats.currentIndexChanged[native_string_type].connect(self.setup_pipeline)
        self.output_formats.currentIndexChanged[native_string_type].connect(self.setup_pipeline)
        self.groups.setSpacing(5)
        self.groups.activated[(QModelIndex)].connect(self.show_pane)
        self.groups.clicked[(QModelIndex)].connect(self.show_pane)
        self.groups.entered[(QModelIndex)].connect(self.show_group_help)
        rb = self.buttonBox.button(self.buttonBox.RestoreDefaults)
        rb.setText(_('Restore &defaults'))
        rb.clicked.connect(self.restore_defaults)
        self.groups.setMouseTracking(True)
        geom = gprefs.get('convert_single_dialog_geom', None)
        if geom:
            self.restoreGeometry(geom)
        else:
            self.resize(self.sizeHint())

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(1024, 700)
        self.setWindowIcon(QIcon(I('convert.png')))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_label = QLabel(self)
        self.input_label.setObjectName("input_label")
        self.horizontalLayout.addWidget(self.input_label)
        self.input_formats = QComboBox(self)
        self.input_formats.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.input_formats.setMinimumContentsLength(5)
        self.input_formats.setObjectName("input_formats")
        self.horizontalLayout.addWidget(self.input_formats)
        self.opt_individual_saved_settings = QCheckBox(self)
        self.opt_individual_saved_settings.setObjectName("opt_individual_saved_settings")
        self.horizontalLayout.addWidget(self.opt_individual_saved_settings)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QLabel(self)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.output_formats = QComboBox(self)
        self.output_formats.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.output_formats.setMinimumContentsLength(5)
        self.output_formats.setObjectName("output_formats")
        self.horizontalLayout.addWidget(self.output_formats)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.groups = QListView(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groups.sizePolicy().hasHeightForWidth())
        self.groups.setSizePolicy(sizePolicy)
        self.groups.setTabKeyNavigation(True)
        self.groups.setIconSize(QSize(48, 48))
        self.groups.setWordWrap(True)
        self.groups.setObjectName("groups")
        self.gridLayout.addWidget(self.groups, 1, 0, 3, 1)
        self.scrollArea = QScrollArea(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 810, 494))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.stack = QStackedWidget(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stack.sizePolicy().hasHeightForWidth())
        self.stack.setSizePolicy(sizePolicy)
        self.stack.setObjectName("stack")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.stack.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.stack.addWidget(self.page_2)
        self.verticalLayout_3.addWidget(self.stack)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 1, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 1)
        self.help = QTextEdit(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help.sizePolicy().hasHeightForWidth())
        self.help.setSizePolicy(sizePolicy)
        self.help.setMaximumSize(QSize(16777215, 130))
        self.help.setObjectName("help")
        self.gridLayout.addWidget(self.help, 2, 1, 1, 1)
        self.input_label.setBuddy(self.input_formats)
        self.label_2.setBuddy(self.output_formats)
        self.input_label.setText(_("&Input format:"))
        self.opt_individual_saved_settings.setText(_("Use &saved conversion settings for individual books"))
        self.label_2.setText(_("&Output format:"))

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def sizeHint(self):
        desktop = QCoreApplication.instance().desktop()
        geom = desktop.availableGeometry(self)
        nh, nw = max(300, geom.height()-100), max(400, geom.width()-70)
        return QSize(nw, nh)

    def restore_defaults(self):
        delete_specifics(self.db, self.book_id)
        self.setup_pipeline()

    @property
    def input_format(self):
        return unicode_type(self.input_formats.currentText()).lower()

    @property
    def output_format(self):
        return unicode_type(self.output_formats.currentText()).lower()

    @property
    def manually_fine_tune_toc(self):
        for i in range(self.stack.count()):
            w = self.stack.widget(i)
            if hasattr(w, 'manually_fine_tune_toc'):
                return w.manually_fine_tune_toc.isChecked()

    def setup_pipeline(self, *args):
        oidx = self.groups.currentIndex().row()
        input_format = self.input_format
        output_format = self.output_format
        self.plumber = create_dummy_plumber(input_format, output_format)

        def widget_factory(cls):
            return cls(self.stack, self.plumber.get_option_by_name,
                self.plumber.get_option_help, self.db, self.book_id)

        self.mw = widget_factory(MetadataWidget)
        self.setWindowTitle(_('Convert')+ ' ' + unicode_type(self.mw.title.text()))
        lf = widget_factory(LookAndFeelWidget)
        hw = widget_factory(HeuristicsWidget)
        sr = widget_factory(SearchAndReplaceWidget)
        ps = widget_factory(PageSetupWidget)
        sd = widget_factory(StructureDetectionWidget)
        toc = widget_factory(TOCWidget)
        from calibre.gui2.actions.toc_edit import SUPPORTED
        toc.manually_fine_tune_toc.setVisible(output_format.upper() in SUPPORTED)
        debug = widget_factory(DebugWidget)

        output_widget = self.plumber.output_plugin.gui_configuration_widget(
                self.stack, self.plumber.get_option_by_name,
                self.plumber.get_option_help, self.db, self.book_id)
        input_widget = self.plumber.input_plugin.gui_configuration_widget(
                self.stack, self.plumber.get_option_by_name,
                self.plumber.get_option_help, self.db, self.book_id)
        while True:
            c = self.stack.currentWidget()
            if not c:
                break
            self.stack.removeWidget(c)

        widgets = [self.mw, lf, hw, ps, sd, toc, sr]
        if input_widget is not None:
            widgets.append(input_widget)
        if output_widget is not None:
            widgets.append(output_widget)
        widgets.append(debug)
        for w in widgets:
            self.stack.addWidget(w)
            w.set_help_signal.connect(self.help.setPlainText)

        self._groups_model = GroupModel(widgets)
        self.groups.setModel(self._groups_model)

        idx = oidx if -1 < oidx < self._groups_model.rowCount() else 0
        self.groups.setCurrentIndex(self._groups_model.index(idx))
        self.stack.setCurrentIndex(idx)
        try:
            shutil.rmtree(self.plumber.archive_input_tdir, ignore_errors=True)
        except:
            pass

    def setup_input_output_formats(self, db, book_id, preferred_input_format,
            preferred_output_format):
        if preferred_output_format:
            preferred_output_format = preferred_output_format.upper()
        output_formats = get_output_formats(preferred_output_format)
        input_format, input_formats = get_input_format_for_book(db, book_id,
                preferred_input_format)
        preferred_output_format = preferred_output_format if \
            preferred_output_format in output_formats else \
            sort_formats_by_preference(output_formats,
                    [prefs['output_format']])[0]
        self.input_formats.addItems((unicode_type(x.upper()) for x in input_formats))
        self.output_formats.addItems((unicode_type(x.upper()) for x in output_formats))
        self.input_formats.setCurrentIndex(input_formats.index(input_format))
        self.output_formats.setCurrentIndex(output_formats.index(preferred_output_format))

    def show_pane(self, index):
        self.stack.setCurrentIndex(index.row())

    def accept(self):
        recs = GuiRecommendations()
        for w in self._groups_model.widgets:
            if not w.pre_commit_check():
                return
            x = w.commit(save_defaults=False)
            recs.update(x)
        self.opf_file, self.cover_file = self.mw.opf_file, self.mw.cover_file
        self._recommendations = recs
        if self.db is not None:
            recs['gui_preferred_input_format'] = self.input_format
            save_specifics(self.db, self.book_id, recs)
        self.break_cycles()
        QDialog.accept(self)

    def reject(self):
        self.break_cycles()
        QDialog.reject(self)

    def done(self, r):
        if self.isVisible():
            gprefs['convert_single_dialog_geom'] = \
                bytearray(self.saveGeometry())
        return QDialog.done(self, r)

    def break_cycles(self):
        for i in range(self.stack.count()):
            w = self.stack.widget(i)
            w.break_cycles()

    @property
    def recommendations(self):
        recs = [(k, v, OptionRecommendation.HIGH) for k, v in
                self._recommendations.items()]
        return recs

    def show_group_help(self, index):
        widget = self._groups_model.widgets[index.row()]
        self.help.setPlainText(widget.HELP)
