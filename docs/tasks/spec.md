# Generate spec for given yang model
* This function generates skeleton json and xml configuration which can be referred while generating
the json configuration which is the input to [configure](https://github.com/ansible-network/yang/blob/devel/docs/tasks/configure.md) function.
This function also generated a tree representation of yang model based on RFC 8340.
* This function takes `yang_model_name` as the input and it fetches the yang model and it's
dependent files from network device and stores it in a location on disk defined by variable [yang_dir](https://github.com/ansible-network/yang/blob/devel/meta/spec_options.yml),
by default it is stored in `~/.ansible/yang/spec` directory.
* If the network device doesn't support fetching of yang schema you can set `yang_fetch_schema` to `false` to disabling
fetching schema and set the variable `yang_dir` to point to the path where the main yang model and it's depedent files are stored.
* If the yang file name doesn't match with the `yang_model_name` you can set `yang_file` variable to the absolute yang file path
and `yang_search_path` to set the colon separated search path directory having dependent yang schema files.
* The json and xml configuration and yang tree representation is stored in file on disk in a directory
defined by vairbale `yang_spec_dir`.

Below is an example of how to use the `spec` function.

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


## Arguments

For arguments (options) that can be passed to this function [refer](https://github.com/ansible-network/yang/blob/devel/meta/spec_options.yml)

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
