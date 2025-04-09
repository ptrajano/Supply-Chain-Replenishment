import matplotlib.pyplot as plt
from datetime import datetime
from Product import Product
import pandas as pd

"""
DATE
STORE
PRODUCT
DEMAND
"""

if __name__ == '__main__':
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
    """
    dict_product = {
        'lt_store_mean': 3,
        'lt_store_std': 0.7,
        'lt_store_data': 150,
        
        'lt_supplier_mean': 30,
        'lt_supplier_std': 15,
        'lt_supplier_data': 50,
        
        'ini_data': datetime(2019, 1, 1),   
        'sim_time': 400,
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
    }
    """
    products = [Product(**dict_product) for dict_product in list_product]
    #product = Product(**dict_product)
    
    #store = '03'
    #name_product = 'H32-9'
    #date, demand = product.demand
    
    #plt.plot(date, demand)
    #plt.show()
    
    list_data = [
        {
            'date': product.demand[0][i],
            'store': product.store,
            'product': product.product,
            'demand': product.demand[1][i],
        }
        for product in products
        for i in range(len(product.demand[0]))
    ]
    
    pd.DataFrame(list_data).to_pickle('demand.pkl')