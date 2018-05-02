#! /usr/bin/env python2

"""
Send a downlink message to a specific node.

If a gateway is not specified, Conductor will route the message automatically.
"""

import argparse
import logging
import itertools
import struct
from getpass import getpass
import requests

import conductor

try:
    requests.packages.urllib3.disable_warnings()
except AttributeError:
    pass

LOG = logging.getLogger(__name__)

def send_message_checked(account, message, node_addr, gateway_addr=None, acked=False):
    """
    Sends a command through conductor, and waits for Conductor to indicate the message
    was successfully sent.
    """
    if node_addr == 'broadcast':
        LOG.debug("Sending broadcast message")
        gateway = account.get_gateway(gateway_addr)
        message = gateway.send_broadcast(message)
    else:
        LOG.debug("Sending unicast message")
        module = account.get_module(node_addr)
        message = module.send_message(message, gateway_addr, acked)

    LOG.info("Command generated with ID %s", message)

    LOG.debug("Polling status for %s", message)
    message.wait_for_success()
    LOG.info("Command %s success", message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('username', help='The username to authenticate to Conductor')
    parser.add_argument('--password', '-p', help='The Conductor account password. '
                        'This is optional: if omitted, the script will prompt securely for '
                        'the password.')
    parser.add_argument('node_addr', help='The 36-bit node id, in hex form, or `broadcast` to '
                        'send to all nodes with a gateway')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--payload', help='The payload to send, in hex', type=bytearray.fromhex)
    group.add_argument('--counter', action='store_true',
                       help='Continually send a 4-byte counter value')
    parser.add_argument('--gateway',
                        help='Specify the gateway through with the message will be routed.')
    parser.add_argument('--ack', help='request an ACK from the node', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    LOG.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    account = conductor.ConductorAccount(args.username, args.password or getpass())

    if args.counter:
        for counter in itertools.count():
            message = struct.pack('>L', counter)
            send_message_checked(account, message, args.node_addr, args.gateway, args.ack)
    else:
        send_message_checked(account, args.payload, args.node_addr, args.gateway, args.ack)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    main()
