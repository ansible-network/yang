# Developer Guide

This role is developed and maintained by the Ansible Network Working Group.
Contributions to this role are welcomed.  This document will provide individuals
with information about how to contribute to the further development of this
role.

## Contributing

There are many ways you can contribute to this role.  Adding new artifacts such
as modules and plugins, testing and/or reviewing and updating documentation.

### Adding support for new plugins/modules

To add support for a new plugins/modules to this role, there are a couple of things
that need to be done.

1) If you are adding new action plugin add it to `action_plugins`.
If the action pluign works like a module add the new action
plugin say `foo.py` in `action_plugins/foo.py` and the corresponding module
documentation in `library/foo.py`

2) If adding the module code directly to this role, add the module to `library/`

3) If adding a lookup plugin add it to `lookup_plugins/`

4) This role currently uses netconf transport to configure the network device (we plan extend support with other transports in future).
In order to ensure netconf is enabled on remote host this role depends on the platform specific roles [refer](https://github.com/ansible-network/yang/blob/devel/includes/netconf.yml)
where the value of `ansible_network_provider` is the name of the platform role for example [cisco_iosxr](https://github.com/ansible-network/cisco_iosxr).
If you are adding support of new platform ensure the role has a task in the `tasks` folder with name `configure_netconf.yml` that
configures netconf on remote device and update [README](README.md) Dependencies section to include the name of the role.

4) If you are adding a new task to this role please update the [README](README.md) Functions and Variables section
and if required add the task option spec [here](https://github.com/ansible-network/yang/tree/devel/meta)

5) For any new feature pull request or bugifx pull request please update module docs and new/update existing [docs](https://github.com/ansible-network/yang/tree/devel/docs) if required.
Also it is preferred to add test case with pull request.


### Adding platform specific task support

For new platform support add a role that can be distributed through galaxy
which enables the required transport for this role.
Note: It is the responsibility of the task writer to handle the implementation
of the platform specific arguments.

Here is an example that implements a platform specific task:

```yaml
tasks:
  - name: configure network device resource
    include_role:
      name: cisco_iosxr
    tasks_from: configure_netconf
```

### Adding test cases

Refer [test guide](https://github.com/ansible-network/yang/blob/devel/docs/tests/test_guide.md)

# Note

The release cadence for the yang role is two weeks and it will be
released on every second Tuesday at 12:00 PM (GMT) from the date of prior release.
For the PR to be available in the upcoming release it should be in a mergeable state
that is CI is passing and all review comments fixed at least two days prior to scheduled date
of release.

## Bug Reporting

If you have found a bug in the with the current role please open a [GitHub
issue](../../issues)

## Contact

* [#ansible-network IRC channel](https://webchat.freenode.net/?channels=ansible-network) on Freenode.net
