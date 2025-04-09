from scipy.stats import norm, gaussian_kde
import numpy as np

class LeadTime:
    def __init__(self,
                 mean,
                 std,
                 tot):
        self.mean = mean,
        self.std = std,
        self.tot = tot,
        
        self.generate_new_data()
    
    def generate_new_data(self):
        self.data = np.ceil(np.absolute(np.random.normal(self.mean, self.std, self.tot))).astype(int)
        self._distribution =  Distribution(self.data)
        return self.data
    
    @property
    def distribution(self):
        return self._distribution.distribuition

    @property
    def distribution_cls(self):
        return self._distribution

    def add_distribution(self, otr, size = 100000):
        return self._distribution.add_distribution(otr.distribution_cls, size)

class Distribution:
    def __init__(self, data):
        self.data = data
        
    @property
    def distribuition(self):
        return norm(np.mean(self.data), np.std(self.data))
    
    def add_distribution(self, otr, size = 100000):
        return Distribution(MonteCarlo().generate_data(self.data, otr.data, size))

class MonteCarlo:
    @staticmethod
    def generate_data(list1, list2, size = 100000):
        return np.random.choice(list1, size=size) + np.random.choice(list2, size=size)



"""
import matplotlib.pyplot as plt
N = 1000

fornec = LeadTime(30, 7, N)
loja = LeadTime(3, 1, N)

tot_dist = fornec.add_distribution(loja, N)

x = np.linspace(0, max(tot_dist.data), 60)

#plt.plot(tot_dist.distribuition.pdf(x), label='Total')

plt.hist(tot_dist.data, label = 'Total')

plt.hist(fornec.data, label='Fornecedor')

plt.hist(loja.data, label='Loja')

#plt.plot(x, fornec.distribution.pdf(x), label='Fornecedor')
#plt.plot(x, loja.distribution.pdf(x), label='Loja')

plt.ylabel('Frequência')
plt.xlabel('Tempo')
plt.legend()
plt.show()

kde = gaussian_kde(tot_dist.data)
x_vals = np.linspace(min(tot_dist.data), max(tot_dist.data), 1000)

kde_vals = kde(x_vals)

percentil = np.percentile(tot_dist.data, 95)

print(f"O valor do percentil é {percentil}")

plt.plot(x_vals, kde_vals, label='KDE')
plt.axvline(percentil, color='r', linestyle='--', label=f'Percentil 95')
plt.legend()
plt.show()
"""