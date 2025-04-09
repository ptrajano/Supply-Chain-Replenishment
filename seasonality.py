from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import numpy as np

class GenerateDemand:
    def __init__(self, 
                 ini_data,
                 sim_time,
                 mean_dem,
                 std_dem,
                 weekly_seanonality = 0.05,
                monthly_seanonality = 0.1,
                yearly_seanonality = 0.2,
                relaxation = 13000,
                prct_saturday = 1,
                holidays = True,
                dem_sunday = False,
                promotions = True):
        
        self.ini_data = ini_data
        self.sim_time = sim_time
        self.mean_dem = mean_dem
        self.std_dem = std_dem
        
        self._prct_saturday = prct_saturday
        
        self._holiday_flag = holidays
        self._sunday_flag = dem_sunday
        self._promotion_flag = promotions
        
        self.param_weekly_seanonality =weekly_seanonality
        self.param_monthly_seanonality =monthly_seanonality
        self.param_yearly_seanonality =yearly_seanonality
        
        self._holidays = [
        "01/01", "12/02", "13/02", "14/02", "29/03", "21/04", "01/05",
        "30/05", "31/05", "07/09", "12/10", "28/10", "02/11", "15/11",
        "20/11", "30/11", "24/12", "25/12", "30/12", "31/12"
        ]

        self.relaxation_time = relaxation

        self._dates = [ini_data + timedelta(days=i) for i in range(sim_time)] 


        self.yearly_seanonality = mean_dem * (1 + self.param_yearly_seanonality * np.sin(2 * np.pi * np.arange(0, sim_time) / 7))

        self.monthly_seanonality = mean_dem * (1 + self.param_monthly_seanonality * np.sin(2 * np.pi * np.arange(0, sim_time) / 30))

        self.weekly_seanonality = mean_dem * (1 + self.param_weekly_seanonality * np.sin(2 * np.pi * np.arange(0, sim_time) / 365))


    @property
    def demand(self):
        demand = np.random.normal(loc=self.mean_dem, scale=self.std_dem, size=self.sim_time) + self.seasonality
        
        demand = np.array([demand[i] * np.exp(i/self.relaxation_time) for i in range(len(demand))])
        
        demand = np.ceil(np.abs(demand))
        
        conditions = {
            "promotion": lambda d, i, date: d[i] * 1.2 
                                    if self._promotion_flag and np.random.rand() < 5e-3 
                                    else d[i],
            "holiday": lambda d, i, date: 0 
                                    if self._holiday_flag and date.strftime("%d/%m") in self._holidays else d[i],
            "sunday": lambda d, i, date: 0 
                                    if date.weekday() == 6 and self._sunday_flag
                                    else d[i],
            "saturday": lambda d, i, date: d[i] * self._prct_saturday 
                                    if date.weekday() == 5 
                                    else d[i]
        }
        
        for i, date in enumerate(self.dates):
            for condition in conditions.values():
                demand[i] = condition(demand, i, date)
        
        """
        for i, data in enumerate(self.dates):
            if self._promotion_flag and np.random.rand() < 5e-3:
                demand[i] *= 1.2
                
            if self._holiday_flag and data.strftime("%d/%m") in self._holidays:
                demand[i] = 0
            
            if data.weekday() == 6 and self._sunday_flag:
                demand[i] = 0
            
            if data.weekday() == 5:
                demand[i] *= self._prct_saturday
        """     
        return demand                

    @property
    def seasonality(self):
        return self.monthly_seanonality + self.yearly_seanonality + self.weekly_seanonality

    @property
    def seasonality_monthly(self):
        return self.monthly_seanonality

    @property
    def seasonality_yearly(self):
        return self.yearly_seanonality

    @property
    def seasonality_weekly(self):
        return self.weekly_seanonality


    @property
    def dates(self):
        return self._dates
"""
dict_data = {
    'ini_data': datetime(2019, 1, 1),
    'sim_time': 365 * 2,
    'mean_dem': 50,
    'std_dem': 10,
    'weekly_seanonality': 0.005,
    'monthly_seanonality': 0.1,
    'yearly_seanonality': 0.2,
    'relaxation': 130000,
    'prct_saturday': 0.6,
    'holidays': False,
    'dem_sunday': False,
    'promotions': True,
}

data = GenerateDemand(**dict_data)

# Visualização
plt.figure(figsize=(10, 6))
plt.plot(data.dates, data.demand, label='Sazionalidade')
#plt.plot(data.dates, data.seasonality_yearly,  '-', label='Senoide Anual')
#plt.plot(data.dates, data.seasonality_monthly, '--', label='Senoide Mensal')
#plt.plot(data.dates, data.seasonality_weekly, '.', label='Senoide Semanal')
#plt.legend()
plt.grid(True)
plt.show()
"""