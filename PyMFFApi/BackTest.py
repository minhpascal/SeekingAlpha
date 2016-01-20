#encoding=utf-8
'''
Created on Jan 20, 2016

@author: vitheano
'''
from SeekingAlpha.PyMFFApi.Init import PyMFFApiInit
import pandas as pd
import numpy as np




class PyMFFApiMulFactors(PyMFFApiInit):
        
    """Main class of MFF.
    
    Arrtibutes:
    
    
    
    
        
    
    
    
    

    """
    
    def __init__(self, BeginDate = None, EndDate = None , IndexId = None, 
                Cycle = "month", GroupType = 0, GroupsList = None,
                RateType = 0, GroupHy = None, IndustryMethod = None, 
                IndustryType = None, BuyRatio = 0.01, SellRatio = 0.01,
                ConstrList = None, AbnormalType = 0, StandarizeType = 0,
                FactorsList = None, FactorsListRatio = None,
                InitCash = 100000000.0):
        
        PyMFFApiInit.__init__(self)
        
        
    #    日期相关    
        self.BeginDate = BeginDate
        self.EndDate = EndDate
    #    基准 
        self.IndexId = IndexId
    #    调仓周期
        self.Cycle = Cycle
    #    分组信息 
        self.GroupType = GroupType
        self.GroupsList = GroupsList
    #    资金比例分配
        self.RateType = RateType 
    #    行业属性
        self.GroupHy = GroupHy
        self.IndustryMethod = IndustryMethod
        self.IndustryType = IndustryType
    #    手续费
        self.BuyRatio = BuyRatio
        self.SellRatio = SellRatio
        
    #    剔除条件     
        self.ConstrList = ConstrList
    #    极值处理
        self.AbnormalType = AbnormalType
        self.StandarizeType =StandarizeType
        
        self.InitCash = InitCash
        
        
        
        self.FactorsList = FactorsList
        
        
        self.ConstrListdict = {'BackTestConstrIsSTByDate':self.BackTestConstrIsSTByDate}
        
        self.FactorsListRatio = FactorsListRatio
       
       
        self.FetchTradeDays(self.BeginDate, self.EndDate)
        self.FetchIndustryGroup()
        self.FetchPositionAdjustmentDays(self.PyMFFApiDataStruct.TradeDaysDf, self.Cycle)
        
        
        
        
        
        
        self.FetchHs300Index(self.BeginDate, self.EndDate)
        self.FetchIFIndex(self.BeginDate, self.EndDate)
        self.FetchBasicStockPoolByPeriod(self.BeginDate, self.EndDate)
        self.FetchSTStockTable()
        self.BackTestFetchStockPoolAlfterConstrByPeriod()
        self.PyMFFApiDataStruct.FactorsByPeriodMap = {}
        for factor in self.FactorsList:
            self.FetchFactorsByPeriod(self.BeginDate, self.EndDate, factor)
       
       
      
        self.BackTestFetchAllFactorsByPeriod()
        self.BackTestSortFactorsByPeriod()
        self.FetchDividend()
        self.FetchMarketDataDf(self.BeginDate, self.EndDate)
       
       
    def BackTestConstrIsSTByDate(self, StockCode, Date):
        """Determine whether StockCode is st.
        
        if stock is st ,return True
        else return False
        Args:
            StockCode: '600000.SH'
            Date: '20100101'
        Return:
            True/False
        
        
        
        """
        
        ConstrDf = self.PyMFFApiDataStruct.STStockDf

        ConstrDf = ConstrDf[(ConstrDf['WindStockCode']==StockCode)&(ConstrDf['entry_dt'] <= Date)&((ConstrDf['Remove_dt']>=Date)|(ConstrDf['remove_dtnan']==1))]
        

        if len(ConstrDf) == 0:
            return False
        else:
            return True
        
        
        
        
        
    def BackTestFetchStockPoolAfterConstrByDate(self, Date):
        BasicStockPool = self.FetchBasicStockPoolByDate(Date)
        for name in self.ConstrList:
        
            BasicStockPool['Result_%s'%name] = BasicStockPool['WindStockCode'].apply(lambda x:self.ConstrListdict[name](x,Date))
            BasicStockPool = BasicStockPool[BasicStockPool['Result_%s'%name]==False]
        return BasicStockPool[['WindStockCode','groupNameLevel1', 'Industriesname']]
            
            
            
        
    def BackTestFetchStockPoolAlfterConstrByPeriod(self):
        BasicStockPoolDf = self.PyMFFApiDataStruct.StockPoolPositionAdjustmentDf
        BasicStockPoolDf['id'] = BasicStockPoolDf.index
        for name in self.ConstrList:
            BasicStockPoolDf['Result_%s'%name] = BasicStockPoolDf['id'].apply(lambda x:self.ConstrListdict[name](BasicStockPoolDf['WindStockCode'].iloc[x],BasicStockPoolDf['TradeDays'].iloc[x]))
            BasicStockPoolDf = BasicStockPoolDf[BasicStockPoolDf['Result_%s'%name]==False]
        
        BasicStockPoolDf = BasicStockPoolDf.sort_values(by = 'TradeDays', ascending = True)
        BasicStockPoolDf.index = range(len(BasicStockPoolDf))
        self.PyMFFApiDataStruct.BasicStockPoolDf = BasicStockPoolDf
        return BasicStockPoolDf[['WindStockCode','TradeDays', 'Industriesname']]

               
        
    
        
        
        
        
        
    
    def BackTestFetchAllFactorsByDate(self, Date):
        FactorsByPeriodDf = self.PyMFFApiDataStruct.FactorsByPeriodDf
        FactorsByDateDf = FactorsByPeriodDf[FactorsByPeriodDf['TradeDays']==Date].copy()
        AllFactorsByDateDf = pd.DataFrame(index = xrange(len(FactorsByDateDf)))
        AllFactorsByDateDf['WindStockCode'] = self.BackTestFetchStockPoolAfterConstrByDate(Date)['WindStockCode'].tolist()
        for name in self.FactorsList:
            SingleFactorByDate = FactorsByDateDf
            AllFactorsByDateDf =  AllFactorsByDateDf.merge(SingleFactorByDate, on = 'WindStockCode', how = 'left')
            
        return AllFactorsByDateDf
    
    
    def BackTestFetchAllFactorsByPeriod(self):

        FactorsByPeriodMap = self.PyMFFApiDataStruct.FactorsByPeriodMap
        AllFactorsByPeriodDf = self.PyMFFApiDataStruct.BasicStockPoolDf
        
        for name in self.FactorsList:
            AllFactorsByPeriodDf =  AllFactorsByPeriodDf.merge(FactorsByPeriodMap[name], on = ['WindStockCode','TradeDays'], how = 'left')
        
        AllFactorsByPeriodDf = AllFactorsByPeriodDf.sort_values(by = 'TradeDays', ascending = True)
        AllFactorsByPeriodDf.index = range(len(AllFactorsByPeriodDf))
        self.PyMFFApiDataStruct.AllFactorsByPeriodDf = AllFactorsByPeriodDf
        return AllFactorsByPeriodDf
    
    
    
    
    
    
    
            
    def BackTestFactorsAbnormalMethod0(self, AllBasicFactors,):
        
        for name in self.FactorsList:
            FactorMedianBasic = AllBasicFactors[name].median()
            AllBasicFactors['%s_abnormal'%name] = AllBasicFactors[name].apply(lambda x:abs((x-FactorMedianBasic)))
            FactorMedian = AllBasicFactors['%s_abnormal'%name].median()
            AllBasicFactors['%s_abnormal'%name] = AllBasicFactors[name].apply(lambda x: 
                                                FactorMedianBasic-5.2*FactorMedian if x<=FactorMedianBasic-5.2*FactorMedian else x)
            AllBasicFactors['%s_abnormal'%name] = AllBasicFactors[name].apply(lambda x: 
                                                FactorMedianBasic+5.2*FactorMedian if x>=FactorMedianBasic+5.2*FactorMedian else x)
         
        return AllBasicFactors
     
     
     
        
    def BackTestFactorsAbnormalByDate(self, Date):
        if self.AbnormalType == 0:
            AllBasicFactors = self.PyMFFApiDataStruct.AllFactorsByPeriodDf[self.PyMFFApiDataStruct.AllFactorsByPeriodDf['TradeDays']==Date].copy()
            AllFactorsAfterAbnormal = self.BackTestFactorsAbnormalMethod0(AllBasicFactors)
                                    
        return AllFactorsAfterAbnormal
    
    
    def BackTestFactorsAbnormalByPeriod(self):
        if self.AbnormalType == 0:
            AllBasicFactors = self.PyMFFApiDataStruct.AllFactorsByPeriodDf
            AllFactorsAfterAbnormal = pd.DataFrame()
            for i in AllBasicFactors['TradeDays'].unique():
                AllBasicFactorsiterm = AllBasicFactors[AllBasicFactors['TradeDays']==i].copy()
                AllFactorsAfterAbnormal = AllFactorsAfterAbnormal.append(self.BackTestFactorsAbnormalMethod0(AllBasicFactorsiterm),ignore_index = False )
                                    
        return AllFactorsAfterAbnormal    
    
    
    
    
    def BackTestFactorsStandarizeMethod0(self, AllBasicFactors):          
        for name in self.FactorsList:
            Factorsmean = AllBasicFactors['%s_abnormal'%name].mean()
            Factorsstd = AllBasicFactors['%s_abnormal'%name].std()
            AllBasicFactors['%s_stardarize'%name] = AllBasicFactors['%s_abnormal'%name].apply(lambda x: 
                                                    (x-Factorsmean)/Factorsstd)
            
        return AllBasicFactors
        
    
    
    def BackTestFactorsStandarizeByDate(self, Date):
        if self.StandarizeType == 0:
            AllTestFactors = self.BackTestFactorsAbnormalByDate(Date)
            AllFactorsAfterStandarize = self.BackTestFactorsStandarizeMethod0(AllTestFactors)
        return AllFactorsAfterStandarize 
    
    
    
    def BackTestFactorsStandarizeByPeriod(self):
        if self.StandarizeType == 0:
            AllTestFactors = self.BackTestFactorsAbnormalByPeriod()
            AllFactorsAfterStandarize = pd.DataFrame()
            for i in list(AllTestFactors['TradeDays'].unique()):
                AllTestFactorsiterm = AllTestFactors[AllTestFactors['TradeDays']==i]
                AllFactorsAfterStandarize = AllFactorsAfterStandarize.append(self.BackTestFactorsStandarizeMethod0(AllTestFactorsiterm), ignore_index = False)
        
        return AllFactorsAfterStandarize
    
        
    def BackTestFactorsCombineByDate(self, Date):
        AllTestFactors = self.BackTestFactorsStandarizeByDate(Date)
        AllTestFactors['Combine'] = 0
        
        for index, name in enumerate(self.FactorsList):
            
            AllTestFactors['Combine'] = AllTestFactors['Combine']+AllTestFactors['%s_stardarize'%name]*self.FactorsListRatio[index]
        
        return AllTestFactors
    
    def BackTestFactorsCombineByPeriod(self):
        AllTestFactors = self.BackTestFactorsStandarizeByPeriod()
        AllTestFactors['Combine'] = 0
        
        for index, name in enumerate(self.FactorsList):
            
            AllTestFactors['Combine'] = AllTestFactors['Combine']+AllTestFactors['%s_stardarize'%name]*self.FactorsListRatio[index]
        
        return AllTestFactors
    
    
    
    
    
    def BackTestSortFactorsByDate(self, Date):
        AllTestFactors = self.BackTestFactorsCombineByDate(Date)
        
        AllTestFactors = AllTestFactors.sort_values(by = 'Combine', ascending = False)
        
        AllTestFactors.index=xrange(len(AllTestFactors))
        return AllTestFactors
    
    
    def BackTestSortFactorsByPeriod(self):
        AllTestFactors = self.BackTestFactorsCombineByPeriod()        
        AllTestFactors.index=xrange(len(AllTestFactors))
        
        self.PyMFFApiDataStruct.FinalFactorsDf = AllTestFactors
        
        return AllTestFactors
    
    
    def BackTestPortforlioRatioByDate(self, Date):

        AllFactorsDf = self.PyMFFApiDataStruct.FinalFactorsDf
        AllFactorsByDateDf = AllFactorsDf[AllFactorsDf['TradeDays'] == Date]
        AllFactorsByDateDf = AllFactorsByDateDf.sort_values(by = 'Combine', ascending = False)
        AllFactorsByDateDf.index = xrange(len(AllFactorsByDateDf))


        return AllFactorsByDateDf    

          

        

 
        
    def BackTestMainFunc(self):


        TradedaysDf = self.PyMFFApiDataStruct.TradeDaysDf
        PositionTradedaysDf = self.PyMFFApiDataStruct.PositionAdjustmentDaysDf
        PositionTradedaysDf = PositionTradedaysDf[:-1].copy()
        
        MarketDataDf = self.PyMFFApiDataStruct.MarketDataDf
        TradedaysDf = TradedaysDf[TradedaysDf['TradeDays']>=PositionTradedaysDf['TradeDays'].iloc[0]]
        AllBackTestDf = pd.DataFrame(columns =['TradeDays','WindStockCode','group','cash','Cjprice','openint'])
        DividendDf= self.PyMFFApiDataStruct.DividendDf
        InitCash = self.InitCash
        count = 0
        
        for i_number,i in enumerate(TradedaysDf['TradeDays']):
            if i in list(PositionTradedaysDf['TradeDays']):
                
                #print "today is 换仓日 ！！！！ plz pay attention to this !!!!!"
                print i
                if count == 0:
                    count+=1
                    df_b = self.BackTestPortforlioRatioByDate(i)
                    df_a = MarketDataDf[MarketDataDf['TradeDays'] ==i].copy()

                    df_b = df_b.merge(df_a, on ='WindStockCode', how ='left' )
                    

                    
                    for number, xtick in enumerate(self.GroupsList):
                        df_b_i = df_b[xtick[0]:xtick[-1]].copy()
                        InitPre = InitCash
                        maxiter = 0
                        while 1:  
                            maxiter+=1      
                            iterm = pd.DataFrame(index = xrange(len(df_b_i)),columns=['WindStockCode'])
                            iterm['WindStockCode'] = list(df_b_i['WindStockCode'])
                            iterm['TradeDays'] = i
                            iterm['group'] = number+1
                            iterm['cash'] = InitCash/len(df_b_i)
                            iterm['Cjprice'] = list(df_b_i['Cjprice'])
                            iterm['preclose'] = list(df_b_i['preclose'])
                            iterm['openint'] = iterm['cash']/iterm['Cjprice']
                            iterm['openint_pre'] = iterm['openint']
                            iterm['id'] = iterm.index
                            iterm['fenhong'] = 0
                            DividendByDateDf =DividendDf[DividendDf['RecordDate']==i]
                            if len(DividendByDateDf)!=0:
                                iterm=iterm.merge(DividendByDateDf,on = 'WindStockCode', how = 'left')
                                iterm['fenhong'] = iterm['id'].apply(lambda x: 0 if np.isnan(iterm['paixishuihou'].iloc[x]) else iterm['openint'].iloc[x]*iterm['paixishuihou'].iloc[x] )
                                iterm['openint'] = iterm['id'].apply(lambda x: iterm['openint'].iloc[x] if np.isnan(iterm['songzhuan'].iloc[x]) else  iterm['openint'].iloc[x]*(1+iterm['songzhuan'].iloc[x]))

                            InitNV1 = (iterm['openint']*iterm['Cjprice']).sum()*(1-self.BuyRatio)
                            InitCash = 1.0/2*(InitNV1 + InitPre) 
                  
                            if maxiter>100 or abs(InitCash-InitPre) <0.001:
                                
                                break
                        

                        
                        AllBackTestDf = AllBackTestDf.append(iterm)

                else:
                    positionTradeDays = self.PyMFFApiDataStruct.PositionAdjustmentDaysDf
                    positionTradeDays =  list((positionTradeDays[positionTradeDays['TradeDays']<i])['TradeDays'])
                    pospre = positionTradeDays.pop()

                    whatday = AllBackTestDf[AllBackTestDf['TradeDays']==TradedaysDf['TradeDays'].iloc[i_number-1]]
                    whatyear = AllBackTestDf[(AllBackTestDf['TradeDays']<TradedaysDf['TradeDays'].iloc[i_number-1])&(AllBackTestDf['TradeDays']>=pospre)]
                    df_b = self.BackTestPortforlioRatioByDate(i)
                    
                    df_a = MarketDataDf[MarketDataDf['TradeDays'] ==i].copy()
                    df_b = df_b.merge(df_a, on = 'WindStockCode', how ='left' )
                    whatday = whatday.merge(df_a, on = 'WindStockCode', how ='left' )
                    for number, xtick in enumerate(self.GroupsList):
                        
                        
                        
                        
                        df_b_ii = df_b[xtick[0]:xtick[-1]].copy()
                            
                        whatday_iterm = whatday[xtick[0]:xtick[-1]].copy()

                        whatyear_iterm = whatyear[whatyear['group']==(number+1)].copy()
                        maxiter = 0

                        InitCashPre  = whatday_iterm['cash'].sum()+whatyear_iterm['fenhong'].sum()

                        InitCash = InitCashPre
                        
                        while 1:

                            maxiter+=1   
                            iterm = pd.DataFrame(index = xrange(len(df_b_ii)),columns=['WindStockCode'])
                            iterm['WindStockCode'] = list(df_b_ii['WindStockCode'])
                            iterm['TradeDays'] = i
                            iterm['group'] = number+1
                            iterm['cash'] = (InitCash/len(df_b_ii))
                            iterm['Cjprice'] = list(df_b_ii['Cjprice'])
                            iterm['preclose'] = list(df_b_ii['preclose'])
                            
                            iterm['openint'] = iterm['cash']/iterm['Cjprice']
                            iterm['openint_pre'] = iterm['openint']
                            iterm['fenhong'] = 0
                            iterm['id'] = iterm.index
                            DividendByDateDf =DividendDf[DividendDf['RecordDate']==i]
                            
                            if len(DividendByDateDf)!=0:
                                iterm=iterm.merge(DividendByDateDf,on = 'WindStockCode', how = 'left')
                                iterm['fenhong'] = iterm['id'].apply(lambda x: 0 if np.isnan(iterm['paixishuihou'].iloc[x]) else iterm['openint'].iloc[x]*iterm['paixishuihou'].iloc[x] )
                                iterm['openint'] = iterm['id'].apply(lambda x: iterm['openint'].iloc[x] if np.isnan(iterm['songzhuan'].iloc[x]) else  iterm['openint'].iloc[x]*(1+iterm['songzhuan'].iloc[x]))
                            sellStockCode = whatday_iterm[['WindStockCode', 'openint']]
                            buyStockCode = iterm[['WindStockCode','openint']]
                            u_sell = set(list(sellStockCode['WindStockCode']))-set(list(buyStockCode['WindStockCode']))
                            
                            u_buy  = set(list(buyStockCode['WindStockCode']))- set(list(sellStockCode['WindStockCode']))
                            u_union = set(list(sellStockCode['WindStockCode']))-u_sell
                            
                            
                            u_sell_df = pd.DataFrame(columns = ['WindStockCode'])
                            
                            u_sell_df['WindStockCode'] = list(u_sell)
                            
                            u_sell_df = u_sell_df.merge(whatday_iterm, on = 'WindStockCode', how ='left')
                            
                            u_buy_df = pd.DataFrame(columns = ['WindStockCode'])
                            
                            u_buy_df['WindStockCode'] = list(u_buy)
                            
                            u_buy_df = u_buy_df.merge(iterm, on = 'WindStockCode', how ='left')
                            
                            
                            u_union_df = pd.DataFrame(columns = ['WindStockCode'])
                            
                            u_union_df['WindStockCode'] = list(u_union)
                            #print u_union_df
                            
                            
                            u_union_df = u_union_df.merge(iterm, on = 'WindStockCode', how ='left')
                            
                            
                            
                            u_union_df = u_union_df.merge(whatday_iterm, on = 'WindStockCode', how ='left')

                            u_union_df['x-y'] = u_union_df['openint_x']-u_union_df['openint_y']
                            u_union_df['x-y'] = u_union_df['x-y'].apply(lambda x: abs(x))

                            delta = (whatday_iterm['Cjprice_y']*whatday_iterm['openint']).sum()-(whatday_iterm['Cjprice_x']*whatday_iterm['openint_pre']).sum()+whatday_iterm['fenhong'].sum()

                            InitCash2 = delta+InitCashPre - (u_sell_df['Cjprice_y']*u_sell_df['openint']).sum()*(self.SellRatio) -(u_buy_df['Cjprice']*u_buy_df['openint']).sum()*(self.BuyRatio) - ((u_union_df['x-y'])*u_union_df['Cjprice_y']).sum()*(self.BuyRatio)

                            InitCash = (InitCash+InitCash2)/2

                            if maxiter>100 or abs(InitCash-InitCashPre) <0.001:
                                break
 
                        iterm['shizhi'] = iterm['cash'] + iterm['fenhong']
                        AllBackTestDf = AllBackTestDf.append(iterm)

            else:
                #print "平常日而已"
                whatday = AllBackTestDf[AllBackTestDf['TradeDays']==TradedaysDf['TradeDays'].iloc[i_number-1]]
                for number, xtick in enumerate(self.GroupsList):
                    df_b_i = whatday[whatday['group']==(number+1)].copy()
                    df_a = MarketDataDf[MarketDataDf['TradeDays']==i]
                    iterm = pd.DataFrame(index = xrange(len(df_b_i)),columns=['WindStockCode'])
                    iterm['WindStockCode'] = df_b_i['WindStockCode']
                    iterm['TradeDays'] = i
                    iterm['group'] = number+1
                    PriceDf = iterm.merge(df_a,on = 'WindStockCode', how = 'left')
                    iterm['Cjprice'] = list(PriceDf['Cjprice'])
                    iterm['preclose'] = list(PriceDf['preclose'])
                    iterm['openint'] = df_b_i['openint']
                    iterm['openint_pre'] = iterm['openint']
                    iterm['cash'] = iterm['Cjprice']*iterm['openint']
                    iterm['id'] = iterm.index
                    iterm['fenhong'] = 0
                    DividendByDateDf =DividendDf[DividendDf['RecordDate']==i].copy()
   
                    if len(DividendByDateDf)!=0:
                        iterm=iterm.merge(DividendByDateDf,on = 'WindStockCode', how = 'left')
                        iterm['fenhong'] = iterm['id'].apply(lambda x: 0 if np.isnan(iterm['paixishuihou'].iloc[x]) else iterm['openint'].iloc[x]*iterm['paixishuihou'].iloc[x] )

                        iterm['openint'] = iterm['id'].apply(lambda x: iterm['openint'].iloc[x] if np.isnan(iterm['songzhuan'].iloc[x]) else  iterm['openint'].iloc[x]*(1+iterm['songzhuan'].iloc[x]))

                    AllBackTestDf = AllBackTestDf.append(iterm)
        self.PyMFFApiDataStruct.BackTestAllStockProfitDf = AllBackTestDf
        
    def BackTestPoforlioDf(self):
        self.BackTestMainFunc()
        num = len(self.GroupsList)
        columns = ['TradeDays']+['group_%s'%(x+1) for x in range(num)]+['shizhi_%s'%(x+1) for x in range(num)]
        Df = pd.DataFrame(columns =['TradeDays', 'group'])
        AllBackTestDf = self.PyMFFApiDataStruct.BackTestAllStockProfitDf
        for name, df in AllBackTestDf.groupby('TradeDays'):
            cash = {}
            cash['TradeDays'] = name
            for i in xrange(num):
                df_i = df[df['group']==(i+1)]

                cash['group_%s'%(i+1)] = df_i['cash'].sum() 

            iterm = pd.Series(cash)
                
            Df = Df.append(iterm, ignore_index = True)
        self.PyMFFApiDataStruct.BackTestAllProforlioDf = Df        
                
        return Df    
    
    
    def BackTestCombineIndex(self):
        self.BackTestPoforlioDf()
        AllProforlioDf = self.PyMFFApiDataStruct.BackTestAllProforlioDf
        
        Hs300IndexDf = self.PyMFFApiDataStruct.Hs300IndexDf
        HsIFIndexDf = self.PyMFFApiDataStruct.HsIFIndexDf
        AllProforlioDf['TradeDays'] = AllProforlioDf['TradeDays'].apply(lambda x:int(x))
        Hs300IndexDf['TradeDays'] = Hs300IndexDf['TradeDays'].apply(lambda x:int(x))
        HsIFIndexDf['TradeDays'] = HsIFIndexDf['TradeDays'].apply(lambda x:int(x))
        
        AllCombieDf = AllProforlioDf.merge(Hs300IndexDf, on = 'TradeDays',how = 'left')
        AllCombieDf = AllCombieDf.merge(HsIFIndexDf, on = 'TradeDays',how = 'left')
        
        AllCombieDf = AllCombieDf.sort_values(by = 'TradeDays', ascending = 1)

        AllCombieDf['HS300index'] =self.InitCash

        AllCombieDf['HSIFindex'] = self.InitCash

        for i in xrange(1, len(AllCombieDf)):
            AllCombieDf.loc[i,'HS300index']= AllCombieDf['HS300index'].iloc[i-1]*(AllCombieDf['close'].iloc[i]/AllCombieDf['close'].iloc[i-1])
            AllCombieDf.loc[i,'HSIFindex']= AllCombieDf['HSIFindex'].iloc[i-1]*(AllCombieDf['settle'].iloc[i]/AllCombieDf['settle'].iloc[i-1])
            
        AllCombieDf['HsIndex'] = 0
        AllCombieDf['PorIndex'] = 0
        AllCombieDf['IFIndex'] = 0
        for  i in xrange(1,len(AllCombieDf)):
            AllCombieDf.loc[0,'HsIndex'] = 1
            AllCombieDf.loc[i,'HsIndex'] = ((AllCombieDf.loc[i,'HS300index'])/AllCombieDf.loc[i-1,'HS300index']-1)*100
            AllCombieDf.loc[0,'IFIndex'] = 1
            AllCombieDf.loc[i,'IFIndex'] = ((AllCombieDf.loc[i,'HSIFindex'])/AllCombieDf.loc[i-1,'HSIFindex']-1)*100
            AllCombieDf.loc[0,'PorIndex'] = 1
            AllCombieDf.loc[i,'PorIndex'] = ((AllCombieDf.loc[i,'group_1'])/AllCombieDf.loc[i-1,'group_1']-1)*100
            
        AllCombieDf['Por-Hs'] = AllCombieDf['PorIndex'] - AllCombieDf['HsIndex']
        AllCombieDf['Por-IF'] = 0.8*(AllCombieDf['PorIndex'] - AllCombieDf['IFIndex'])
        AllCombieDf['(Por-IF).index'] = self.InitCash
        for i in xrange(1, len(AllCombieDf)):
            AllCombieDf.loc[i,'(Por-IF).index']= AllCombieDf.loc[(i-1),'(Por-IF).index']*(1+AllCombieDf.loc[i,'Por-IF']/100)
        AllCombieDf['DailyReturn'] = 0
        
        
        
        self.PyMFFApiDataStruct.BackTestAllCombieDf= AllCombieDf
        return AllCombieDf
    
    def BackTestFactorAnalyze(self):
        
        AllcombieDf = self.PyMFFApiDataStruct.BackTestAllCombieDf
        
        
        
        AllcombieDf['year'] = AllcombieDf['TradeDays'].apply(lambda x: int(str(x)[:4]))
        
        DfIRYear=pd.DataFrame(columns=['year','IndexRatioPerYear','PorRatioPerYear','varPerYear','IRPerYear','SRPerYear','Return'])
        
        
        mymap ={}
        for year,df_i in AllcombieDf.groupby('year'):

            mymap[year]=df_i
        for x in mymap.keys():

            if x-1 in mymap.keys():
                for i in xrange(len(mymap[x])):
                    
                    max = mymap[x]['(Por-IF).index'][:i].max()
                    mymap[x]['DailyReturn'].iloc[i] = 1 - mymap[x]['(Por-IF).index'].iloc[i]/max

                
                iterm=pd.Series({'year':x,
                                 'IndexRatioPerYear':(mymap[x]['HS300index'].iloc[-1]/mymap[x-1]['HS300index'].iloc[-1]-1)*100,
                                 'PorRatioPerYear':(mymap[x]['group_1'].iloc[-1]/mymap[x-1]['group_1'].iloc[-1]-1)*100,
                                 'varPerYear':mymap[x]['Por-Hs'].std()*np.sqrt(250),
                                 "IRPerYear":(mymap[x]['Por-Hs'].mean()*250)/(mymap[x]['Por-Hs'].std()*np.sqrt(250)),
                                 "SRPerYear":(mymap[x]['Por-IF'].mean()*250)/(mymap[x]['Por-IF'].std()*np.sqrt(250)),
                                 "Return":mymap[x]['DailyReturn'].max()})
     
                DfIRYear=DfIRYear.append(iterm,ignore_index=True)
            else:
                for i in xrange(len(mymap[x])):
                    
                    max = mymap[x]['(Por-IF).index'][:i].max()
                    mymap[x]['DailyReturn'].iloc[i] = 1 - mymap[x]['(Por-IF).index'].iloc[i]/max

                iterm=pd.Series({'year':x,
                                 'IndexRatioPerYear':(mymap[x]['HS300index'].iloc[-1]/mymap[x]['HS300index'].iloc[0]-1)*100,
                                 'PorRatioPerYear':(mymap[x]['group_1'].iloc[-1]/mymap[x]['group_1'].iloc[0]-1)*100,
                                 'varPerYear':mymap[x]['Por-Hs'].std()*np.sqrt(250),
                                 "IRPerYear":(mymap[x]['Por-Hs'].mean()*250)/(mymap[x]['Por-Hs'].std()*np.sqrt(250)),
                                 "SRPerYear":(mymap[x]['Por-IF'].mean()*250)/(mymap[x]['Por-IF'].std()*np.sqrt(250)),
                                 "Return":mymap[x]['DailyReturn'].max()*100})
                
                DfIRYear=DfIRYear.append(iterm,ignore_index=True)
            DfIRYear['IR'] = (AllcombieDf['Por-Hs'].mean()*250)/(AllcombieDf['Por-Hs'].std()*np.sqrt(250))
            
            
        self.PyMFFApiDataStruct.BackTestIRYearDf = DfIRYear
        return DfIRYear
        
        
        
        #PorforlioDf = self.BackTestCombineIndex()
