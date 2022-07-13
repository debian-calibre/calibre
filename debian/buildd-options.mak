# -*- mode: makefile-gmake -*-

# In case builds fail with current source code
# Exclude memory test because garbage collection is prone to happen
# at inconvenient intervals and disturb the memory test
# TEST_FLAGS += --exclude-test-name=mem_leaks

