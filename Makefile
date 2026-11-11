.PHONY: all clean

all:
	lua build.lua

clean:
	rm -f ./pages/*.html ./post-list.html ./index.html