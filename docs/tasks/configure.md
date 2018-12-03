# Configure the remote network device
The `configure` function reads in the input json configuration store in a file on
a disk, validates it against the yang file which is either fetched from network device
or stored locall on disk. If the validation is successful it converts the json configuration
to xml format and sends it over netconf transport to configure the device.

## Fetch yang model from the device
* The yang schema name is defined by variable [yang_model_name](https://github.com/ansible-network/yang/blob/devel/meta/configure_options.yml)
(mentioned without any extension) eg. `openconfig-interfaces`.
* If the network device support fetching yang schemas as run time you can set
`yang_fetch_schema` to `True` (default is True) in the task. This ensure the main yang
model and it's dependent one are fetched from remote network device and stored
locally in a path defined by [yang_dir](https://github.com/ansible-network/yang/blob/devel/meta/fetch_options.yml),
by default it is stored in `~/.ansible/yang/fetch` directory.
* If the device doesn't support fetching yang schema you can checkout the yang schema's on local disk
and set `yang_dir` variable to point to this path, also ensure all the dependent yang files required
bu the main yang schema are present is same directory path, also set `yang_fetch_schema` to `False`
* The path to main yang file is derived by combining `yang_dir` and `yang_model_name`. If the yang file
name doesn't match with the `yang_model_name` you can set `yang_file` variable to the absolute yang file path
and `yang_search_path` to set the colon separated search path directory having dependent yang schema files.

Below is an example of how to use the `configure` function.

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


## How to configure the device
This function uses `netconf_config` module to configure the remote network device.
Refer [netconf_config](https://docs.ansible.com/ansible/latest/modules/netconf_config_module.html) module for the options that can be used for configuration.

## Arguments

For arguments (options) that can be passed to this function [refer](https://github.com/ansible-network/yang/blob/devel/meta/configure_options.yml)

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
