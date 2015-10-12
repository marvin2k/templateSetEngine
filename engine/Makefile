# set these from outside
ifndef T
    $(error set directory of templateSet to T)
endif
ifndef O
    $(error set output directory of templateSet to O)
endif
ifndef DB
    $(error set location of database to DB)
endif

# some variables:
T_DB=$(T)template.yaml
# "$(E)" contains the location of the engine itself
E:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# how to call the tool we actually rely on
PYRATOOL=$(E)pyratemp-0.3.2/pyratemp_tool.py
PYRATEMP=python $(PYRATOOL)
# the schema of the 'template.yaml' description
T_SCH=$(E)template.yaml.schema

# checking file existence
ifeq ("$(wildcard $(T_DB))","")
    $(error no 'template.yaml' found in template folder '$(T)')
endif

# if we do not know what to do then just start to work
all: generate

# self-documenting ,-)
sysdeps::
	sudo apt-get install python-yaml wget kwalify

# declare some self-verification before including the generated Makefile.
# this way we perform these steps before trying to optional verify the
# provided user database itself.

# verify the schema for the "template.yaml" templateSet description
#
# great, the return value of kwalify is always zero... directly piping to
# grep will hide the error message... so output into "out" file, grep
# separatly to check. output the error or create the target of recipe.
$(O)template.verified: $(T_DB) $(T_SCH) | $(O)
	kwalify -lf $(T_SCH) $(T_DB) > $@.out
	@grep "$<#0: valid" $@.out >/dev/null \
	    || (cat $@.out && rm -f $@ && false) \
	    && (mv $@.out $@)

# verify the schema itself. i don't think this has to be done often. but it can't hurt either ;-)
$(O)meta.verified: $(T_SCH) | $(O)
	kwalify -lm $< > $@.out
	@grep "$<#0: valid" $@.out >/dev/null \
	    || (cat $@.out && rm -f $@ && false) \
	    && (mv $@.out $@)

# this is used to collect the various "validation" steps. the generated
# Makefile.inc might attach here.
verify:: $(O)meta.verified $(O)template.verified

# Note: if there is an syntax error in the generated Makefile.in, the
# file has to be deleted manually... also a problem: when this file is
# empty it will not be regenerated and nothing happens
-include $(O)Makefile.inc

# printing the info after all inclusions are done
info::
	@echo "info from main-makefile:"
	@echo "this makefile folder: '$(E)'"
	@echo "template folder: '$(T)'"
	@echo "template database: '$(T_DB)'"
	@echo "template schema: '$(T_SCH)'"
	@echo "output folder: '$(O)'"
	@echo "database: '$(DB)'"
	@echo "pyratemp: '$(PYRATOOL)'"

# for the time beeing: obtain the tool if it is not there. this is
# silently broken... manually downloading it is strongly advised.
$(E)pyratemp-0.3.2/pyratemp_tool.py:
	wget -qO- http://www.simple-is-better.org/template/pyratemp-0.3.2.tgz \
	    | tar xvz --directory $(E)

pyratemp: $(E)pyratemp-0.3.2/pyratemp_tool.py

# create output directory
$(O):
	mkdir --parent $@

# the templates own bootstrap rule:
$(O)Makefile.inc: $(E)Makefile.inc.template $(T_DB) | $(O) pyratemp
	$(PYRATEMP) -d templateDatabase=$(T_DB) -f $(T_DB) $< > $@ || (rm $@ && false)

# diligent cleaning
clean: clean_state clean_template

# this target does just delete the temporary files created by the
# template-engine itself.
clean_state::
	rm -f $(O)Makefile.inc
	rm -f $(O)meta.verified $(O)template.verified

# this is the collection of the main-task: first verify everything,
# then generate the templates.
generate: verify generate_template
	@echo "generate done!"
