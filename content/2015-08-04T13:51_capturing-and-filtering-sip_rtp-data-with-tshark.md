Title: Capturing and filtering SIP/RTP data with tshark
Category: Networking
Tags: wireshark, tshark, SIP, VoIP, networking
Author: Matt Klich - Chief Abuser
Summary: Create a ring buffer of packet captures on a VoIP/SIP server.

When filing issues with my SIP trunk provider they usually want some sort of call record to help track/troubleshoot the issue. In my case I don't have any eavesdropping concerns as all the calls are with family members. So, I use tshark to grab a ring buffer of RTP/SIP data as follows:

```language-bash
# ensure that the dumpcap binary has the proper Linux capabilities
/sbin/setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip'

# Grab SIP and related RTP packets and store them in a ring buffer
cap_dir='/var/cache/sip-dump'
cap_file=${cap_dir}/sip-rtp.pcap
cap_files=50
cap_size=51200

tshark \
 -i eth0 \
 -o 'rtp.heuristic_rtp: TRUE' \
 -w ${cap_file} \
 -b filesize:${cap_size} \ # Ring
 -b files:${cap_files} \   # Buffer
 '(udp port 5080) or (udp port 5060) or (udp[1] & 1 != 1 && udp[3] & 1 != 1 && udp[8] & 0x80 == 0x80 && length < 250)' \
 2>/dev/null &
```
The filter comes straight from the Freeswitch wiki page on [packet capturing](https://freeswitch.org/confluence/display/FREESWITCH/Packet+Capture#PacketCapture-tsharkakatethereal).

Of course all of that is wrapped up in a service script that starts/stops the capture and performs tool installation and cron-based cleanup.

Since this creates multiple reasonably sized capture files I generally need to merge some in order to filter on the correct time range:
```language-bash
# create a single file for all of 20150804
mergecap -w all.pcapng sip-rtp_*_20150804*.pcap
```

To build a list of all SIP BYE messages:
```language-bash
tshark \
 -n \ # Disable network object name resolution
 -N nN \ # Turn on name resolving only for network address resolution using external resolvers (e.g., DNS)
 -W n \ # save host name resolution records along with captured packets.
 -Y 'sip.Method == "BYE"' \ # display filter - only show SIP BYEs
 -t ad \ # timestamp format: absolute with date
 -T fields \ # Output format (print fields given with '-e')
 -E header=y \ # print headers
 -e frame.number \ # Field: Ethernet frame number
 -e frame.time \ # Field: Ethernet frame timestamp
 -e ip.src_host \ # Field: source ip
 -e ip.dst_host \ # Field: destination ip
 -e sip.To \ # Field: Who's being called
 -e sip.From \ # Field: Who's calling
 -e sip.Reason \ # Field: Why did we hangup
 -r all.pcapng \ # which pcap to read from
| column -t -s'   ' #make it pretty <- that's a tab character
```
*Hint:* To create an actual tab character on the shell type `Ctrl+v Ctrl+i`.
