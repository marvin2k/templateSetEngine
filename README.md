# templateSetEngine

Solves the problem of configuring a set of template files according to an
external database. Therefore it uses a simple python based template engine to
process the individual files.

The templateSet itself is located in the directory pointed to by `$(T)` and the
resulting files will be put into `$(O)`. The engine is located in `$(E)`.

## Collection of files: the 'templateSet'

Set of files resident in the `$(T)` folder. They form a collection of files
together with a `$(T)template.yaml` describing what files have to be processes.
See `engine/template.yaml.schema` what is allowed.

Each templateSet is suitable for one type of input database understood by
[pyratemp][1] (which is yaml or json). Pyratemp was choosen because it tries to
leverage a strong model/view separation and looks simple enough.

## Idea

The whole 'tool' is actually a just Makefile which looks for the
`$(T)/template.yaml` to bootstrap. It uses the very same template engine to
create an additional `$(T)Makefile.inc` which then controls the single calls for
each individual file of the templateSet.

Pro:
- Possible automatic parallelization via `-j`
- `make` can check the "model" of the template-generation itself, which is
  coded in the targets of the Makefiles

Contra:
- Some generated files like `$(T)Makefile.inc` are used to keep state and litter
  the output folder.
- The syntax of Makefiles is sometimes not very straight-forward. Well, it is
  used to solve a complex problem.

## Design

Uses the template engine [pyratemp][1] and the description of the templateSet to
generate the `$(T)Makefile.inc` to control the template-generation process.
Someone can then execute the `generate` target to call the template engine and
whatever `make` thinks it has to call to perform the whole generation. After the
initial bootstrap only the relevant commands are re-executed according to the
rules in the Makefiles.

A templateSet can optionally chain its own `$(T)Makefile.add` into the
generation process to allow additional transformation steps.

Extra variables can optionally be passed from the `$(T)template.yaml` into the
models of each template file.

## Validation

The tool uses [kwalify][2] to verify the `$(T)template.yaml` of a templateSet
and optionally the user-provided database. To mark successfull verification, the
following files are created:

- `$(O)meta.success`: The description of the tools schema file for the
  `$(T)template.yaml` is correct. This step prevent the developer of the tool from making
mistakes.
- `$(O)template.success`: The `$(T)template.yaml` of the templateSet is
  correct. This prevents the developer of the templateSet from making mistakes.
- `$(O)database.success`: Optional step. Denotes that the last database used was alright 
  according to the given schema file defined in `$(T)template.yaml`. This
prevents users of the templateSet from making mistakes.

Since the `kwalify` tool will return 0 even on failure (!) some hidden shell trickery has to be performed.

## Calling

Options can be passed to `make` as command line options. See early wrapper script `engine/engine.sh`. Call for example:

```bash
$ ./engine/engine.sh info
```

And then to generate the actual files of the example templateSet in this
repository:

```bash
$ ./engine/engine.sh generate
```

Note: The script is just a proof of concept. Some scripting language should be
used to provide proper command line argument handling.

Note: If the `$(O)Makefile.inc` has syntax errors the tool will stop working as
make cannot recover from parsing errors. This could be fixed in the
wrapper-script.

## Example templateSet

Contains a simple cmake project. The generated files can then be used:

```bash
mkdir ./testbf/build
cd ./testbf/build
cmake ..
make
cd -
```

# next steps

- Might wanna move to [Rx][3] as schema language? Project does look more
  alive.
- careful, the example template uses the "XML_DB" hack to demonstrate internal
  database conversion, like xml2yaml... this feature is not tought-out...

[1]: http://www.simple-is-better.org/template
[2]: http://www.kuwata-lab.com/kwalify
[3]: http://rx.codesimply.com/index.html
[4]: https://docs.python.org/2/library/argparse.html
