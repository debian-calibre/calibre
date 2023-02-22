# -*- mode: makefile-gmake -*-

# In case builds fail with current source code
# Exclude memory test because garbage collection is prone to happen
# at inconvenient intervals and disturb the memory test
# TEST_FLAGS += --exclude-test-name=mem_leaks

# Disable some tests for specific platforms
ifeq      (armhf, $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
  TEST_FLAGS += --exclude-test-name=dom_load

  # Standard "/run/user/{UID}" is not available in armhf builder,
  # and "/run/user" is write-protected.
  # Set writable place to build calibre translation resources,
  # because they uses Qt library.
  #
  # > QStandardPaths: error creating runtime directory '/run/user/{UID}' (No such file or directory)
  export XDG_RUNTIME_DIR=$(CURDIR)/debian/runtime-calibre-build

else ifeq (i386,  $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
  TEST_FLAGS += --exclude-test-name=dom_load
endif
