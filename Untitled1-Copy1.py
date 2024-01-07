#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install keras')


# In[4]:


get_ipython().system('pip install tensorflow')


# In[5]:


# 필요한 라이브러리 설치
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import LSTM, Dense

# 데이터 불러오기
data_path = r'C:\Users\wrwqr\Downloads\kosPI (2).csv'
df = pd.read_csv(data_path)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# 데이터 시각화
plt.figure(figsize=(10, 6))
plt.plot(df['Close'])
plt.title('KOSPI Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.show()

# 데이터 전처리
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

training_data_len = int(np.ceil(len(scaled_data) * .95))  # 95% 데이터를 훈련에 사용

train_data = scaled_data[0:int(training_data_len), :]

# 데이터 생성 함수
def create_dataset(dataset, time_step=1):
    data_x, data_y = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        data_x.append(a)
        data_y.append(dataset[i + time_step, 0])
    return np.array(data_x), np.array(data_y)

time_step = 1
X_train, y_train = create_dataset(train_data, time_step)

# 데이터를 LSTM 모델에 맞게 reshape
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 훈련
model.fit(X_train, y_train, epochs=10, batch_size=1)

# 테스트 데이터 생성
test_data = scaled_data[training_data_len - time_step:, :]

# 테스트 데이터를 LSTM 모델에 맞게 reshape
X_test, y_test = create_dataset(test_data, time_step)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# 예측
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# 평가
rmse = np.sqrt(np.mean(np.power((y_test - predictions), 2)))
print("Root Mean Squared Error (RMSE):", rmse)

# 실제값과 예측값 시각화
train = df[:training_data_len]
valid = df[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price (KOSPI)')
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Validation', 'Predictions'])
plt.show()

