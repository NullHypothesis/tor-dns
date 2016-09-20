SUBDIRS = alexa dist pct rounds scale window

all:
	for dir in $(SUBDIRS); do \
		cd $$dir; sh generate-graphs.sh; \
	done

clean:
	for dir in $(SUBDIRS); do \
		rm -f $$dir/*.pdf; \
	done
