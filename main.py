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

    # print(market_index.head())

    # Calculate the rolling maximum (all-time high) to each point
    market_index['All_Time_High'] = market_index['Price'].cummax()

    # Considering every 4 weeks we receive the paycheck variables holds
    # how many salaries were received during the whole period.
    # = (last day - first day) / 28 days
    num_of_salaries = \
        int((market_index.index[-1] - market_index.index[0]).days / 28)

    # last price of the index
    last_price = market_index.iloc[-1][['Price']].to_numpy()

    # Identify points where the price dropped 5%, 10%, 15% and 20%
    # market_index.astype({'Price': 'float32'})
    market_index['Drop_5_Percent'] = \
        market_index['Price'] <= (market_index['All_Time_High'] * 0.90)
    # market_index['Drop_10_Percent'] = \
    #     market_index['Price'] <= (market_index['All_Time_High'] * 0.90)
    # market_index['Drop_15_Percent'] = \
    #     market_index['Price'] <= (market_index['All_Time_High'] * 0.85)
    # market_index['Drop_20_Percent'] = \
    #     market_index['Price'] <= (market_index['All_Time_High'] * 0.80)
    
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
            operations[index] = (row['Price'], int(distance / 28))
            prev_date = index - datetime.timedelta(days=distance % 28)

    sum = 0
    for key in operations:
        sum += last_price / operations[key][0] * operations[key][1]

    print('ett', sum / num_of_salaries - 1)

    prev_date = market_index.index[0]
    del operations
    operations = {}
    for index, row in market_index.iterrows():
        distance = (index - prev_date).days
        if distance > 28: # salary every 4 weeks
            operations[index] = (row['Price'], int(distance / 28))
            prev_date = index

    sum = 0
    for key in operations:
        sum += last_price / operations[key][0] * operations[key][1]

    print('tva', sum / num_of_salaries - 1)

    dates = pd.Series(market_index.index)
    first_day_of_month = dates.groupby([dates.dt.year, dates.dt.month]).min().reset_index(drop=True)
    # relationship = last_day_price / market_index.loc[first_day_of_month,'Price']

    # print(relationship)
    # print(relationship.sum())
    # print(relationship.size)
    
    # print(relationship.sum() / relationship.size - 1)

    # print(market_index.index.to_period('M').unique())

    # pd.DataFrame(market_index.index).to_csv('diobono.csv')

    # first_days = market_index.index.to_period('M').to_timestamp().drop_duplicates()

    # print(first_days)

    # Plotting both datasets
    plt.figure(figsize=(14, 7))
    plt.plot(market_index.index, market_index['Price'], label='FTSE All World Index', color='blue')
    plt.plot(unique_drops.index, unique_drops['Price'], 'r.', markersize=10, label='5% Drop from All-Time High')
    plt.plot(first_day_of_month, market_index.loc[first_day_of_month,'Price'], 'g.', markersize=10, label='5% Drop from All-Time High')
    plt.title('FTSE All World Index')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()


    # plt.show()