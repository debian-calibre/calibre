# "py3" howto

## Why we use beta ("py3" branch) code

Current Debian's Calibre source code uses upstream release with "py3" branch
fixes because Debian wants Python 3 even in build time.
Current upstream code supports Python 3, but it still wants Python 2 in
build time.

So we use "py3" branch code because it can be build without Python 2.

## How to update upstream "py3" branch files into current Debian souce code

Current Debian's Calibre source code uses upstream newest release code with
"py3" branch patch.

1. Import and merge upstream source code with `gbp import-orig --uscan`.
2. Take "py3" branch patch set with `git format-patch --find-renames --find-copies [from rev]..py3` from upstream Git repository.
3. Update `debian/patches/py3` directory with new "py3" branch patch set as quilt(1) patch set.
4. Update `debian/patches/series` file to quilt(1) works.
5. Refresh `debian/patches/py3` patches to quilt(1) works well.
