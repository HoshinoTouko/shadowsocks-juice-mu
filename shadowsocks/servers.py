#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 clowwindy
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import os
import logging
import signal
import socket
import config
import thread
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from shadowsocks import shell, daemon, eventloop, tcprelay, udprelay, \
    asyncdns, manager


def socket_send_command(command):
    data = ''
    logging.info('Socket send: %s' % command)
    try:
        cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli.settimeout(2)
        cli.sendto(command, ('%s' % config.MANAGER_BIND_IP, config.MANAGER_BIND_PORT))
        data, addr = cli.recvfrom(1500)
        cli.close()
        # TODO: bad way solve timed out
        time.sleep(0.05)
    except Exception as e:
        if config.SS_VERBOSE:
            import traceback
            traceback.print_exc()
        logging.warn('Exception thrown when sending command: %s' % e)
    return data


def subprocess_callback(stack, exception):
    logging.info('Exception thrown in %s: %s' % (stack, exception))
    if config.SS_VERBOSE:
        traceback.print_exc()


def main():
    configurations = {
        'server': config.S_BIND_IP,
        'local_port': config.S_BIND_PORT,
        'port_password': {},
        'method': config.S_METHOD,
        'manager_address': '%s:%s' % (config.MANAGER_BIND_IP, config.MANAGER_BIND_PORT),
        'timeout': config.S_TIMEOUT,
        'fast_open': config.S_FASTOPEN,
        'debug': config.S_DEBUG,
        'one_time_auth': config.S_OTA,
    }

    # Init logging
    logging.basicConfig(format=config.LOG_FORMAT,
            datefmt=config.LOG_DATE_FORMAT, stream=sys.stdout, level=config.LOG_LEVEL)
    logging.info('----------------------------------------------')
    logging.info('Shadowsocks-juice-mu Server Starting...')
    logging.info('Ver. 0.1')

    logging.info('Run sub process')
    thread.start_new_thread(manager.run, (configurations, subprocess_callback,))
    time.sleep(5)

    socket_send_command(
            'add: {"server_port": 8389, "password": "123", "method":"%s"}' % config.S_METHOD)
    
    while True:
        time.sleep(50)

if __name__ == '__main__':
    main()
