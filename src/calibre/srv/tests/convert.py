#!/usr/bin/env python
# License: GPLv3 Copyright: 2026, Kovid Goyal <kovid at kovidgoyal.net>

from calibre.srv.convert import FORBIDDEN_CLIENT_OPTIONS, get_conversion_options, sanitize_conversion_options
from calibre.srv.tests.base import LibraryBaseTest


class ConvertTest(LibraryBaseTest):
    def test_sanitize_conversion_options(self):
        "Client supplied conversion options must be restricted to the advertised, safe set"
        with self.create_server() as server:
            ctx = server.handler.router.ctx
            db = ctx.library_broker.get(None)
            book_id = 1  # has an EPUB format in the test library

            # A genuinely advertised option should survive so we know the
            # allowlist is not simply dropping everything.
            allowed = set(get_conversion_options('epub', 'epub', book_id, db)['options'])
            self.assertTrue(allowed, 'expected the server to advertise at least one conversion option')
            good = min(allowed)

            client_options = {
                good: 'somevalue',
                # dangerous path/URL/guard options a remote client must never set
                'cover': '/etc/passwd',
                'read_metadata_from_opf': '/etc/passwd',
                'debug_pipeline': '/tmp/attacker',
                'allow_local_files_outside_root': True,
                # not advertised by the API at all
                'this_option_does_not_exist': 'x',
            }
            sanitized = sanitize_conversion_options(ctx, db, 'epub', 'epub', book_id, client_options)

            self.assertIn(good, sanitized)
            self.assertEqual(sanitized[good], 'somevalue')
            for name in FORBIDDEN_CLIENT_OPTIONS:
                self.assertNotIn(name, sanitized, f'forbidden option {name!r} was not dropped')
            self.assertNotIn('this_option_does_not_exist', sanitized)
