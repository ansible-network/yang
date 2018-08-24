# Enable netconf on network device
* This function enables netconf on network device is not already enabled. This function
relies on the platform specific role to provide the functionality to enable netconf within
`configure_netconf` task.
* This function requires setting `ansible_network_provider` variable
to the name of the platform specific role eg. `cisco_iosxr`. This role is expected to be pre-installed
on the ansible controller node and should be accessible to yang role. Additionally you
can pass `netconf_port` variable to control the port in which netconf will be enabled, default
value of netconf port is 830.

## Notes

None
