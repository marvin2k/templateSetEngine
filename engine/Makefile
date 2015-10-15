# check this:
ifdef INTERNAL_DB
    $(error _not_ set INTERNAL_DB!)
endif

# the location of the engine itself. needs to use immidiate expansion!
E:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# we _can_ run locally, but this is not the real way to use it.
ifeq ("$(shell pwd)/","$(E)")
    $(error Should not be executing the template engine in local dir.)
endif

# how to call the tool we actually rely on
PYRATOOL=$(E)pyratemp-0.3.2/pyratemp_tool.py
PYRATEMP=python $(PYRATOOL)
# the schema of the 'template.yaml' description is part of the tool
T_SCH=$(E)template.yaml.schema

# should set these from outside. but provide sensible defaults which will
# create a new template from the "templateTemplate".
ifndef T
    T=$(E)../templateTemplate/
    $(warning Setting template directory '$$(T)' of templateSet to default '$(T)')
endif
ifndef O
    O=out/
    $(warning Setting output directory '$$(O)' of templateSet to default '$(O)')
endif
ifndef DB
    DB=$(T)exampleInput.xml
    $(warning Setting location of database '$$(DB)' to default '$(DB)')
endif

# the database describing the templateSet
T_DB=$(T)template.yaml
# the actual template files will be found here
T_FILES?=$(T)files/
# we'll put temporary files of the template engine here
O_STATE?=$(O)state/

# checking existence of template description
ifeq ("$(wildcard $(T_DB))","")
    $(error No templateSet description 'template.yaml' found in template folder '$(T)')
endif

# if we do not know what to do then just start to work
all: state verify generate clean_state

# self-documenting ,-)
sysdeps::
	sudo apt-get install python-yaml wget libyaml-syck-perl libxml-simple-perl kwalify


# this... is... getting.. fucking... complicated...
#
# it is possible to put yaml- or xml-databases into the tool. it either
# converts a xml-database into yaml or copies the yaml. both cases the
# resulting "database.yaml"  is put into the $(O_STATE)-folder.
INTERNAL_DB=$(O_STATE)database.yaml
# when cleaning state, remove the additional yaml-database
clean_state::
	rm -f $(INTERNAL_DB)
# and then check the suffix of the provided $(DB). first the "xml"-case
ifeq (.xml,$(suffix $(DB)))
# convert xml to yaml. not perfect, but it works (tm).
$(O_STATE)database.yaml: $(DB) | $(O_STATE)
	perl $(E)xml2yaml.pl $< > $@
# second the "yaml" case
else ifeq (.yaml,$(suffix $(DB)))
# just copy
$(O_STATE)database.yaml: $(DB) | $(O_STATE)
	cp $< $@
# and error out in any other case
else
    $(error the suffix '$(suffix $(DB))' for $(DB) is unkown?)
endif

# declare some self-verification before including the generated Makefile.
# this way we perform these steps before trying to optional verify the
# provided user database itself.
#
# TODO: switch to xml... throw out kwalify

# verify the schema for the "template.yaml" templateSet description
#
# great, the return value of kwalify is always zero... directly piping to
# grep will hide the error message... so output into "out" file, grep
# separatly to check. output the error or create the target of recipe.
#
# verify the schema itself. i don't think this has to be done often. but it can't hurt either ;-)
$(O_STATE)meta.verified: $(T_SCH) | $(O_STATE)
	kwalify -lm $< > $@.out
	@grep "$<#0: valid" $@.out >/dev/null \
	    || (cat $@.out && rm -f $@ && false) \
	    && (mv $@.out $@)
# and then verify the actual "template.yaml"
$(O_STATE)template.verified: $(T_DB) $(T_SCH) | $(O_STATE)
	kwalify -lf $(T_SCH) $(T_DB) > $@.out
	@grep "$<#0: valid" $@.out >/dev/null \
	    || (cat $@.out && rm -f $@ && false) \
	    && (mv $@.out $@)

# this is used to collect the various "validation" steps. this additionally
# includes the converted input database.
verify:: $(O_STATE)meta.verified $(O_STATE)template.verified $(INTERNAL_DB)

# Note: if there is an syntax error in the generated $(O_STATE)Makefile.in, the
# file has to be deleted manually...
#
# TODO: this is broken... if the "template.yaml" is not correct, the
# "Makefile.inc" cannot be generated and the "template.yaml" can never be
# verfied... more this kwalify call into the engine.py!
-include $(O_STATE)Makefile.inc

# printing the info after all inclusions are done
info::
	@echo "info from main-makefile:"
	@echo "this makefile folder: '$(E)'"
	@echo "template folder: '$(T)'"
	@echo "template files: '$(T_FILES)'"
	@echo "template database: '$(T_DB)'"
	@echo "template schema: '$(T_SCH)'"
	@echo "output folder: '$(O)'"
	@echo "output state folder: '$(O_STATE)'"
	@echo "database: '$(DB)'"
	@echo "pyratemp: '$(PYRATOOL)'"

# for the time beeing: obtain the underlying template-engine.
$(E)pyratemp-0.3.2/pyratemp_tool.py:
	wget -qO- http://www.simple-is-better.org/template/pyratemp-0.3.2.tgz \
	    | tar xvz --directory $(E)

pyratemp: $(E)pyratemp-0.3.2/pyratemp_tool.py

# create output directories
$(O):
	mkdir --parent $@
$(O_STATE):
	mkdir --parent $@

# the templates own bootstrap rule:
#
# TODO: add all variables into generated model, use them instead of the
# variables for more safety. then maybe make the generated makefiles .PHONY?
$(O_STATE)Makefile.inc: $(E)Makefile.inc.template $(T_DB) | $(O_STATE) pyratemp
	$(PYRATEMP) -d templateDatabase=$(T_DB) -f $(T_DB) $< > $@ || (rm $@ && false)

# this is the collection of the main-task: first verify everything,
# then generate the templates.
generate: verify generate_template
	@echo "generate done!"

# diligent cleaning
clean: clean_state clean_template

# this target does delete all temporary state-files created by the
# template-engine for its own usage. at the end the state-folder is "rmdir"ed,
# in the hope that its actually empty.
clean_state::
	rm -f $(O_STATE)Makefile.inc
	rm -f $(O_STATE)meta.verified $(O_STATE)template.verified
	rmdir $(O_STATE)

