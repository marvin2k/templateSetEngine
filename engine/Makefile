# sudo apt-get install python-yaml wget

# set these from outside
ifndef T
    $(error set directory of templates to T)
endif
ifndef PYRATOOL
    $(error set location of pyratool to PYRATOOL)
endif
# not checking DB to allows automatic conversion makefiles to set the
# value later
#ifndef DB
#    $(error set location of database to DB)
#endif

# some variables:
TEMPL_DB=$(T)template.yaml
PYRATEMP=python $(PYRATOOL)
mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifeq ("$(wildcard $(TEMPL_DB))","")
    $(error no 'template.yaml' found in '$(T)')
endif

# problematic: if there is an syntax error in the generated Makefile.in,
# the file has to be deleted manually... also a problem: when this file
# is empty it will not be regenerated and nothing happens
-include $(O)Makefile.inc

all: generate

# printing the info after all inclusions are done
info::
	@echo "info: main-makefile:"
	@echo "this makefile folder: '$(mkfile_path)'"
	@echo "template folder: '$(T)'"
	@echo "output folder: '$(O)'"
	@echo "database: '$(DB)'"
	@echo "pyratemp: '$(PYRATOOL)'"

# obtaining the tool if it is not there
pyratemp-0.3.2:
	wget -qO- http://www.simple-is-better.org/template/pyratemp-0.3.2.tgz | tar xvz

# create output directory
$(O):
	mkdir --parent $@

# the templates own bootstrap rule:
$(O)Makefile.inc: $(mkfile_path)Makefile.inc.template $(TEMPL_DB) | $(O)
	$(PYRATEMP) -d templateDatabase=$(TEMPL_DB) -f $(TEMPL_DB) $< > $@ || rm $@

# diligent cleaning
clean: clean_template
	rm -f $(O)Makefile.inc

# status printing
clean_template::
	@echo "clean_template done!"
generate::
	@echo "generate done!"
