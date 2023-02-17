#!/usr/bin/env python


__license__ = 'GPL v3'
__copyright__ = '2015, Kovid Goyal <kovid at kovidgoyal.net>'

import bz2
import errno
import importlib
import json
import math
import os
import sys
import tempfile
from contextlib import suppress
from functools import lru_cache
from io import BytesIO
from itertools import count
from multiprocessing.pool import ThreadPool
from qt.core import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFormLayout, QGroupBox, QHBoxLayout, QIcon, QImage, QImageReader,
    QItemSelectionModel, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPen, QPixmap,
    QProgressDialog, QSize, QSpinBox, QSplitter, QStackedLayout, QStaticText, QStyle,
    QStyledItemDelegate, Qt, QTabWidget, QTextEdit, QVBoxLayout, QWidget, pyqtSignal,
    sip,
)
from threading import Event, Thread

from calibre import detect_ncpus as cpu_count, fit_image, human_readable, walk
from calibre.constants import cache_dir
from calibre.customize.ui import interface_actions
from calibre.gui2 import (
    choose_dir, choose_save_file, empty_index, error_dialog, gprefs,
    icon_resource_manager, must_use_qt, safe_open_url,
)
from calibre.gui2.dialogs.progress import ProgressDialog
from calibre.gui2.progress_indicator import ProgressIndicator
from calibre.gui2.widgets2 import Dialog
from calibre.utils.date import utcnow
from calibre.utils.filenames import ascii_filename, atomic_rename
from calibre.utils.https import HTTPError, get_https_resource_securely
from calibre.utils.icu import numeric_sort_key as sort_key
from calibre.utils.img import Canvas, image_from_data, optimize_jpeg, optimize_png
from calibre.utils.resources import get_image_path as I, get_path as P
from calibre.utils.zipfile import ZIP_STORED, ZipFile
from polyglot import http_client
from polyglot.builtins import as_bytes, iteritems, reraise
from polyglot.queue import Empty, Queue

IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
THEME_COVER = 'icon-theme-cover.jpg'
THEME_METADATA = 'metadata.json'
BASE_URL = 'https://code.calibre-ebook.com/icon-themes/'

# Theme creation {{{

COVER_SIZE = (340, 272)


def render_svg(filepath):
    must_use_qt(headless=False)
    pngpath = filepath[:-4] + '.png'
    i = QImage(filepath)
    i.save(pngpath)


def read_images_from_folder(path):
    name_map = {}
    path = os.path.abspath(path)
    for filepath in walk(path):
        name = os.path.relpath(filepath, path).replace(os.sep, '/')
        ext = name.rpartition('.')[-1]
        bname = os.path.basename(name)
        if bname.startswith('.') or bname.startswith('_'):
            continue
        if ext == 'svg':
            render_svg(filepath)
            ext = 'png'
            filepath = filepath[:-4] + '.png'
            name = name[:-4] + '.png'
        if ext in IMAGE_EXTENSIONS:
            name_map[name] = filepath
    return name_map


class Theme:

    def __init__(self, title='', author='', version=-1, description='', license='Unknown', url=None, cover=None):
        self.title, self.author, self.version, self.description = title, author, version, description
        self.license, self.cover, self.url = license, cover, url


class Report:

    def __init__(self, path, name_map, extra, missing, theme):
        self.path, self.name_map, self.extra, self.missing, self.theme = path, name_map, extra, missing, theme
        self.bad = {}

    @property
    def name(self):
        return ascii_filename(self.theme.title).replace(' ', '_').replace('.', '_').lower()


def read_theme_from_folder(path):
    path = os.path.abspath(path)
    current_image_map = read_images_from_folder(P('images', allow_user_override=False))
    name_map = read_images_from_folder(path)
    name_map.pop(THEME_COVER, None)
    name_map.pop('blank.png', None)
    current_names = frozenset(current_image_map)
    names = frozenset(name_map)
    extra = names - current_names
    missing = current_names - names
    try:
        with open(os.path.join(path, THEME_METADATA), 'rb') as f:
            metadata = json.load(f)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
        metadata = {}
    except ValueError:
        # Corrupted metadata file
        metadata = {}

    def safe_int(x):
        try:
            return int(x)
        except Exception:
            return -1

    def g(x, defval=''):
        return metadata.get(x, defval)
    theme = Theme(g('title'), g('author'), safe_int(g('version', -1)), g('description'), g('license', 'Unknown'), g('url', None))

    ans = Report(path, name_map, extra, missing, theme)
    try:
        with open(os.path.join(path, THEME_COVER), 'rb') as f:
            theme.cover = f.read()
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
        theme.cover = create_cover(ans)
    return ans


