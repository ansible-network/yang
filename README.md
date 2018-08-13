# yang

This role provides the foundation for building network roles by providing
modules and plugins that are common to all Ansible Network roles. The role
is platform-agnostic - all of the artifacts in this role can be used on any
Ansible-managed network platform.

To install this role: `ansible-galaxy install ansible-network.yang`

To see the version of this role you currently have installed: `ansible-galaxy list | grep yang`

To ensure you have the latest version available: `ansible-galaxy install -f ansible-network.yang`

To use this role, follow the [User Guide](https://github.com/ansible-network/yang/blob/devel/docs/user_guide/README.md).

To find other roles maintained by the Ansible Network team, see our [Galaxy Profile](https://galaxy.ansible.com/ansible-network/). 

Any open bugs and/or feature requests are tracked in [GitHub issues](https://github.com/ansible-network/yang/issues).

Interested in contributing to this role? Check out [CONTRIBUTING](https://github.com/ansible-network/yang/blob/devel/CONTRIBUTING.md) before submitting a pull request.

## Documentation

* User guide:
    - [How to use](https://github.com/ansible-network/yang/blob/devel/docs/user_guide/README.md)
* Development guide: [How to test](https://github.com/ansible-network/yang/blob/devel/docs/tests/test_guide.md)

For module documentation see the [modules](#modules) section below.

## Requirements

* Ansible 2.6.0 (or higher)

## Tasks

The following are the available tasks provided by this role for use in
playbooks.

* `configure` [source](https://github.com/ansible-network/yang/blob/devel/tasks/configure.yaml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/tasks/configure.md).
* `spec` [source](https://github.com/ansible-network/yang/blob/devel/tasks/spec.yaml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/tasks/spec.md).
* `fetch` [source](https://github.com/ansible-network/yang/blob/devel/includes/fetch.yaml) [docs](https://github.com/ansible-network/yang/blob/devel/docs/includes/fetch.md).
## Variables

The following are the list of variables this role accepts

* yang_config_file:
* yang_model_name:
* yang_dir:
* yang_search_path:
* yang_doctype:
* yang_annotations:


## Modules

The following is a list of modules that are provided by this role, which include documentation & examples:

* `yang_fetch` [source](https://github.com/ansible-network/yang/blob/devel/action_plugins/yang_fetch.py) [docs](https://github.com/ansible-network/yang/blob/devel/library/yang_fetch.py).

## Plugins

The following is a list of plugins that are provided by this role.

### Lookup

* `yang_json2xml` [[source]](https://github.com/ansible-network/yang/blob/devel/lookup_plugins/yang_json2xml.py) [docs](https://github.com/ansible-network/yang/blob/devel/docs/lookup_plugins/yang_json2xml.md).
* `yang_spec` [[source]](https://github.com/ansible-network/yang/blob/devel/lookup_plugins/yang_spec.py) [docs](https://github.com/ansible-network/yang/blob/devel/docs/lookup_plugins/yang_spec.md).

### Filter

## Dependencies

The following is the list of dependencies on other roles this role requires.

None

## License

GPLv3

## Author Information

Ansible Network Engineering Team
