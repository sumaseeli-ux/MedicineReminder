import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load Dataset
data = pd.read_csv("health.csv")

# Inputs
X = data[["Age", "BP", "Sugar", "BMI"]]

# Output
y = data["Risk"]

# Train Model
model = DecisionTreeClassifier()

model.fit(X, y)

# Save Model
joblib.dump(model, "health_model.pkl")

print("AI Model Trained Successfully!")
print("health_model.pkl created.")