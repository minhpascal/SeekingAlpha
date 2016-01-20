#encodng=utf-8
'''
Created on Jan 20, 2016

@author: vitheano
'''
class PyMFFApiDataStruct(object):
    
    @property
    def Hs300IndexDf(self):
        
        return self._Hs300IndexDf

    @Hs300IndexDf.setter
    def Hs300IndexDf(self, value):
        
        self._Hs300IndexDf = value 
        
        
    @Hs300IndexDf.deleter
    def Hs300IndexDf(self):
        
        del self._Hs300IndexDf
    
    @property
    def HsIFIndexDf(self):
        
        return self._HsIFIndexDf

    @HsIFIndexDf.setter
    def HsIFIndexDf(self, value):
        
        self._HsIFIndexDf = value 
        
        
    @HsIFIndexDf.deleter
    def HsIFIndexDf(self):
        
        del self._HsIFIndexDf
    



    @property
    def TradeDaysDf(self):
        
        return self._TradedaysDf

    @TradeDaysDf.setter
    def TradeDaysDf(self, value):
        
        self._TradedaysDf = value 
        
        
    @TradeDaysDf.deleter
    def TradeDaysDf(self):
        
        del self._TradedaysDf
        
        
        
    @property
    def PositionAdjustmentDaysDf(self):
    
        return self._PositionAdjustmentdaysDf

    @PositionAdjustmentDaysDf.setter
    def PositionAdjustmentDaysDf(self, value):
        
        self._PositionAdjustmentdaysDf = value 
        
        
    @PositionAdjustmentDaysDf.deleter
    def PositionAdjustmentDaysDf(self):
        
        del self._PositionAdjustmentdaysDf
        
        
        
    
    @property
    def StockPoolPositionAdjustmentDf(self):
    
        return self._StockPoolPositionAdjustmentDf

    @StockPoolPositionAdjustmentDf.setter
    def StockPoolPositionAdjustmentDf(self, value):
        
        self._StockPoolPositionAdjustmentDf = value 
        
        
    @StockPoolPositionAdjustmentDf.deleter
    def StockPoolPositionAdjustmentDf(self):
        
        del self._StockPoolPositionAdjustmentDf 
    
   
   
    @property
    def STStockDf(self):
    
        return self._STStockDf

    @STStockDf.setter
    def STStockDf(self, value):
        
        self._STStockDf = value 
        
        
    @STStockDf.deleter
    def STStockDf(self):
        
        del self._STStockDf  
   
  
        
    @property
    def BasicStockPoolDf(self):
    
        return self._BasicStockPoolDf

    @BasicStockPoolDf.setter
    def BasicStockPoolDf(self, value):
        
        self._BasicStockPoolDf = value 
        
        
    @BasicStockPoolDf.deleter
    def BasicStockPoolDf(self):
        
        del self._BasicStockPoolDf   
   
   
   
   
   
   
   
   
    
    @property
    def FactorsByPeriodMap(self):
    
        return self._FactorsByPeriodMap

    @FactorsByPeriodMap.setter
    def FactorsByPeriodMap(self, value):
        
        self._FactorsByPeriodMap = value 
        
        
    @FactorsByPeriodMap.deleter
    def FactorsByPeriodMap(self):
        
        del self._FactorsByPeriodMap
    
    

    
    @property
    def AllFactorsByPeriodDf(self):
    
        return self._AllFactorsByPeriodDf

    @AllFactorsByPeriodDf.setter
    def AllFactorsByPeriodDf(self, value):
        
        self._AllFactorsByPeriodDf = value 
        
        
    @AllFactorsByPeriodDf.deleter
    def AllFactorsByPeriodDf(self):
        
        del self._AllFactorsByPeriodDf    
       
    
    @property
    def FinalFactorsDf(self):
    
        return self._FinalFactorsDf

    @FinalFactorsDf.setter
    def FinalFactorsDf(self, value):
        
        self._FinalFactorsDf = value 
        
        
    @FinalFactorsDf.deleter
    def FinalFactorsDf(self):
        
        del self._FinalFactorsDf
    
    @property
    def DividendDf(self):
    
        return self._DividendDf

    @DividendDf.setter
    def DividendDf(self, value):
        
        self._DividendDf = value 
        
        
    @DividendDf.deleter
    def DividendDf(self):
        
        del self._DividendDf
    
    
    
    
    @property
    def MarketDataDf(self):
    
        return self._MarketDataDf

    @MarketDataDf.setter
    def MarketDataDf(self, value):
        
        self._MarketDataDf = value 
        
        
    @MarketDataDf.deleter
    def MarketDataDf(self):
        
        del self._MarketDataDf
        
        
        
    @property
    def BackTestAllStockProfitDf(self):
        
        return self._BackTestAllStockProfitDf 

    @BackTestAllStockProfitDf.setter
    def BackTestAllStockProfitDf(self, value):
        
        self._BackTestAllStockProfitDf = value 
        
        
    @BackTestAllStockProfitDf.deleter
    def BackTestAllStockProfitDf(self):
        
        del self._BackTestAllStockProfitDf

    
        

    
    @property
    def BackTestAllProforlioDf(self):
        
        return self._BackTestAllProforlioDf

    @BackTestAllProforlioDf.setter
    def BackTestAllProforlioDf(self, value):
        
        self._BackTestAllProforlioDf = value 
        
        
    @BackTestAllProforlioDf.deleter
    def BackTestAllProforlioDf(self):
        
        del self.BackTestAllProforlioDf 




    @property
    def BackTestEvaluationDf(self):
        
        return self._BackTestEvaluationDf

    @BackTestEvaluationDf.setter
    def BackTestEvaluationDf(self, value):
        
        self._BackTestEvalutionDf = value 
        
        
    @BackTestEvaluationDf.deleter
    def BackTestEvaluationDf(self):
        
        del self._BackTestEvaluatonDf  



    @property
    def BackTestAllCombieDf(self):
        
        return self._BackTestAllCombieDf
    
    @BackTestAllCombieDf.setter
    def BackTestAllCombieDf(self, value):
        
        self._BackTestAllCombieDf = value
        
        
    @BackTestAllCombieDf.deleter
    def BackTestAllCombieDf(self):
        
        del self._BackTestAllCombieDf
        
        
        

    @property
    def BackTestIRYearDf(self):
        
        return self._BackTestIRYearDf
    
    @BackTestIRYearDf.setter
    def BackTestIRYearDf(self, value):
        
        self._BackTestIRYearDf = value
        
        
    @BackTestIRYearDf.deleter
    def BackTestIRYearDf(self):
        
        del self._BackTestIRYearDf
        
        
        
    @property
    def IndustryGroupDf(self):
        
        return self._IndustryGroupDf
    
    @IndustryGroupDf.setter
    def IndustryGroupDf(self, value):
        
        self._IndustryGroupDf= value
        
        
    @IndustryGroupDf.deleter
    def IndustryGroupDf(self):
        
        del self._IndustryGroupDf
