# -*- mode: makefile-gmake -*-

# D-Bus is not wroks on build server environment
TEST_FLAGS += --exclude-test-name=dbus

# network connection is unreliable on build server environment
TEST_FLAGS += --exclude-test-name=recipe_browser_qt

# Network connection stalled and reaches timeout
TEST_FLAGS += --exclude-test-name=recipe_browser_webengine

# Disable some tests for specific platforms
ifeq      (armhf, $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
else ifeq (i386,  $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
endif
