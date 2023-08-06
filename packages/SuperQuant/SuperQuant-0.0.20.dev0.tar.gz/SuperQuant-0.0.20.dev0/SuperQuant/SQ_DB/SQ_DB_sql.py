#coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Junfeng Li/SuperQuant
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
SuperQuant

SuperQuant Financial Strategy Framework

by Junfeng Li

2019/02/06
"""

import pandas as pd
import numpy as np
import pymssql

class SQ_sql():
    def __init__(self,
                 server=None,
                 port=None,
                 user=None,
                 password=None,
                 database=None
                 ):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    def connect(self):
        self.connection = pymssql.connect(server=self.server,
                                           port=self.port,
                                           user=self.user,
                                           password=self.password,
                                           database=self.database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def execute(self,sql_cmd=None,types='DataFrame'):
    # TODO(617644591@qq.com): 增加需要其他数据格式的情况.

        self.connect()
        if types == 'DataFrame':
            result = pd.read_sql(sql_cmd, self.connection)
        self.close()
        return result
