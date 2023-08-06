=====================
pytest-disable-plugin
=====================

.. image:: https://img.shields.io/pypi/v/pytest-disable-plugin.svg
    :target: https://pypi.org/project/pytest-disable-plugin
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-disable-plugin.svg
    :target: https://pypi.org/project/pytest-disable-plugin
    :alt: Python versions

.. image:: https://travis-ci.org/username/pytest-disable-plugin.svg?branch=master
    :target: https://travis-ci.org/username/pytest-disable-plugin
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/username/pytest-disable-plugin?branch=master
    :target: https://ci.appveyor.com/project/username/pytest-disable-plugin/branch/master
    :alt: See Build Status on AppVeyor

Disable plugins per test

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Disable pytest plugins for specific tests.


Requirements
------------

* pytest


Installation
------------

You can install "pytest-disable-plugin" via `pip`_ from `PyPI`_::

    $ pip install pytest-disable-plugin


Usage
-----

```python
import pytest

@pytest.mark.disable_plugin("some_plugin_name")
def test_something():
    # This test will unload the plugin during setup and reload it afterwards.
    assert f() == 1

def test_something_else():
    # This test will use the plugin as normal.
    assert f() == 2
```

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-disable-plugin" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/username/pytest-disable-plugin/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
