#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

import json
from collections import Counter
from threading import Thread

import regex
from PyQt5.Qt import (
    QCheckBox, QComboBox, QHBoxLayout, QIcon, QLabel, QListWidget, QListWidgetItem,
    QStaticText, QStyle, QStyledItemDelegate, Qt, QToolButton, QVBoxLayout, QWidget,
    pyqtSignal
)

from calibre.ebooks.conversion.search_replace import REGEX_FLAGS
from calibre.gui2 import warning_dialog
from calibre.gui2.progress_indicator import ProgressIndicator
from calibre.gui2.viewer.web_view import get_data, get_manifest, vprefs
from calibre.gui2.widgets2 import HistoryComboBox
from polyglot.builtins import iteritems, unicode_type
from polyglot.functools import lru_cache
from polyglot.queue import Queue


class BusySpinner(QWidget):  # {{{

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.l = l = QHBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        self.pi = ProgressIndicator(self, 24)
        l.addWidget(self.pi)
        self.la = la = QLabel(_('Searching...'))
        l.addWidget(la)
        l.addStretch(10)
        self.is_running = False

    def start(self):
        self.setVisible(True)
        self.pi.start()
        self.is_running = True

    def stop(self):
        self.setVisible(False)
        self.pi.stop()
        self.is_running = False
# }}}


quote_map= {'"':'"“”', "'": "'‘’"}
qpat = regex.compile(r'''(['"])''')


def text_to_regex(text):
    ans = []
    for part in qpat.split(text):
        r = quote_map.get(part)
        if r is not None:
            ans.append('[' + r + ']')
        else:
            ans.append(regex.escape(part))
    return ''.join(ans)


class Search(object):

    def __init__(self, text, mode, case_sensitive, backwards):
        self.text, self.mode = text, mode
        self.case_sensitive = case_sensitive
        self.backwards = backwards
        self._regex = None

    def __eq__(self, other):
        return self.text == other.text and self.mode == other.mode and self.case_sensitive == other.case_sensitive

    @property
    def regex(self):
        if self._regex is None:
            expr = self.text
            flags = REGEX_FLAGS
            if not self.case_sensitive:
                flags = regex.IGNORECASE
            if self.mode != 'regex':
                if self.mode == 'word':
                    words = []
                    for part in expr.split():
                        words.append(r'\b{}\b'.format(text_to_regex(part)))
                    expr = r'\s+'.join(words)
                else:
                    expr = text_to_regex(expr)
            self._regex = regex.compile(expr, flags)
        return self._regex


class SearchFinished(object):

    def __init__(self, search_query):
        self.search_query = search_query


class SearchResult(object):

    __slots__ = ('search_query', 'before', 'text', 'after', 'spine_idx', 'index', 'file_name', '_static_text')

    def __init__(self, search_query, before, text, after, name, spine_idx, index):
        self.search_query = search_query
        self.before, self.text, self.after = before, text, after
        self.spine_idx, self.index = spine_idx, index
        self.file_name = name
        self._static_text = None

    @property
    def static_text(self):
        if self._static_text is None:
            before_words = self.before.split()
            before = ' '.join(before_words[-3:])
            before_extra = len(before) - 15
            if before_extra > 0:
                before = before[before_extra:]
            before = '…' + before
            before_space = '' if self.before.rstrip() == self.before else ' '
            after_words = self.after.split()
            after = ' '.join(after_words[:3])[:15] + '…'
            after_space = '' if self.after.lstrip() == self.after else ' '
            self._static_text = st = QStaticText('<p>{}{}<b>{}</b>{}{}'.format(before, before_space, self.text, after_space, after))
            st.setTextFormat(Qt.RichText)
            st.setTextWidth(10000)
        return self._static_text

    @property
    def for_js(self):
        return {
            'file_name': self.file_name, 'spine_idx': self.spine_idx, 'index': self.index, 'text': self.text,
            'before': self.before, 'after': self.after, 'mode': self.search_query.mode
        }

    def is_or_is_after(self, result_from_js):
        return result_from_js['spine_idx'] == self.spine_idx and self.index >= result_from_js['index'] and result_from_js['text'] == self.text


