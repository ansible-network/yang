# Fetch yang schema from network device
If the network device supports fetching yang schema this task can be used
to fetch the main and it's dependent yang schema's and store it in path on disk
defined by [yang_dir](https://github.com/ansible-network/yang/blob/devel/meta/fetch_options.yml) variable,
by default it is stored in `~/.ansible/yang/fetch` directory.
This function is currently only supported over netconf connection and uses the platform specific role
`configure_netconf` task.

Below is an example of how to use the `fetch` function.

```
- hosts: iosxr
  connection: netconf
  gather_facts: no
  tasks:
  - name: include yang role
    include_role:
      name: ansible-network.yang
      tasks_from: fetch
    loop:
       - openconfig-interfaces
       - openconfig-bgp
    loop_control:
      loop_var: yang_model_name
    vars:
      ansible_network_provider: cisco_iosxr
```


## Arguments

For arguments (options) that can be passed to this function [refer](https://github.com/ansible-network/yang/blob/devel/meta/fetch_options.yml)

## Notes

* If netconf is already enabled on network device and if you don't want to run the task that
enables netconf if not already enabled set the role variable `yang_netconf_enable_task_run` to `false`
