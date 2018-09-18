====================
Ansible Network yang
====================

.. _Ansible Network yang_v2.6.0:

v2.6.0
==============

.. _Ansible Network yang_v2.6.0_Major Changes:

Major Changes
-------------

- Initial release of the ``yang`` Ansible role.

- This role provides functions to perform automation activities using yang models using supported transports.


.. _Ansible Network yang_v2.6.0_New Lookup Plugins:

New Lookup Plugins
------------------

- NEW ``yang_json2xml`` Plugin to validate json configuration against a yang mode and convert it to xml format.

- NEW ``yang_spec`` Plugin to generate skeleton json and xml configuration for reference config generation and yang tree representation.


.. _Ansible Network yang_v2.6.0_New Modules:

New Modules
-----------

- NEW ``yang_fetch`` module to fetch yang models from remote network device if supported.


.. _Ansible Network yang_v2.6.0_New Functions:

New Functions
-------------

- NEW ``fetch`` function to fetch yang models from network device if supported.

- NEW ``configure`` function to validate input ``json`` configuration against a yang model push it to device.

- NEW ``spec`` function to generate skeleton json and xml configuration for reference config generation and yang tree representation from given yang model.
