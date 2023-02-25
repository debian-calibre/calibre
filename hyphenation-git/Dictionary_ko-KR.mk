# -*- Mode: makefile-gmake; tab-width: 4; indent-tabs-mode: t -*-
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

$(eval $(call gb_Dictionary_Dictionary,dict-ko,dictionaries/ko_KR))

$(eval $(call gb_Dictionary_add_root_files,dict-ko,\
	dictionaries/ko_KR/README_ko_KR.txt \
	dictionaries/ko_KR/ko_KR.aff \
	dictionaries/ko_KR/ko_KR.dic \
))

# vim: set noet sw=4 ts=4:
