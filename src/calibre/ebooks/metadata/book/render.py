#!/usr/bin/env python


__license__ = 'GPL v3'
__copyright__ = '2014, Kovid Goyal <kovid at kovidgoyal.net>'

import os
from contextlib import suppress
from functools import partial

from calibre import force_unicode, prepare_string_for_xml
from calibre.constants import filesystem_encoding
from calibre.db.constants import DATA_DIR_NAME, NO_SEARCH_LINK
from calibre.ebooks.metadata import fmt_sidx, rating_to_stars
from calibre.ebooks.metadata.book.formatter import SafeFormat
from calibre.ebooks.metadata.search_internet import DEFAULT_AUTHOR_SOURCE, name_for, qquote, url_for_author_search, url_for_book_search
from calibre.ebooks.metadata.sources.identify import urls_from_identifiers
from calibre.library.comments import comments_to_html, markdown
from calibre.utils.date import format_date, is_date_undefined
from calibre.utils.formatter import EvalFormatter
from calibre.utils.icu import sort_key
from calibre.utils.localization import calibre_langcode_to_name, ngettext
from calibre.utils.serialize import json_dumps
from polyglot.binary import as_hex_unicode

default_sort = ('title', 'title_sort', 'authors', 'author_sort', 'series', 'rating', 'pubdate', 'tags', 'publisher', 'identifiers')


def field_sort(mi, name):
    try:
        title = mi.metadata_for_field(name)['name']
    except:
        title = 'zzz'
    return {x:(i, None) for i, x in enumerate(default_sort)}.get(name, (10000, sort_key(title)))


def displayable_field_keys(mi):
    for k in mi.all_field_keys():
        try:
            m = mi.metadata_for_field(k)
        except:
            continue
        if (
                m is not None and m.get('kind') == 'field' and m.get('datatype') is not None and
                k not in ('au_map', 'marked', 'ondevice', 'cover', 'series_sort', 'in_tag_browser') and
                not k.endswith('_index')
        ):
            yield k


def get_field_list(mi):
    for field in sorted(displayable_field_keys(mi), key=partial(field_sort, mi)):
        yield field, True


def action(main, **keys):
    keys['type'] = main
    return 'action:' + as_hex_unicode(json_dumps(keys))


def search_action(search_term, value, **k):
    return action('search', term=search_term, value=value, **k)


def search_action_with_data(search_term, value, book_id, field=None, **k):
    field = field or search_term
    return search_action(search_term, value, field=field, book_id=book_id, **k)


def web_search_link(template, mi, value):
    formatter = SafeFormat()
    iv = str(value)
    mi.set('item_value', iv)
    mi.set('item_value_quoted', qquote(iv, True))
    mi.set('item_value_no_plus', qquote(iv, False))
    u = formatter.safe_format(template, mi, 'BOOK DETAILS WEB LINK', mi)
    if u:
        return u, prepare_string_for_xml(_('Click to browse to: {}').format(u), attribute=True)
    return '', ''


def cc_search_action_with_data(search_term, value, book_id, fm, mi, field=None,  **k):
    if mi is not None and fm is not None:
        if template := fm.get('display', {}).get('web_search_template'):
            try:
                u, v = web_search_link(template, mi, value)
                return action('cc_url', url=u), v
            except Exception:
                import traceback
                traceback.print_exc()
    t = _('Click to see books with {0}: {1}').format(mi.get('name', search_term), prepare_string_for_xml(value))
    return search_action_with_data(search_term, value, book_id, **k), t


def notes_action(**keys):
    return 'notes:' + as_hex_unicode(json_dumps(keys))


DEFAULT_AUTHOR_LINK = f'search-{DEFAULT_AUTHOR_SOURCE}'


def resolve_default_author_link(ans: str | None = None) -> str:
    if ans == 'https://en.wikipedia.org/w/index.php?search={author}':
        # The old default value for this setting
        ans = ''
    return ans or DEFAULT_AUTHOR_LINK


