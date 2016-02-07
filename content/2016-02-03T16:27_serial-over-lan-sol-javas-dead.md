Title: Serial Over LAN (SOL) - Java's dead!
Category: Linux
Tags: ipmi, linux, java, sol, remote console, serial over lan
Summary: I've been a sysadmin and worked with sysadmins for years but we've always used the cruddy Java applet interfaces to the remote consoles. I started a new job recently and was fed up with it. So, I went about learning how to do Serial Ove LAN (SOL) using IPMI. Turns out, its _super_ easy!

I've been a sysadmin and worked with sysadmins for years but we've always used the cruddy Java applet interfaces to the remote consoles. I started a new job recently and was fed up with it. So, I went about learning how to do Serial Ove LAN (SOL) using IPMI. Turns out, its _super_ easy!

So, I've written up some simple instructions to configure SOL on Ubuntu Trusty (14.somethingorother). One super important thing to keep in mind is that the bit rates configured at each step need to be the same.

Assumption: You're using sudo liberally or, like my favorite SA, you just drop into a root shell and stay there. Forever.

## Bios Redirection
These settings allow you to see and manipulate Bios level screens (POST, Bios settings, PXE boot, etc.).

Make sure that the BIOS has SOL enabled and set to 115.2K. In my case this was on com2. Note that com2 maps to ttyS1 in Linux.

## Grub and Linux Kernel Space Redirection
These settings allow you to see and manipulate Grub and to see kernel level boot messages.

Ensure the following are configured in `/etc/default/grub`:

```
# Enable kernel space redirection so you can see kernel boot messages.
GRUB_CMDLINE_LINUX="console=tty0 console=ttyS1,115200n8"

# Enable Grub to be seen over SOL.
GRUB_TERMINAL="serial console"

# Configures Grub's serial output
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=1 --word=8 --parity=no --stop=1"
```

Then run `update-grub`.

## Linux User Space Redirection
Once the kernel hands things over to user space we need to redirect a virtual terminal to the serial port.

Create `/etc/init/ttyS1.conf`.
```
# ttyS1 - getty
#
# This service maintains a getty on ttyS1 from the point the system is
# started until it is shut down again.

start on stopped rc RUNLEVEL=[12345]
stop on runlevel [!12345]

respawn
exec /sbin/getty -L ttyS1 115200 vt102
```

And start it: `service ttyS1 start`.

I'm not sure what this would look like for Debian. Stupid Ubuntu I’m on is using upstart.

Install and configure `ipmitool`.
```bash
apt-get install ipmitool
ipmitool sol set non-volatile-bit-rate 115.2 1
ipmitool sol set volatile-bit-rate 115.2 1
```

## What's the point if you can't use it?
On a Mac with brew.sh installed and functioning:
```bash
brew install freeipmi
# -P prompts for the password
# -e '~' sets the escape character to match SSH's
ipmiconsole -h rack2-spare-adm -u ADMIN -P -e '~'
```

##Helpful links:
- https://wiki.nikhef.nl/grid/Serial_Consoles
- https://help.ubuntu.com/community/SerialConsoleHowto
- http://www.alleft.com/sysadmin/ipmi-sol-inexpensive-remote-console/
- ftp://ftp.supermicro.com/utility/SMCIPMItool/Linux/
