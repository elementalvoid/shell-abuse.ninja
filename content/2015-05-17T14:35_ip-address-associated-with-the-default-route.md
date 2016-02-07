Title: IP address associated with the default route
Category: Linux
Tags: hack, osx, linux, networking, ifconfig
Summary: Find the IP associated with the default route on Linux and Mac OSX.

Need a way to determine the IP address which would be used for outbound communication without actually making any outbound connections? Here's one method.

Tested on Debian, CoreOS, CentOS, and OSX Yosemite.
```bash
ifconfig $(
  { route get 4.2.2.2 || route -n; } 2>/dev/null | \
    awk '/UG/ {print $8}; /interface:/ {print $2}' | head -n 1
) | awk '/inet / {print $2}' | sed -e 's/addr://'
```
