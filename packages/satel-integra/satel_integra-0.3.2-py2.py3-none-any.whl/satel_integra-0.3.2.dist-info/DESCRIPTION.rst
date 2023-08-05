=============
Satel Integra
=============


.. image:: https://img.shields.io/pypi/v/satel_integra.svg
        :target: https://pypi.python.org/pypi/satel_integra

.. image:: https://img.shields.io/travis/c-soft/satel_integra.svg
        :target: https://travis-ci.org/c-soft/satel_integra

.. image:: https://readthedocs.org/projects/satel-integra/badge/?version=latest
        :target: https://satel-integra.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/c-soft/satel_integra/shield.svg
     :target: https://pyup.io/repos/github/c-soft/satel_integra/
     :alt: Updates


Communication library and basic testing tool for Satel Integra alarm system. Communication via tcpip protocol published by SATEL. 


* Free software: MIT license
* Documentation: https://satel-integra.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.0 (2017-08-24)
------------------

* First release on PyPI.

0.2.0 (2018-12-20)
------------------

* Integrated changes from community: added monitoring of ouitputs.
* Attempt at fixing issue with "state unknown" of the alarm. Unfurtunately unsuccesful.

0.3.1 (2019-02-13)
------------------

* improved robustness when connection disapears
* fixed issues with "status unknown" which caused blocking of the functionality in HA
- still existing issues with alarm status - to be fixed

