# -*- mode: makefile-gmake -*-

# avoid Python runtime error
TEST_FLAGS += --exclude-test-name=workers

# D-Bus is not wroks on build server environment
TEST_FLAGS += --exclude-test-name=dbus

# network connection is unreliable on build server environment
TEST_FLAGS += --exclude-test-name=recipe_browser_qt

# Disable some tests for specific platforms
ifeq      (armhf, $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
  TEST_FLAGS += --exclude-test-name=dom_load
else ifeq (i386,  $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
  TEST_FLAGS += --exclude-test-name=dom_load
endif
