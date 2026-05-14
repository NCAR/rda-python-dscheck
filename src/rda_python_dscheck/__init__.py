"""rda_python_dscheck: dataset check (dscheck) utility package.

This package exposes two parallel APIs:

1. Legacy module-based API (back-compat). Import the capitalized
   submodule and call its module-level functions, e.g.::

       from rda_python_dscheck import PgCheck

2. Class-based API (preferred for new code). Import the class from the
   lower-case module and either instantiate or subclass it, e.g.::

       from rda_python_dscheck.pg_check import PgCheck

The legacy submodule is eagerly imported below so that
``from rda_python_dscheck import PgCheck`` continues to return the module
object that existing callers expect.
"""

from . import PgCheck

__version__ = "2.0.7"

__all__ = [
   "PgCheck",
   "__version__",
]
