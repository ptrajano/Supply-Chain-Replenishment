from datetime import datetime, timedelta
from seasonality import GenerateDemand
from typing import List, Type, Dict
from dataclasses import dataclass
from lead_time import LeadTime

@dataclass
class Product:
    def __init__(self,
                product: str,
                store: str,
                lt_store_mean: float,
                lt_store_std: float,
                lt_store_data: int,
                lt_supplier_mean: float,
                lt_supplier_std: float,
                lt_supplier_data: int,
                ini_data: datetime,
                sim_time: int,
                mean_dem: float,
                std_dem: float,
                weekly_seanonality: float,
                monthly_seanonality: float,
                yearly_seanonality: float,
                relaxation: float,
                prct_saturday: float,
                holidays: bool,
                dem_sunday: bool,
                promotions: bool,
                 ) -> None:
        self.product = product
        self.store = store
        
        # DATA LEAD TIME DISTRIBUTION CENTER TO STRORE
        self.lt_store_mean = lt_store_mean
        self.lt_store_std = lt_store_std
        self.lt_store_tot = lt_store_data
        
        # DATA LEAD TIME SUPPLIER TO DISTRIBUTION CENTER
        self.lt_supplier_mean = lt_supplier_mean
        self.lt_supplier_std = lt_supplier_std
        self.lt_supplier_tot = lt_supplier_data
        
        # DATA GENERATE DEMAND
        self.ini_data = ini_data
        self.sim_time = sim_time
        self.mean_dem = mean_dem
        self.std_dem = std_dem
        self.weekly_seanonality = weekly_seanonality
        self.monthly_seanonality = monthly_seanonality
        self.yearly_seanonality = yearly_seanonality
        self.relaxation = relaxation
        self.prct_saturday = prct_saturday
        self.holidays = holidays
        self.dem_sunday = dem_sunday
        self.promotions = promotions

    def generate_demand(self):
        self._demand = GenerateDemand(
            self.ini_data,
            self.sim_time,
            self.mean_dem,
            self.std_dem,
            self.weekly_seanonality,
            self.monthly_seanonality,
            self.yearly_seanonality,
            self.relaxation,
            self.prct_saturday,
            self.holidays,
            self.dem_sunday,
            self.promotions
        )
        
    def generate_lead_times(self, N = 10000):
        self.supplier = LeadTime(
            self.lt_supplier_mean,
            self.lt_supplier_std,
            self.lt_supplier_tot
        )
        
        self.store = LeadTime(
            self.lt_store_mean,
            self.lt_store_std,
            self.lt_store_tot
        )
        
        self.total = self.store.add_distribution(self.supplier, N)
        
    @property
    def demand(self):
        if not hasattr(self, '_demand'):
            self.generate_demand()
        return self._demand.dates, self._demand.demand
    
    
    def lead_time(self, type = 'total'):
        if type not in ['total', 'supplier', 'store']:
            raise ValueError(f'Invalid Lead Time Type: {type}')
        if not hasattr(self, type):
            self.generate_lead_times()
        
        return getattr(self, type).data
