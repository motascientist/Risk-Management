import numpy as np # Linear Algebra
import pandas as pd # Manipulate DataSets
import yfinance as yf # Import financial data
import plotly.express as px  # Plot interactive graphic
from scipy.stats import norm # Statistical inference

class AssetsAnalytics:
    
    def __init__(self, asset=['MXRF11.SA'], start='2019-01-01', end='2021-06-12'):
        
        self.asset = asset
        self.start = start
        self.end = end
        self.data = self.download_data()
        
    def download_data(self):
        data = yf.download(self.asset, start=self.start, end=self.end, progress=False)['Adj Close']
        data.dropna(inplace=True)
        return data

    def Show(self):
        print('First Five Lines')
        print(self.data.head())
        print('\nLast Five Lines')
        print(self.data.tail())
        
    def Seasonality(self):
        print(f'Percentage Variation between [{self.start} at {self.end}]')
        variation = (self.data.iloc[-1] - self.data.iloc[0]) / self.data.iloc[0]
        print(variation)
        self.data.dropna(inplace=True)
        vp = self.data.pct_change()
        x = vp.index
        
        for asset in vp.columns:
            graph_vol = px.line(vp, x=x, y=asset, title=f'Percentage Variation for {asset}')
            graph_vol.show()
        
    def Benchmarking(self):
        data = self.data.copy()
        data.dropna(inplace=True)     
        vp = data.pct_change()
    
        for asset in data.columns:
            vp[asset] = (1 + vp[asset]).cumprod()
        
        print('Value in reais (R$)')
        print(vp.tail(1), 'R$')
        
        for asset in vp.columns:
            vp[asset] = vp[asset] - 1
        
        print('\nValue in % (decimal)')
        print(vp.tail(1))
        x = vp.index
        
        graph = px.line(vp, x=x, y=vp.columns, title='Benchmarking')
        graph.show()
        
    def Volatility(self, window=30):
        self.window = window
        data = self.data.copy()
        var_per = data.pct_change()
                
        for asset in data.columns:
            var_per[asset] = var_per[asset].rolling(window=window).std() * np.sqrt(window)
            
        print('\nVolatility\n')
        print(data.std())
        x = var_per.index
        graph_vol = px.line(var_per, x=x, y=var_per.columns, title='Volatility')
        graph_vol.show() 
        
    def Asset_Portfolio_Return(self, positions=[1000], risk_free_rate=0.125, show=False):
        data = self.data.copy()
        data_2 = data.copy()
        
        x = 0
        for asset in data.columns:   
            data[asset] = data[asset] * positions[x]
            x += 1
        
        if show:
            print('Your Position in the Beginning')
            print('\n')
            print(data.head())
            print('Your Position at the end')
            print('\n')
            print(data.tail())
        
        data = data.pct_change()
        data.dropna(how='any', inplace=True)

        print('Average Return\n')
        for asset in data:
            print(f'{asset} = {round(data[asset].mean()*100,2)} %')
        print('\nVolatility')
        for asset in data:
            print(f'{asset} = {round(data[asset].std()*100,2)} %')
        
        print('\nCorrelation Between Assets\n')
        print(data.corr())
        
        print('\nSharpe Rate')
        
        for asset in data:
            average = data[asset].mean()
            std = data[asset].std()
            sharpe_rate = (average - risk_free_rate) / std
            
            if sharpe_rate >= 0:
                print(f'Sharpe Rate ({asset}) = {round(sharpe_rate, 5)}')
            else:
                print(f'Sharpe Rate ({asset}) = Undefined')
                
        positions = list(positions)
        
        x = 0
        positions_2 = []
        for asset in data: 
            a = positions[x] * data_2[asset].iloc[-1]
            positions_2.append(a)
            x += 1
            
        for index, asset in enumerate(data):
            data[asset] = positions_2[index] * data[asset]
        
        data['Portfolio'] = data.sum(axis=1)
        
        print('\nSTOCK PORTFOLIO INFORMATION')
        data.dropna(how='any', inplace=True)
        
        print('\nAverage Return')
        print(round(data['Portfolio'].mean(), 2))
        print('\nVolatility')
        print(round(data['Portfolio'].std(), 2))
        print('\nValue - at - Risk (95%)')
        print(round(data['Portfolio'].mean() + data['Portfolio'].std() * (-norm.ppf(0.95)), 2))

if __name__ == "__main__":
    analytics = AssetsAnalytics(asset = ['MGLU3.SA','AMER3.SA'],start = '2022-01-28',end = '2023-01-28')
    analytics.Show()
    analytics.Seasonality()
    analytics.Benchmarking()
    analytics.Volatility()
    analytics.Asset_Portfolio_Return(positions=[1,1])
