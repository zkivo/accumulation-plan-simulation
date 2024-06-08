from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import os
import gc
import datetime

# Specify the directory you want to iterate through
indices_folder = 'market-indices'

list_results = []

# Loop through each file in the directory
for file_name in os.listdir(indices_folder):
    file_path = os.path.join(indices_folder, file_name)
    if not os.path.isfile(file_path): continue
    print(f'\nProcessing file: {file_name}')

    list_results.append({'file_name': file_name})

    # Reading the csv file and store it in a pandas dataframe
    market_index = pd.read_csv(file_path)

    market_index['Date'] = pd.to_datetime(market_index['Date'], dayfirst=False)
    market_index.sort_values('Date', inplace=True)
    market_index.set_index('Date', inplace=True)

    # Calculate the rolling maximum (all-time high) to each point
    market_index['All_Time_High'] = market_index['Price'].cummax()
    
    # last price of the index
    last_price = market_index.iloc[-1][['Price']].to_numpy()
    last_date  = market_index.iloc[-1].name

    dca = 0
    prev_date = market_index.index[0] # day of start working, 
                                      # first salary in 28 days
    for index, row in market_index.iterrows():
        distance = (index - prev_date).days
        if distance > 28: # salary every 4 weeks
            dca += last_price / row['Price']
            prev_date = index - datetime.timedelta(days=distance % 28)

    # Identify points where the price dropped 5%, 10%, 15% and 20%
    # market_index.astype({'Price': 'float32'})
    market_index['Drop_5_Percent'] = \
        market_index['Price'] <= (market_index['All_Time_High'] * 0.95)
    market_index['Drop_10_Percent'] = \
        market_index['Price'] <= (market_index['All_Time_High'] * 0.90)
    market_index['Drop_15_Percent'] = \
        market_index['Price'] <= (market_index['All_Time_High'] * 0.85)
    market_index['Drop_20_Percent'] = \
        market_index['Price'] <= (market_index['All_Time_High'] * 0.80)

    list_drop_strings = ['Drop_5_Percent', 'Drop_10_Percent', 'Drop_15_Percent', 'Drop_20_Percent']

    # Preparing plot of the figure
    plt.figure(figsize=(14, 7))
    plt.plot(market_index.index, market_index['Price'], label=file_name, color='blue')
    for string in list_drop_strings:
        # print("\tresults for ", string)
        try:
            del unique_drops
            gc.collect() # garbage collector
        except:
            pass        
        try:
            del operations
            gc.collect() # garbage collector
        except:
            pass

        unique_drops = market_index[['All_Time_High',string]] \
                    .drop_duplicates(keep='first')
        unique_drops = unique_drops[unique_drops[string] == True]
        unique_drops = unique_drops.merge(market_index, on='Date', how='inner')

        # calculating for each drop how much investing in the index
        # considering that the paycheck is received every 28 days
        operations = {}
        prev_date = market_index.index[0] # day of start working, 
                                        # first salary in 28 days
        for index, row in unique_drops.iterrows():
            distance = (index - prev_date).days
            if distance > 28: # salary every 4 weeks
                # operation is a dict where keys are dates and values:
                # (price, num of salaries accumulated during the last period)
                operations[index] = (row['Price'], int(distance / 28))
                prev_date = index - datetime.timedelta(days=distance % 28)

        # sum adds how much each operation have valuated till the end  
        market_timing = 0
        for key in operations:
            market_timing += last_price / operations[key][0] * operations[key][1]

        unused_salaries = int((last_date - prev_date).days / 28)

        performance_strategy = round((((market_timing / dca) - 1) * 100)[0].item(), 2)

        # print(type(performance_strategy))

        # print('market timing / dca = ', str(performance_strategy), '%')
        # print('unused salaries in market timing = ', unused_salaries)

        list_results[-1][string] = {'mt / dca': performance_strategy,
                                    'unused_salaries' : unused_salaries}

        plt.plot(unique_drops.index, unique_drops['Price'], '.', markersize=10, label=string)
    # plt.plot(first_day_of_month, market_index.loc[first_day_of_month,'Price'], 'g.', markersize=10, label='5% Drop from All-Time High')
    plt.title(file_name)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

pprint(list_results)
plt.show()
