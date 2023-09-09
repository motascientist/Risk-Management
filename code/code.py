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
        self.data = self.download_data()
        
    def download_data(self):
        data = yf.download(self.asset, start=self.start, end=self.end, progress=False)['Adj Close']
        data.dropna(inplace=True)
        return data
    

    # Showing first five lines and last five lines
    def Show(self):
    
        print('First Five Lines')
        print(self.data.head())
        print('\n')
        print('LAST FIVE LINES')
        print(self.data.tail())
        
    # Percentage Variation
        
    def Seasonality(self):
        
        print(f'Percentage Variation between [{self.start} at {self.end}]')
        
        print('\n')
        print((self.data.iloc[-1,:]-self.data.iloc[0,:])/self.data.iloc[0,:])
        self.data.dropna(inplace = True)
        vp = self.data.copy()
        for i in self.data.columns[0:]:
            vp[i] = vp[i].pct_change()    
        
        x = vp.index
        
        graph_vol = px.line(vp,x = x,y = vp.columns[0:],title = 'Percentage Variation')
        graph_vol.show()
        
    def Benchmarking(self):
        
        self.data = pd.DataFrame(self.data)
        self.data.dropna(inplace = True)     
        vp = self.data.copy()
    
        for i in self.data.columns[0:]:
            vp[i] = vp[i].pct_change()

        for i in self.data.columns[0:]:
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
        self.data = yf.download(self.asset, 
                          start = self.start, 
                          end= self.end,progress=False)['Adj Close']
        
        var_per = self.data.copy()
        for i in self.data.columns[0:]:
            var_per[i] = var_per[i].pct_change()
                
        for i in self.data.columns[0:]:
            var_per[i] = var_per[i].rolling(window=window).std() * np.sqrt(window)
            
        print('\nVolatility\n')
        print(self.data.std())
        x = var_per.index
        graph_vol = px.line(var_per,x = x,y = var_per.columns[0:],title = 'Volatility')
        graph_vol.show() 
        
    def Asset_Portfolio_Return(self, positions = [1000], risk_free_rate = 0.125,show = False):
        
        self.data_2 = self.data.copy()
        
        x = 0
        for i in self.data.columns[0:]:   
            self.data[i] = self.data[i]*positions[x]
            x += 1
        
        if show == True:
            print('Your Position in the Beginning')
            print('\n')
            print(self.data.head())
            print('Your Position at the end')
            print('\n')
            print(self.data.tail())
        else:
            pass
        
        self.data = self.data.pct_change()
        self.data.dropna(how='any', inplace=True)

        print('Average Return\n')
        for i in self.data:
            print(f'{i} = {round(self.data[i].mean()*100,2)} %')
        print('\nVolatility')
        for i in self.data:
            print(f'{i} = {round(self.data[i].std()*100,2)} %')
        
        print('\nCorrelation Between Assets\n')
        print(self.data.corr())
        
        print('\nSharpe Rate')
        
        for i in self.data:
            
            average = self.data[i].mean()
            std = self.data[i].std()
            sharpe_rate = (average-risk_free_rate)/std
            
            if sharpe_rate >= 0:
                print(f'Shape Rate:{i} = {round(sharpe_rate,5)}')
            else:
                print(f'Shape Rate:{i} = Undefined')
                
        positions = list(positions)
        
        x = 0
        positions_2 = []
        for index,asset in enumerate(self.data): 
            
            a = positions[index] * self.data_2[asset].iloc[-1]
            positions_2.append(a)
            
        for index,asset in enumerate(self.data):
            
            self.data[asset] = positions_2[index] * self.data[asset]
        
        self.data['Portfolio'] = self.data.sum(axis = 1)
        
        print('\nSTOCK PORTFOLIO INFORMATION')
        self.data.dropna(how='any', inplace=True)
        
        print('\nAverage Return')
        print(round(self.data['Portfolio'].mean(),2))
        print('\nVolatility')
        print(round(self.data['Portfolio'].std(),2))
        print('\nValue - at - Risk (95%)')
        print(round(self.data['Portfolio'].mean()+self.data['Portfolio'].std()* (- norm.ppf(0.95)),2))

if __name__ == "__main__":
    analytics = AssetsAnalytics(asset = ['MGLU3.SA','AMER3.SA'],start = '2022-01-28',end = '2023-01-28')
    analytics.Show()
    analytics.Seasonality()
    analytics.Benchmarking()
    analytics.Volatility()
    analytics.Asset_Portfolio_Return(positions=[1,1])
