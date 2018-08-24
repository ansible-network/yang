# Using yang role
The yang role provides following functionality
1) Fetch yang model's from network device [refer](https://github.com/ansible-network/yang/tree/devel/docs/tasks/fetch.md) (optional).
2) Validate the input json configuration against a yang model and configure it on network device [refer](https://github.com/ansible-network/yang/tree/devel/docs/tasks/configure.md).
3) Generate spec files that is json and xml configuration skeleton's and yang tree representation to aide in creating input json configuration [refer](https://github.com/ansible-network/yang/tree/devel/docs/tasks/spec.md).


## Fetch and configure

Below is an example of how to use fetch yang model the configure network device

```
- hosts: iosxr
  connection: netconf

  tasks:
  - name: include yang role
    include_role:
      name: ansible-network.yang
      tasks_from: configure
    vars:
       yang_config_file: config/interfaces.json
       yang_model_name: openconfig-interfaces
       ansible_network_provider: cisco_iosxr
```


## Generate spec files
Below is an example of how to use generate yang spec files

```
  - name: include yang role
    include_role:
      name: ansible-network.yang
      tasks_from: spec
    loop:
       - openconfig-interfaces
       - openconfig-bgp
    loop_control:
      loop_var: yang_model_name
    vars:
      ansible_network_provider: cisco_iosxr
```

## Notes

None
