__license__ = 'GPL 3'
__copyright__ = '2009, John Schember <john@nachtimwald.com>'
__docformat__ = 'restructuredtext en'

import os

from calibre.customize.conversion import InputFormatPlugin, OptionRecommendation
from polyglot.builtins import as_bytes

ENGINES = 'calibre', 'pdftohtml'


class PDFInput(InputFormatPlugin):

    name        = 'PDF Input'
    author      = 'Kovid Goyal and John Schember and Alan Pettigrew'
    description = _('Convert PDF files to HTML')
    file_types  = {'pdf'}
    commit_name = 'pdf_input'

    options = {
        OptionRecommendation(name='no_images', recommended_value=False,
            help=_('Do not extract images from the document')),
        OptionRecommendation(name='unwrap_factor', recommended_value=0.45,
            help=_('Scale used to determine the length at which a line should '
            'be unwrapped. Valid values are a decimal between 0 and 1. The '
            'default is 0.45, just below the median line length.')),
        OptionRecommendation(name='pdf_engine', recommended_value='calibre', choices=('calibre', 'pdftohtml'),
            help=_('The PDF engine to use, the "calibre" engine is recommended as it has automatic header and footer removal.'
                   ' Choices: {}'
            ).format(', '.join(ENGINES))),
        OptionRecommendation(name='pdf_header_skip', recommended_value=-1,
            help=_('Skip everything to the specified number of pixels at the top of a page.'
            ' Negative numbers mean auto-detect and remove headers, zero means do not remove headers and positive numbers'
            ' mean remove headers that appear above that many pixels from the top of the page. Works only'
            ' with the new PDF engine.'
        )),
        OptionRecommendation(name='pdf_footer_skip', recommended_value=-1,
            help=_('Skip everything to the specified number of pixels at the bottom of a page.'
            ' Negative numbers mean auto-detect and remove footers, zero means do not remove footers and positive numbers'
            ' mean remove footers that appear below that many pixels from the bottom of the page. Works only'
            ' with the calibre PDF engine.'
        )),
        OptionRecommendation(name='pdf_header_regex', recommended_value='',
            help=_('Regular expression to remove lines at the top of a page. '
                   'This only looks at the first line of a page and works only with the calibre PDF engine.')),
        OptionRecommendation(name='pdf_footer_regex', recommended_value='',
            help=_('Regular expression to remove lines at the bottom of a page. '
                   'This only looks at the last line of a page and works only with the calibre PDF engine.')),
    }

    def convert(self, stream, options, file_ext, log,
                accelerators):
        from calibre.ebooks.metadata.opf2 import OPFCreator
        from calibre.ebooks.pdf.pdftohtml import pdftohtml

        log.debug('Converting file to html...')
        # The main html file will be named index.html
        self.opts, self.log = options, log
        if options.pdf_engine == 'calibre':
            from calibre.ebooks.pdf.reflow import PDFDocument
            from calibre.utils.cleantext import clean_ascii_chars
            pdftohtml(os.getcwd(), stream.name, self.opts.no_images, as_xml=True)
            with open('index.xml', 'rb') as f:
                xml = clean_ascii_chars(f.read())
            PDFDocument(xml, self.opts, self.log)
        else:
            pdftohtml(os.getcwd(), stream.name, options.no_images)

        from calibre.ebooks.metadata.meta import get_metadata
        log.debug('Retrieving document metadata...')
        mi = get_metadata(stream, 'pdf')
        opf = OPFCreator(os.getcwd(), mi)

        manifest = [('index.html', None)]

        images = os.listdir(os.getcwd())
        images.remove('index.html')
        for i in images:
            manifest.append((i, None))
        log.debug('Generating manifest...')
        opf.create_manifest(manifest)

        opf.create_spine(['index.html'])
        log.debug('Rendering manifest...')
        with open('metadata.opf', 'wb') as opffile:
            opf.render(opffile)
        if os.path.exists('toc.ncx'):
            ncxid = opf.manifest.id_for_path('toc.ncx')
            if ncxid:
                with open('metadata.opf', 'r+b') as f:
                    raw = f.read().replace(b'<spine', b'<spine toc="%s"' % as_bytes(ncxid))
                    f.seek(0)
                    f.write(raw)

        return os.path.join(os.getcwd(), 'metadata.opf')
