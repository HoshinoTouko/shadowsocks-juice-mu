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
import dbconnect
import copy
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from shadowsocks import common, shell, daemon, eventloop, tcprelay, udprelay, \
    asyncdns, manager

# Test
# import struct
# from shadowsocks import cryptor

def socket_send_command(command):
    data = ''
    if config.S_DEBUG:
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
        if config.S_DEBUG:
            import traceback
            traceback.print_exc()
        logging.warn('Exception thrown when sending command: %s' % e)
    return data


def socket_get_transfer():
    transfer = {}
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli.sendto('stat: {}', (config.MANAGER_BIND_IP, config.MANAGER_BIND_PORT))
    while True:
        data, addr = cli.recvfrom(1500)
        if data == 'ok':
            break
        data = json.loads(data.replace('stat:', ''))
        transfer.update(data)
    cli.close()
    return transfer


def subprocess_callback(stack, exception):
    logging.info('Exception thrown in %s: %s' % (stack, exception))
    if config.S_DEBUG:
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
        'verbose': config.S_DEBUG,
        'firewall_mode': config.S_FIREWALL_MODE,
    }
    customMethod = config.S_ENABLE_CUSTOM_METHOD

    # Database
    dbconn = dbconnect.DBconnect()

    # Init logging
    logging.basicConfig(format=config.LOG_FORMAT,
            datefmt=config.LOG_DATE_FORMAT, stream=sys.stdout, level=config.LOG_LEVEL)
    logging.info('----------------------------------------------')
    logging.info('Shadowsocks-juice-mu Server Starting...')
    logging.info('Ver. 0.5')

    logging.info('Run sub process')
    thread.start_new_thread(manager.run, (configurations, subprocess_callback,))
    # time.sleep(1)

    # socket_send_command(
    #        'add: {"server_port": 8389, "password": "123", "method":"%s"}' % config.S_METHOD)
    
    alias = config.DB_ALIAS
    users = dbconn.fetchAll()
    activeList = []
    loopTime = config.S_LOOP_CIRCLE
    while True:
        time.sleep(loopTime)
        # Keep old users
        oldUsers = []
        for user in users:
            oldUsers.append(user)
        # Fetch all data
        users = []
        users = dbconn.fetchAll()
        
        if config.S_DEBUG and 0:
            logging.info('oldUsers----------------')
            logging.info(str(oldUsers))
            logging.info('Users----------------')
            logging.info(str(users))
        # Init some vars
        transfer = socket_get_transfer()
        if config.S_DEBUG:
            logging.info('Transfer data %s' % str(transfer))
            logging.info('----------------')

        # Check if the user's password has been changed
        if config.S_DEBUG:
            logging.info('Check pass...')
        for user in users:
            serverPort = user[0]
            newPass = user[1]
            for oldUser in oldUsers:
                if serverPort == oldUser[0]:
                    if newPass != oldUser[1]:
                        if serverPort in activeList:
                            logging.info('port %d change its pass to %s' % (serverPort, newPass))
                            socket_send_command('del: {"server_port": %d}' % serverPort)
                            activeList.remove(userverPort)
                    continue
        if config.S_DEBUG:
            logging.info('Check pass end.')
            logging.info('----------------')
        
        # Check if the user can use ss
        if config.S_DEBUG:
            logging.info('Check available...')
            logging.info('ActiveList before: %s' % str(activeList))
        for user in users:
            # logging.info(str(user))
            if (user[5]) and (user[2] + user[3] < user[4]):
                if user[0] not in activeList:
                    data = {'server_port': int(user[0]), 'password': user[1]}
                    if customMethod:
                        data['method'] = user[8]
                    if config.S_DEBUG:
                        logging.info('Add %s' % str(data))
                    socket_send_command('add: ' + str(data).replace("'", '"'))
                    activeList.append(user[0])
            else:
                if user[0] in activeList:
                    socket_send_command('remove: {"server_port": %d}' % user[0])
                    if config.S_DEBUG:
                        logging.info('Remove port at %s' % user[0])
                    activeList.remove(user[0])
        if config.S_DEBUG:
            logging.info('ActiveList after: %s' % str(activeList))
            logging.info('Check available end...')
            logging.info('----------------')
        

        # Update traffic
        updateList = []
        if config.S_DEBUG:
            logging.info('Stat transfer...')
        for port, traffic in transfer.items():
            port = int(port)
            for user in users:
                if user[0] == port:
                    if config.S_DEBUG:
                        logging.info('Update user port at: %d' % port)
                    updateList.append({'port': port, 'u': user[2],'d': user[3] + traffic})
                    break
        if config.S_DEBUG:
            logging.info('Update list: %s' % str(updateList))
            logging.info('Stat transfer end...')

        # Update to Database
        sqlList = []
        if config.S_DEBUG:
            logging.info('Update to database...')
        for i in updateList:
            sql = 'UPDATE %s SET %s=%d, %s=%d, %s=%s WHERE %s=%d;' % (
                config.DB_TABLE, 
                alias[2], int(i['u']), 
                alias[3], int(i['d']), 
                alias[6], str(int(time.time())),
                alias[0], int(i['port'])
            )
            sqlList.append(sql)
        if len(sqlList):
            result = dbconn.runSql(' '.join(sqlList))
            if config.S_DEBUG:
                logging.info('SQL: %s, result: %s' % (';'.join(sqlList), result))
        else:
            if config.S_DEBUG:
                logging.info('Nothing to update')
        if config.S_DEBUG:
            logging.info('Update to database end.')
            logging.info('----------------------')
        
if __name__ == '__main__':
    main()
