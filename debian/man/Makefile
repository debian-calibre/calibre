TXTS=$(shell find . -name "*.txt")
MANS=$(TXTS:.txt=.1)
VERSION=unknown

all: $(MANS)

%.1: %.txt
	@echo "Creating man page for $$(echo $@ | sed -e 's/.1//')" ; \
	printf "NAME\n\n$(shell cat names | grep -E "^$$(echo $@ | sed -e 's/.1//') - ")\n\n" | \
	cat - $< | \
		sed -e "s/TEXT_SIZE_MULTIPLIER_FOR_RENDERED_TABLES/SIZE/" | \
		sed -e "s/ *$$//g" | \
		sed -e "s/'/\\\\'/g" | \
		sed -e "s/\"/\\\\'/g" | \
		sed -e "s/ - feeds2/   feeds2/g" | \
		sed -e "s/^Options:$$/\n\n  MAIN OPTIONS:/" | \
		sed -e "s/^  \([^- ].*\):$$/\n\n\1 OPTIONS#BR#/" | \
		sed -e "s/OPTIONS OPTIONS/OPTIONS/" | \
		sed -e "s/2DISK OPTIONS/ TO DISK OPTIONS/" | \
		sed -e "s/#BR# */\n/" | \
		sed -e "s/^Created by/AUTHOR\nCreated by/" | \
		sed -e "s/^ARG can be one of:/ARGUMENT\nARG can be one of:\n/" | \
		sed -e "s/^Usage:/USAGE\n/" | \
		awk '{if (/^USAGE$$/) { \
				out=$$0 "\n\n" ; \
				getline ; \
				out=out $$0 ; \
				getline ; \
				out=out $$0 ; \
				print out "\n\nDESCRIPTION\n\n" \
			} else {print $$0}}' | \
		awk '{if (/ *-/) { out=$$0; getline; out=out $$0;print out} else {print $$0}}' | \
		awk '/^$$/{ if (! blank++) print; next } { blank=0; print }' | \
		txt2man \
			-s 1 \
			-t `echo "$@" | sed -e "s/.1//"` \
			-P "Calibre $(VERSION)" \
			> $@

check: $(MANS)
	@for i in *.1; do \
		echo "Checking man page for $$i" ; \
		LANG=C man --warnings -l "$$i" >/dev/null ; \
	done

clean:
	rm -f *.1

