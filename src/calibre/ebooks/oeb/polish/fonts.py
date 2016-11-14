#!/usr/bin/env python2
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2014, Kovid Goyal <kovid at kovidgoyal.net>'

import re

from calibre.ebooks.oeb.polish.container import OEB_STYLES, OEB_DOCS
from calibre.ebooks.oeb.normalize_css import normalize_font

def unquote(x):
    if x and len(x) > 1 and x[0] == x[-1] and x[0] in ('"', "'"):
        x = x[1:-1]
    return x

def font_family_data_from_declaration(style, families):
    font_families = []
    f = style.getProperty('font')
    if f is not None:
        f = normalize_font(f.propertyValue, font_family_as_list=True).get('font-family', None)
        if f is not None:
            font_families = [unquote(x) for x in f]
    f = style.getProperty('font-family')
    if f is not None:
        font_families = [x.value for x in f.propertyValue]

    for f in font_families:
        families[f] = families.get(f, False)

def font_family_data_from_sheet(sheet, families):
    for rule in sheet.cssRules:
        if rule.type == rule.STYLE_RULE:
            font_family_data_from_declaration(rule.style, families)
        elif rule.type == rule.FONT_FACE_RULE:
            ff = rule.style.getProperty('font-family')
            if ff is not None:
                for f in ff.propertyValue:
                    families[f.value] = True

def font_family_data(container):
    families = {}
    for name, mt in container.mime_map.iteritems():
        if mt in OEB_STYLES:
            sheet = container.parsed(name)
            font_family_data_from_sheet(sheet, families)
        elif mt in OEB_DOCS:
            root = container.parsed(name)
            for style in root.xpath('//*[local-name() = "style"]'):
                if style.text and style.get('type', 'text/css').lower() == 'text/css':
                    sheet = container.parse_css(style.text)
                    font_family_data_from_sheet(sheet, families)
            for style in root.xpath('//*/@style'):
                if style:
                    style = container.parse_css(style, is_declaration=True)
                    font_family_data_from_declaration(style, families)
    return families

def change_font_family_value(cssvalue, new_name):
    # If cssvalue.type == 'IDENT' cssutils will not serialize the font
    # name properly (it will not enclose it in quotes). So we
    # use the following hack (setting an internal property of the
    # Value class)
    cssvalue.value = new_name
    cssvalue._type = 'STRING'

def change_font_family_in_property(style, prop, old_name, new_name=None):
    changed = False
    families = {x.value for x in prop.propertyValue}
    _dummy_family = 'd7d81cf1-1c8c-4993-b788-e1ab596c0f1f'
    if new_name and new_name in families:
        new_name = None  # new name already exists in this property, so simply remove old_name
    for val in prop.propertyValue:
        if val.value == old_name:
            change_font_family_value(val, new_name or _dummy_family)
            changed = True
    if changed and not new_name:
        # Remove dummy family, cssutils provides no clean way to do this, so we
        # roundtrip via cssText
        pat = re.compile(r'''['"]{0,1}%s['"]{0,1}\s*,{0,1}''' % _dummy_family)
        repl = pat.sub('', prop.propertyValue.cssText).strip().rstrip(',').strip()
        if repl:
            prop.propertyValue.cssText = repl
            if prop.name == 'font' and not prop.validate():
                style.removeProperty(prop.name)  # no families left in font:
        else:
            style.removeProperty(prop.name)
    return changed

def change_font_in_declaration(style, old_name, new_name=None):
    changed = False
    for x in ('font', 'font-family'):
        prop = style.getProperty(x)
        if prop is not None:
            changed |= change_font_family_in_property(style, prop, old_name, new_name)
    return changed

def remove_embedded_font(container, sheet, rule, sheet_name):
    src = getattr(rule.style.getProperty('src'), 'value')
    if src is not None:
        if src.startswith('url('):
            src = src[4:-1]
    sheet.cssRules.remove(rule)
    if src:
        src = unquote(src)
        name = container.href_to_name(src, sheet_name)
        if container.has_name(name):
            container.remove_item(name)

def change_font_in_sheet(container, sheet, old_name, new_name, sheet_name):
    changed = False
    removals = []
    for rule in sheet.cssRules:
        if rule.type == rule.STYLE_RULE:
            changed |= change_font_in_declaration(rule.style, old_name, new_name)
        elif rule.type == rule.FONT_FACE_RULE:
            ff = rule.style.getProperty('font-family')
            if ff is not None:
                families = {x.value for x in ff.propertyValue}
                if old_name in families:
                    changed = True
                    removals.append(rule)
    for rule in reversed(removals):
        remove_embedded_font(container, sheet, rule, sheet_name)
    return changed

def change_font(container, old_name, new_name=None):
    '''
    Change a font family from old_name to new_name. Changes all occurrences of
    the font family in stylesheets, style tags and style attributes.
    If the old_name refers to an embedded font, it is removed. You can set
    new_name to None to remove the font family instead of changing it.
    '''
    changed = False
    for name, mt in tuple(container.mime_map.iteritems()):
        if mt in OEB_STYLES:
            sheet = container.parsed(name)
            if change_font_in_sheet(container, sheet, old_name, new_name, name):
                container.dirty(name)
                changed = True
        elif mt in OEB_DOCS:
            root = container.parsed(name)
            for style in root.xpath('//*[local-name() = "style"]'):
                if style.text and style.get('type', 'text/css').lower() == 'text/css':
                    sheet = container.parse_css(style.text)
                    if change_font_in_sheet(container, sheet, old_name, new_name, name):
                        container.dirty(name)
                        changed = True
            for elem in root.xpath('//*[@style]'):
                style = elem.get('style', '')
                if style:
                    style = container.parse_css(style, is_declaration=True)
                    if change_font_in_declaration(style, old_name, new_name):
                        style = style.cssText.strip().rstrip(';').strip()
                        if style:
                            elem.set('style', style)
                        else:
                            del elem.attrib['style']
                        container.dirty(name)
                        changed = True
    return changed
