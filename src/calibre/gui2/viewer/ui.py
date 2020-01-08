#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>


import json
import os
import re
import sys
from collections import defaultdict, namedtuple
from hashlib import sha256
from threading import Thread

from PyQt5.Qt import (
    QApplication, QDockWidget, QEvent, QMimeData, QModelIndex, QPixmap, QScrollBar,
    Qt, QToolBar, QUrl, QVBoxLayout, QWidget, pyqtSignal
)

from calibre import prints
from calibre.constants import DEBUG
from calibre.customize.ui import available_input_formats
from calibre.gui2 import choose_files, error_dialog
from calibre.gui2.dialogs.drm_error import DRMErrorMessage
from calibre.gui2.image_popup import ImagePopup
from calibre.gui2.main_window import MainWindow
from calibre.gui2.viewer.annotations import (
    merge_annotations, parse_annotations, save_annots_to_epub, serialize_annotations
)
from calibre.gui2.viewer.bookmarks import BookmarkManager
from calibre.gui2.viewer.convert_book import (
    clean_running_workers, prepare_book, update_book
)
from calibre.gui2.viewer.lookup import Lookup
from calibre.gui2.viewer.overlay import LoadingOverlay
from calibre.gui2.viewer.toc import TOC, TOCSearch, TOCView
from calibre.gui2.viewer.toolbars import ActionsToolBar
from calibre.gui2.viewer.web_view import (
    WebView, get_path_for_name, get_session_pref, set_book_path, viewer_config_dir,
    vprefs
)
from calibre.utils.date import utcnow
from calibre.utils.img import image_from_path
from calibre.utils.ipc.simple_worker import WorkerError
from calibre.utils.monotonic import monotonic
from calibre.utils.serialize import json_loads
from polyglot.builtins import as_bytes, iteritems, itervalues

annotations_dir = os.path.join(viewer_config_dir, 'annots')


def is_float(x):
    try:
        float(x)
        return True
    except Exception:
        pass
    return False


def dock_defs():
    Dock = namedtuple('Dock', 'name title initial_area allowed_areas')
    ans = {}

    def d(title, name, area, allowed=Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea):
        ans[name] = Dock(name + '-dock', title, area, allowed)

    d(_('Table of Contents'), 'toc', Qt.LeftDockWidgetArea),
    d(_('Lookup'), 'lookup', Qt.RightDockWidgetArea),
    d(_('Bookmarks'), 'bookmarks', Qt.RightDockWidgetArea)
    d(_('Inspector'), 'inspector', Qt.RightDockWidgetArea, Qt.AllDockWidgetAreas)
    return ans


def path_key(path):
    return sha256(as_bytes(path)).hexdigest()


class ScrollBar(QScrollBar):

    def paintEvent(self, ev):
        if self.isEnabled():
            return QScrollBar.paintEvent(self, ev)


