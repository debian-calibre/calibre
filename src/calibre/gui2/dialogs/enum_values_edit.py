#!/usr/bin/env python
# License: GPLv3 Copyright: 2020, Charles Haley

from qt.core import (Qt, QDialog, QColor, QDialogButtonBox, QHeaderView,
                     QGridLayout, QTableWidget, QTableWidgetItem, QVBoxLayout,
                     QToolButton, QIcon, QAbstractItemView, QComboBox)

from calibre.gui2 import error_dialog, gprefs


class EnumValuesEdit(QDialog):

    def __init__(self, parent, db, key):
        QDialog.__init__(self, parent)

        self.setWindowTitle(_('Edit permissible values for {0}').format(key))
        self.db = db
        l = QGridLayout()

        bbox = QVBoxLayout()
        bbox.addStretch(10)
        self.del_button = QToolButton()
        self.del_button.setIcon(QIcon.ic('trash.png'))
        self.del_button.setToolTip(_('Remove the currently selected value'))
        self.ins_button = QToolButton()
        self.ins_button.setIcon(QIcon.ic('plus.png'))
        self.ins_button.setToolTip(_('Add a new permissible value'))
        self.move_up_button= QToolButton()
        self.move_up_button.setIcon(QIcon.ic('arrow-up.png'))
        self.move_down_button= QToolButton()
        self.move_down_button.setIcon(QIcon.ic('arrow-down.png'))
        bbox.addWidget(self.del_button)
        bbox.addStretch(1)
        bbox.addWidget(self.ins_button)
        bbox.addStretch(1)
        bbox.addWidget(self.move_up_button)
        bbox.addStretch(1)
        bbox.addWidget(self.move_down_button)
        bbox.addStretch(10)
        l.addItem(bbox, 0, 0)

        self.del_button.clicked.connect(self.del_line)

        self.all_colors = {str(s) for s in list(QColor.colorNames())}

        tl = QVBoxLayout()
        l.addItem(tl, 0, 1)
        self.table = t = QTableWidget(parent)
        t.setColumnCount(2)
        t.setRowCount(1)
        t.setHorizontalHeaderLabels([_('Value'), _('Color')])
        t.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        tl.addWidget(t)

        self.key = key
        self.fm = fm = db.field_metadata[key]
        permitted_values = fm.get('display', {}).get('enum_values', '')
        colors = fm.get('display', {}).get('enum_colors', '')
        t.setRowCount(len(permitted_values))
        for i,v in enumerate(permitted_values):
            self.make_name_item(i, v)
            c = self.make_color_combobox(i, -1)
            if colors:
                c.setCurrentIndex(c.findText(colors[i]))
            else:
                c.setCurrentIndex(0)

        t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.setLayout(l)

        self.bb = bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        l.addWidget(bb, 1, 0, 1, 2)

        self.ins_button.clicked.connect(self.ins_button_clicked)
        self.move_down_button.clicked.connect(self.move_down_clicked)
        self.move_up_button.clicked.connect(self.move_up_clicked)
        self.restore_geometry(gprefs, 'enum-values-edit-geometry')

    def sizeHint(self):
        sz = QDialog.sizeHint(self)
        sz.setWidth(max(sz.width(), 600))
        sz.setHeight(max(sz.height(), 400))
        return sz

    def make_name_item(self, row, txt):
        it = QTableWidgetItem(txt)
        it.setData(Qt.ItemDataRole.UserRole, txt)
        it.setCheckState(Qt.CheckState.Unchecked)
        it.setToolTip('<p>' + _('Check the box if you change the value and want it renamed in books where it is used') + '</p>')
        self.table.setItem(row, 0, it)

    def make_color_combobox(self, row, dex):
        c = QComboBox(self)
        c.addItem('')
        c.addItems(QColor.colorNames())
        c.setToolTip('<p>' + _('Selects the color of the text when displayed in the book list. '
                               'Either all rows must have a color or no rows have a color') + '</p>')
        self.table.setCellWidget(row, 1, c)
        if dex >= 0:
            c.setCurrentIndex(dex)
        return c

    def move_up_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            error_dialog(self, _('Select a cell'),
                               _('Select a cell before clicking the button'), show=True)
            return
        if row == 0:
            return
        self.move_row(row, -1)

    def move_row(self, row, direction):
        t = self.table.takeItem(row, 0)
        c = self.table.cellWidget(row, 1).currentIndex()
        self.table.removeRow(row)
        row += direction
        self.table.insertRow(row)
        self.table.setItem(row, 0, t)
        self.make_color_combobox(row, c)
        self.table.setCurrentCell(row, 0)

    def move_down_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            error_dialog(self, _('Select a cell'),
                               _('Select a cell before clicking the button'), show=True)
            return
        if row >= self.table.rowCount() - 1:
            return
        self.move_row(row, 1)

    def del_line(self):
        if self.table.currentRow() >= 0:
            self.table.removeRow(self.table.currentRow())

    def ins_button_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            error_dialog(self, _('Select a cell'),
                               _('Select a cell before clicking the button'), show=True)
            return
        self.table.insertRow(row)
        self.make_name_item(row, '')
        self.make_color_combobox(row, -1)

    def save_geometry(self):
        super().save_geometry(gprefs, 'enum-values-edit-geometry')

    def accept(self):
        disp = self.fm['display']
        values = []
        colors = []
        id_map = {}
        for i in range(0, self.table.rowCount()):
            it = self.table.item(i, 0)
            v = str(it.text())
            if not v:
                error_dialog(self, _('Empty value'),
                                   _('Empty values are not allowed'), show=True)
                return
            ov = str(it.data(Qt.ItemDataRole.UserRole))
            if v != ov and it.checkState() == Qt.CheckState.Checked:
                fid = self.db.new_api.get_item_id(self.key, ov)
                id_map[fid] = v
            values.append(v)
            c = str(self.table.cellWidget(i, 1).currentText())
            if c:
                colors.append(c)

        l_lower = [v.lower() for v in values]
        for i,v in enumerate(l_lower):
            if v in l_lower[i+1:]:
                error_dialog(self, _('Duplicate value'),
                                   _('The value "{0}" is in the list more than '
                                     'once, perhaps with different case').format(values[i]),
                             show=True)
                return

        if colors and len(colors) != len(values):
            error_dialog(self, _('Invalid colors specification'), _(
                'Either all values or no values must have colors'), show=True)
            return

        disp['enum_values'] = values
        disp['enum_colors'] = colors
        self.db.set_custom_column_metadata(self.fm['colnum'], display=disp,
                                           update_last_modified=True)
        if id_map:
            self.db.new_api.rename_items(self.key, id_map)
        self.save_geometry()
        return QDialog.accept(self)

    def reject(self):
        self.save_geometry()
        return QDialog.reject(self)
