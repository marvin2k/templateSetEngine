# templateSetEngine

Solves the problem of configuring a set of template files according to an
external database using a simple python based template engine.

## idea

The whole 'tool' is a just Makefile which looks for the `$(T)/template.yaml` to bootstrap. It uses the very same template engine to create an additional 'Makefile.inc' which controls the single calls for each individual template file.

Pro:
- Possible automatic parallelization via "-j"
- make can check the "model" of the template-generation itself

Contra:
- generated file "Makefile.inc" litters in target folder to keep state

## design

Uses the template engine [pyratemp][1] and the description of the 'template set' to
generate a 'Makefile.inc' describing the template-generation process. Someone
can then executes the 'generate' target to call the template engine and whatever
make thinks it has to call to perform the whole generation.

After the initial bootstrap only the relevant commands are re-executed.

A 'template set' can include its own Makefile into the generation process.

Extra variables can be passed from the 'template.yaml' into the models of each
template file.

## calling

Options are passed to make as command line options.

See early wrapper script `engine/engine.sh`, call for example:

```bash
$ ./engine/engine.sh info
```

And then:

```bash
$ ./engine/engine.sh generate
```

## example set

The generated files can then be used:

```bash
mkdir ./testbf/build
cd ./testbf/build
cmake ..
make
cd -
```

# a collection of files: the 'template set'

Set of files belonging together with a 'template.yaml' describing what files
have to be processes.

Each set is suitable for one type of input database understood by [pyratemp][1] (yaml/json). Tries to leverage a strong model/view separation.

[1]: http://www.simple-is-better.org/template
