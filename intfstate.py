import jsonrpclib
import json

'''
Script to automate bringing up/down interfaces based on the if-state of a
different interface.

Example Config:
---
event-handler Intf-Eth1
   trigger on-intf Ethernet1 operstatus
   action bash python /mnt/flash/intfstate.py
   delay 1
---

Requirements:
 * This script stored on /mnt/flash/intfstate.py on the switch.
 * The event-handler above configured to watch the intf-state of the parent Interface.
 * The parentIntf and childIntfs variables defined to match the correct parent/child intf combination.
 * Uses eAPI's unix-socket protocol to create an api call on-box. Activate with:
---
management api http-commands
   protocol unix-socket
---
'''

parentIntf = 'Ethernet1'
childIntfs = ['Ethernet2', 'Ethernet3']

def main():
    #SESSION SETUP FOR eAPI TO DEVICE, uses unix socket
    url = "unix:/var/run/command-api.sock"
    ss = jsonrpclib.Server(url)

    #CONNECT TO DEVICE
    response = ss.runCmds( 1, [ 'enable', 'show interfaces '+parentIntf+' status' ] )
    intfState = response[1]['interfaceStatuses'][parentIntf]['lineProtocolStatus']
    if intfState == 'up':
        for intf in childIntfs:
            response = ss.runCmds (1, [ 'enable', 'configure', 'interface '+intf, 'no shutdown'])
            print 'bringing interface '+intf+' online'
    elif intfState == 'down':
        for intf in childIntfs:
            response = ss.runCmds (1, [ 'enable', 'configure', 'interface '+intf, 'shutdown'])
            print 'shutting down interface '+intf+'.'

if __name__ == "__main__":
    main()
