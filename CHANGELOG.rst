====================
Ansible Network Yang
====================

.. _Ansible Network Yang_v2.7.0:

v2.7.0
======

.. _Ansible Network Yang_v2.7.0_New Functions:

New Functions
-------------

- Add support for get function `yang#33 <https://github.com/ansible-network/yang/pull/33>`_.


.. _Ansible Network Yang_v2.7.0_Bugfixes:

Bugfixes
--------

- Fix connection type check issue `yang#32 <https://github.com/ansible-network/yang/pull/32>`_.


.. _Ansible Network Yang_v2.6.2:

v2.6.2
======

.. _Ansible Network Yang_v2.6.2_Minor Changes:

Minor Changes
-------------

- Remove travis-ci support  `yang#30 <https://github.com/ansible-network/yang/pull/30>`_.

- Resync tox.ini file `yang#29 <https://github.com/ansible-network/yang/pull/29>`_.


.. _Ansible Network Yang_v2.6.1:

v2.6.1
======

.. _Ansible Network Yang_v2.6.1_Minor Changes:

Minor Changes
-------------

- Add network-engine role dependency in meta file `yang#14 <https://github.com/ansible-network/yang/pull/14>`_.

- Check for ansible-min-version `yang#16 <https://github.com/ansible-network/yang/pull/16>`_.

- Add support for bindep.txt `yang#25 <https://github.com/ansible-network/yang/pull/25>`_.


.. _Ansible Network Yang_v2.6.0:

v2.6.0
======

.. _Ansible Network Yang_v2.6.0_Major Changes:

Major Changes
-------------

- Initial release of the ``yang`` Ansible role.

- This role provides functions to perform automation activities using yang models using supported transports.


.. _Ansible Network Yang_v2.6.0_New Lookup Plugins:

New Lookup Plugins
------------------

- NEW ``yang_json2xml`` Plugin to validate json configuration against a yang mode and convert it to xml format.

- NEW ``yang_spec`` Plugin to generate skeleton json and xml configuration for reference config generation and yang tree representation.


.. _Ansible Network Yang_v2.6.0_New Modules:

New Modules
-----------

- NEW ``yang_fetch`` module to fetch yang models from remote network device if supported.


.. _Ansible Network Yang_v2.6.0_New Functions:

New Functions
-------------

- NEW ``fetch`` function to fetch yang models from network device if supported.

- NEW ``configure`` function to validate input ``json`` configuration against a yang model push it to device.

- NEW ``spec`` function to generate skeleton json and xml configuration for reference config generation and yang tree representation from given yang model.