class EbookViewer(MainWindow):

    msg_from_anotherinstance = pyqtSignal(object)
    book_preparation_started = pyqtSignal()
    book_prepared = pyqtSignal(object, object)
    MAIN_WINDOW_STATE_VERSION = 1

    def __init__(self, open_at=None, continue_reading=None, force_reload=False):
        MainWindow.__init__(self, None)
        self.shutting_down = False
        self.force_reload = force_reload
        connect_lambda(self.book_preparation_started, self, lambda self: self.loading_overlay(_(
            'Preparing book for first read, please wait')), type=Qt.QueuedConnection)
        self.maximized_at_last_fullscreen = False
        self.pending_open_at = open_at
        self.base_window_title = _('E-book viewer')
        self.setWindowTitle(self.base_window_title)
        self.in_full_screen_mode = None
        self.image_popup = ImagePopup(self)
        self.actions_toolbar = at = ActionsToolBar(self)
        at.open_book_at_path.connect(self.ask_for_open)
        self.addToolBar(Qt.LeftToolBarArea, at)
        try:
            os.makedirs(annotations_dir)
        except EnvironmentError:
            pass
        self.current_book_data = {}
        self.book_prepared.connect(self.load_finished, type=Qt.QueuedConnection)
        self.dock_defs = dock_defs()

        def create_dock(title, name, area, areas=Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea):
            ans = QDockWidget(title, self)
            ans.setObjectName(name)
            self.addDockWidget(area, ans)
            ans.setVisible(False)
            ans.visibilityChanged.connect(self.dock_visibility_changed)
            return ans

        for dock_def in itervalues(self.dock_defs):
            setattr(self, '{}_dock'.format(dock_def.name.partition('-')[0]), create_dock(
                dock_def.title, dock_def.name, dock_def.initial_area, dock_def.allowed_areas))

        self.toc_container = w = QWidget(self)
        w.l = QVBoxLayout(w)
        self.toc = TOCView(w)
        self.toc.clicked[QModelIndex].connect(self.toc_clicked)
        self.toc.searched.connect(self.toc_searched)
        self.toc_search = TOCSearch(self.toc, parent=w)
        w.l.addWidget(self.toc), w.l.addWidget(self.toc_search), w.l.setContentsMargins(0, 0, 0, 0)
        self.toc_dock.setWidget(w)

        self.lookup_widget = w = Lookup(self)
        self.lookup_dock.visibilityChanged.connect(self.lookup_widget.visibility_changed)
        self.lookup_dock.setWidget(w)

        self.bookmarks_widget = w = BookmarkManager(self)
        connect_lambda(
            w.create_requested, self,
            lambda self: self.web_view.get_current_cfi(self.bookmarks_widget.create_new_bookmark))
        w.edited.connect(self.bookmarks_edited)
        w.activated.connect(self.bookmark_activated)
        w.toggle_requested.connect(self.toggle_bookmarks)
        self.bookmarks_dock.setWidget(w)

        self.web_view = WebView(self)
        self.web_view.cfi_changed.connect(self.cfi_changed)
        self.web_view.reload_book.connect(self.reload_book)
        self.web_view.toggle_toc.connect(self.toggle_toc)
        self.web_view.toggle_bookmarks.connect(self.toggle_bookmarks)
        self.web_view.toggle_inspector.connect(self.toggle_inspector)
        self.web_view.toggle_lookup.connect(self.toggle_lookup)
        self.web_view.quit.connect(self.quit)
        self.web_view.update_current_toc_nodes.connect(self.toc.update_current_toc_nodes)
        self.web_view.toggle_full_screen.connect(self.toggle_full_screen)
        self.web_view.ask_for_open.connect(self.ask_for_open, type=Qt.QueuedConnection)
        self.web_view.selection_changed.connect(self.lookup_widget.selected_text_changed, type=Qt.QueuedConnection)
        self.web_view.view_image.connect(self.view_image, type=Qt.QueuedConnection)
        self.web_view.copy_image.connect(self.copy_image, type=Qt.QueuedConnection)
        self.web_view.show_loading_message.connect(self.show_loading_message)
        self.web_view.show_error.connect(self.show_error)
        self.web_view.print_book.connect(self.print_book, type=Qt.QueuedConnection)
        self.web_view.reset_interface.connect(self.reset_interface, type=Qt.QueuedConnection)
        self.web_view.shortcuts_changed.connect(self.shortcuts_changed)
        self.actions_toolbar.initialize(self.web_view)
        self.setCentralWidget(self.web_view)
        self.loading_overlay = LoadingOverlay(self)
        self.restore_state()
        self.actions_toolbar.update_visibility()
        self.dock_visibility_changed()
        if continue_reading:
            self.continue_reading()

    def shortcuts_changed(self, smap):
        rmap = defaultdict(list)
        for k, v in iteritems(smap):
            rmap[v].append(k)
        self.actions_toolbar.set_tooltips(rmap)

    def toggle_inspector(self):
        visible = self.inspector_dock.toggleViewAction().isChecked()
        self.inspector_dock.setVisible(not visible)

    def resizeEvent(self, ev):
        self.loading_overlay.resize(self.size())
        return MainWindow.resizeEvent(self, ev)

    # IPC {{{
    def handle_commandline_arg(self, arg):
        if arg:
            if os.path.isfile(arg) and os.access(arg, os.R_OK):
                self.load_ebook(arg)
            else:
                prints('Cannot read from:', arg, file=sys.stderr)

    def another_instance_wants_to_talk(self, msg):
        try:
            path, open_at = msg
        except Exception:
            return
        self.load_ebook(path, open_at=open_at)
        self.raise_()
    # }}}

    # Fullscreen {{{
    def set_full_screen(self, on):
        if on:
            self.maximized_at_last_fullscreen = self.isMaximized()
            if not self.actions_toolbar.visible_in_fullscreen:
                self.actions_toolbar.setVisible(False)
            self.showFullScreen()
        else:
            self.actions_toolbar.update_visibility()
            if self.maximized_at_last_fullscreen:
                self.showMaximized()
            else:
                self.showNormal()

    def changeEvent(self, ev):
        if ev.type() == QEvent.WindowStateChange:
            in_full_screen_mode = self.isFullScreen()
            if self.in_full_screen_mode is None or self.in_full_screen_mode != in_full_screen_mode:
                self.in_full_screen_mode = in_full_screen_mode
                self.web_view.notify_full_screen_state_change(self.in_full_screen_mode)
        return MainWindow.changeEvent(self, ev)

    def toggle_full_screen(self):
        self.set_full_screen(not self.isFullScreen())
    # }}}

    # Docks (ToC, Bookmarks, Lookup, etc.) {{{

    def toggle_toc(self):
        self.toc_dock.setVisible(not self.toc_dock.isVisible())

    def toggle_bookmarks(self):
        is_visible = self.bookmarks_dock.isVisible()
        self.bookmarks_dock.setVisible(not is_visible)
        if is_visible:
            self.web_view.setFocus(Qt.OtherFocusReason)
        else:
            self.bookmarks_widget.bookmarks_list.setFocus(Qt.OtherFocusReason)

    def toggle_lookup(self):
        self.lookup_dock.setVisible(not self.lookup_dock.isVisible())

    def toc_clicked(self, index):
        item = self.toc_model.itemFromIndex(index)
        self.web_view.goto_toc_node(item.node_id)

    def toc_searched(self, index):
        item = self.toc_model.itemFromIndex(index)
        self.web_view.goto_toc_node(item.node_id)

    def bookmarks_edited(self, bookmarks):
        self.current_book_data['annotations_map']['bookmark'] = bookmarks

    def bookmark_activated(self, cfi):
        self.web_view.goto_cfi(cfi)

    def view_image(self, name):
        path = get_path_for_name(name)
        if path:
            pmap = QPixmap()
            if pmap.load(path):
                self.image_popup.current_img = pmap
                self.image_popup.current_url = QUrl.fromLocalFile(path)
                self.image_popup()
            else:
                error_dialog(self, _('Invalid image'), _(
                    "Failed to load the image {}").format(name), show=True)
        else:
            error_dialog(self, _('Image not found'), _(
                    "Failed to find the image {}").format(name), show=True)

    def copy_image(self, name):
        path = get_path_for_name(name)
        if not path:
            return error_dialog(self, _('Image not found'), _(
                "Failed to find the image {}").format(name), show=True)
        try:
            img = image_from_path(path)
        except Exception:
            return error_dialog(self, _('Invalid image'), _(
                "Failed to load the image {}").format(name), show=True)
        url = QUrl.fromLocalFile(path)
        md = QMimeData()
        md.setImageData(img)
        md.setUrls([url])
        QApplication.instance().clipboard().setMimeData(md)

    def dock_visibility_changed(self):
        vmap = {dock.objectName().partition('-')[0]: dock.toggleViewAction().isChecked() for dock in self.dock_widgets}
        self.actions_toolbar.update_dock_actions(vmap)
    # }}}

    # Load book {{{

    def show_loading_message(self, msg):
        if msg:
            self.loading_overlay(msg)
        else:
            self.loading_overlay.hide()

    def show_error(self, title, msg, details):
        self.loading_overlay.hide()
        error_dialog(self, title, msg, det_msg=details or None, show=True)

    def print_book(self):
        from .printing import print_book
        print_book(set_book_path.pathtoebook, book_title=self.current_book_data['metadata']['title'], parent=self)

    @property
    def dock_widgets(self):
        return self.findChildren(QDockWidget, options=Qt.FindDirectChildrenOnly)

    def reset_interface(self):
        for dock in self.dock_widgets:
            dock.setFloating(False)
            area = self.dock_defs[dock.objectName().partition('-')[0]].initial_area
            self.removeDockWidget(dock)
            self.addDockWidget(area, dock)
            dock.setVisible(False)

        for toolbar in self.findChildren(QToolBar):
            toolbar.setVisible(False)
            self.removeToolBar(toolbar)
            self.addToolBar(Qt.LeftToolBarArea, toolbar)

    def ask_for_open(self, path=None):
        if path is None:
            files = choose_files(
                self, 'ebook viewer open dialog',
                _('Choose e-book'), [(_('E-books'), available_input_formats())],
                all_files=False, select_only_single_file=True)
            if not files:
                return
            path = files[0]
        self.load_ebook(path)

    def continue_reading(self):
        rl = vprefs['session_data'].get('standalone_recently_opened')
        if rl:
            entry = rl[0]
            self.load_ebook(entry['pathtoebook'])

    def load_ebook(self, pathtoebook, open_at=None, reload_book=False):
        self.web_view.show_home_page_on_ready = False
        if open_at:
            self.pending_open_at = open_at
        self.setWindowTitle(_('Loading book') + '… — {}'.format(self.base_window_title))
        self.loading_overlay(_('Loading book, please wait'))
        self.save_annotations()
        self.current_book_data = {}
        t = Thread(name='LoadBook', target=self._load_ebook_worker, args=(pathtoebook, open_at, reload_book or self.force_reload))
        t.daemon = True
        t.start()

    def reload_book(self):
        if self.current_book_data:
            self.load_ebook(self.current_book_data['pathtoebook'], reload_book=True)

    def _load_ebook_worker(self, pathtoebook, open_at, reload_book):
        if DEBUG:
            start_time = monotonic()
        try:
            ans = prepare_book(pathtoebook, force=reload_book, prepare_notify=self.prepare_notify)
        except WorkerError as e:
            self.book_prepared.emit(False, {'exception': e, 'tb': e.orig_tb, 'pathtoebook': pathtoebook})
        except Exception as e:
            import traceback
            self.book_prepared.emit(False, {'exception': e, 'tb': traceback.format_exc(), 'pathtoebook': pathtoebook})
        else:
            if DEBUG:
                print('Book prepared in {:.2f} seconds'.format(monotonic() - start_time))
            self.book_prepared.emit(True, {'base': ans, 'pathtoebook': pathtoebook, 'open_at': open_at, 'reloaded': reload_book})

    def prepare_notify(self):
        self.book_preparation_started.emit()

    def load_finished(self, ok, data):
        if self.shutting_down:
            return
        open_at, self.pending_open_at = self.pending_open_at, None
        self.web_view.clear_caches()
        if not ok:
            self.setWindowTitle(self.base_window_title)
            tb = data['tb'].strip()
            tb = re.split(r'^calibre\.gui2\.viewer\.convert_book\.ConversionFailure:\s*', tb, maxsplit=1, flags=re.M)[-1]
            last_line = tuple(tb.strip().splitlines())[-1]
            if last_line.startswith('calibre.ebooks.DRMError'):
                DRMErrorMessage(self).exec_()
            else:
                error_dialog(self, _('Loading book failed'), _(
                    'Failed to open the book at {0}. Click "Show details" for more info.').format(data['pathtoebook']),
                    det_msg=tb, show=True)
            self.loading_overlay.hide()
            self.web_view.show_home_page()
            return
        try:
            set_book_path(data['base'], data['pathtoebook'])
        except Exception:
            if data['reloaded']:
                raise
            self.load_ebook(data['pathtoebook'], open_at=data['open_at'], reload_book=True)
            return
        self.current_book_data = data
        self.current_book_data['annotations_map'] = defaultdict(list)
        self.current_book_data['annotations_path_key'] = path_key(data['pathtoebook']) + '.json'
        self.load_book_data()
        self.update_window_title()
        initial_cfi = self.initial_cfi_for_current_book()
        initial_position = {'type': 'cfi', 'data': initial_cfi} if initial_cfi else None
        if open_at:
            if open_at.startswith('toc:'):
                initial_toc_node = self.toc_model.node_id_for_text(open_at[len('toc:'):])
                initial_position = {'type': 'toc', 'data': initial_toc_node}
            elif open_at.startswith('toc-href:'):
                initial_toc_node = self.toc_model.node_id_for_href(open_at[len('toc-href:'):], exact=True)
                initial_position = {'type': 'toc', 'data': initial_toc_node}
            elif open_at.startswith('toc-href-contains:'):
                initial_toc_node = self.toc_model.node_id_for_href(open_at[len('toc-href-contains:'):], exact=False)
                initial_position = {'type': 'toc', 'data': initial_toc_node}
            elif open_at.startswith('epubcfi(/'):
                initial_position = {'type': 'cfi', 'data': open_at}
            elif open_at.startswith('ref:'):
                initial_position = {'type': 'ref', 'data': open_at[len('ref:'):]}
            elif is_float(open_at):
                initial_position = {'type': 'bookpos', 'data': float(open_at)}
        self.web_view.start_book_load(initial_position=initial_position)

    def load_book_data(self):
        self.load_book_annotations()
        path = os.path.join(self.current_book_data['base'], 'calibre-book-manifest.json')
        with open(path, 'rb') as f:
            raw = f.read()
        self.current_book_data['manifest'] = manifest = json.loads(raw)
        toc = manifest.get('toc')
        self.toc_model = TOC(toc)
        self.toc.setModel(self.toc_model)
        self.bookmarks_widget.set_bookmarks(self.current_book_data['annotations_map']['bookmark'])
        self.current_book_data['metadata'] = set_book_path.parsed_metadata
        self.current_book_data['manifest'] = set_book_path.parsed_manifest

    def load_book_annotations(self):
        amap = self.current_book_data['annotations_map']
        path = os.path.join(self.current_book_data['base'], 'calibre-book-annotations.json')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                raw = f.read()
            merge_annotations(json_loads(raw), amap)
        path = os.path.join(annotations_dir, self.current_book_data['annotations_path_key'])
        if os.path.exists(path):
            with open(path, 'rb') as f:
                raw = f.read()
            merge_annotations(parse_annotations(raw), amap)

    def update_window_title(self):
        try:
            title = self.current_book_data['metadata']['title']
        except Exception:
            title = _('Unknown')
        book_format = self.current_book_data['manifest']['book_format']
        title = '{} [{}] — {}'.format(title, book_format, self.base_window_title)
        self.setWindowTitle(title)
    # }}}

    # CFI management {{{
    def initial_cfi_for_current_book(self):
        lrp = self.current_book_data['annotations_map']['last-read']
        if lrp and get_session_pref('remember_last_read', default=True):
            lrp = lrp[0]
            if lrp['pos_type'] == 'epubcfi':
                return lrp['pos']

    def cfi_changed(self, cfi):
        if not self.current_book_data:
            return
        self.current_book_data['annotations_map']['last-read'] = [{
            'pos': cfi, 'pos_type': 'epubcfi', 'timestamp': utcnow()}]
    # }}}

    # State serialization {{{
    def save_annotations(self):
        if not self.current_book_data:
            return
        amap = self.current_book_data['annotations_map']
        annots = as_bytes(serialize_annotations(amap))
        with open(os.path.join(annotations_dir, self.current_book_data['annotations_path_key']), 'wb') as f:
            f.write(annots)
        if self.current_book_data.get('pathtoebook', '').lower().endswith(
                '.epub') and get_session_pref('save_annotations_in_ebook', default=True):
            path = self.current_book_data['pathtoebook']
            if os.access(path, os.W_OK):
                before_stat = os.stat(path)
                save_annots_to_epub(path, annots)
                update_book(path, before_stat, {'calibre-book-annotations.json': annots})

    def save_state(self):
        with vprefs:
            vprefs['main_window_state'] = bytearray(self.saveState(self.MAIN_WINDOW_STATE_VERSION))
            vprefs['main_window_geometry'] = bytearray(self.saveGeometry())

    def restore_state(self):
        state = vprefs['main_window_state']
        geom = vprefs['main_window_geometry']
        if geom and get_session_pref('remember_window_geometry', default=False):
            QApplication.instance().safe_restore_geometry(self, geom)
        if state:
            self.restoreState(state, self.MAIN_WINDOW_STATE_VERSION)
            self.inspector_dock.setVisible(False)

    def quit(self):
        self.close()

    def closeEvent(self, ev):
        self.shutting_down = True
        try:
            self.save_annotations()
            self.save_state()
        except Exception:
            import traceback
            traceback.print_exc()
        clean_running_workers()
        return MainWindow.closeEvent(self, ev)
    # }}}