def author_search_href(which, title=None, author=None):
    if which == 'calibre':
        return 'calibre', _('Search the calibre library for books by %s') % author
    search_type, key = 'author', which
    if which.endswith('-book'):
        key, search_type = which.rpartition('-')[::2]
    name = name_for(key)
    if name is None:
        search_type = 'author'
        return author_search_href(DEFAULT_AUTHOR_LINK.partition('-')[2], title=title, author=author)
    if search_type == 'author':
        tt = _('Search {0} for the author: {1}').format(name, author)
    else:
        tt = _('Search {0} for the book: {1} by the author {2}').format(name, title, author)
    func = url_for_book_search if search_type == 'book' else url_for_author_search
    return func(key, title=title, author=author), tt


def render_author_link(default_author_link, author, book_title=None, author_sort=None):
    book_title = book_title or ''
    if default_author_link == NO_SEARCH_LINK:
        return '',''
    elif default_author_link.startswith('search-'):
        which_src = default_author_link.partition('-')[2]
        link, lt = author_search_href(which_src, title=book_title, author=author)
    else:
        formatter = EvalFormatter()
        vals = {'author': qquote(author), 'title': qquote(book_title), 'author_sort': qquote(author_sort or author)}
        link = lt = formatter.safe_format(default_author_link, vals, '', vals)
    return link, lt


