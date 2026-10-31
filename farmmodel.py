import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import joblib

# 1. Load data
data = pd.read_csv("farm.csv")

x = data.drop(columns= ("farm_id","yield_q_per_ha" ), axis=1)
y = data['yield_q_per_ha']

# 2. Train-Test Split (80% train, 20% test)
Xtrain, Xtest, Ytrain, Ytest = train_test_split(x, y, test_size=0.2, random_state=1485)

# 3. Feature Scaling
scaler = StandardScaler()
Xtrain_scaled = scaler.fit_transform(Xtrain)
Xtest_scaled = scaler.transform(Xtest)

# 4. Model Architecture
model = Sequential([
    Input(shape=(Xtrain.shape[1],)),  # Dynamically matches feature count (29)
    Dense(30, activation='relu'),
    Dense(15, activation='relu'),
    Dense(1, activation='linear')
])

# 5. Compile with Regression Loss & Metrics
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

# 6. Fit Model
model.fit(Xtrain_scaled, Ytrain, epochs=300, batch_size=32, verbose=1)

# 7. Evaluate on Test Set
test_loss, test_mae = model.evaluate(Xtest_scaled, Ytest)
print(f"Test MAE: {test_mae:.4f}")

# 8. Predict on New Sample (Must scale input before predicting)
sample_data = np.array([[18, 16, 2, 3, 1, 1, 3, 2, 0, 0.22, 7.17, 0.6, 179.9, 33.1, 
                         184.5, 28.1, 29.4, 67.7, 72.1, 9.6, 4, 125, 33.7, 128.6, 
                         4.2, 2.78, 21, 155.3, 1]])

sample_data_scaled = scaler.transform(sample_data)
predictedY = model.predict(sample_data_scaled)

print("Predicted Yield:", predictedY[0][0])


joblib.dump(model, "trainedmodel.joblib")