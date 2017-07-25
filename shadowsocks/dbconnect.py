#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 clowwindy
# Copyright 2017 HoshinoTouko
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

import config
import cymysql
import logging

class DBconnect:
    conn = cymysql.connect(
        host = config.DB_HOST, 
        user = config.DB_USER, 
        passwd = config.DB_PASS, 
        db = config.DB_NAME,
        port = config.DB_PORT,
    )
    alias = config.DB_ALIAS
    table = config.DB_TABLE
    if config.S_ENABLE_CUSTOM_METHOD:
        alias.append('method')

    def __init__(self):
        pass
        
    def fetchAll(self):
        result = []
        try:
            conn = cymysql.connect(
                host = config.DB_HOST, 
                user = config.DB_USER, 
                passwd = config.DB_PASS, 
                db = config.DB_NAME,
                port = config.DB_PORT,
            )
            cur = conn.cursor()
            cur.execute('SELECT %s FROM %s' % (', '.join(DBconnect.alias), DBconnect.table))
            result = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            logging.error('Database error: %s' % str(e))
        return result

    def runSql(self, sql):
        result = []
        try:
            conn = cymysql.connect(
                host = config.DB_HOST, 
                user = config.DB_USER, 
                passwd = config.DB_PASS, 
                db = config.DB_NAME,
                port = config.DB_PORT,
            )
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error('Database error: %s' % str(e))
        return result
