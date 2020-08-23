# -*- mode: makefile-gmake -*-

%:
	$(MAKE) MAKEFLAGS= -f debian/rules calibre_auto_$@
