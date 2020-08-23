# -*- mode: makefile-gmake -*-
#
# Trampoline script to avoid target name conflict between Debian packager and
# Calibre builder
#
# Calibre build script writes XDG folders when test/install.
# Use automatic HOME/XDG_* values from dh_auto_*(1) programs.
#

%:
	$(MAKE) MAKEFLAGS= -f debian/rules calibre_auto_$@
