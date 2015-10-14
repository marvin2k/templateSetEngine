# templateSetEngine

Solves the problem of configuring a set of template files according to an
external database. Therefore it uses a simple python based template engine to
process the individual files.

The templateSet itself is located in the directory pointed to by `$(T)`, the
database used to fill them is in `$(DB)` and the resulting files will be put
into `$(O)`. The engine is located in `$(E)`.

## Collection of files: the 'templateSet'

Set of files resident in the `$(T)` folder. They form a collection of files
together with a `$(T)template.yaml` describing what files have to be processes.
See `engine/template.yaml.schema` what is allowed.

Each templateSet is suitable for one type of input database understood by
[pyratemp][1] (which is yaml or json). Pyratemp was chosen because it tries to
leverage a strong model/view separation and looks simple enough.

## Idea

The whole 'tool' is actually a just Makefile which looks for the
`$(T)template.yaml` to bootstrap. It uses the very same template engine to
create an additional `$(O)Makefile.inc` which then controls the single calls for
each individual file of the templateSet.

Pro:
- Possible automatic parallelization via `-j`
- `make` can check the "model" of the template-generation itself, which is
  coded in the targets of the Makefiles

Contra:
- Some generated files like `$(O)Makefile.inc` are used to keep state and litter
  the output folder.
- The syntax of Makefiles is sometimes not very straight-forward. Well, it is
  used to solve a complex problem.

## Design

Uses the template engine [pyratemp][1] and the description of the templateSet to
generate the `$(O)Makefile.inc` which controls the template-generation process.
This file is included into the main-makefile together with a target to create
it. The file is not there initially, `make` recognises the target to create the
file, executes it reevaluates everything to incorporate the added targets.

Someone can then execute the `generate` target to call the template engine and
whatever `make` thinks it has to call to perform the whole generation. After the
initial bootstrap only the relevant commands are re-executed according to the
rules in the Makefiles. To remove all temporary files call the
`clean_state` target.

A templateSet can optionally chain its own `$(T)Makefile.add` into the
generation process to allow additional transformation steps.

Extra variables can optionally be passed from the `$(T)template.yaml` into the
models of each template file.

## Validation

The tool uses [kwalify][2] to verify the `$(T)template.yaml` of a templateSet
and optionally the user-provided database. To mark successful verification, the
following files are created:

- `$(O)meta.verified`: The description of the tools schema file for the
  `$(T)template.yaml` is correct. This step prevent the developer of the tool from making
mistakes.
- `$(O)template.verified`: The `$(T)template.yaml` of the templateSet is
  correct. This prevents the developer of the templateSet from making mistakes.
- `$(O)database.verified`: Optional step. Denotes that the last database used was alright 
  according to the given schema file defined in `$(T)template.yaml`. This
prevents users of the templateSet from making mistakes.

Since the `kwalify` tool will return 0 even on failure (!) some hidden shell trickery has to be performed.

Note: Validation might be broken (read: missing) when verifying with one database, then using another one with an earlier time stamp to generate...

## Wrapper script

Options to underlying `make` can be passed as command line options. See wrapper script `engine/engine.py`. Call for example:

```bash
$ ./engine/engine.py -h
```

Note that unknown options are passed on to `make`, especially useful for
debugging. To generate the actual files of the example templateSet in this
repository using 4 processes in parallel:

```bash
$ ./engine/engine.py -DB templates/bla.yaml -T templates -O outdir generate -j4
```

Note: If the `$(O)Makefile.inc` has syntax errors the tool will stop working as
make cannot recover from parsing errors. This could be fixed in the
wrapper-script.

## Creating new templateSet

At first clone this project into a local directory. Then use the
templateSetEngine to create a new template from the stock-templateTemplate:

```bash
mkdir work && cd work
git clone https://github.com/marvin2k/templateSetEngine
./templateSetEngine/engine/engine.py -T templateSetEngine/templateTemplate -O newTemplate -DB templateSetEngine/templateTemplate/exampleInput.xml generate clean_state
```

Now you can edit the files in `newTemplate`, or use the engine on the new template:

```bash
./templateSetEngine/engine/engine.py -T newTemplate -O output -DB newTemplate/exampleInput.xml generate clean_state
```

In `output` is the new generated instance. Careful to not wrap your head
accidentally around the wrong thing...

# next steps

- Might wanna move to [Rx][3] as schema language? Project does look more
  alive.
- Careful, the example template uses the "XML_DB" hack to demonstrate internal
  database conversion, like xml2yaml... This feature is not thought-out...
- Shipping of pyratemp is a problem...
- is this `$(T)template.yaml` really needed? Why not fall back to make's implicit
  rules? The informations provided in this yaml-file just feel redundant...
  subdirectory handling could be complicated... globbing additional makefiles
  should be easy... otherwise hiding makefile-syntax behind a simple yaml file
  sounds like a good idea...
- research on how to use this stuff to add c++ code to existing project.
  problem: cmake cannot re-execute itself after initial configuration (make
  can). so: have an including CMakeLists.txt with an "ExternalProject()"
  referencing a makefile based mini-lib. there, some CMakeLists is generated

[1]: http://www.simple-is-better.org/template
[2]: http://www.kuwata-lab.com/kwalify
[3]: http://rx.codesimply.com/index.html
[4]: https://docs.python.org/2/library/argparse.html
