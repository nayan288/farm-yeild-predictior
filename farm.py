import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Input
import numpy as np


data = pd.read_csv("farm.csv")

x = data.drop('yield_q_per_ha',axis = 1)
y = data['yield_q_per_ha']

Xtrain,Xtest,Ytrain,Ytest = train_test_split(x,y,train_size=0.8,random_state=1485)

model = Sequential([Input (shape=(29,)),Dense(30, activation='relu'),Dense(15, activation='relu'),Dense(1,activation='linear')])

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

model.fit(Xtrain,Ytrain,epochs=300,verbose=1)

data = np.array([[18,16,2,3,1,1,3,2,0,0.22,7.17,0.6,179.9,33.1,184.5,28.1,29.4,67.7,72.1,9.6,4,125,33.7,128.6,4.2,2.78,21,155.3,1]])

predictedYtest = model.predict(data)

print(predictedYtest)