def icon_for_action(name):
    for plugin in interface_actions():
        if plugin.name == name:
            module, class_name = plugin.actual_plugin.partition(':')[::2]
            mod = importlib.import_module(module)
            cls = getattr(mod, class_name)
            icon = cls.action_spec[1]
            if icon:
                return icon


def default_cover_icons(cols=5):
    count = 0
    for ac in gprefs.defaults['action-layout-toolbar']:
        if ac:
            icon = icon_for_action(ac)
            if icon:
                count += 1
                yield icon
    for x in 'user_profile plus minus series sync tags default_cover'.split():
        yield x + '.png'
        count += 1
    extra = 'search donate cover_flow reader publisher back forward'.split()
    while count < 15 or count % cols != 0:
        yield extra[0] + '.png'
        del extra[0]
        count += 1


def create_cover(report=None, icons=(), cols=5, size=120, padding=16, darkbg=False):
    icons = icons or tuple(default_cover_icons(cols))
    rows = int(math.ceil(len(icons) / cols))
    with Canvas(cols * (size + padding), rows * (size + padding), bgcolor='#444' if darkbg else '#eee') as canvas:
        y = -size - padding // 2
        x = 0
        for i, icon in enumerate(icons):
            if i % cols == 0:
                y += padding + size
                x = padding // 2
            else:
                x += size + padding
            if report and icon in report.name_map:
                ipath = os.path.join(report.path, report.name_map[icon])
            else:
                ipath = I(icon, allow_user_override=False)
            with open(ipath, 'rb') as f:
                img = image_from_data(f.read())
            scaled, nwidth, nheight = fit_image(img.width(), img.height(), size, size)
            img = img.scaled(int(nwidth), int(nheight), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            dx = (size - nwidth) // 2
            canvas.compose(img, x + dx, y)
    return canvas.export()


def verify_theme(report):
    must_use_qt()
    report.bad = bad = {}
    for name, path in iteritems(report.name_map):
        reader = QImageReader(os.path.join(report.path, path))
        img = reader.read()
        if img.isNull():
            bad[name] = reader.errorString()
    return bool(bad)


class ThemeCreateDialog(Dialog):

    def __init__(self, parent, report):
        self.report = report
        Dialog.__init__(self, _('Create an icon theme'), 'create-icon-theme', parent)

    def setup_ui(self):
        self.splitter = QSplitter(self)
        self.l = l = QVBoxLayout(self)
        l.addWidget(self.splitter)
        self.h = h = QHBoxLayout()
        self.use_in_calibre = uic = QCheckBox(_('Use this theme in calibre'))
        uic.setToolTip(_('Change the current calibre icon theme to this theme'))
        uic.setChecked(bool(gprefs.get('use_created_icon_theme_in_calibre', True)))
        uic.toggled.connect(lambda checked: gprefs.set('use_created_icon_theme_in_calibre', bool(checked)))
        h.addWidget(uic), h.addStretch(), h.addWidget(self.bb)
        l.addLayout(h)
        self.w = w = QGroupBox(_('Theme Metadata'), self)
        self.splitter.addWidget(w)
        l = w.l = QFormLayout(w)
        l.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.missing_icons_group = mg = QGroupBox(self)
        self.missing_icons = mi = QListWidget(mg)
        mi.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        mg.l = QVBoxLayout(mg)
        mg.l.addWidget(mi)
        self.splitter.addWidget(mg)
        self.title = QLineEdit(self)
        l.addRow(_('&Title:'), self.title)
        self.author = QLineEdit(self)
        l.addRow(_('&Author:'), self.author)
        self.version = v = QSpinBox(self)
        v.setMinimum(1), v.setMaximum(1000000)
        l.addRow(_('&Version:'), v)
        self.license = lc = QLineEdit(self)
        self.color_palette = cp = QComboBox(self)
        cp.addItem(_('Light and Dark'), 'any')
        cp.addItem(_('Light only'), 'light')
        cp.addItem(_('Dark only'), 'dark')
        cp.setToolTip(_('Specify the color palette this icon theme is suited for'))
        l.addRow(_('&Color palette:'), cp)
        l.addRow(_('&License:'), lc)
        self.url = QLineEdit(self)
        l.addRow(_('&URL:'), self.url)
        lc.setText(_(
            'The license for the icons in this theme. Common choices are'
            ' Creative Commons or Public Domain.'))
        self.description = QTextEdit(self)
        l.addRow(self.description)
        self.refresh_button = rb = self.bb.addButton(_('&Refresh'), QDialogButtonBox.ButtonRole.ActionRole)
        rb.setIcon(QIcon.ic('view-refresh.png'))
        rb.clicked.connect(self.refresh)

        self.apply_report()

    def sizeHint(self):
        return QSize(900, 670)

    @property
    def metadata(self):
        self.report.theme.title = self.title.text().strip()  # Needed for report.name to work
        return {
            'title': self.title.text().strip(),
            'author': self.author.text().strip(),
            'color_palette': self.color_palette.currentData(),
            'version': self.version.value(),
            'description': self.description.toPlainText().strip(),
            'number': len(self.report.name_map) - len(self.report.extra),
            'date': utcnow().date().isoformat(),
            'name': self.report.name,
            'license': self.license.text().strip() or 'Unknown',
            'url': self.url.text().strip() or None,
        }

    def save_metadata(self):
        data = json.dumps(self.metadata, indent=2)
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        with open(os.path.join(self.report.path, THEME_METADATA), 'wb') as f:
            f.write(data)

    def refresh(self):
        self.save_metadata()
        self.report = read_theme_from_folder(self.report.path)
        self.apply_report()

    def apply_report(self):
        theme = self.report.theme
        self.title.setText((theme.title or '').strip())
        self.author.setText((theme.author or '').strip())
        self.version.setValue(theme.version or 1)
        self.description.setText((theme.description or '').strip())
        self.license.setText((theme.license or 'Unknown').strip())
        self.url.setText((theme.url or '').strip())
        if self.report.missing:
            title =  _('%d icons missing in this theme') % len(self.report.missing)
        else:
            title = _('No missing icons')
        self.missing_icons_group.setTitle(title)
        mi = self.missing_icons
        mi.clear()
        for name in sorted(self.report.missing):
            QListWidgetItem(QIcon(I(name, allow_user_override=False)), name, mi)

    def accept(self):
        mi = self.metadata
        if not mi.get('title'):
            return error_dialog(self, _('No title specified'), _(
                'You must specify a title for this icon theme'), show=True)
        if not mi.get('author'):
            return error_dialog(self, _('No author specified'), _(
                'You must specify an author for this icon theme'), show=True)
        return Dialog.accept(self)


class Compress(QProgressDialog):

    update_signal = pyqtSignal(object, object)

    def __init__(self, report, theme_metadata, parent=None):
        total = 2 + len(report.name_map)
        self.theme_metadata = theme_metadata
        QProgressDialog.__init__(self, _('Losslessly optimizing images, please wait...'), _('&Abort'), 0, total, parent)
        self.setWindowTitle(self.labelText())
        self.setWindowIcon(QIcon.ic('lt.png'))
        self.setMinimumDuration(0)
        self.update_signal.connect(self.do_update, type=Qt.ConnectionType.QueuedConnection)
        self.raw = self.prefix = None
        self.abort = Event()
        self.canceled.connect(self.abort.set)
        self.t = Thread(name='CompressIcons', target=self.run_compress, args=(report,))
        self.t.daemon = False
        self.t.start()

    def do_update(self, num, message):
        if num < 0:
            return self.onerror(_('Optimizing images failed, click "Show details" for more information'), message)
        self.setValue(num)
        self.setLabelText(message)

    def onerror(self, msg, details):
        error_dialog(self, _('Compression failed'), msg, det_msg=details, show=True)
        self.close()

    def onprogress(self, num, msg):
        self.update_signal.emit(num, msg)
        return not self.wasCanceled()

    def run_compress(self, report):
        try:
            self.raw, self.prefix, self.icon_zip_data = create_themeball(report, self.theme_metadata, self.onprogress, self.abort)
        except Exception:
            import traceback
            traceback.print_exc()
            self.update_signal.emit(-1, traceback.format_exc())
        else:
            self.update_signal.emit(self.maximum(), '')


def create_themeball(report, theme_metadata, progress=None, abort=None):
    pool = ThreadPool(processes=cpu_count())
    buf = BytesIO()
    num = count()
    error_occurred = Event()

    def optimize(name):
        if abort is not None and abort.is_set():
            return
        if error_occurred.is_set():
            return
        try:
            i = next(num)
            if progress is not None:
                progress(i, _('Optimizing %s') % name)
            srcpath = os.path.join(report.path, name)
            ext = srcpath.rpartition('.')[-1].lower()
            if ext == 'png':
                optimize_png(srcpath)
            elif ext in ('jpg', 'jpeg'):
                optimize_jpeg(srcpath)
        except Exception:
            return sys.exc_info()

    errors = tuple(filter(None, pool.map(optimize, tuple(report.name_map))))
    pool.close(), pool.join()
    if abort is not None and abort.is_set():
        return None, None, None
    if errors:
        e = errors[0]
        reraise(*e)

    if progress is not None:
        progress(next(num), _('Creating theme file'))
    with ZipFile(buf, 'w') as zf:
        for name in report.name_map:
            srcpath = os.path.join(report.path, name)
            with open(srcpath, 'rb') as f:
                zf.writestr(name, f.read(), compression=ZIP_STORED)
    buf.seek(0)
    icon_zip_data = buf
    if abort is not None and abort.is_set():
        return None, None, None
    if progress is not None:
        progress(next(num), _('Compressing theme file'))
    import lzma
    compressed = lzma.compress(icon_zip_data.getvalue(), format=lzma.FORMAT_XZ, preset=9)
    buf = BytesIO()
    prefix = report.name
    if abort is not None and abort.is_set():
        return None, None, None
    with ZipFile(buf, 'w') as zf:
        with open(os.path.join(report.path, THEME_METADATA), 'rb') as f:
            zf.writestr(prefix + '/' + THEME_METADATA, f.read())
        zf.writestr(prefix + '/' + THEME_COVER, create_cover(report, darkbg=theme_metadata.get('color_palette') == 'dark'))
        zf.writestr(prefix + '/' + 'icons.zip.xz', compressed, compression=ZIP_STORED)
    if progress is not None:
        progress(next(num), _('Finished'))
    return buf.getvalue(), prefix, icon_zip_data


def create_theme(folder=None, parent=None):
    if folder is None:
        folder = choose_dir(parent, 'create-icon-theme-folder', _(
            'Choose a folder from which to read the icons'))
        if not folder:
            return
    report = read_theme_from_folder(folder)
    d = ThemeCreateDialog(parent, report)
    if d.exec() != QDialog.DialogCode.Accepted:
        return
    use_in_calibre = d.use_in_calibre.isChecked()
    theme = d.metadata
    d.save_metadata()
    d = Compress(d.report, theme, parent=parent)
    d.exec()
    if d.wasCanceled() or d.raw is None:
        return
    raw, prefix = d.raw, d.prefix
    dest = choose_save_file(parent, 'create-icon-theme-dest', _(
        'Choose destination for icon theme'),
        [(_('ZIP files'), ['zip'])], initial_filename=prefix + '.zip')
    if not dest:
        return
    with open(dest, 'wb') as f:
        f.write(raw)

    if use_in_calibre:
        path = icon_resource_manager.user_theme_resource_file(theme['color_palette'])
        install_icon_theme(theme, d.icon_zip_data, path, theme['color_palette'])
        icon_resource_manager.register_user_resource_files()
        icon_resource_manager.set_theme()
# }}}

# Choose Theme  {{{


def download_cover(cover_url, etag=None, cached=b''):
    url = BASE_URL + cover_url
    headers = {}
    if etag:
        if etag[0] != '"':
            etag = '"' + etag + '"'
        headers['If-None-Match'] = etag
    try:
        response = get_https_resource_securely(url, headers=headers, get_response=True)
        cached = response.read()
        etag = response.getheader('ETag', None) or None
        return cached, etag
    except HTTPError as e:
        if etag and e.code == http_client.NOT_MODIFIED:
            return cached, etag
        raise


def get_cover(metadata):
    cdir = os.path.join(cache_dir(), 'icon-theme-covers')
    try:
        os.makedirs(cdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    def path(ext):
        return os.path.join(cdir, metadata['name'] + '.' + ext)
    etag_file, cover_file = map(path, 'etag jpg'.split())

    def safe_read(path):
        with suppress(FileNotFoundError):
            with open(path, 'rb') as f:
                return f.read()
        return b''
    etag, cached = safe_read(etag_file), safe_read(cover_file)
    etag = etag.decode('utf-8')
    cached, etag = download_cover(metadata['cover-url'], etag, cached)
    if cached:
        aname = cover_file + '.atomic'
        with open(aname, 'wb') as f:
            f.write(cached)
        atomic_rename(aname, cover_file)
    if etag:
        with open(etag_file, 'wb') as f:
            f.write(as_bytes(etag))
    return cached or b''


def get_covers(themes, dialog, num_of_workers=8):
    items = Queue()
    for i in themes:
        items.put(i)

    def callback(metadata, x):
        if not sip.isdeleted(dialog) and not dialog.dialog_closed:
            dialog.cover_downloaded.emit(metadata, x)

    def run():
        while True:
            try:
                metadata = items.get_nowait()
            except Empty:
                return
            try:
                cdata = get_cover(metadata)
            except Exception as e:
                import traceback
                traceback.print_exc()
                callback(metadata, e)
            else:
                callback(metadata, cdata)

    for w in range(num_of_workers):
        t = Thread(name='IconThemeCover', target=run)
        t.daemon = True
        t.start()


class Delegate(QStyledItemDelegate):

    SPACING = 10

    def sizeHint(self, option, index):
        return QSize(COVER_SIZE[0] * 2, COVER_SIZE[1] + 2 * self.SPACING)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, empty_index)
        theme = index.data(Qt.ItemDataRole.UserRole)
        if not theme:
            return
        painter.save()
        pixmap = index.data(Qt.ItemDataRole.DecorationRole)
        if pixmap and not pixmap.isNull():
            rect = option.rect.adjusted(0, self.SPACING, COVER_SIZE[0] - option.rect.width(), - self.SPACING)
            painter.drawPixmap(rect, pixmap)
        if option.state & QStyle.StateFlag.State_Selected:
            painter.setPen(QPen(QApplication.instance().palette().highlightedText().color()))
        bottom = option.rect.bottom() - 2
        painter.drawLine(0, bottom, option.rect.right(), bottom)
        if 'static-text' not in theme:
            visit = _('Right click to visit theme homepage') if theme.get('url') else ''
            theme['static-text'] = QStaticText(_(
                '''
            <h2>{title}</h2>
            <p>by <i>{author}</i> with <b>{number}</b> icons [{size}]</p>
            <p>{description}</p>
            <p>Version: {version} Number of users: {usage:n}</p>
            <p><i>{visit}</i></p>
            ''').format(title=theme.get('title', _('Unknown')), author=theme.get('author', _('Unknown')),
                       number=theme.get('number', 0), description=theme.get('description', ''),
                       size=human_readable(theme.get('compressed-size', 0)), version=theme.get('version', 1),
                       usage=theme.get('usage', 0), visit=visit
        ))
        painter.drawStaticText(COVER_SIZE[0] + self.SPACING, option.rect.top() + self.SPACING, theme['static-text'])
        painter.restore()


class DownloadProgress(ProgressDialog):

    ds = pyqtSignal(object)
    acc = pyqtSignal()
    rej = pyqtSignal()

    def __init__(self, parent, size):
        ProgressDialog.__init__(self, _('Downloading icons...'), _(
            'Downloading icons, please wait...'), max=size, parent=parent, icon='download_metadata.png')
        self.ds.connect(self.bar.setValue, type=Qt.ConnectionType.QueuedConnection)
        self.acc.connect(self.accept, type=Qt.ConnectionType.QueuedConnection)
        self.rej.connect(self.reject, type=Qt.ConnectionType.QueuedConnection)

    def downloaded(self, byte_count):
        self.ds.emit(byte_count)

    def queue_accept(self):
        self.acc.emit()

    def queue_reject(self):
        self.rej.emit()


@lru_cache(maxsize=2)
def default_theme():
    dc = 0
    for name in walk(P('images')):
        if name.endswith('.png') and '/textures/' not in name.replace(os.sep, '/'):
            dc += 1
    p = QPixmap()
    p.loadFromData(create_cover())
    return {
        'name': 'default', 'title': _('Default icons'), 'color_palette': 'any',
        'user_msg': _('Use the calibre default icons'),
        'usage': 3_000_000, 'author': 'Kovid Goyal', 'number': dc,
        'cover-pixmap': p, 'compressed-size': os.path.getsize(P('icons.rcc', allow_user_override=False))
    }


def is_default_theme(t):
    return t.get('name') == default_theme()['name']


class ChooseThemeWidget(QWidget):

    sync_sorts = pyqtSignal(int)

    def __init__(self, for_theme='any', parent=None):
        super().__init__(parent)
        if parent:
            self.sync_sorts.connect(parent.sync_sorts)
        self.vl = vl = QVBoxLayout(self)
        self.for_theme = for_theme
        if self.for_theme == 'any':
            msg = _('Choose an icon theme below. It will be used for both light and dark color'
                    ' themes unless a color specific theme is chosen in one of the other tabs.')
        elif self.for_theme == 'light':
            msg = _('Choose an icon theme below. It will be used preferentially for light color themes.'
                    ' If the default is chosen then the theme for "light and dark" will be used.')
        elif self.for_theme == 'dark':
            msg = _('Choose an icon theme below. It will be used preferentially for dark color themes.'
                    ' If the default is chosen then the theme for "light and dark" will be used.')
        self.currently_installed_theme_metadata = icon_resource_manager.user_icon_theme_metadata(for_theme)
        self.currently_installed_theme_name = self.currently_installed_theme_metadata.get('name')
        self.msg = la = QLabel(msg)
        la.setWordWrap(True)
        vl.addWidget(la)
        self.sort_by = sb = QComboBox(self)
        self.hl = hl = QHBoxLayout()
        vl.addLayout(hl)
        self.sl = sl = QLabel(_('&Sort by:'))
        sl.setBuddy(sb)
        hl.addWidget(sl), hl.addWidget(sb), hl.addStretch(10)
        sb.addItems([_('Number of icons'), _('Popularity'), _('Name'),])
        sb.setEditable(False), sb.setCurrentIndex(gprefs.get('choose_icon_theme_sort_by', 1))
        sb.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        sb.currentIndexChanged.connect(self.sort_by_changed)
        self.theme_list = tl = QListWidget(self)
        vl.addWidget(tl)
        tl.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.delegate = Delegate(tl)
        tl.setItemDelegate(self.delegate)
        tl.itemPressed.connect(self.item_clicked)

    def sort_by_changed(self):
        self.re_sort()
        gprefs.set('choose_icon_theme_sort_by', self.sort_by.currentIndex())
        self.sync_sorts.emit(self.sort_by.currentIndex())

    def sync_sort(self, idx):
        if self.sort_by.currentIndex() != idx:
            self.blockSignals(True)
            self.sort_by.setCurrentIndex(idx)
            self.blockSignals(False)

    def item_clicked(self, item):
        if QApplication.mouseButtons() & Qt.MouseButton.RightButton:
            theme = item.data(Qt.ItemDataRole.UserRole) or {}
            url = theme.get('url')
            if url:
                safe_open_url(url)

    @property
    def sort_on(self):
        return {0:'number', 1:'usage', 2:'title'}[self.sort_by.currentIndex()]

    def __iter__(self):
        for i in range(self.theme_list.count()):
            yield self.theme_list.item(i)

    def item_from_name(self, name):
        for item in self:
            if item.data(Qt.ItemDataRole.UserRole)['name'] == name:
                return item

    def set_cover(self, name, pixmap):
        item = self.item_from_name(name)
        if item is not None:
            item.setData(Qt.ItemDataRole.DecorationRole, pixmap)

    def show_themes(self, themes):
        self.themes = [default_theme()] + [t for t in themes if t.get('color_palette', 'any') in (self.for_theme, 'any')]
        self.re_sort()
        self.set_current_theme(self.currently_installed_theme_name)

    def re_sort(self):
        ct = self.current_theme
        self.themes.sort(key=lambda x:sort_key(x.get('title', '')))
        field = self.sort_on
        if field == 'number':
            self.themes.sort(key=lambda x:x.get('number', 0), reverse=True)
        elif field == 'usage':
            self.themes.sort(key=lambda x:x.get('usage', 0), reverse=True)
        self.theme_list.clear()
        for theme in self.themes:
            i = QListWidgetItem(theme.get('title', '') + ' {} {}'.format(theme.get('number'), theme.get('usage', 0)), self.theme_list)
            i.setData(Qt.ItemDataRole.UserRole, theme)
            if 'cover-pixmap' in theme:
                i.setData(Qt.ItemDataRole.DecorationRole, theme['cover-pixmap'])
        if ct:
            self.set_current_theme(ct.get('name', ''))

    @property
    def current_theme(self):
        ci = self.theme_list.currentItem()
        if ci:
            return ci.data(Qt.ItemDataRole.UserRole)
        return default_theme()

    def set_current_theme(self, name):
        if not hasattr(self, "themes"):
            return False
        for i, t in enumerate(self.themes):
            if t.get('name') == name:
                self.theme_list.setCurrentRow(i, QItemSelectionModel.SelectionFlag.SelectCurrent | QItemSelectionModel.SelectionFlag.Clear)
                self.theme_list.scrollToItem(self.theme_list.currentItem())
                return True
        return False


class ChooseTheme(Dialog):

    cover_downloaded = pyqtSignal(object, object)
    themes_downloaded = pyqtSignal()

    def __init__(self, parent=None):
        Dialog.__init__(self, _('Choose an icon theme'), 'choose-icon-theme-dialog', parent)
        self.finished.connect(self.on_finish)
        self.dialog_closed = False
        self.themes_downloaded.connect(self.show_themes, type=Qt.ConnectionType.QueuedConnection)
        self.cover_downloaded.connect(self.set_cover, type=Qt.ConnectionType.QueuedConnection)
        self.keep_downloading = True
        self.commit_changes = None

    def on_finish(self):
        self.dialog_closed = True

    def sizeHint(self):
        h = self.screen().availableSize().height()
        return QSize(900, h - 75)

    def setup_ui(self):
        self.vl = vl = QVBoxLayout(self)
        self.stack = l = QStackedLayout()
        self.pi = pi = ProgressIndicator(self, 256)
        vl.addLayout(l), vl.addWidget(self.bb)
        self.restore_defs_button = b = self.bb.addButton(_('Restore &default icons'), QDialogButtonBox.ButtonRole.ActionRole)
        b.clicked.connect(self.restore_defaults)
        b.setIcon(QIcon.ic('view-refresh.png'))
        self.c = c = QWidget(self)
        self.c.v = v = QVBoxLayout(self.c)
        v.addStretch(), v.addWidget(pi, 0, Qt.AlignmentFlag.AlignCenter)
        self.wait_msg = m = QLabel(self)
        v.addWidget(m, 0, Qt.AlignmentFlag.AlignCenter), v.addStretch()
        f = m.font()
        f.setBold(True), f.setPointSize(28), m.setFont(f)
        self.start_spinner()

        l.addWidget(c)
        self.tabs = QTabWidget(self)
        l.addWidget(self.tabs)
        self.all_colors = ChooseThemeWidget(parent=self)
        self.tabs.addTab(self.all_colors, _('For light and dark'))
        self.light_colors = ChooseThemeWidget(for_theme='light', parent=self)
        self.tabs.addTab(self.light_colors, _('For light only'))
        self.dark_colors = ChooseThemeWidget(for_theme='dark', parent=self)
        self.tabs.addTab(self.dark_colors, _('For dark only'))
        self.tabs.setCurrentIndex(gprefs.get('choose_icon_theme_initial_tab', 0))
        self.tabs.currentChanged.connect(lambda idx: gprefs.set('choose_icon_theme_initial_tab', idx))

        t = Thread(name='GetIconThemes', target=self.get_themes)
        t.daemon = True
        t.start()

    def sync_sorts(self, idx):
        for tab in (self.tabs.widget(i) for i in range(self.tabs.count())):
            tab.sync_sort(idx)

    def start_spinner(self, msg=None):
        self.pi.startAnimation()
        self.stack.setCurrentIndex(0)
        self.wait_msg.setText(msg or _('Downloading, please wait...'))

    def end_spinner(self):
        self.pi.stopAnimation()
        self.stack.setCurrentIndex(1)

    def get_themes(self):

        self.usage = {}

        def get_usage():
            try:
                self.usage = json.loads(bz2.decompress(get_https_resource_securely(BASE_URL + '/usage.json.bz2')))
            except Exception:
                import traceback
                traceback.print_exc()

        t = Thread(name='IconThemeUsage', target=get_usage)
        t.daemon = True
        t.start()

        try:
            self.themes = json.loads(bz2.decompress(get_https_resource_securely(BASE_URL + '/themes.json.bz2')))
        except Exception:
            import traceback
            self.themes = traceback.format_exc()
        t.join()
        if not sip.isdeleted(self):
            self.themes_downloaded.emit()

    def show_themes(self):
        self.end_spinner()
        if not isinstance(self.themes, list):
            error_dialog(self, _('Failed to download list of themes'), _(
                'Failed to download list of themes, click "Show details" for more information'),
                         det_msg=self.themes, show=True)
            self.reject()
            return
        self.setWindowTitle(_('Choose from {} available icon themes').format(len(self.themes)))
        for theme in self.themes:
            theme['usage'] = self.usage.get(theme['name'], 0)
        for tab in (self.tabs.widget(i) for i in range(self.tabs.count())):
            tab.show_themes(self.themes)
        self.tabs.currentWidget().theme_list.setFocus(Qt.FocusReason.OtherFocusReason)
        get_covers(self.themes, self)

    def set_cover(self, theme, cdata):
        theme['cover-pixmap'] = p = QPixmap()
        dpr = self.devicePixelRatioF()
        if isinstance(cdata, bytes):
            p.loadFromData(cdata)
            p.setDevicePixelRatio(dpr)
        for tab in (self.tabs.widget(i) for i in range(self.tabs.count())):
            tab.set_cover(theme['name'], p)

    def restore_defaults(self):
        for tab in (self.tabs.widget(i) for i in range(self.tabs.count())):
            tab.set_current_theme(default_theme()['name'])

    def accept(self):
        themes_to_download = {}
        themes_to_remove = set()
        for tab in (self.tabs.widget(i) for i in range(self.tabs.count())):
            t = tab.current_theme
            if is_default_theme(t):
                themes_to_remove.add(tab.for_theme)
            else:
                themes_to_download[t['name']] = t
                t.setdefault('for_themes', []).append(tab.for_theme)
        self.keep_downloading = True
        self.err_traceback = None

        def download():
            dc = 0
            for theme in themes_to_download.values():
                buf = BytesIO()
                try:
                    url = BASE_URL + theme['icons-url']
                    response = get_https_resource_securely(url, get_response=True)
                    while self.keep_downloading:
                        raw = response.read(1024)
                        if not raw:
                            break
                        buf.write(raw)
                        dc += len(raw)
                        d.downloaded(dc)
                except Exception:
                    import traceback
                    self.err_traceback = traceback.format_exc()
                    d.queue_reject()
                    return
                import lzma
                data = lzma.decompress(buf.getvalue())
                theme['buf'] = BytesIO(data)
            d.queue_accept()

        if themes_to_download:
            size = sum(t['compressed-size'] for t in themes_to_download.values())
            d = DownloadProgress(self, size)
            d.canceled_signal.connect(lambda : setattr(self, 'keep_downloading', False))
            t = Thread(name='DownloadIconTheme', target=download)
            t.daemon = True
            t.start()
            ret = d.exec()
            if self.err_traceback:
                return error_dialog(self, _('Download failed'), _(
                    'Failed to download icon themes, click "Show details" for more information.'), show=True, det_msg=self.err_traceback)
            if ret == QDialog.DialogCode.Rejected or not self.keep_downloading or d.canceled:
                return

        self.commit_changes = CommitChanges(tuple(themes_to_download.values()), themes_to_remove)
        return super().accept()

    @property
    def new_theme_title(self):
        if QApplication.instance().is_dark_theme:
            order = 'dark', 'any', 'light'
        else:
            order = 'light', 'any', 'dark'
        tm = {tab.for_theme: tab for tab in (self.tabs.widget(i) for i in range(self.tabs.count()))}
        for x in order:
            tab = tm[x]
            t = tab.current_theme
            if not is_default_theme(t):
                return t['title']

# }}}


class CommitChanges:

    def __init__(self, downloaded_themes, themes_to_remove):
        self.downloaded_themes = downloaded_themes
        self.themes_to_remove = themes_to_remove

    def __call__(self):
        for x in self.themes_to_remove:
            icon_resource_manager.remove_user_theme(x)
        for theme in self.downloaded_themes:
            for x in theme['for_themes']:
                icon_resource_manager.remove_user_theme(x)
                path = icon_resource_manager.user_theme_resource_file(x)
                t = {k: theme[k] for k in 'name title version'.split()}
                t['color_palette'] = theme.get('color_palette', 'any')
                install_icon_theme(t, theme['buf'], path, x)
        icon_resource_manager.register_user_resource_files()
        icon_resource_manager.set_theme()


def install_icon_theme(theme, f, rcc_path, for_theme):
    from calibre.utils.rcc import compile_icon_dir_as_themes
    with ZipFile(f) as zf, tempfile.TemporaryDirectory() as tdir:
        zf.extractall(tdir)
        with open(os.path.join(tdir, 'metadata.json'), 'w') as f:
            json.dump(theme, f)
        inherits = 'calibre-default' if for_theme == 'any' else f'calibre-default-{for_theme}'
        compile_icon_dir_as_themes(
            tdir, rcc_path, theme_name=f'calibre-user-{for_theme}', inherits=inherits, for_theme=for_theme)


if __name__ == '__main__':
    from calibre.gui2 import Application
    app = Application([])
    create_theme(sys.argv[-1])
    # d = ChooseTheme()
    # if d.exec() == QDialog.DialogCode.Accepted and d.commit_changes is not None:
    #     d.commit_changes()
    del app
