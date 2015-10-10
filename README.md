# engine

the whole 'tool' is a Makefile which looks for the template.yaml to
bootstrap.

## design

make uses the template engine 'pyratemp' and the description of a 'template set'
to generate a Makefile.inc describing the template-generation process.  it then
executes this 'generate' and calls the template engine and whatever makes thinks
it has to call to perform the whole generation.

after initial bootstrap only the relevant commands are re-executed.

## calling

options to the tool are passed to make as commandline options.

see early wrapper script `engine/engine.sh`, call for example:

```bash
$ ./engine/engine.sh info
```

## result

the generated stuff can then be used:

```bash
mkdir ./testbf/build
cd ./testbf/build
cmake ..
make
cd -
```

# a collection of files: the 'template set'

set of files belonging together with a 'template.yaml' describing what files
have to be processes.

suitable for one type of input database understood by pyratemp (yaml/json).

a 'template set' can add their own makefile into the generation run
