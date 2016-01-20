#encoding=utf-8
'''
Created on Jan 20, 2016

@author: vitheano
'''
import pandas as pd
import pymssql

class PyMFFApiMssql(object):
    """Summary of class here.

    Attributes:
        MssqlConfig: a config for Mssql Connetion Init.

    """

    def __init__(self, PyMFFApiMssqlConfig):
        self.MssqlConfig = PyMFFApiMssqlConfig

    def MssqlOnRspConnected(self):
        """Connect to Mssql. """


        self.conn = pymssql.connect(host = self.MssqlConfig['Host'],
                                    user = self.MssqlConfig['User'],
                                    password = self.MssqlConfig['Passwd'],
                                    database = self.MssqlConfig['Database'],
                                    port = self.MssqlConfig['Port'],
                                    charset = 'utf8')
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"can't connect to SqlServer ! ")

        else:
            print "connect to SqlServer succeed !"
            return cur


    def MssqlOnRspQuery(self, Query):
        """MysqlOnRspQuery.


        Args:
            Query: a sql statement.

        Return:
            pandas.dataframe.

        """
        

        SqlQueryDf = pd.read_sql(Query, self.conn)

        return SqlQueryDf
