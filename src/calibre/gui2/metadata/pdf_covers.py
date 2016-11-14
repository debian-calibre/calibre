#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:fdm=marker:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import sys, shutil, os
from threading import Thread
from glob import glob

import sip
from PyQt5.Qt import (
    QDialog, QApplication, QLabel, QGridLayout, QDialogButtonBox, Qt,
    pyqtSignal, QListWidget, QListWidgetItem, QSize, QPixmap, QStyledItemDelegate
)

from calibre import as_unicode
from calibre.ebooks.metadata.pdf import page_images
from calibre.gui2 import error_dialog, file_icon_provider
from calibre.ptempfile import PersistentTemporaryDirectory


class CoverDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)
        style = QApplication.style()
        # Ensure the cover is rendered over any selection rect
        style.drawItemPixmap(painter, option.rect, Qt.AlignTop|Qt.AlignHCenter,
            QPixmap(index.data(Qt.DecorationRole)))


class PDFCovers(QDialog):
    'Choose a cover from the first few pages of a PDF'

    rendering_done = pyqtSignal()

    def __init__(self, pdfpath, parent=None):
        QDialog.__init__(self, parent)
        self.pdfpath = pdfpath
        self.l = l = QGridLayout()
        self.setLayout(l)

        self.la = la = QLabel(_('Choose a cover from the list of PDF pages below'))
        l.addWidget(la)
        self.loading = la = QLabel('<b>'+_('Rendering PDF pages, please wait...'))
        l.addWidget(la)

        self.covers = c = QListWidget(self)
        l.addWidget(c)
        self.item_delegate = CoverDelegate(self)
        c.setItemDelegate(self.item_delegate)
        c.setIconSize(QSize(120, 160))
        c.setSelectionMode(c.SingleSelection)
        c.setViewMode(c.IconMode)
        c.setUniformItemSizes(True)
        c.setResizeMode(c.Adjust)
        c.itemDoubleClicked.connect(self.accept)

        self.bb = bb = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        l.addWidget(bb)
        self.rendering_done.connect(self.show_pages, type=Qt.QueuedConnection)
        self.tdir = PersistentTemporaryDirectory('_pdf_covers')
        self.thread = Thread(target=self.render)
        self.thread.daemon = True
        self.thread.start()
        self.setWindowTitle(_('Choose cover from PDF'))
        self.setWindowIcon(file_icon_provider().icon_from_ext('pdf'))
        self.resize(QSize(800, 600))

    @property
    def cover_path(self):
        for item in self.covers.selectedItems():
            return unicode(item.data(Qt.UserRole) or '')
        if self.covers.count() > 0:
            return unicode(self.covers.item(0).data(Qt.UserRole) or '')

    def cleanup(self):
        try:
            shutil.rmtree(self.tdir)
        except:
            pass

    def render(self):
        self.error = None
        try:
            page_images(self.pdfpath, self.tdir, last=10)
        except Exception as e:
            self.error = as_unicode(e)
        if not sip.isdeleted(self) and self.isVisible():
            self.rendering_done.emit()

    def show_pages(self):
        self.loading.setVisible(False)
        if self.error is not None:
            error_dialog(self, _('Failed to render'),
                _('Could not render this PDF file'), show=True)
            self.reject()
            return
        files = (glob(os.path.join(self.tdir, '*.jpg')) +
                 glob(os.path.join(self.tdir, '*.jpeg')))
        if not files:
            error_dialog(self, _('Failed to render'),
                _('This PDF has no pages'), show=True)
            self.reject()
            return

        try:
            dpr = self.devicePixelRatioF()
        except AttributeError:
            dpr = self.devicePixelRatio()

        for i, f in enumerate(sorted(files)):
            p = QPixmap(f).scaled(self.covers.iconSize()*dpr, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            p.setDevicePixelRatio(dpr)
            i = QListWidgetItem(_('page %d') % (i + 1))
            i.setData(Qt.DecorationRole, p)
            i.setData(Qt.UserRole, f)
            self.covers.addItem(i)

if __name__ == '__main__':
    app = QApplication([])
    app
    d = PDFCovers(sys.argv[-1])
    d.exec_()
    print (d.cover_path)
