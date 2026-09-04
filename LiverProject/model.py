import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import joblib

# Load dataset
url = "Indian Liver Patient Dataset (ILPD).csv"

columns = [
'Age','Gender','Total_Bilirubin','Direct_Bilirubin',
'Alkaline_Phosphotase','Alamine_Aminotransferase',
'Aspartate_Aminotransferase','Total_Protiens',
'Albumin','Albumin_and_Globulin_Ratio','Dataset'
]

df = pd.read_csv(url, names=columns)

# Preprocessing
df['Gender'] = df['Gender'].map({'Male':1, 'Female':0})

df['Albumin_and_Globulin_Ratio'] = df['Albumin_and_Globulin_Ratio'].fillna(
    df['Albumin_and_Globulin_Ratio'].mean()
)

df['Dataset'] = df['Dataset'].map({1:1, 2:0})

# Remove missing values
df = df.dropna()

# Split
X = df.drop('Dataset', axis=1)
y = df['Dataset']

# Balance data
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = XGBClassifier()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, "liver_model.pkl")

print("Model saved successfully!")

