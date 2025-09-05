# -*- mode: makefile-gmake -*-

# D-Bus is not wroks on build server environment
TEST_FLAGS += --exclude-test-name=dbus

# network connection is unreliable on build server environment
TEST_FLAGS += --exclude-test-name=recipe_browser_qt

# Network connection stalled and reaches timeout
TEST_FLAGS += --exclude-test-name=recipe_browser_webengine

# Disable some tests for specific platforms
ifeq (arm64, $(DEB_HOST_ARCH))
  # "Illegal instruction" error on buildd "arm-ubc-*".
  # But buildd "arm-conova-*" works well.
  TEST_FLAGS += --exclude-test=import_of_all_python_modules
endif
