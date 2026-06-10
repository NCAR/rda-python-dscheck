# dscheck

Python project to add and process batch jobs for the
[NSF NCAR Geoscience Data Exchange (GDEX)](https://gdex.ucar.edu).

The user guide for this utility tool can be viewed at:
[User guide](https://gdex-docs-dscheck.readthedocs.io).

## Source layout

The package lives under `src/rda_python_dscheck/`.  The three files most
relevant to setup and customization are:

- **`dscheck.py`** — entry point installed as the `dscheck` console script.
  Defines the `DsCheck` class which subclasses `PgCheck`, parses command-line
  options via `self.parsing_input`, and dispatches to the appropriate action
  handler (`add_check_info`, `process_check`, `get_check_info`,
  `set_dscheck_options`, ...).  Build new actions by adding a method here and
  routing to it from `start_actions()`.

- **`pg_check.py`** — defines the `PgCheck` class (inherits from `PgCMD` in
  `rda_python_common`).  Holds the master `OPTS` option table, the `ALIAS`
  map for long/alias names, the `TBLHASH` table field maps for `dscheck` and
  `dsdaemon`, and the helper methods shared by every action (option
  validation, dynamic batch-option resolution, daemon control,
  host/specialist resolution, etc.).  Add or change options here, then
  document them in `dscheck.usg`.

- **`dscheck.usg`** — single source of truth for the user-facing documentation
  displayed by `dscheck -?` and rendered as the
  [user guide](https://gdex-docs-dscheck.readthedocs.io).  Section 3 lists
  Action options, Section 4 lists Mode options, and Section 5 lists Single-
  and Multi-Value Info options.  When you add a new option to `OPTS` in
  `pg_check.py`, add a matching entry to the appropriate subsection of this
  file and (if relevant) to the per-action usage block in Section 3.

## Environment setup

Create a Python environment first; package installs in the next section run
inside whichever environment you activate here.

### Option A — Python venv (DECS machines)

```bash
python3 -m venv $ENVHOME          # e.g. /glade/u/home/gdexdata/gdexmsenv
source $ENVHOME/bin/activate
```

### Option B — Conda (DAV/Casper)

```bash
conda create --prefix $ENVHOME python=3.12   # e.g. /glade/work/gdexdata/conda-envs/pg-gdex
conda activate $ENVHOME
```

## Dependencies

In addition to `rda_python_common`, this package depends on
`rda_python_setuid`.  When `dscheck` runs as the common user, the
`start_one_dscheck()` method in `pg_check.py` submits each PBS batch job via a
`pgstart_<specialist>` wrapper, and those per-specialist `pgstart_*` wrappers
are provisioned by `rda_python_setuid`.  Both dependencies are declared in
`pyproject.toml` and are pulled in automatically on install.

## Installing rda-python-dscheck

Pick whichever install mode fits your workflow.  All variants pull in the
transitive dependencies (`rda_python_common` and `rda_python_setuid`)
automatically.

For local development, clone this repo alongside your project and install it
in editable mode so that changes are picked up without re-installing:

```bash
git clone https://github.com/NCAR/rda-python-dscheck.git
cd rda-python-dscheck
pip install -e .
```

To test a specific branch (e.g. an in-progress feature or fix branch), pass
`-b/--branch` to `git clone`:

```bash
git clone -b <branch-name> https://github.com/NCAR/rda-python-dscheck.git
cd rda-python-dscheck
pip install -e .
```

For a regular (non-editable) install from a checkout:

```bash
pip install /path/to/rda-python-dscheck
```

For a production install on a system that uses the published distribution:

```bash
pip install rda_python_dscheck
```

To upgrade an existing install to the latest published release:

```bash
pip install --upgrade rda_python_dscheck
```

## Setuid Setup

Unlike `dsarch`, `dscheck` is **not** wired as a `setuid_dscheck` link.  It
relies instead on the `pgstart_*` setuid binaries provided by
`rda_python_setuid` (pulled in automatically as a dependency):

- In cron, `dscheck` itself is run as the common user `PGLOG['COMMONUSER']`
  (default `gdexdata`) via `pgstart_<COMMONUSER> dscheck` (e.g.
  `pgstart_gdexdata dscheck`).
- While running as the common user, `start_one_dscheck()` in `pg_check.py`
  submits each PBS batch job as the owning specialist via
  `pgstart_<specialist> ... qsub ...`, so each job runs under that specialist's
  identity.

This means setup is about installing the `pgstart_*` binaries, not creating a
`dscheck -> pywrapper` symlink.

> **Note:** The setuid actions in this section are optional.  If
> `rda_python_setuid` is already installed and fully set up in your
> environment, you can skip this section.

### Install the pgstart binaries (requires sudo access to each user)

Run these steps once per environment:

```bash
# 1. Compile the pywrapper C binary (once per environment):
pywrapper-install -c|--compile -n|--username gdexdata

# 2. Install pgstart_<COMMONUSER> so cron can run 'pgstart_gdexdata dscheck':
pywrapper-install -p|--pgstart -n|--username gdexdata

# 3. Install a pgstart_<specialist> binary for each specialist whose jobs
#    dscheck submits.  Run either by PGLOG['ADMINUSER'] (default zji, if it
#    has 'sudo -u <specialist>'), or by <specialist> directly:
pywrapper-install -p|--pgstart -n|--username <specialist>
```

`pywrapper-install` with no arguments displays the full user guide.

### Update an existing installation (no sudo required)

When the package is upgraded and a new `pywrapper.c` is bundled, recompile and
reinstall all `pgstart_*` binaries using the existing ones:

```bash
pywrapper-install -u|--update
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
