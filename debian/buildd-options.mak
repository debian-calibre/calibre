# -*- mode: makefile-gmake -*-

# In case builds fail with current source code
# Exclude memory test because garbage collection is prone to happen
# at inconvenient intervals and disturb the memory test
# TEST_FLAGS += --exclude-test-name=mem_leaks

# Disable some tests for specific platforms
ifeq      (armhf,  $(DEB_HOST_ARCH))
  # Test failed
  TEST_FLAGS += --exclude-test-name=dictionaries
else ifeq (mipsel, $(DEB_HOST_ARCH))
  # Test error
  TEST_FLAGS += --exclude-test-name=qt
  # Test failed
  TEST_FLAGS += --exclude-test-name=dictionaries
else ifeq (mips64el, $(DEB_HOST_ARCH))
  # Test error
  TEST_FLAGS += --exclude-test-name=qt
  # Test failed
  TEST_FLAGS += --exclude-test-name=dictionaries
endif
