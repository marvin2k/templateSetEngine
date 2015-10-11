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
TEMPL_SCH=$(mkfile_path)template.yaml.schema

ifeq ("$(wildcard $(TEMPL_DB))","")
    $(error no 'template.yaml' found in '$(T)')
endif

# declare the self-verification before including the generated Makefile.
# this way we perform these steps before trying to optional validate the
# provided user datadase itself.

# validate the schema for the "template.yaml" templateSet description
#
# great, return value isl always zero... directly piping to grep will
# hide the error message... so output into "out" file, grep separatly to
# check. output the error or provide target of recipe.
$(O)template.verified: $(TEMPL_DB) $(TEMPL_SCH) | $(O)
	kwalify -lf $(TEMPL_SCH) $(TEMPL_DB) > $@.out
	@grep "$<#0: valid" $@.out >/dev/null \
	    || (cat $@.out && rm -f $@ && false) \
	    && (mv $@.out $@)

# validate the schema itself. i don't think this has to be done often. but it can't hurt either ;-)
$(O)meta.verified: $(TEMPL_SCH) | $(O)
	kwalify -lm $< > $@.out
	@grep "$<#0: valid" $@.out >/dev/null \
	    || (cat $@.out && rm -f $@ && false) \
	    && (mv $@.out $@)

# this is used to collect "validation" steps on the way
validate:: $(O)meta.verified $(O)template.verified

# Note: if there is an syntax error in the generated Makefile.in, the
# file has to be deleted manually... also a problem: when this file is
# empty it will not be regenerated and nothing happens
-include $(O)Makefile.inc

all: generate

# self-documenting ,-)
sysdeps:
	sudo apt-get install python-yaml wget kwalify

# printing the info after all inclusions are done
info::
	@echo "info from main-makefile:"
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

# this is the collection of the main-task: first validate everything,
# then generate the templates.
generate: validate generate_template
	@echo "generate done!"
