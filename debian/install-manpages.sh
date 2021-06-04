#!/bin/sh

set -eu

dh_installman -pcalibre --language=C man-pages/man1/*.1

for i in man-pages/*
do
    lang=$(basename ${i})
    if [ "${lang}" = man1 ]
    then
	continue
    fi

    dh_installman -pcalibre --language=${lang} ${i}/man1/*.1
done