@lru_cache(maxsize=None)
def searchable_text_for_name(name):
    ans = []
    serialized_data = json.loads(get_data(name)[0])
    stack = []
    for child in serialized_data['tree']['c']:
        if child.get('n') == 'body':
            stack.append(child)
    ignore_text = {'script', 'style', 'title'}
    while stack:
        node = stack.pop()
        if isinstance(node, unicode_type):
            ans.append(node)
            continue
        g = node.get
        name = g('n')
        text = g('x')
        tail = g('l')
        children = g('c')
        if name and text and name not in ignore_text:
            ans.append(text)
        if tail:
            stack.append(tail)
        if children:
            stack.extend(reversed(children))
    # Normalize whitespace to a single space, this will cause failures
    # when searching over spaces in pre nodes, but that is a lesser evil
    # since the DOM converts \n, \t etc to a single space
    return regex.sub(r'\s+', ' ', ''.join(ans))


def search_in_name(name, search_query, ctx_size=50):
    raw = searchable_text_for_name(name)
    for match in search_query.regex.finditer(raw):
        start, end = match.span()
        before = raw[max(0, start-ctx_size):start]
        after = raw[end:end+ctx_size]
        yield before, match.group(), after


class SearchBox(HistoryComboBox):

    history_saved = pyqtSignal(object, object)

    def save_history(self):
        ret = HistoryComboBox.save_history(self)
        self.history_saved.emit(self.text(), self.history)
        return ret

    def contextMenuEvent(self, event):
        menu = self.lineEdit().createStandardContextMenu()
        menu.addSeparator()
        menu.addAction(_('Clear search history'), self.clear_history)
        menu.exec_(event.globalPos())


