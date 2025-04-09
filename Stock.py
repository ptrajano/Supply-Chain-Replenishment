import datetime

class Stock:
    def __init__(self,
                 store: str,
                 product: str,
                 stock: int) -> None:
        self.store = store
        self.product = product
        
        self.stock = stock
        self.virutal_stock = []
        
        self.log = []
        
    def order(self, predicted_arrival: str, real_arrival: str , size: int) -> None:
        self.log.append({
            'type': 'virtual stock',
            'size': size,
            'predicted_date': predicted_arrival,
            'real_date':  real_arrival
        })
        self.virutal_stock.append({
            'stock': size,
            'predicted_date': predicted_arrival,
            'real_date':  real_arrival
            })
        
    def arrival(self, date: str) -> None:
        self.log.append({
            'type': 'arrival',
            'date': date,
            'old stock': self.stock,
            'arrival': sum([stock['stock'] 
                           for stock in self.virutal_stock 
                           if stock['real_date'] == date]),
        })
        self.stock += sum([stock['stock'] 
                           for stock in self.virutal_stock 
                           if stock['real_date'] == date])
        
    def sell(self, size: int) -> None:
        self.log.append({
            'type': 'sell',
            'old stock': self.stock,
            'new stock': self.stock - (size if size < self.stock else self.stock),
            'missing': size - self.stock if size > self.stock else 0 
        })
        self.stock -= size if size < self.stock else self.stock     
        
    def check_arrival_stock(self, start_date: str, end_date: str) -> int:
        return sum([stock['stock']
                    for stock in self.virutal_stock
                    if stock['real_date'] <= end_date 
                    and stock['real_date'] >= start_date])
        
    def __eq__(self, product: str, store: str) -> bool:
        return self.product == product and self.store == store