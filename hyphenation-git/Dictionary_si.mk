# -*- Mode: makefile-gmake; tab-width: 4; indent-tabs-mode: t -*-
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

$(eval $(call gb_Dictionary_Dictionary,dict-si,dictionaries/si_LK))

$(eval $(call gb_Dictionary_add_root_files,dict-si,\
	dictionaries/si_LK/LICENSES-en.txt \
	dictionaries/si_LK/si_LK.aff \
	dictionaries/si_LK/si_LK.dic \
))

# vim: set noet sw=4 ts=4:
