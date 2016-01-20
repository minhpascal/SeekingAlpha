#encoding=utf-8
'''
Created on Jan 20, 2016

@author: vitheano
'''
import pandas as pd
import MySQLdb



class PyMFFApiMysql(object):    
    """Summary of class here.
    
    Attributes:
        MysqlConfig: a config for Mysql Connetion Init.
        
    """
    def __init__(self,PyMFFApiMysqlConfig):
        self.MysqlConfig = PyMFFApiMysqlConfig
        
    
    def MysqlOnRspConnected(self):
        """Connect to Mysql """
        
        try:
            self.conn = MySQLdb.connect(host = self.MysqlConfig['Host'],
                                        user = self.MysqlConfig['User'], 
                                        passwd = self.MysqlConfig['Passwd'], 
                                        db = self.MysqlConfig['Database'], 
                                        port = self.MysqlConfig['Port'],
                                        charset = 'utf8')
            print "connect to Mysql succeed !"
        except:
            print "can't connect to Mysql ! "
        
    def MysqlOnRspQuery(self, Query):
        """MysqlOnRspQuery.
        
        
        Args:
            Query: a sql statement.
            
        Return:
            pandas.dataframe.
     
        """  
        
        
        SqlQueryDf = pd.read_sql(Query,self.conn)
           
      
        return SqlQueryDf