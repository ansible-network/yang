# Get configuration and state data from the remote network device
The `get` function used `netconf_get` module to fetch configuration and/or
state data from target device over netconf transport. The received xml rpc response
is validated against the respective yang models that pre-fetched from device
and stored on local disk. After the validation is succeful it converts xml data into
json format that adheres to yang json standard defined in [RFC 7951][https://tools.ietf.org/html/rfc7951].


## Get data from the device
* `yang_datastore_source` identifies the datastore from which configuration data should be fetched.
  If this option is not set it will fetch both configuration and state data.

* `yang_get_filter` varaible idenifies the subtree filter that is the subset of data to be fetched from
  remote device. If this option is not provided entire configuration and/or state data will be fetched.
  For some of the Netconf server implementation this is a mandatory option. Please vendor netconf releated
  documents for more details

* `yang_datastore_lock` variable is a boolean flag to control if datastore should be locked or not
  before issuing `get` or `get_config` operation.

* `yang_modules_file_path` variable that points to the yang modules
  stored on local disk that are pre-fetched from remote host or published by the vendor.
  Note:
  ```
  All the depedent yang modules for particular rpc-reply should be present in this folder else
  xml to json conversion won't be successful.
  ```


* `yang_search_path` variable points to the dependent yang modules stored on the local disk.
  These modules are typically imported from the main yang modules, if the imported yang module
  is not present in this path it will result in error.

* `yang_keep_tmp_files` variable is a boolean flag that controls if the intermediate temporary files
  generated on local disk should be removed or not. This option can be useful to debug issues.

* `yang_netconf_enable_task_run` varaible is boolean flag to control running of netconf enable task.
  This can be disabled by setting it to `false` is netconf is already enable on remote host

Below is an example of how to use the `get` function.
```
- hosts: iosxr
  connection: netconf

  tasks:
  - name: fetch yang file from remote device
    include_role:
      name: ansible-network.yang
      tasks_from: fetch
    loop:
       - Cisco-IOS-XR-ifmgr-cfg
       - Cisco-IOS-XR-drivers-media-eth-cfg
       - Cisco-IOS-XR-ipv4-io-cfg
       - Cisco-IOS-XR-ipv4-io-cfg
       - Cisco-IOS-XR-infra-rsi-cfg
       - Cisco-IOS-XR-l2-eth-infra-cfg
    loop_control:
      loop_var: yang_model_name
    vars:
      ansible_network_provider: cisco_iosxr
      yang_dir: "{{ playbook_dir }}/cisco_iosxr_yang"


  - name: get configuration/state data and convert to yang json format as per rfc 7951
    include_role:
      name: ansible-network.yang
      tasks_from: get
    vars:
       yang_get_filter: <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration></interface-configuration></interface-configurations>
       ansible_network_provider: cisco_iosxr
       yang_netconf_enable_task_run: false
       yang_datastore_source: running
       yang_modules_file_path: "{{ playbook_dir }}/cisco_iosxr_yang/*.yang"
       yang_search_path: "{{ playbook_dir }}/cisco_iosxr_yang"
       yang_keep_tmp_files: true
       yang_get_output: ""
```

In the above task the output json format is stored in `yang_get_output` variable.

Example output:
```
ok: [iosxr02] => {
    "ansible_facts": {
        "yang_get_output": {
            "Cisco-IOS-XR-ifmgr-cfg:interface-configurations": {
                "interface-configuration": [
                    {
                        "Cisco-IOS-XR-drivers-media-eth-cfg:ethernet": {
                            "duplex": "full",
                            "speed": "100"
                        },
                        "active": "pre",
                        "description": "test-interface-3",
                        "interface-name": "GigabitEthernet0/0/0/3",
                        "mtus": {
                            "mtu": [
                                {
                                    "mtu": 256,
                                    "owner": "GigabitEthernet"
                                }
                            ]
                        }
                    }
                    {
                        "Cisco-IOS-XR-infra-rsi-cfg:vrf": "management",
                        "Cisco-IOS-XR-ipv4-io-cfg:ipv4-network": {
                            "addresses": {
                                "primary": {
                                    "address": "10.8.38.70",
                                    "netmask": "255.255.255.0"
                                }
                            }
                        },
                        "active": "act",
                        "interface-name": "MgmtEth0/0/CPU0/0"
                    }
                ]
            }
        }
    },
    "changed": false
}
```

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
