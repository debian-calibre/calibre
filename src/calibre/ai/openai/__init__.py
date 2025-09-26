#!/usr/bin/env python
# License: GPLv3 Copyright: 2025, Kovid Goyal <kovid at kovidgoyal.net>

from calibre.customize import AIProviderPlugin


class OpenAI(AIProviderPlugin):
    name = 'OpenAI'
    version        = (1, 0, 0)
    description    = _('AI services from OpenAI')
    author = 'Kovid Goyal'
    builtin_live_module_name = 'calibre.ai.openai.backend'

    @property
    def capabilities(self):
        from calibre.ai import AICapabilities
        return (
            AICapabilities.text_to_text | AICapabilities.embedding | AICapabilities.text_and_image_to_image |
            AICapabilities.text_to_image | AICapabilities.tts
        )
