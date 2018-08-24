# Test Guide

The tests in yang are role based where the entry point is `tests/test.yml`.
The tests for `yang_json2xml` and `yang_spec` are run against `localhost` and
test for `yang_fetch` run against a virtual network appliance instance running
in zuul CI.

* Tested agianst:
1) vqfx junos 17.4 version.

Note: Work is in progress to add testing against more network appliances.

## How to run tests locally

```
cd tests/
ansible-playbook -i inventory test.yml
```

## Role Structure

```
yang
├── action_plugins
│   ├── yang_fetch.py
├── defaults
│   └── main.yml
├── includes
│   └── netconf.yml
├── library
│   └── yang_fetch.py
├── lookup_plugins
│   ├── yang_json2xml.py
│   ├── yang_spec.py
├── meta
│   ├── configure_options.yml
│   ├── fetch_options.yml
│   ├── main.yml
│   └── spec_options.yml
├── tasks
│   ├── configure.yml
│   ├── fetch.yml
│   ├── main.yml
│   └── spec.yml
├── tests
│   ├── ansible.cfg
│   ├── fixtures
│   │   └── files
│   ├── inventory
│   ├── test.yml
│   ├── yang_fetch
│   │   ├── test.yml
│   │   └── yang_fetch
│   │       ├── defaults
│   │       │   └── main.yml
│   │       └── tasks
│   │           ├── basic.yml
│   │           └── main.yml
│   ├── yang_json2xml
│   │   ├── test.yml
│   │   └── yang_json2xml
│   │       ├── defaults
│   │       │   └── main.yml
│   │       ├── files
│   │       │   └── config
│   │       └── tasks
│   │           ├── basic.yml
│   │           └── main.yml
│   └── yang_spec
│       ├── test.yml
│       └── yang_spec
│           ├── defaults
│           │   └── main.yml
│           └── tasks
│               ├── basic.yml
│               └── main.yml
```

If you add any new Role for test, make sure to add the `test.yml` file to import that role
and import the file in the top test enrty file that is `tests/test.yml` file:

```yaml

- import_playbook: yang_json2xml/test.yml
- import_playbook: yang_spec/test.yml
- import_playbook: yang_fetch/test.yml
- import_playbook: $role_name/test.yml
```

If you are adding new plugins/modules and the test requires fixtures add them to `tests/fixture` folder.
