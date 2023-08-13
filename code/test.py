import code

assets = code.AssetsAnalytics(asset = ['MGLU3.SA','AMER3.SA'],start = '2022-01-28',end = '2023-01-28') # Y/M/D
print(assets.Show())
print('\n')
print(assets.Seasonality()) 
print('\n')
print(assets.Volatility())
print('\n')
print(assets.Benchmarking())
print('\n')
print(assets.Asset_Portfolio_Return(positions=[1,1]))
print('\n')
