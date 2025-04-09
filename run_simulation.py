from scipy.stats import norm, gaussian_kde
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np

from lead_time import LeadTime
from Stock import Stock

list_product = [
    {
        'store': '01',
        'product': 'H7',
        'lt_store_mean': 3,
        'lt_store_std': 0.7,
        'lt_store_data': 150,
        
        'lt_supplier_mean': 30,
        'lt_supplier_std': 15,
        'lt_supplier_data': 50,
        
        'ini_data': datetime(2019, 1, 1),   
        'sim_time': 1460,
        'mean_dem': 50,
        'std_dem': 10,
        'weekly_seanonality': 0.05,
        'monthly_seanonality': 0.1,
        'yearly_seanonality': 0.2,
        'relaxation': 130000,
        'prct_saturday': 0.6,
        'holidays': True,
        'dem_sunday': False,
        'promotions': True,
    },
    {
        'store': '01',
        'product': 'H4',
        'lt_store_mean': 3,
        'lt_store_std': 0.8,
        'lt_store_data': 150,
        
        'lt_supplier_mean': 15,
        'lt_supplier_std': 10,
        'lt_supplier_data': 50,
        
        'ini_data': datetime(2019, 1, 1),   
        'sim_time': 1460,
        'mean_dem': 120,
        'std_dem': 20,
        'weekly_seanonality': 0.01,
        'monthly_seanonality': 0.4,
        'yearly_seanonality': 0.1,
        'relaxation': 150000,
        'prct_saturday': 0.4,
        'holidays': True,
        'dem_sunday': False,
        'promotions': True,
    },
    {
        'store': '02',
        'product': 'P32',
        'lt_store_mean': 3,
        'lt_store_std': 0.7,
        'lt_store_data': 150,
        
        'lt_supplier_mean': 30,
        'lt_supplier_std': 15,
        'lt_supplier_data': 50,
        
        'ini_data': datetime(2019, 1, 1),   
        'sim_time': 1460,
        'mean_dem': 0,
        'std_dem': 1,
        'weekly_seanonality': 0.01,
        'monthly_seanonality': 0.1,
        'yearly_seanonality': 0.1,
        'relaxation': 130000,
        'prct_saturday': 1,
        'holidays': True,
        'dem_sunday': False,
        'promotions': True,
    },
    {
        'store': '02',
        'product': 'P57',
        'lt_store_mean': 5,
        'lt_store_std': 0.7,
        'lt_store_data': 150,
        
        'lt_supplier_mean': 30,
        'lt_supplier_std': 15,
        'lt_supplier_data': 50,
        
        'ini_data': datetime(2019, 1, 1),   
        'sim_time': 1460,
        'mean_dem': 72,
        'std_dem': 5,
        'weekly_seanonality': 0.1,
        'monthly_seanonality': 0.02,
        'yearly_seanonality': 0.05,
        'relaxation': 90000,
        'prct_saturday': 0.2,
        'holidays': True,
        'dem_sunday': False,
        'promotions': True,
    }
    ]

def main():
    pct = 95
    N = 1000
    
    dtype = {
    'date': 'str',  
    'store': 'str',  
    'product': 'str',  
    'real_demand': 'float',  
    'predicted_demand': 'float'  
    }
    
    df = pd.read_csv('predictions.csv', dtype=dtype)
    
    lead_time = [{
                'product': product['product'], 
                'store': product['store'], 
                'percentile': np.percentile(LeadTime(product['lt_supplier_mean'], product['lt_supplier_std'], N).
                                        add_distribution(LeadTime(product['lt_store_mean'], 
                                        product['lt_store_std'], N), N).data, pct)
                 }
                 for product in list_product]    
    
    df_lead = pd.DataFrame(lead_time)
    
    df = df.merge(df_lead, on=['product', 'store'])
    
    df['date'] = pd.to_datetime(df['date'])
    
    df['lead_date'] = df['date'] + pd.to_timedelta(df['percentile'], unit='D')

    df = df.sort_values(by=['product', 'store', 'date']).reset_index(drop=True)

    predicted_demand_shifted = []

    stocks = {}

    for (product, store), group in df.groupby(['product', 'store']):
        # Calcular o shift usando o valor de percentile do primeiro item do grupo
        shift_value = int(group.iat[0, -2])

        # Aplicar o shift no predicted_demand
        group['demand_lead'] = group['predicted_demand'].shift(-shift_value, fill_value=0)
        # Adicionar o grupo processado à lista de resultados
        predicted_demand_shifted.append(group)

        stocks[product] = Stock(
                product=product,
                store= store,
                stock= shift_value * sum([prod['mean_dem'] for prod in list_product 
                                          if prod['store'] == store and prod['product'] == product])
            )

    df = pd.concat(predicted_demand_shifted).reset_index(drop=True)
    
    stock_data = {'P32': [], 'P57': [], 'H4': [], 'H7': []}
    
    for date in df['date'].unique():
        for index, row in df[df['date'] == date].iterrows():
            virtual_stock = (curr_stock := stocks[row['product']]).check_arrival_stock(date, row['lead_date']) 
            stock = curr_stock.stock + virtual_stock
            
            curr_stock.arrival(date)
            
            stock_data[row['product']].append(curr_stock.stock)
            
            sum_demand = df[(df['product'] == row['product']) & 
                            (df['store'] == row['store']) &
                            (df['date'] <= row['lead_date']) &
                            (df['date'] >= date)]['predicted_demand'].sum()
            
            
            missing = stock - sum_demand
            
            product = [prod for prod in list_product if prod['product'] == row['product'] and row['store'] == prod['store']][0]
            
            if missing < 0:
                curr_stock.order(row['lead_date'], 
                                row['date'] + pd.to_timedelta(LeadTime(product['lt_supplier_mean'], product['lt_supplier_std'], 1).data[0] + LeadTime(product['lt_store_mean'], product['lt_store_std'], 1).data[0], unit='days'),
                                -round(missing)
                                )
               
            curr_stock.sell(row['real_demand'])
            
    for name, stock in stocks.items():
        sell = 0
        arrival = 0
        for log in stock.log:
            if log['type'] == 'sell':
                sell += log['missing']
            if log['type'] == 'arrival':
                arrival += log['arrival']
        print(name)
        print(sell)
        print(arrival)
        print()
        
    for name, data in stock_data.items():
        plt.plot([i for i in range(len(data))], data, label=name)
    plt.legend()
    plt.show()
    
    plt.plot([i for i in range(len(data))][40:  ], stock_data['P32'][40:  ], label='P32')
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    main()