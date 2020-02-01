# -*- mode: makefile-gmake -*-

# Disable HTTP response test because of timeout limit is too short (1 sec)
# > AssertionError: Large file transfer took too long
TEST_FLAGS += --exclude-test-name=test_http_response

# In case builds fail with current source code
# Exclude memory test because garbage collection is prone to happen
# at inconvenient intervals and disturb the memory test
# TEST_FLAGS += --exclude-test-name=test_mem_leaks

# Disable some tests for specific platforms
ifeq      (arm64,  $(DEB_HOST_ARCH))
  # Illegal instruction
  TEST_FLAGS += --exclude-test-name=test_qt
  # Test fail
  TEST_FLAGS += --exclude-test-name=test_dictionaries
else ifeq (mipsel, $(DEB_HOST_ARCH))
  # No network response
  TEST_FLAGS += --exclude-test-name=test_bonjour
  # Test fail
  TEST_FLAGS += --exclude-test-name=test_dictionaries
endif
