# yang

This role provides the foundation for building network roles by providing
modules and plugins related to yang support.

To install this role: `ansible-galaxy install ansible-network.yang`

To see the version of this role you currently have installed: `ansible-galaxy list | grep yang`

To ensure you have the latest version available: `ansible-galaxy install -f ansible-network.yang`

To use this role, follow the [User Guide](https://github.com/ansible-network/yang/blob/devel/docs/user_guide/README.md).

To find other roles maintained by the Ansible Network team, see our [Galaxy Profile](https://galaxy.ansible.com/ansible-network/). 

Any open bugs and/or feature requests are tracked in [GitHub issues](https://github.com/ansible-network/yang/issues).

Interested in contributing to this role? Check out [CONTRIBUTING](https://github.com/ansible-network/yang/blob/devel/CONTRIBUTING.md) before submitting a pull request.

## Documentation

* User guide: [How to use](https://github.com/ansible-network/yang/blob/devel/docs/user_guide/README.md)
* Test guide: [How to test](https://github.com/ansible-network/yang/blob/devel/docs/tests/test_guide.md)

For module documentation see the [modules](#modules) section below.

## Requirements

* Ansible 2.6.0 or later
* Ansible Network Engine Role 2.6.2 or later

## List of network os the role is actively tested against
* iosxr (version 6.1.2)
* junos (version 17.4)

## Functions

This section provides a list of the available functions that are including in this role.
Any of the provided functions can be implemented in Ansible playbooks to perform automation activities
on yang/netconf supported devices.

* `configure` [source](https://github.com/ansible-network/yang/blob/devel/tasks/configure.yml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/tasks/configure.md).
* `spec` [source](https://github.com/ansible-network/yang/blob/devel/tasks/spec.yml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/tasks/spec.md).
* `fetch` [source](https://github.com/ansible-network/yang/blob/devel/tasks/fetch.yml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/tasks/fetch.md).
* `get` [source](https://github.com/ansible-network/yang/blob/devel/tasks/get.yml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/tasks/get.md).

## Variables

The following are the list of variables for each of the role functions.

* `configure`: [options](https://github.com/ansible-network/yang/blob/devel/meta/configure_options.yml)
* `spec`: [options](https://github.com/ansible-network/yang/blob/devel/meta/spec_options.yml)
* `fetch`: [options](https://github.com/ansible-network/yang/blob/devel/meta/fetch_options.yml)
* `fetch`: [options](https://github.com/ansible-network/yang/blob/devel/meta/get_options.yml)


## Modules

The following is a list of modules that are provided by this role, which include documentation & examples:

* `yang_fetch` [source](https://github.com/ansible-network/yang/blob/devel/action_plugins/yang_fetch.py) [docs](https://github.com/ansible-network/yang/blob/devel/library/yang_fetch.py).

## Plugins

The following is a list of plugins that are provided by this role.

### Lookup

* `yang_json2xml` [source](https://github.com/ansible-network/yang/blob/devel/lookup_plugins/yang_json2xml.py).
* `yang_spec` [source](https://github.com/ansible-network/yang/blob/devel/lookup_plugins/yang_spec.py).
* `yang_xml2json` [source](https://github.com/ansible-network/yang/blob/devel/lookup_plugins/yang_xml2json.py).

### netconf

* `iosxr` [source](https://github.com/ansible-network/yang/blob/devel/netconf_plugins/iosxr.py).

### Note:
```
The iosxr netconf plugin is added to this role due the existing issue in iosxr plugin
shipped with ansible package. This issue will be fixed in ansible version 2.8
and the plugin will be removed from this role after ansible 2.8 is released.
This plugin can be used by setting configuration variable in ansible configuration file

[defaults]
netconf_plugins= <yang_role_path>/netconf_plugins

or by setting enviornment variable
$ export ANSIBLE_NETCONF_PLUGINS=<yang_role_path>/netconf_plugins
```
### Filter

## Dependencies

The following is the list of dependencies on other roles this role requires.
* Platform specific provider role task to enable Netconf on remote host

## License

GPLv3

## Author Information

Ansible Network Engineering Team