class SearchInput(QWidget):  # {{{

    do_search = pyqtSignal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ignore_search_type_changes = False
        self.l = l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 0)
        l.addLayout(h)

        self.search_box = sb = SearchBox(self)
        sb.initialize('viewer-search-panel-expression')
        sb.item_selected.connect(self.saved_search_selected)
        sb.history_saved.connect(self.history_saved)
        sb.lineEdit().setPlaceholderText(_('Search'))
        sb.lineEdit().setClearButtonEnabled(True)
        sb.lineEdit().returnPressed.connect(self.find_next)
        h.addWidget(sb)

        self.next_button = nb = QToolButton(self)
        h.addWidget(nb)
        nb.setFocusPolicy(Qt.NoFocus)
        nb.setIcon(QIcon(I('arrow-down.png')))
        nb.clicked.connect(self.find_next)
        nb.setToolTip(_('Find next match'))

        self.prev_button = nb = QToolButton(self)
        h.addWidget(nb)
        nb.setFocusPolicy(Qt.NoFocus)
        nb.setIcon(QIcon(I('arrow-up.png')))
        nb.clicked.connect(self.find_previous)
        nb.setToolTip(_('Find previous match'))

        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 0)
        l.addLayout(h)
        self.query_type = qt = QComboBox(self)
        qt.setFocusPolicy(Qt.NoFocus)
        qt.addItem(_('Contains'), 'normal')
        qt.addItem(_('Whole words'), 'word')
        qt.addItem(_('Regex'), 'regex')
        qt.setToolTip(('<p>' + _(
            'Choose the type of search: <ul>'
            '<li><b>Contains</b> will search for the entered text anywhere.'
            '<li><b>Whole words</b> will search for whole words that equal the entered text.'
            '<li><b>Regex</b> will interpret the text as a regular expression.'
        )))
        qt.setCurrentIndex(qt.findData(vprefs.get('viewer-search-mode', 'normal') or 'normal'))
        qt.currentIndexChanged.connect(self.save_search_type)
        h.addWidget(qt)

        self.case_sensitive = cs = QCheckBox(_('&Case sensitive'), self)
        cs.setFocusPolicy(Qt.NoFocus)
        cs.setChecked(bool(vprefs.get('viewer-search-case-sensitive', False)))
        cs.stateChanged.connect(self.save_search_type)
        h.addWidget(cs)

    def history_saved(self, new_text, history):
        if new_text:
            sss = vprefs.get('saved-search-settings') or {}
            sss[new_text] = {'case_sensitive': self.case_sensitive.isChecked(), 'mode': self.query_type.currentData()}
            history = frozenset(history)
            sss = {k: v for k, v in iteritems(sss) if k in history}
            vprefs['saved-search-settings'] = sss

    def save_search_type(self):
        text = self.search_box.currentText().strip()
        if text and not self.ignore_search_type_changes:
            sss = vprefs.get('saved-search-settings') or {}
            sss[text] = {'case_sensitive': self.case_sensitive.isChecked(), 'mode': self.query_type.currentData()}
            vprefs['saved-search-settings'] = sss

    def saved_search_selected(self):
        text = self.search_box.currentText().strip()
        if text:
            s = (vprefs.get('saved-search-settings') or {}).get(text)
            if s:
                self.ignore_search_type_changes = True
                if 'case_sensitive' in s:
                    self.case_sensitive.setChecked(s['case_sensitive'])
                if 'mode' in s:
                    idx = self.query_type.findData(s['mode'])
                    if idx > -1:
                        self.query_type.setCurrentIndex(idx)
                self.ignore_search_type_changes = False
            self.find_next()

    def search_query(self, backwards=False):
        text = self.search_box.currentText().strip()
        if text:
            return Search(
                text, self.query_type.currentData() or 'normal',
                self.case_sensitive.isChecked(), backwards
            )

    def emit_search(self, backwards=False):
        vprefs['viewer-search-case-sensitive'] = self.case_sensitive.isChecked()
        vprefs['viewer-search-mode'] = self.query_type.currentData()
        sq = self.search_query(backwards)
        if sq is not None:
            self.do_search.emit(sq)

    def find_next(self):
        self.emit_search()

    def find_previous(self):
        self.emit_search(backwards=True)

    def focus_input(self):
        self.search_box.setFocus(Qt.OtherFocusReason)
        le = self.search_box.lineEdit()
        le.end(False)
        le.selectAll()
# }}}


class ResultsDelegate(QStyledItemDelegate):  # {{{

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)
        result = index.data(Qt.UserRole)
        painter.save()
        p = option.palette
        c = p.HighlightedText if option.state & QStyle.State_Selected else p.Text
        group = (p.Active if option.state & QStyle.State_Active else p.Inactive)
        c = p.color(group, c)
        painter.setClipRect(option.rect)
        painter.setPen(c)
        try:
            painter.drawStaticText(option.rect.topLeft(), result.static_text)
        except Exception:
            import traceback
            traceback.print_exc()
        painter.restore()
# }}}


class Results(QListWidget):  # {{{

    show_search_result = pyqtSignal(object)

    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet('QListWidget::item { padding: 3px; }')
        self.delegate = ResultsDelegate(self)
        self.setItemDelegate(self.delegate)
        self.itemClicked.connect(self.item_activated)

    def add_result(self, result):
        i = QListWidgetItem(' ', self)
        i.setData(Qt.UserRole, result)
        return self.count()

    def item_activated(self):
        i = self.currentItem()
        if i:
            sr = i.data(Qt.UserRole)
            self.show_search_result.emit(sr)

    def find_next(self, previous):
        if self.count() < 1:
            return
        i = self.currentRow()
        i += -1 if previous else 1
        i %= self.count()
        self.setCurrentRow(i)
        self.item_activated()

    def search_result_not_found(self, sr):
        remove = []
        for i in range(self.count()):
            item = self.item(i)
            r = item.data(Qt.UserRole)
            if r.is_or_is_after(sr):
                remove.append(i)
        if remove:
            last_i = remove[-1]
            if last_i < self.count() - 1:
                self.setCurrentRow(last_i + 1)
                self.item_activated()
            elif remove[0] > 0:
                self.setCurrentRow(remove[0] - 1)
                self.item_activated()
            for i in reversed(remove):
                self.takeItem(i)
            if self.count():
                warning_dialog(self, _('Hidden text'), _(
                    'Some search results were for hidden text, they have been removed.'), show=True)

