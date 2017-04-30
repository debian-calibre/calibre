#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__   = 'GPL v3'
__copyright__ = '2010, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import time

from PyQt5.Qt import Qt, QUrl, QDialog, QSize, QVBoxLayout, QLabel, \
    QPlainTextEdit, QDialogButtonBox, QTimer

from calibre.gui2.preferences import ConfigWidgetBase, test_widget
from calibre.gui2.preferences.server_ui import Ui_Form
from calibre.library.server import server_config
from calibre.utils.config import ConfigProxy
from calibre.gui2 import error_dialog, config, open_url, warning_dialog, \
        Dispatcher, info_dialog
from calibre import as_unicode
from calibre.utils.icu import sort_key


class ConfigWidget(ConfigWidgetBase, Ui_Form):

    def genesis(self, gui):
        self.gui = gui
        self.proxy = ConfigProxy(server_config())
        db = self.db = gui.library_view.model().db
        self.server = self.gui.content_server

        r = self.register

        r('port', self.proxy)
        r('username', self.proxy)
        r('password', self.proxy)
        r('max_cover', self.proxy)
        r('max_opds_items', self.proxy)
        r('max_opds_ungrouped_items', self.proxy)
        r('url_prefix', self.proxy)

        self.show_server_password.stateChanged[int].connect(
                     lambda s: self.opt_password.setEchoMode(
                         self.opt_password.Normal if s == Qt.Checked
                         else self.opt_password.Password))
        self.opt_password.setEchoMode(self.opt_password.Password)

        restrictions = sorted(db.prefs['virtual_libraries'].iterkeys(), key=sort_key)
        choices = [('', '')] + [(x, x) for x in restrictions]
        # check that the virtual library still exists
        vls = db.prefs['cs_virtual_lib_on_startup']
        if vls and vls not in restrictions:
            db.prefs['cs_virtual_lib_on_startup'] = ''
        r('cs_virtual_lib_on_startup', db.prefs, choices=choices)

        self.start_button.setEnabled(not getattr(self.server, 'is_running', False))
        self.test_button.setEnabled(not self.start_button.isEnabled())
        self.stop_button.setDisabled(self.start_button.isEnabled())
        self.start_button.clicked.connect(self.start_server)
        self.stop_button.clicked.connect(self.stop_server)
        self.test_button.clicked.connect(self.test_server)
        self.view_logs.clicked.connect(self.view_server_logs)

        r('autolaunch_server', config)

    def start_server(self):
        ConfigWidgetBase.commit(self)
        self.setCursor(Qt.BusyCursor)
        try:
            self.gui.start_content_server(check_started=False)
            while (not self.gui.content_server.is_running and
                    self.gui.content_server.exception is None):
                time.sleep(0.1)
            if self.gui.content_server.exception is not None:
                error_dialog(self, _('Failed to start content server'),
                        as_unicode(self.gui.content_server.exception)).exec_()
                return
            self.start_button.setEnabled(False)
            self.test_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        finally:
            self.unsetCursor()

    def stop_server(self):
        self.gui.content_server.threaded_exit()
        self.stopping_msg = info_dialog(self, _('Stopping'),
                _('Stopping server, this could take up to a minute, please wait...'),
                show_copy_button=False)
        QTimer.singleShot(500, self.check_exited)
        self.stopping_msg.exec_()

    def check_exited(self):
        if getattr(self.gui.content_server, 'is_running', False):
            QTimer.singleShot(20, self.check_exited)
            return

        self.gui.content_server = None
        self.start_button.setEnabled(True)
        self.test_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.stopping_msg.accept()

    def test_server(self):
        prefix = unicode(self.opt_url_prefix.text()).strip()
        open_url(QUrl('http://127.0.0.1:'+str(self.opt_port.value())+prefix))

    def view_server_logs(self):
        from calibre.library.server import log_access_file, log_error_file
        d = QDialog(self)
        d.resize(QSize(800, 600))
        layout = QVBoxLayout()
        d.setLayout(layout)
        layout.addWidget(QLabel(_('Error log:')))
        el = QPlainTextEdit(d)
        layout.addWidget(el)
        try:
            el.setPlainText(open(log_error_file, 'rb').read().decode('utf8', 'replace'))
        except IOError:
            el.setPlainText('No error log found')
        layout.addWidget(QLabel(_('Access log:')))
        al = QPlainTextEdit(d)
        layout.addWidget(al)
        try:
            al.setPlainText(open(log_access_file, 'rb').read().decode('utf8', 'replace'))
        except IOError:
            al.setPlainText('No access log found')
        bx = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(bx)
        bx.accepted.connect(d.accept)
        d.show()

    def commit(self):
        ConfigWidgetBase.commit(self)
        warning_dialog(self, _('Restart needed'),
                _('You need to restart the server for changes to'
                    ' take effect'), show=True)
        return False

    def refresh_gui(self, gui):
        gui.content_server = self.server
        if gui.content_server is not None:
            gui.content_server.state_callback = \
                Dispatcher(gui.iactions['Connect Share'].content_server_state_changed)
            gui.content_server.state_callback(gui.content_server.is_running)


if __name__ == '__main__':
    from PyQt5.Qt import QApplication
    app = QApplication([])
    test_widget('Sharing', 'Server')

