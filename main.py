import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import os
import datetime

# Specify the directory you want to iterate through
indices_folder = 'market-indices'

# Loop through each file in the directory
for file_name in os.listdir(indices_folder):
    file_path = os.path.join(indices_folder, file_name)
    if not os.path.isfile(file_path): continue
    print(f'Processing file: {file_name}')

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


    unique_drops = market_index[['All_Time_High','Drop_5_Percent']] \
                   .drop_duplicates(keep='first')
    unique_drops = unique_drops[unique_drops['Drop_5_Percent'] == True]
    unique_drops = unique_drops.merge(market_index, on='Date', how='inner')

    # calculating for each drop how much investing in the index
    # considering that the paycheck is received every 28 days
    operations = {}
    prev_date = market_index.index[0] # day of start working, 
                                      # first salary in 28 days
    for index, row in unique_drops.iterrows():
        distance = (index - prev_date).days
        if distance > 28: # salary every 4 weeks
            # operation is a dict where keys are dates and values and 
            # (price, num of salaries accumulated during the last period)
            operations[index] = (row['Price'], int(distance / 28))
            prev_date = index - datetime.timedelta(days=distance % 28)

    # sum adds how much each operation have valuated till the end  
    market_timing = 0
    for key in operations:
        market_timing += last_price / operations[key][0] * operations[key][1]

    unused_salaries = int((last_date - prev_date).days / 28)

    print('market timing / dca = ' + str(market_timing / dca))
    print('unused salaries in market timing = ', unused_salaries)

    # Plotting both datasets
    plt.figure(figsize=(14, 7))
    plt.plot(market_index.index, market_index['Price'], label=file_name, color='blue')
    plt.plot(unique_drops.index, unique_drops['Price'], 'r.', markersize=10, label='5% Drop from All-Time High')
    # plt.plot(first_day_of_month, market_index.loc[first_day_of_month,'Price'], 'g.', markersize=10, label='5% Drop from All-Time High')
    plt.title(file_name)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()