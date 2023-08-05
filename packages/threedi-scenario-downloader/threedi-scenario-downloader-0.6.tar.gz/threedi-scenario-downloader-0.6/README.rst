threedi-scenario-downloader
==========================================

The threedi-scenario-downloader package includes functions in order to
automate most used download actions on the 3Di results.

Example methods are:

- Download raw results.
- Download logging.
- Download maximum waterdepth (non-temporal raster).
- Download waterdepth (temporal raster, supply timestamp for snapshot).
- Find all scenarios model slug or scenario name.


Installation
------------

We can be installed with::

  $ pip install threedi-scenario-downloader


Development installation of this project itself
-----------------------------------------------

We're installed with `pipenv <https://docs.pipenv.org/>`_, a handy wrapper
around pip and virtualenv. Install that first with ``pip install
pipenv``. Then run::

  $ PIPENV_VENV_IN_PROJECT=1 pipenv --three
  $ pipenv install --dev

In order to get nicely formatted python files without having to spend manual
work on it, run the following command periodically::

  $ pipenv run black threedi_scenario_downloader

Run the tests regularly. This also checks with pyflakes, black and it reports
coverage. Pure luxury::

  $ pipenv run pytest

The tests are also run automatically `on travis-ci
<https://travis-ci.com/nens/threedi-scenario-downloader>`_, you'll see it in
the pull requests. There's also `coverage reporting
<https://coveralls.io/github/nens/threedi-scenario-downloader>`_ on
coveralls.io.

If you need a new dependency (like `requests`), add it in `setup.py` in
`install_requires`. Afterwards, run install again to actuall install your
dependency::

  $ pipenv install --dev
