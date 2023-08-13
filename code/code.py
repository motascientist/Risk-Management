import numpy as np # Linear Algebra
import pandas as pd # Manipulate DataSets
import yfinance as yf # Import financial data
import plotly.express as px  # Plot interactive graphic
from scipy.stats import norm # Statistical inference

class AssetsAnalytics:
    
    def __init__ (self,asset = ['MXRF11.SA'],start = '2019-01-01',end = '2021-06-12'):
        
        self.asset = asset
        self.start = start
        self.end = end
        
        data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
        
        data = pd.DataFrame(data)
        data.dropna(inplace = True)
        
      
    # Showing first five lines and last five lines
    def Show(self):
    
        data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
    
        print('First Five Lines')
        print(data.head())
        print('\n')
        print('LAST FIVE LINES')
        print(data.tail())
        
    # Percentage Variation
        
    def Seasonality(self):
        
        data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
        
        print(f'Percentage Variation between [{self.start} at {self.end}]')
        
        print('\n')
        print((data.iloc[-1,:]-data.iloc[0,:])/data.iloc[0,:])
        data.dropna(inplace = True)
        vp = data.copy()
        for i in data.columns[0:]:
            vp[i] = vp[i].pct_change()    
        
        x = vp.index
        
        graph_vol = px.line(vp,x = x,y = vp.columns[0:],title = 'Percentage Variation')
        graph_vol.show()
        
    def Benchmarking(self):
    
        data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
        
        data = pd.DataFrame(data)
        data.dropna(inplace = True)     
        vp = data.copy()
    
        for i in data.columns[0:]:
            vp[i] = vp[i].pct_change()

        for i in data.columns[0:]:
            vp[i] = (1 + vp[i]).cumprod()
        
        print('Value in reais (R$)')
        print(vp.tail(1),'R$')
        
        for i in vp.columns[0:]:
            vp[i] = (vp[i] - 1)
        
        print('\n')
        print('Value in % (decimal)')
        print(vp.tail(1))
        x = vp.index
        
        graph = px.line(vp,x = x,y = vp.columns[0:],title = 'Benchmarking')
        graph.show()
        
    def Volatility(self,window = 30):
            
        self.window = window
        data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
        
        var_per = data.copy()
        for i in data.columns[0:]:
            var_per[i] = var_per[i].pct_change()
                
        for i in data.columns[0:]:
            var_per[i] = var_per[i].rolling(window=window).std() * np.sqrt(window)
            
        print('\nVolatility\n')
        print(data.std())
        x = var_per.index
        graph_vol = px.line(var_per,x = x,y = var_per.columns[0:],title = 'Volatility')
        graph_vol.show() 
        
    def Asset_Portfolio_Return(self, positions = [1000], risk_free_rate = 0.125,show = False):
        
        data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
        
        data_2 = data.copy()
        
        x = 0
        for i in data.columns[0:]:   
            data[i] = data[i]*positions[x]
            x += 1
        
        if show == True:
            print('Your Position in the Beginning')
            print('\n')
            print(data.head())
            print('Your Position at the end')
            print('\n')
            print(data.tail())
        else:
            pass
        
        data = data.pct_change()
        data.dropna(how='any', inplace=True)

        print('Average Return\n')
        for i in data:
            print(f'{i} = {round(data[i].mean()*100,2)} %')
        print('\nVolatility')
        for i in data:
            print(f'{i} = {round(data[i].std()*100,2)} %')
        
        print('\nCorrelation Between Assets\n')
        print(data.corr())
        
        print('\nSharpe Rate')
        
        for i in data:
            
            average = data[i].mean()
            std = data[i].std()
            sharpe_rate = (average-risk_free_rate)/std
            
            if sharpe_rate >= 0:
                print(f'Shape Rate:{i} = {round(sharpe_rate,5)}')
            else:
                print(f'Shape Rate:{i} = Undefined')
                
        positions = list(positions)
        
        x = 0
        positions_2 = []
        for index,asset in enumerate(data): 
            
            a = positions[index] * data_2[asset].iloc[-1]
            positions_2.append(a)
            
        for index,asset in enumerate(data):
            
            data[asset] = positions_2[index] * data[asset]
        
        data['Portfolio'] = data.sum(axis = 1)
        
        print('\nSTOCK PORTFOLIO INFORMATION')
        data.dropna(how='any', inplace=True)
        
        print('\nAverage Return')
        print(round(data['Portfolio'].mean(),2))
        print('\nVolatility')
        print(round(data['Portfolio'].std(),2))
        print('\nValue - at - Risk (95%)')
        print(round(data['Portfolio'].mean()+data['Portfolio'].std()* (- norm.ppf(0.95)),2))