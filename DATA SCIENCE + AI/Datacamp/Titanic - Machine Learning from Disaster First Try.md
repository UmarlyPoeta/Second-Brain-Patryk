```
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# === Import danych ===
train_df = pd.read_csv("/kaggle/input/titanic/train.csv")
test_df = pd.read_csv("/kaggle/input/titanic/test.csv")

# === Czyszczenie i wstępne przetwarzanie ===

def preprocess_data(df, is_train=True):
    # Uzupełnianie braków
    df["Age"] = df["Age"].fillna(df["Age"].mean())
    df["Fare"] = df["Fare"].fillna(df["Fare"].mean())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    
    # Usuwamy zbędne kolumny
    drop_cols = ["Name", "Ticket", "Cabin"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])
    
    # One-hot encoding dla kolumn kategorycznych
    df = pd.get_dummies(df, columns=["Sex", "Embarked"], drop_first=True)
    
    if is_train:
        X = df.drop("Survived", axis=1)
        y = df["Survived"]
        return X, y
    else:
        return df

# Przetwarzanie danych
X_train, y_train = preprocess_data(train_df, is_train=True)
X_test = preprocess_data(test_df, is_train=False)

# === Model ===
model = DecisionTreeClassifier(random_state=42, max_depth=5)
model.fit(X_train, y_train)

# === Ewaluacja na zbiorze treningowym ===
y_pred_train = model.predict(X_train)
print("Accuracy (train):", accuracy_score(y_train, y_pred_train))

# === Predykcja na zbiorze testowym ===
predictions = model.predict(X_test)

# === Przygotowanie submission.csv ===
submission = pd.DataFrame({
    "PassengerId": test_df["PassengerId"],
    "Survived": predictions
})
submission.to_csv("submission.csv", index=False)
print("Plik submission.csv zapisany!")

```