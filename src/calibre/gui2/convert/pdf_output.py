# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2009, John Schember <john@nachtimwald.com>'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QHBoxLayout, QFormLayout, QDoubleSpinBox, QCheckBox, QVBoxLayout

from calibre.gui2.convert.pdf_output_ui import Ui_Form
from calibre.gui2.convert import Widget
from calibre.utils.localization import localize_user_manual_link

paper_size_model = None
orientation_model = None


class PluginWidget(Widget, Ui_Form):

    TITLE = _('PDF output')
    HELP = _('Options specific to')+' PDF '+_('output')
    COMMIT_NAME = 'pdf_output'
    ICON = I('mimetypes/pdf.png')

    def __init__(self, parent, get_option, get_help, db=None, book_id=None):
        Widget.__init__(self, parent, [
            'use_profile_size', 'paper_size', 'custom_size', 'pdf_hyphenate',
            'preserve_cover_aspect_ratio', 'pdf_serif_family', 'unit',
            'pdf_sans_family', 'pdf_mono_family', 'pdf_standard_font',
            'pdf_default_font_size', 'pdf_mono_font_size', 'pdf_page_numbers',
            'pdf_footer_template', 'pdf_header_template', 'pdf_add_toc', 'toc_title',
            'pdf_page_margin_left', 'pdf_page_margin_top', 'pdf_page_margin_right', 'pdf_page_margin_bottom',
            'pdf_use_document_margins',
        ])
        self.db, self.book_id = db, book_id
        try:
            self.hf_label.setText(self.hf_label.text() % localize_user_manual_link(
                'https://manual.calibre-ebook.com/conversion.html#converting-to-pdf'))
        except TypeError:
            pass  # link already localized

        for x in get_option('paper_size').option.choices:
            self.opt_paper_size.addItem(x)
        for x in get_option('unit').option.choices:
            self.opt_unit.addItem(x)
        for x in get_option('pdf_standard_font').option.choices:
            self.opt_pdf_standard_font.addItem(x)

        self.initialize_options(get_option, get_help, db, book_id)
        self.layout().setFieldGrowthPolicy(self.layout().ExpandingFieldsGrow)
        self.template_box.layout().setFieldGrowthPolicy(self.layout().AllNonFixedFieldsGrow)
        self.toggle_margins()

    def toggle_margins(self):
        enabled = not self.opt_pdf_use_document_margins.isChecked()
        for which in 'left top right bottom'.split():
            getattr(self, 'opt_pdf_page_margin_' + which).setEnabled(enabled)

    def setupUi(self, *a):
        Ui_Form.setupUi(self, *a)
        v = self.page_margins_box.v = QVBoxLayout(self.page_margins_box)
        self.opt_pdf_use_document_margins = c = QCheckBox(_('Use page margins from the &document being converted'))
        v.addWidget(c)
        c.stateChanged.connect(self.toggle_margins)
        h = self.page_margins_box.h = QHBoxLayout()
        l = self.page_margins_box.l = QFormLayout()
        r = self.page_margins_box.r = QFormLayout()
        h.addLayout(l), h.addLayout(r)
        v.addLayout(h)

        def margin(which):
            w = QDoubleSpinBox(self)
            w.setRange(-100, 500), w.setSuffix(' pt'), w.setDecimals(1)
            setattr(self, 'opt_pdf_page_margin_' + which, w)
            return w

        l.addRow(_('&Left:'), margin('left'))
        l.addRow(_('&Right:'), margin('right'))
        r.addRow(_('&Top:'), margin('top'))
        r.addRow(_('&Bottom:'), margin('bottom'))
