#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

from PyQt5.Qt import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from calibre.gui2 import Application


def main(url):
    # This function is run in a separate process and can do anything it likes,
    # including use QWebEngine. Here it simply opens the passed in URL
    # in a QWebEngineView
    app = Application([])
    w = QWebEngineView()
    w.setUrl(QUrl(url))
    w.show()
    w.raise_()
    app.exec_()
