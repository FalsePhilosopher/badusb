# -*- mode: makefile-gmake -*-

all:
.PHONY: all clean install

#------------------------------------------------------------------------------
# Settings

# Set UTF-8 locale
ifeq ($(shell locale | grep -Ei 'LC_CTYPE.*utf-?8'),"")
  utf8_locale := $(shell locale -a | grep -Ei 'utf-?8' | head -1)
  ifneq ($(utf8_locale),"")
    export LC_ALL=$(utf8_locale)
  else
    $(warning It seems your system does not support UTF-8)
  endif
endif

# Auto detect gawk
AWK := $(shell which gawk 2>/dev/null || echo awk)
ifeq ($(AWK),"awk")
  $(warning gawk (GNU awk) is not available, which may cause problems. Consider installing GNU awk.)
endif

# C++ compile options
CPPFLAGS = -MD -MP -MF $(@:.o=.dep)
CXXFLAGS := -std=c++17 -Wall -Wextra -Ofast

# @var DESTDIR
# @var PREFIX [/usr/local]
# @var INSTALL_SUBDIR_LICENSE [share/licenses]
#
# These variables control the install location used by "make
# install". Files are copied to the following directories:
#
# - DESTDIR/PREFIX/bin
# - DESTDIR/PREFIX/share/cxxmatrix
# - DESTDIR/PREFIX/INSTALL_SUBDIR_LICENSE/cxxmatrix
#
ifneq ($(filter-out %/,$(DESTDIR)),)
  DESTDIR := $(DESTDIR)/
endif
ifneq ($(DESTDIR)$(PREFIX),)
  insdir_base := $(DESTDIR)$(PREFIX)
else
  insdir_base := /usr/local
endif
INSTALL_SUBDIR_LICENSE := share/licenses/cxxmatrix
insdir_license := $(insdir_base)/$(INSTALL_SUBDIR_LICENSE)

#------------------------------------------------------------------------------
# cxx matrix

all: cxxmatrix

cxxmatrix-OBJS := cxxmatrix.o
ifeq ($(TARGET),win32)
  cxxmatrix-OBJS += term_win32.o
  CXXFLAGS += -s -static -static-libgcc -static-libstdc++
else
  cxxmatrix-OBJS += term_unix.o
endif

-include $(wildcard *.dep)
cxxmatrix: $(cxxmatrix-OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

cxxmatrix.o: cxxmatrix.cpp glyph.inl
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c -o $@ $<

glyph.inl: glyph.awk glyph.def
	$(AWK) -f glyph.awk glyph.def > glyph.inl.part
	mv glyph.inl.part $@

clean:
	-rm -rf *.o glyph.inl


install: cxxmatrix
	mkdir -p "$(insdir_base)/bin"
	cp cxxmatrix "$(insdir_base)/bin/cxxmatrix"
	chmod +x "$(insdir_base)/bin/cxxmatrix"
	mkdir -p "$(insdir_base)/share/man/man1"
	gzip -c cxxmatrix.1 > "$(insdir_base)/share/man/man1/cxxmatrix.1.gz"
	mkdir -p "$(insdir_license)"
	cp LICENSE.md "$(insdir_license)/LICENSE.md"

#------------------------------------------------------------------------------
