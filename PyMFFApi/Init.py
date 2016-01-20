#encoding=utf-8
'''
Created on Jan 20, 2016

@author: vitheano
'''
#from SeekingAlpha import DataBase
from SeekingAlpha.DataBase.Mssql import PyMFFApiMssql
from SeekingAlpha.DataBase.Mysql import PyMFFApiMysql
from SeekingAlpha.DataBase.config import *
from SeekingAlpha.PyMFFApi.DataStruct import PyMFFApiDataStruct

import numpy as np
import pandas as pd



class PyMFFApiInit(object):   
    """Summary of PyMFFApiInit here.
    
    This is for MultiFactorModel Initing.
    
    Arrtibutes:
        PyMFFApiDataStruct: InitClassObject
        PyMFFApiMysql: PyMFFApiMysql object.
        PyMFFApiMssql: PyMFFApiMssql object.
        PyMFFApiFactorsFromDb: Factors is to use for backtest.
    
    """
    
    
    
    def __init__(self):

        self.PyMFFApiDataStruct = PyMFFApiDataStruct()
        self.PyMFFApiMysql = PyMFFApiMysql(PyMFFApiMysqlConfig)
        self.PyMFFApiMssql = PyMFFApiMssql(PyMFFApiMssqlConfig) 
        self.PyMFFApiFactorIndex = PyMFFApiMysql(PyMFFApiFactorConfig) 
        
        self.PyMFFApiMysql.MysqlOnRspConnected()
        self.PyMFFApiMssql.MssqlOnRspConnected()
        self.PyMFFApiFactorIndex.MysqlOnRspConnected()
        
        self.PyMFFApiFactorsFromDb = self.FetchFactorIndex()
    
    def FetchFactorIndex(self):
        
        
        FetchFactorIndex = self.PyMFFApiFactorIndex.MysqlOnRspQuery(
                           "select factorname as FactorName, "
                           "Dbfactorname as DbFactorName," 
                           "DatabaseName as DataBaseF," 
                           "TableName as TableF," 
                           "Classification from factorindex")
        FetchFactorIndex.columns = ['FactorName', 'DbFactorName', 'DataBase','Table','Classification']
    
    
        return FetchFactorIndex
    
    
    def CreateMysqlApi(self):
        """Create Mysql Api.
        
        Return:
             MysqlApi Class which is connected.
        
        """ 
                 
        return self.PyMFFApiMysql
     
    def CreateMssqlApi(self):
        """Create Mssql Api.
        
        Return:
            SqlServerApi Class which is connected.
        
        """
        
        return self.PyMFFApiMssql 
     
     
    def FetchTradeDays(self, BeginDate, EndDate):       
        """Fetch TradeDays from SH.
        
        Args:
            BeginDate: '20100101'
            EndDate: '20110101'
        
        Return:
            TradeDaysDf: pandas.DataFrame
       
        """ 
        
        
        TradeDaysDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                        "select  TRADE_DAYS as TradeDays from AShareCalendar where S_INFO_EXCHMARKET='SSE' and (TRADE_DAYS>=%s and TRADE_DAYS<=%s)"
                        %(BeginDate, EndDate))
        TradeDaysDf = TradeDaysDf.sort_values(by = 'TradeDays', ascending = True)
        TradeDaysDf.index = range(len(TradeDaysDf))
        self.PyMFFApiDataStruct.TradeDaysDf = TradeDaysDf
        return TradeDaysDf
    
    
    def FetchReportDays(self):
         
        """
        return reportdate 
         
         
        """
        pass
    
    
    def FetchPositionAdjustmentDays(self, TradeDaysDf, Cycle):
        """Fetch PositionAdjustmentDate.
        
        Args:
            TradeDayDf: input must be pandas.DataFrame(index,columns=['TradeDays'])
        
        Return:
            PositionAdjustmentDaysDf: pandas.DataFrame
        
        
        """
        PositionAdjustmentDaysDf = pd.DataFrame(columns=['TradeDays'])
       
            
        if Cycle == "month":
            TradeDaysDf['year'] = TradeDaysDf['TradeDays'].apply(lambda x: x[:4] )
            TradeDaysDf['month'] = TradeDaysDf['TradeDays'].apply(lambda x: x[4:6])
            TradeDaysDf['day'] = TradeDaysDf['TradeDays'].apply(lambda x: x[6:])
            for name,df in TradeDaysDf.groupby(['year', 'month']):
                iterm = pd.Series({'TradeDays':name[0]+name[1]+df['day'].iloc[-1]})
            
                PositionAdjustmentDaysDf = PositionAdjustmentDaysDf.append(iterm, ignore_index = True)  
            
        else:
            print "must offer Position AjustmentDate"   
            
        PositionAdjustmentDaysDf = PositionAdjustmentDaysDf.sort_values(by = 'TradeDays', ascending = True)  
        PositionAdjustmentDaysDf.index = range(len(PositionAdjustmentDaysDf)) 
        self.PyMFFApiDataStruct.PositionAdjustmentDaysDf = PositionAdjustmentDaysDf
        
            
        return PositionAdjustmentDaysDf
    
    
    def FetchHs300Index(self, BeginT, EndT):
        """Fetch Hs300 index
        
        
        Args:
            BeginT: '20110101'
            EndT: '20110202'
        
        Return:
            Hs300IndexDf:pandas.Dataframe
        
        """
        
        
        Hs300IndexDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                       "select s_info_windcode as WindStockCode, trade_dt as TradeDays, s_dq_close as close, pre_close as preclose from HS300IEODPrices where trade_dt>=%s and trade_dt<=%s"%(BeginT, EndT))   
        Hs300IndexDf = Hs300IndexDf.sort_values(by = 'TradeDays', ascending = True)
        
        Hs300IndexDf.index = range(len(Hs300IndexDf))
        self.PyMFFApiDataStruct.Hs300IndexDf = Hs300IndexDf
        return Hs300IndexDf

    def FetchIFIndex(self, BeginT, EndT):
        """Fetch IF index
        
        
        Args:
            BeginT: '20110101'
            EndT: '20110202'
        
        Return:
            Hs300IndexDf:pandas.Dataframe
        
        """
        
        
        HsIFIndexDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                       "select trade_dt as TradeDays, s_dq_settle as settle, s_dq_presettle as settlepre from CIndexFuturesEODPrices where trade_dt>=%s and trade_dt<=%s and fs_info_type = 1"%(BeginT, EndT))   
        HsIFIndexDf = HsIFIndexDf.sort_values(by = 'TradeDays', ascending = True)
        
        HsIFIndexDf.index = range(len(HsIFIndexDf))
        self.PyMFFApiDataStruct.HsIFIndexDf = HsIFIndexDf
        return HsIFIndexDf




    
    
    
    
     
    def FetchBasicStockPoolByDate(self, Date):
        """Get Basic StockPool on the whole market on Date.
        
        Args:
            Date: '20100105'
        Return:
            pandas.Dataframe.stockpool
        
        """ 
        
        
        StockPoolDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                     "select s_info_windcode as WindStockCode from AShareDescription where s_info_listdate <=%s and (%s<=s_info_delistdate or s_info_delistdate is Null)"
                     %(Date, Date))
        
        IndustryGroupDf = self.FetchIndustryGroupByDate(self.PyMFFApiDataStruct.IndustryGroupDf, Date)
        
        StockPoolDf = StockPoolDf.merge(IndustryGroupDf, on = 'WindStockCode', how = 'left')
        
        
        return StockPoolDf
    
    
    def FetchBasicStockPoolByPeriod(self, BeginT, EndT):
        """Get Basic StockPool on the whole market on Date.
        
        Args:
            BeginT: '20100105'
            EndT: '201101015'
            
            
        Return:
            pandas.Dataframe
        
        """
        IndustryGroupDf = self.PyMFFApiDataStruct.IndustryGroupDf
        StockPoolPositionAdjustmentDf = pd.DataFrame(columns = ['WindStockCode', 'TradeDays'])
        StockPoolDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                      "select s_info_windcode as WindStockCode, s_info_listdate as startDate, s_info_delistdate as endDate from AShareDescription")
        StockPoolDf['endDatenan'] = StockPoolDf['endDate'].apply(lambda x: 1 if x is None else 0)
        
        for i in self.PyMFFApiDataStruct.PositionAdjustmentDaysDf['TradeDays']:
            df = StockPoolDf[(StockPoolDf['startDate'] <= i) & ((StockPoolDf['endDatenan'] == 1) | (StockPoolDf['endDate']>=i))].copy()
            df['TradeDays'] = str(i)
            IndustryGroupByDate = self.FetchIndustryGroupByDate(IndustryGroupDf, i)
            df = df.merge(IndustryGroupByDate, on = ['WindStockCode','TradeDays'], how = 'left')

            StockPoolPositionAdjustmentDf = StockPoolPositionAdjustmentDf.append(df, ignore_index = True)
        StockPoolPositonAdjustmendDf = StockPoolPositionAdjustmentDf.sort_values(by = 'TradeDays', ascending = True)
        StockPoolPositonAdjustmendDf.index = range(len(StockPoolPositonAdjustmendDf))
        
        self.PyMFFApiDataStruct.StockPoolPositionAdjustmentDf = StockPoolPositionAdjustmentDf
        return StockPoolPositionAdjustmentDf
     
    def FetchSTStockTable(self):
        """Get st stock table
        
        Return:pandas.DataFrame
        
        
        
        """
        
        STStockDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                   "select S_Info_windcode as WindStockCode, S_Type_St, entry_dt, Remove_dt from AShareST")
        STStockDf['remove_dtnan'] = STStockDf['Remove_dt'].apply(lambda x: 1 if x is None else 0)
        
        #STStockDf = STStockDf.sort_values(by = 'TradeDays', ascending = True)
        STStockDf.index = range(len(STStockDf))
        
        self.PyMFFApiDataStruct.STStockDf = STStockDf
        
        return STStockDf
     
     
     
     
     
        
    
    
    def FetchFactorsByDate(self, Date, Factor, StockCode = None, FromDb = 1):
        """Get Factors by single day
        Args:
            Date: '20100105'
            Factor: 'High'
            StockCode: '600000.SH' if is none return the whole stockpool factors
            FromDb: if =1, select from Db
         
        Return:
            pandas.DataFrame
         
         
        """
        
        
        if FromDb == 1:
    
            FactorByDateDf = self.FetchFactorsFromDbByDate(Date, Factor, StockCode)
            
            FactorByDateMap = {Factor:FactorByDateDf}
        return FactorByDateMap 
    
    def FetchFactorsByPeriod(self, BeginT, EndT, Factor, StockCode = None, FromDb = 1):
        """Get Factors for a period time
        Args:
            BeginT: '20100105'
            EndT: '20101201'
            Factor: 'High'
            StockCode: '600000.SH' if is none return the whole stockpool factors
            FromDb: if =1, select from Db
         
        Return:
            pandas.DataFrame
         
         
        """
        
        
        
        
        if FromDb == 1:
            FactorsByPeriodDf = self.FetchFactorsFromDbByPeriod(BeginT, EndT, Factor, StockCode) 
        FactorsByPeriodDf = FactorsByPeriodDf.sort_values(by = 'TradeDays', ascending = True)
        FactorsByPeriodDf.index = range(len(FactorsByPeriodDf))
        
        self.PyMFFApiDataStruct.FactorsByPeriodMap[Factor] = FactorsByPeriodDf
            
         
    def FetchFactorsFromDbByPeriod(self, BeginT, EndT, Factor, StockCode = None):
        """Get Factors from database for a period time
        Args:
            BeginT: '20100105'
            EndT: '20101201'
            Factor: 'High'
            StockCode: '600000.SH' if is none return the whole stockpool factors
        
        Return:
            pandas.DataFrame
        
        
        """
        
        iterm = (self.PyMFFApiFactorsFromDb[self.PyMFFApiFactorsFromDb['FactorName']==Factor].set_index([[0]])).to_dict()
        
        if iterm['DataBase'][0] == 'Wind':
            if StockCode is None:
                Factordf = self.PyMFFApiMysql.MysqlOnRspQuery(
                                                              "select  s_info_windcode as WindStockCode,trade_dt as TradeDays, %s as %s from %s where trade_dt>=%s and trade_dt<=%s"
                                                              %(iterm['DbFactorName'][0], iterm['FactorName'][0], iterm['Table'][0], BeginT, EndT))
            
            elif isinstance(StockCode,str):
            

                Factordf = self.PyMFFApiMysql.MysqlOnRspQuery(
                                                              "select  s_info_windcode as WindStockCode, trade_dt as TradeDays, %s as %s from %s where ((trade_dt>=%s and trade_dt<=%s)and s_info_windcode='%s')"
                                                              %(iterm['DbFactorName'][0], iterm['FactorName'][0], iterm['Table'][0],BeginT, EndT, StockCode))
        if iterm['DataBase'][0] == 'SunRelease':
            print "DataBase:SunRelease"
            if StockCode is None:
                #print "wahhfafa"
                #print "select  STOCK_CODE as ZYStockCode, TDATE as TradeDays ,%s as %s from dbo.%s where [TDATE]>=%s and [TDATE]<=%s"%(iterm['DbFactorName'][0], iterm['FactorName'][0], iterm['Table'][0], BeginT, EndT)
                Factordf = self.PyMFFApiMssql.MssqlOnRspQuery("select  [STOCK_CODE] as ZYStockCode, [TDATE] as TradeDays ,[%s] as %s from dbo.%s where [TDATE]>=%s and [TDATE]<=%s"
                                                              %(iterm['DbFactorName'][0], iterm['FactorName'][0], iterm['Table'][0], BeginT, EndT))
                Factordf['TradeDays'] = Factordf['TradeDays'].apply(lambda x:str(x))
                
                Factordf['WindStockCode'] = 0  
                Factordf['ZYStockCode'] = Factordf['ZYStockCode'].apply(lambda x: str(x)) 
                
                Factordf['WindStockCode'] = Factordf['ZYStockCode'].apply(lambda x: x+'.SH'if x[0]=='6' else x+'.SZ')  

                
              
            elif isinstance(StockCode,str):
                pass
                
                
                
                
            
        return Factordf
        
        
        
        
        
          
         
     
     
    def FetchFactorsFromDbByDate(self, Date, Factor, StockCode = None):
        """Get factors from database
        Args:
            Data: '20100105'
            Factor: High
            StockCode: '600062.SH'
        Return:
            pandas.DataFrame
            
        """
        
        
         
        if StockCode is None:
            
            iterm = (self.PyMFFApiFactorsFromDb[self.PyMFFApiFactorsFromDb['FactorName']==Factor].set_index([[0]])).to_dict()
            Factordf = self.PyMFFApiMysql.MysqlOnRspQuery(
                       "select  s_info_windcode as WindStockCode, %s as %s from %s where trade_dt=%s"
                       %(iterm['DbFactorName'][0], iterm['FactorName'][0], iterm['Table'][0], Date))
            
        elif isinstance(StockCode,str):
            if StockCode in (pd.Series(self.PyMFFApiGetBasicStockPool(Date)['WindStockCode'])).tolist():
                 
                iterm = (self.PyMFFApiFactorsFromDb[self.PyMFFApiFactorsFromDb['FactorName']==Factor]).to_dict()
                Factordf = self.PyMFFApiMysql.MysqlOnRspQuery(
                           "select  s_info_windcode as WindStockCode, %s as %s from %s where (trade_dt=%s and s_info_windcode='%s')"
                           %(iterm['DbFactorName'][0], iterm['FactorName'][0], iterm['Table'][0], Date, StockCode))
            
            
        return Factordf 
    

         
    
     
             
     
    def FetchDividend(self):
        DividendDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                     "select s_info_windcode as WindStockCode, STK_DVD_PER_SH as songzhuan, CASH_DVD_PER_SH_PRE_TAX as paixishuihou,  Eqy_record_dt as RecordDate, s_div_bonusrate as  songgu, s_div_conversedrate as zhuanzeng from AshareDividend"                                    
                                                        )
        
        self.PyMFFApiDataStruct.DividendDf = DividendDf
   
        return DividendDf 
    
    
    def FetchMarketDataDf(self, BeginT, EndT):
        MarketDataDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                       "select s_info_windcode as WindStockCode, s_dq_close as Cjprice, s_dq_preclose as preclose, trade_dt as TradeDays from AShareEODPrices where trade_dt >= %s and trade_dt <=%s"%(BeginT, EndT))
        
        self.PyMFFApiDataStruct.MarketDataDf = MarketDataDf
        
        
        return MarketDataDf
        
    
    
    
    
    def FetchIndustryGroup(self):
        IndustryGroupDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                        "select s_info_windcode as WindStockCode, citics_ind_code  as ZXIndustryGroup, entry_dt, remove_dt from AShareIndustriesClassCITICS where citics_ind_code regexp  '^b1'"
                                                           )
       
        IndustryGroupDf['groupNameLevel1'] = IndustryGroupDf['ZXIndustryGroup'].apply(lambda x: x[:4])
        
        IndustryChineseNameDf = self.PyMFFApiMysql.MysqlOnRspQuery(
                              "select Industriescode, Industriesname from ashareindustriescode where levelnum =2 and industriescode regexp '^b1'"                                   
                                                                 ) 
        IndustryChineseNameDf['groupNameLevel1'] = IndustryChineseNameDf['Industriescode'].apply(lambda x:x[:4])
        
        IndustryGroupDf = IndustryGroupDf.merge(IndustryChineseNameDf, on = 'groupNameLevel1', how = 'left')
        IndustryGroupDf['groupNameLevel1'] = IndustryGroupDf['groupNameLevel1'].apply(lambda x:x[2:4])
        self.PyMFFApiDataStruct.IndustryGroupDf = IndustryGroupDf
        
        
        return IndustryGroupDf
    
    def FetchIndustryGroupByDate(self, IndustryGroupDf, Date):
        
        IndustryGroupDf['remove_dtnan'] = IndustryGroupDf['remove_dt'].apply(lambda x: 1 if x is None else 0)
        IndustryGroupDf = IndustryGroupDf[(IndustryGroupDf['entry_dt']<=Date) & ((IndustryGroupDf['remove_dt']>=Date)|(IndustryGroupDf['remove_dtnan']==1))].copy()
        IndustryGroupDf.loc[:,'TradeDays'] = Date
        return IndustryGroupDf
 