# }}}


class SearchPanel(QWidget):  # {{{

    search_requested = pyqtSignal(object)
    results_found = pyqtSignal(object)
    show_search_result = pyqtSignal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.current_search = None
        self.l = l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        self.search_input = si = SearchInput(self)
        self.searcher = None
        self.search_tasks = Queue()
        self.results_found.connect(self.on_result_found, type=Qt.QueuedConnection)
        si.do_search.connect(self.search_requested)
        l.addWidget(si)
        self.results = r = Results(self)
        r.show_search_result.connect(self.do_show_search_result, type=Qt.QueuedConnection)
        l.addWidget(r, 100)
        self.spinner = s = BusySpinner(self)
        s.setVisible(False)
        l.addWidget(s)

    def focus_input(self):
        self.search_input.focus_input()

    def start_search(self, search_query, current_name):
        if self.current_search is not None and search_query == self.current_search:
            self.find_next_requested(search_query.backwards)
            return
        if self.searcher is None:
            self.searcher = Thread(name='Searcher', target=self.run_searches)
            self.searcher.daemon = True
            self.searcher.start()
        self.results.clear()
        self.spinner.start()
        self.current_search = search_query
        self.search_tasks.put((search_query, current_name))

    def run_searches(self):
        while True:
            x = self.search_tasks.get()
            if x is None:
                break
            search_query, current_name = x
            try:
                manifest = get_manifest() or {}
                spine = manifest.get('spine', ())
                idx_map = {name: i for i, name in enumerate(spine)}
                spine_idx = idx_map.get(current_name, -1)
            except Exception:
                import traceback
                traceback.print_exc()
                spine_idx = -1
            if spine_idx < 0:
                self.results_found.emit(SearchFinished(search_query))
                continue
            for name in spine:
                counter = Counter()
                spine_idx = idx_map[name]
                try:
                    for i, result in enumerate(search_in_name(name, search_query)):
                        before, text, after = result
                        self.results_found.emit(SearchResult(search_query, before, text, after, name, spine_idx, counter[text]))
                        counter[text] += 1
                except Exception:
                    import traceback
                    traceback.print_exc()
            self.results_found.emit(SearchFinished(search_query))

    def on_result_found(self, result):
        if self.current_search is None or result.search_query != self.current_search:
            return
        if isinstance(result, SearchFinished):
            self.spinner.stop()
            if not self.results.count():
                self.show_no_results_found()
            return
        if self.results.add_result(result) == 1:
            # first result
            self.results.setCurrentRow(0)
            self.results.item_activated()

    def visibility_changed(self, visible):
        if visible:
            self.focus_input()

    def clear_searches(self):
        self.current_search = None
        searchable_text_for_name.cache_clear()
        self.spinner.stop()
        self.results.clear()

    def shutdown(self):
        self.search_tasks.put(None)
        self.spinner.stop()
        self.current_search = None
        self.searcher = None

    def find_next_requested(self, previous):
        self.results.find_next(previous)

    def do_show_search_result(self, sr):
        self.show_search_result.emit(sr.for_js)

    def search_result_not_found(self, sr):
        self.results.search_result_not_found(sr)
        if not self.results.count() and not self.spinner.is_running:
            self.show_no_results_found()

    def show_no_results_found(self):
        if self.current_search:
            warning_dialog(self, _('No matches found'), _(
                'No matches were found for: <b>{}</b>').format(self.current_search.text), show=True)
# }}}
