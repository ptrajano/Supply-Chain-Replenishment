import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

df = pd.read_pickle("C:/Users/Caio/Project_SIM/demand.pkl")

# Supondo que df já esteja definido e que a coluna 'date' esteja no formato datetime
# Se a coluna 'date' não estiver no formato datetime, é necessário convertê-la
df['date'] = pd.to_datetime(df['date'])

# Adicionando a coluna 'weekday' (dia da semana)
df['weekday'] = df['date'].dt.weekday  # 0=Monday, 1=Tuesday, ..., 6=Sunday

# Adicionando a coluna 'week' (semana do ano)
df['week'] = df['date'].dt.isocalendar().week

# Adicionando a coluna 'year' (ano)
df['year'] = df['date'].dt.year

# Exemplo de vetor holidays com datas no formato MM/DD
holidays = ["01/01", "01/12", "02/13", "02/29", "04/21", "05/01", "05/30", "05/31", "09/07", "10/12", "10/28", "11/02", "11/15", "11/20", "12/24", "12/25", "12/31",]  

# Criando uma nova coluna 'date_mmdd' com a data no formato MM/DD
df['date_mmdd'] = df['date'].dt.strftime('%m/%d')

# Criando a coluna 'holidays' com base na comparação com o vetor de feriados
df['holidays'] = df['date_mmdd'].isin(holidays).astype(int)

# Removendo a coluna auxiliar 'date_mmdd'
df = df.drop(columns=['date_mmdd'])

# Supondo que df já esteja definido e que a coluna 'date' esteja no formato datetime
df['date'] = pd.to_datetime(df['date'])

# Criando a coluna 'weekday' (dia da semana) se ainda não existir
if 'weekday' not in df.columns:
    df['weekday'] = df['date'].dt.weekday  # 0=Monday, 1=Tuesday, ..., 6=Sunday

# Criando a coluna 'saturday' (1 se sábado, 0 caso contrário)
df['saturday'] = (df['weekday'] == 5).astype(int)

# Criando a coluna 'sunday' (1 se domingo, 0 caso contrário)
df['sunday'] = (df['weekday'] == 6).astype(int)

# Adicionando lags (valores de demanda dos dias anteriores) e rolling windows (médias móveis)
df['lag_1'] = df.groupby(['store', 'product'])['demand'].shift(1)
df['lag_7'] = df.groupby(['store', 'product'])['demand'].shift(7)
df['lag_30'] = df.groupby(['store', 'product'])['demand'].shift(30)
df['rolling_mean_7'] = df.groupby(['store', 'product'])['demand'].transform(lambda x: x.rolling(window=7).mean())
df['rolling_mean_30'] = df.groupby(['store', 'product'])['demand'].transform(lambda x: x.rolling(window=30).mean())

# Tratando dados faltantes nas novas colunas (opcional, pode ser ajustado conforme necessário)
df = df.fillna(0)

# Função para criar uma RNN
def create_rnn(input_shape):
    model = Sequential()
    model.add(SimpleRNN(50, activation='relu', input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# Treinamento e validação do modelo para cada loja e produto
results = {}

for (store, product), group in df.groupby(['store', 'product']):
    # Ordenar por data
    group = group.sort_values(by='date')
    
    # Definir recursos (features) e rótulos (labels)
    features = ['weekday', 'week', 'year', 'saturday', 'sunday', 'holidays', 'lag_1', 'lag_7', 'rolling_mean_7']
    X = group[features].values
    y = group['demand'].values
    
    # Normalizar os dados
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))
    
    # Dividir em conjuntos de treinamento e teste
    train_size = int(len(group) * 0.8)
    X_train, X_test = X_scaled[:train_size], X_scaled[train_size:]
    y_train, y_test = y_scaled[:train_size], y_scaled[train_size:]
    
    # Remodelar X para (samples, time steps, features)
    X_train_reshaped = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test_reshaped = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
    
    # Criar e treinar o modelo
    model = create_rnn((X_train_reshaped.shape[1], X_train_reshaped.shape[2]))
    model.fit(X_train_reshaped, y_train, epochs=50, batch_size=32, validation_data=(X_test_reshaped, y_test), verbose=2)
    
    # Avaliar o modelo
    loss = model.evaluate(X_test_reshaped, y_test, verbose=0)
    
    # Salvar o resultado
    results[(store, product)] = {
        'model': model,
        'scaler_X': scaler_X,
        'scaler_y': scaler_y,
        'loss': loss
    }
    
    print(f'Store: {store}, Product: {product}, Test Loss: {loss}')

# Função para plotar a demanda real vs. prevista
def plot_demand(store, product, model_info, df):
    model = model_info['model']
    scaler_X = model_info['scaler_X']
    scaler_y = model_info['scaler_y']
    
    # Filtrar o DataFrame para a loja e produto específicos
    group = df[(df['store'] == store) & (df['product'] == product)]
    group = group.sort_values(by='date')
    
    # Definir recursos (features) e rótulos (labels)
    features = ['weekday', 'week', 'year', 'saturday', 'sunday', 'holidays', 'lag_1', 'lag_7', 'rolling_mean_7']
    X = group[features].values
    y = group['demand'].values
    
    # Normalizar os dados
    X_scaled = scaler_X.transform(X)
    y_scaled = scaler_y.transform(y.reshape(-1, 1))
    
    # Dividir em conjuntos de treinamento e teste
    train_size = int(len(group) * 0.8)
    X_train, X_test = X_scaled[:train_size], X_scaled[train_size:]
    y_train, y_test = y_scaled[:train_size], y_scaled[train_size:]
    
    # Remodelar X para (samples, time steps, features)
    X_test_reshaped = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
    
    # Prever os valores
    y_pred_scaled = model.predict(X_test_reshaped)
    
    # Desnormalizar os valores previstos e reais
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    y_test = scaler_y.inverse_transform(y_test)
    
    # Plotar os valores reais vs. previstos
    plt.figure(figsize=(12, 6))
    plt.plot(group['date'].values[train_size:], y_test, label='Demanda Real')
    plt.plot(group['date'].values[train_size:], y_pred, label='Demanda Prevista')
    plt.xlabel('Data')
    plt.ylabel('Demanda')
    plt.title(f'Demanda Real vs. Prevista para Loja: {store}, Produto: {product}')
    plt.legend()
    plt.show()

# Exemplo de como usar a função para uma combinação específica de loja e produto
store, product = list(results.keys())[0]
model_info = results[(store, product)]
plot_demand(store, product, model_info, df)