def mi_to_html(
        mi,
        field_list=None, default_author_link=None, use_roman_numbers=True,
        rating_font='Liberation Serif', rtl=False, comments_heading_pos='hide',
        for_qt=False, vertical_fields=(), show_links=True, item_id_if_has_note=None,
        link_note_icon_size=16
    ):

    link_markup = '↗️'
    if for_qt:
        s = link_note_icon_size
        link_markup = f'<img valign="bottom" src="calibre-icon:///external-link.png" width={s} height={s}>'
        note_markup = f'<img valign="bottom" src="calibre-icon:///notes.png" width={s} height={s}>'
    def get_link_map(column):
        try:
            return mi.link_maps[column]
        except Exception:
            return {}

    def add_other_links(field, field_value):
        if show_links:
            link = get_link_map(field).get(field_value)
            if link:
                link = prepare_string_for_xml(link, True)
                link = ' <a title="{0}: {1}" href="{1}">{2}</a>'.format(_('Click to open'), link, link_markup)
            else:
                link = ''
            note = ''
            item_id = None if item_id_if_has_note is None else item_id_if_has_note(field, field_value)
            if item_id is not None:
                note = ' <a title="{}" href="{}">{}</a>'.format(
                    _('Show notes for: {}').format(field_value), notes_action(field=field, value=field_value, item_id=item_id), note_markup)
            return link + note
        return ''

    if field_list is None:
        field_list = get_field_list(mi)
    ans = []
    comment_fields = []
    isdevice = not hasattr(mi, 'id')
    row = '<td class="title">%s</td><td class="value">%s</td>'
    p = prepare_string_for_xml
    a = partial(prepare_string_for_xml, attribute=True)
    book_id = getattr(mi, 'id', 0)
    title_sep = '\xa0'

    for field in (field for field, display in field_list if display):
        try:
            metadata = mi.metadata_for_field(field)
        except:
            continue
        if not metadata:
            continue

        def value_list(sep, vals):
            if field in vertical_fields:
                return '<br/>'.join(vals)
            return sep.join(vals)

        if field == 'sort':
            field = 'title_sort'
        if metadata['is_custom'] and metadata['datatype'] in {'bool', 'int', 'float'}:
            isnull = mi.get(field) is None
        else:
            isnull = mi.is_null(field)
        if isnull:
            continue
        name = metadata['name']
        if not name:
            name = field
        name += title_sep
        disp = metadata['display']
        if (metadata['datatype'] == 'comments' or field == 'comments'
            or disp.get('composite_show_in_comments', '')):
            val = getattr(mi, field)
            if val:
                ctype = disp.get('interpret_as') or 'html'
                val = force_unicode(val)
                if ctype == 'long-text':
                    val = f'<pre style="white-space:pre-wrap">{p(val)}</pre>'
                elif ctype == 'short-text':
                    val = f'<span>{p(val)}</span>'
                elif ctype == 'markdown':
                    val = markdown(val)
                else:
                    val = comments_to_html(val)
                heading_position = disp.get('heading_position', comments_heading_pos)
                if heading_position == 'side':
                    ans.append((field, row % (name, val)))
                else:
                    if heading_position == 'above':
                        val = f'<h3 class="comments-heading">{p(name)}</h3>{val}'
                    comment_fields.append('<div id="{}" class="comments">{}</div>'.format(field.replace('#', '_'), val))
        elif metadata['datatype'] == 'rating':
            val = getattr(mi, field)
            if val:
                star_string = rating_to_stars(val, disp.get('allow_half_stars', False))
                ans.append((field,
                    f'<td class="title">{name}</td><td class="rating value" '
                    f'style=\'font-family:"{rating_font}"\'>{star_string}</td>'))
        elif metadata['datatype'] == 'composite' and not disp.get('composite_show_in_comments', ''):
            val = getattr(mi, field)
            if val:
                val = force_unicode(val)
                if disp.get('contains_html', False):
                    ans.append((field, row % (name, comments_to_html(val))))
                else:
                    if not metadata['is_multiple']:
                        u, v = cc_search_action_with_data(field, val, book_id, metadata, mi, field)
                        val = f'<a href="{u}" title="{v}">{p(val)}</a>'
                    else:
                        all_vals = [v.strip()
                            for v in val.split(metadata['is_multiple']['cache_to_list']) if v.strip()]
                        if show_links:
                            links = []
                            for x in all_vals:
                                u, v = cc_search_action_with_data(field, x, book_id, metadata, mi, field)
                                links.append(f'<a href="{u}" title="{v}">{p(x)}</a>')
                        else:
                            links = all_vals
                        val = value_list(metadata['is_multiple']['list_to_ui'], links)
                    ans.append((field, row % (name, val)))
        elif field == 'path':
            if mi.path:
                path = force_unicode(mi.path, filesystem_encoding)
                scheme = 'devpath' if isdevice else 'path'
                loc = path if isdevice else book_id
                extra = ''
                if isdevice:
                    durl = path
                    if durl.startswith('mtp:::'):
                        durl = ':::'.join((durl.split(':::'))[2:])
                    extra = f'<br><span style="font-size:smaller">{prepare_string_for_xml(durl)}</span>'
                if show_links:
                    num_of_folders = 1
                    if isdevice:
                        text = _('Click to open')
                    else:
                        data_path = os.path.join(path, DATA_DIR_NAME)
                        with suppress(OSError):
                            for dirpath, dirnames, filenames in os.walk(data_path):
                                if filenames:
                                    num_of_folders = 2
                                    break
                        text = _('Book files')
                        name = ngettext('Folder', 'Folders', num_of_folders) + title_sep
                    links = [f'<a href="{action(scheme, book_id=book_id, loc=loc)}" title="{prepare_string_for_xml(path, True)}">{text}</a>{extra}']
                    if num_of_folders > 1:
                        links.append('<a href="{}" title="{}">{}</a>'.format(
                            action('data-path', book_id=book_id, loc=book_id),
                            prepare_string_for_xml(data_path, True), _('Data files')))
                    link = value_list(', ', links)

                else:
                    link = prepare_string_for_xml(path, True)
                ans.append((field, row % (name, link)))
        elif field == 'formats':
            # Don't need show_links here because formats are removed from mi on
            # cross library displays.
            if isdevice:
                continue
            path = mi.path or ''
            bpath = ''
            if path:
                h, t = os.path.split(path)
                bpath = os.sep.join((os.path.basename(h), t))
            data = ({
                'fmt':x, 'path':a(path or ''), 'fname':a(mi.format_files.get(x, '')),
                'ext':x.lower(), 'id':book_id, 'bpath':bpath, 'sep':os.sep,
                'action':action('format', book_id=book_id, fmt=x, path=path or '', fname=mi.format_files.get(x, ''))
            } for x in mi.formats)
            fmts = ['<a title="{bpath}{sep}{fname}.{ext}" href="{action}">{fmt}</a>'.format(**x)
                    for x in data]
            ans.append((field, row % (name, value_list(', ', fmts))))
        elif field == 'identifiers':
            urls = urls_from_identifiers(mi.identifiers, sort_results=True)
            if show_links:
                links = [
                    '<a href="{}" title="{}:{}">{}</a>'.format(
                        action('identifier', book_id=book_id, url=url, name=namel, id_type=id_typ, value=id_val, field='identifiers'),
                        a(id_typ), a(id_val), p(namel))
                    for namel, id_typ, id_val, url in urls]
                links = value_list(', ', links)
            else:
                links = ', '.join(mi.identifiers)
            if links:
                ans.append((field, row % (_('Ids')+title_sep, links)))
        elif field == 'authors':
            authors = []
            for aut in mi.authors:
                link = ''
                if show_links:
                    if default_author_link:
                        link, lt = render_author_link(default_author_link, aut, mi.title, mi.author_sort_map.get(aut) or aut)
                    else:
                        aut = p(aut)
                if link:
                    val = '<a title="{}" href="{}">{}</a>'.format(a(lt), action('author', book_id=book_id,
                                                              url=link, name=aut, title=lt), aut)
                else:
                    val = aut
                val += add_other_links('authors', aut)
                authors.append(val)
            ans.append((field, row % (name, value_list(' & ', authors))))
        elif field == 'languages':
            if not mi.languages:
                continue
            names = filter(None, map(calibre_langcode_to_name, mi.languages))
            if show_links:
                names = ['<a href="{}" title="{}">{}</a>'.format(search_action_with_data('languages', n, book_id), _(
                    'Search calibre for books with the language: {}').format(n), n) for n in names]
            ans.append((field, row % (name, value_list(', ', names))))
        elif field == 'publisher':
            if not mi.publisher:
                continue
            if show_links:
                val = '<a href="{}" title="{}">{}</a>'.format(
                    search_action_with_data('publisher', mi.publisher, book_id),
                    _('Click to see books with {0}: {1}').format(metadata['name'], a(mi.publisher)),
                    p(mi.publisher))
                val += add_other_links('publisher', mi.publisher)
            else:
                val = p(mi.publisher)
            ans.append((field, row % (name, val)))
        elif field == 'title':
            # otherwise title gets metadata['datatype'] == 'text'
            # treatment below with a click to search link (which isn't
            # too bad), and a right-click 'Delete' option to delete
            # the title (which is bad).
            val = mi.format_field(field)[-1]
            ans.append((field, row % (name, val)))
        else:
            val = unescaped_val = mi.format_field(field)[-1]
            if val is None:
                continue
            val = p(val)
            if show_links:
                if metadata['datatype'] == 'series':
                    sidx = mi.get(field+'_index')
                    if sidx is None:
                        sidx = 1.0
                    try:
                        st = metadata['search_terms'][0]
                    except Exception:
                        st = field
                    series = getattr(mi, field)
                    if metadata.get('display', {}).get('web_search_template'):
                        u, v = cc_search_action_with_data(st, series, book_id, metadata, mi, field)
                        val = _('%(sidx)s of <a href="%(href)s" title="%(tt)s">'
                                '<span class="%(cls)s">%(series)s</span></a>') % dict(
                                    sidx=fmt_sidx(sidx, use_roman=use_roman_numbers), cls='series_name',
                                    series=p(series), href=u, tt=v)
                    else:
                        val = _(
                            '%(sidx)s of <a href="%(href)s" title="%(tt)s">'
                            '<span class="%(cls)s">%(series)s</span></a>') % dict(
                                sidx=fmt_sidx(sidx, use_roman=use_roman_numbers), cls='series_name',
                                series=p(series), href=search_action_with_data(st, series, book_id, field),
                                tt=p(_('Click to see books in this series')))
                    val += add_other_links(field, series)
                elif metadata['datatype'] == 'datetime':
                    aval = getattr(mi, field)
                    if is_date_undefined(aval):
                        continue
                    aval = format_date(aval, 'yyyy-MM-dd')
                    key = field if field != 'timestamp' else 'date'
                    if val == aval:
                        val = '<a href="{}" title="{}">{}</a>'.format(
                            search_action_with_data(key, str(aval), book_id, None, original_value=val), a(
                                _('Click to see books with {0}: {1}').format(metadata['name'] or field, val)), val)
                    else:
                        val = '<a href="{}" title="{}">{}</a>'.format(
                            search_action_with_data(key, str(aval), book_id, None, original_value=val), a(
                                _('Click to see books with {0}: {1} (derived from {2})').format(
                                    metadata['name'] or field, aval, val)), val)
                elif metadata['datatype'] == 'text':
                    try:
                        st = metadata['search_terms'][0]
                    except Exception:
                        st = field
                    if metadata['is_multiple']:
                        all_vals = mi.get(field)
                        if not metadata.get('display', {}).get('is_names', False):
                            all_vals = sorted(all_vals, key=sort_key)
                        links = []
                        for x in all_vals:
                            if metadata['is_custom']:
                                u, v = cc_search_action_with_data(st, x, book_id, metadata, mi, field)
                                v = f'<a href="{u}" title="{v}">{p(x)}</a>'
                            else:
                                v = '<a href="{}" title="{}">{}</a>'.format(
                                    search_action_with_data(st, x, book_id, field),
                                    _('Click to see books with {0}: {1}').format(
                                    metadata['name'] or field, a(x)), p(x))
                            v += add_other_links(field, x)
                            links.append(v)
                        val = value_list(metadata['is_multiple']['list_to_ui'], links)
                    else:
                        if metadata['is_custom']:
                            u, v = cc_search_action_with_data(st, unescaped_val, book_id, metadata, mi, field)
                            v = f'<a href="{u}" title="{v}">{p(unescaped_val)}</a>'
                        else:
                            v = '<a href="{}" title="{}">{}</a>'.format(
                                search_action_with_data(st, unescaped_val, book_id, field),
                                _('Click to see books with {0}: {1}').format(
                                metadata['name'] or field, a(unescaped_val)), p(unescaped_val))
                        val = v + add_other_links(field, val)
                elif metadata['datatype'] == 'enumeration':
                    try:
                        st = metadata['search_terms'][0]
                    except Exception:
                        st = field
                    u, v = cc_search_action_with_data(st, unescaped_val, book_id, metadata, mi, field)
                    val = f'<a href="{u}" title="{v}">{p(unescaped_val)}</a>' + add_other_links(field, val)
                elif metadata['datatype'] == 'bool':
                    val = '<a href="{}" title="{}">{}</a>'.format(
                        search_action_with_data(field, val, book_id, None), a(
                            _('Click to see books with {0}: {1}').format(metadata['name'] or field, val)), val)
                else:
                    try:
                        aval = str(getattr(mi, field))
                        if not aval:
                            continue
                        if val == aval:
                            val = '<a href="{}" title="{}">{}</a>'.format(
                                search_action_with_data(field, str(aval), book_id, None, original_value=val), a(
                                    _('Click to see books with {0}: {1}').format(metadata['name'] or field, val)), val)
                        else:
                            val = '<a href="{}" title="{}">{}</a>'.format(
                                search_action_with_data(field, str(aval), book_id, None, original_value=val), a(
                                    _('Click to see books with {0}: {1} (derived from {2})').format(
                                        metadata['name'] or field, aval, val)), val)
                    except Exception:
                        import traceback
                        traceback.print_exc()

            ans.append((field, row % (name, val)))

    dc = getattr(mi, 'device_collections', [])
    if dc:
        dc = ', '.join(sorted(dc, key=sort_key))
        ans.append(('device_collections',
            row % (_('Collections')+':', dc)))

    def classname(field):
        try:
            dt = mi.metadata_for_field(field)['datatype']
        except:
            dt = 'text'
        return f'datatype_{dt}'

    ans = ['<tr id="{}" class="{}">{}</tr>'.format(fieldl.replace('#', '_'),
        classname(fieldl), html) for fieldl, html in ans]
    # print('\n'.join(ans))
    direction = 'rtl' if rtl else 'ltr'
    rans = f'<table class="fields" style="direction: {direction}; '
    if not for_qt:
        # This causes wasted space at the edge of the table in Qt's rich text
        # engine, see https://bugs.launchpad.net/calibre/+bug/1881488
        margin = 'left' if rtl else 'right'
        rans += f'margin-{margin}: auto; '
    return '{}">{}</table>'.format(rans, '\n'.join(ans)), comment_fields
