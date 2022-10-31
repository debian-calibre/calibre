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
else ifeq (i386,  $(DEB_HOST_ARCH))
  # seccomp-bpf crash
  TEST_FLAGS += --exclude-test-name=qt
  TEST_FLAGS += --exclude-test-name=dom_load
endif
