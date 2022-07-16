#!/usr/bin/env python
# License: GPL v3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>


from calibre.gui2.actions import InterfaceAction


class FullTextSearchAction(InterfaceAction):

    name = 'Full Text Search'
    action_spec = (_('Search full text'), 'fts.png',
                   _('Search the full text of all books in the calibre library'), ('Ctrl+/', 'Ctrl+Alt+F'))
    dont_add_to = frozenset(('context-menu-device',))
    action_type = 'current'

    def genesis(self):
        self.qaction.triggered.connect(self.show_fts)
        self._dialog = None

    @property
    def dialog(self):
        if self._dialog is None:
            from calibre.gui2.fts.dialog import FTSDialog
            self._dialog = FTSDialog(self.gui)
        return self._dialog

    def show_fts(self):
        self.dialog.show()
        self.dialog.raise_()

    def library_changed(self, db):
        if self._dialog is not None:
            self._dialog.library_changed()

    def clear_search_history(self):
        if self._dialog is not None:
            self._dialog.clear_search_history()
