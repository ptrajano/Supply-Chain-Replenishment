from Product import Product, Products
from Distribution import Distribution
from Stock_Prediction import ARIMA, MLPRegressor
from simulation.Day import Day

from typing import List, Type, Callable, Union, Any, Tuple
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from functools import wraps
from scipy import stats
from abc import ABC
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler


DAYS = 100

def new_stock(product: Type[Product], movement: int) -> int:
    mean = product.stock
    std = product.stock
    
    if not product.history.empty:
        mean = product.history['buy'].mean()
        std = product.history['buy'].std()  
        
        std = 0 if pd.isna(std) else std
    
    return max(
        (mean + 2 * std) // 1 + 1,
        product.stock - movement
        )

def normal_movement(product: Type[Product]) -> int:
    return min(max(np.random.normal(product.mean, product.std), 0) // 1,
                        product.stock)



def generate_sample(kde: Type[Distribution]) -> Callable[[Any], int]:

    def decorador(foo: Callable[[Any], int]) -> Callable[[Any], int]:

        @wraps(foo)
        def wrapper(*args, **kwrds) -> int:
            return min(foo(*args, **kwrds), kde.sample_data(1)[0])

        return wrapper

    return decorador

def generate_data(kde: Type[Distribution]) -> Callable[[Type[Product]], int]:

    @generate_sample(kde)
    def product_stock(product: Type[Product]) -> int:

        return product.stock

    return product_stock


    
def base_data(foo_stock: Callable[[Product, int], int], products: Type[Products]) -> None:
    a = Day(foo_stock = foo_stock, 
            foo_movement = normal_movement,
            products = products)
    
    for _ in range(DAYS):
        a()

def main() -> None:
    products = Products()
    
    products_list = [
            {
        'name': 'PASSD',
        'stock': 10,
        'mean': 2.3,
        'std': 7,
        },
        {
        'name': 'WASD',
        'stock': 50,
        'mean': 45,
        'std': 10,
        }
    ]
    
    for product in products_list:
        products.append(Product(**product)) 
    
    base_data(new_stock, products)
    
    history = products[0].history.sort_values(by='date')
    
    X = history[['stock']].values  # Recurso (stock)
    y = history['buy'].values
    
    scaler_X = MinMaxScaler()
    X_normalized = scaler_X.fit_transform(X.reshape(-1, 1))

    # 2. Instanciar e treinar o modelo MLPRegressor
    mlp_regressor = MLPRegressor(input_size=1, hidden_size=10, output_size=1, learning_rate=0.01)
    mlp_regressor.fit(X_normalized, y, epochs=100)

    # 3. Usar o modelo treinado para prever a distribuição do "buy"
    predictions = mlp_regressor.predict_stock(X_normalized)

    # 4. Visualizar a distribuição prevista em comparação com a distribuição real
    plt.figure(figsize=(10, 6))
    plt.hist(y, bins=20, color='skyblue', edgecolor='black', alpha=0.7, label='Real')
    plt.hist(predictions, bins=20, color='orange', edgecolor='black', alpha=0.7, label='Previsto')
    plt.title('Distribuição Real vs. Distribuição Prevista do "buy"')
    plt.xlabel('Valor de "buy"')
    plt.ylabel('Frequência')
    plt.legend()
    plt.grid(True)
    plt.show() 
    #next_buy = generate_data(kde)
    
    #products_forecast = Products()
    
    #for product in products_list:
    #    products_forecast.append(Product(**product))
    
    #a = Day(
    #        foo_stock = new_stock,
    #        foo_movement = next_buy,
    #        products = products_forecast
    #        )
    
    #for _ in range(DAYS):
    #    a()
    #
    #plt.plot(products[0].history['date'], products[0].history['buy'])
    #plt.plot(products[0].history['date'], products[0].history['stock'], '--')
    #
    #plt.show()
    #
    #plt.plot(products_forecast[0].history['date'], products_forecast[0].history['buy'])
    #plt.plot(products_forecast[0].history['date'], products_forecast[0].history['stock'], '--')
    #
    #plt.show()
    
    
if __name__ == "__main__":
    main()