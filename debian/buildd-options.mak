# -*- mode: makefile-gmake -*-

# D-Bus is not wroks on build server environment
TEST_FLAGS += --exclude-test-name=dbus

# network connection is unreliable on build server environment
TEST_FLAGS += --exclude-test-name=recipe_browser_qt

# Network connection stalled and reaches timeout
TEST_FLAGS += --exclude-test-name=recipe_browser_webengine

# Builder dose not have OpenGL/OpenGLES device
# This breaks Qt test
TEST_FLAGS += --exclude-test-name=qt

# Disable some tests for specific platforms
ifeq      (amd64, $(DEB_HOST_ARCH))
  # Network test is unstable in reproducible-builder environment
  TEST_FLAGS += --exclude-test-name=websocket_basic
else ifeq (arm64, $(DEB_HOST_ARCH))
  # "Illegal instruction" error on buildd "arm-ubc-*".
  # But buildd "arm-conova-*" works well.
  TEST_FLAGS += --exclude-test-name=import_of_all_python_modules
  TEST_FLAGS += --exclude-test-name=piper
  TEST_FLAGS += --exclude-test-name=plugins
endif
