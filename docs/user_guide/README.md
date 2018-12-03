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


## Get configuration and/or state data
Below is an example of how to use get configuration and/or state data from remote device

```
 - name: get configuration/state data and convert to yang json format as per rfc 7951
    include_role:
      name: ansible-network.yang
      tasks_from: get
    vars:
       yang_get_filter: <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration></interface-configuration></interface-configurations>
       ansible_network_provider: cisco_iosxr
       yang_netconf_enable_task_run: false
       yang_get_output: ""
```

## Notes

* If netconf is already enabled on network device and if you don't want to run the task that
  enables netconf if not already enabled set the role variable `yang_netconf_enable_task_run` to `false`
* Curated logs required to identify issues in intermediate steps are directed in log file.
  To enable these logs set by log_path configuration variable in ansible configuration file
  ```
  [defaults]
  log_path=<log_file_path>
  ```
  or by setting enviornment variable
  ```
  $ export ANSIBLE_LOG_PATH='<log_file_path>'
  ```
