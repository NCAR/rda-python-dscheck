# dscheck

Python project to add and process batch jobs for the [NSF NCAR Geoscience Data Exchange (GDEX)](https://gdex.ucar.edu).

The user guide for this utility tool can be viewed at: [User guide](https://gdex-docs-dscheck.readthedocs.io).

## Source layout

The package lives under `src/rda_python_dscheck/`.  The three files most
relevant to setup and customization are:

- **`dscheck.py`** — entry point installed as the `setuid_dscheck`
  console script.  Defines the `DsCheck` class which subclasses
  `PgCheck`, parses command-line options via `self.parsing_input`, and
  dispatches to the appropriate action handler (`add_check_info`,
  `process_check`, `get_check_info`, `set_dscheck_options`, ...).
  Build new actions by adding a method here and routing to it from
  `start_actions()`.

- **`pg_check.py`** — defines the `PgCheck` class (inherits from
  `PgCMD` in `rda_python_common`).  Holds the master `OPTS` option
  table, the `ALIAS` map for long/alias names, the `TBLHASH` table
  field maps for `dscheck` and `dsdaemon`, and the helper methods
  shared by every action (option validation, dynamic batch-option
  resolution, daemon control, host/specialist resolution, etc.).
  Add or change options here, then document them in `dscheck.usg`.

- **`dscheck.usg`** — single source of truth for the user-facing
  documentation displayed by `dscheck -?` and rendered as the
  [user guide](https://gdex-docs-dscheck.readthedocs.io).  Section 3
  lists Action options, Section 4 lists Mode options, and Section 5
  lists Single- and Multi-Value Info options.  When you add a new
  option to `OPTS` in `pg_check.py`, add a matching entry to the
  appropriate subsection of this file and (if relevant) to the
  per-action usage block in Section 3.

### Installing from PyPI

The package is published on [PyPI](https://pypi.org/project/rda_python_dscheck/),
so the regular install command is:

```bash
pip install rda_python_dscheck
```

To upgrade an existing install to the latest published release:

```bash
pip install --upgrade rda_python_dscheck
```

This pulls in `rda_python_common` (which provides `PgCMD`, `PgLOG`,
`PgDBI`, ...) and registers the `setuid_dscheck` console script.

### Installing for development

For local changes, clone the repo and install in editable mode so that
edits are picked up immediately without reinstalling:

```bash
git clone https://github.com/NCAR/rda-python-dscheck.git
cd rda-python-dscheck
pip install -e .
```

## Documentation sync

The user guide rendered at
[gdex-docs-dscheck.readthedocs.io](https://gdex-docs-dscheck.readthedocs.io) is
generated from `src/rda_python_dscheck/dscheck.usg` in this repository.  When a
pull request that modifies `dscheck.usg` is merged here, an automated workflow
converts the updated `dscheck.usg` into the RST-format source files in the
[gdex-docs-dscheck](https://github.com/NCAR/gdex-docs-dscheck) repository and
opens a pull request there with the regenerated docs, ready for review and
merge.  No manual RST editing is required — keep all user-facing content in
`dscheck.usg` and let the sync produce the docs.

