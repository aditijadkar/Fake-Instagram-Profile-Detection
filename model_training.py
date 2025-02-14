# model_training.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("train.csv")

data.rename(columns={
    "profile pic": "profile_pic",
    "nums/length username": "nums_length_username",
    "fullname words": "fullname_words",
    "nums/length fullname": "nums_length_fullname",
    "name==username": "name_equals_username",
    "description length": "description_length",
    "external URL": "external_url",
    "#posts": "posts",
    "#followers": "followers",
    "#follows": "following", 
    "fake": "is_fake"
}, inplace=True)

#Select features (match them with your scraping code)
features = [
    "profile_pic",
    "nums_length_username",
    "fullname_words",
    "nums_length_fullname",
    "name_equals_username",
    "description_length",
    "external_url",
    "private",
    "posts",
    "followers",
    "following"
]
X = data[features]
y = data["is_fake"]  # 0 = genuine, 1 = fake/spam

#Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Train multiple models
svm_model = SVC(probability=True, random_state=42)
rf_model = RandomForestClassifier(random_state=42)
gb_model = GradientBoostingClassifier(random_state=42)

svm_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)
gb_model.fit(X_train, y_train)

#Evaluate models
svm_acc = accuracy_score(y_test, svm_model.predict(X_test))
rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
gb_acc = accuracy_score(y_test, gb_model.predict(X_test))

print(f"SVM Accuracy: {svm_acc}")
print(f"RF Accuracy:  {rf_acc}")
print(f"GB Accuracy:  {gb_acc}")

#Select best model
best_model, best_acc = max(
    [(svm_model, svm_acc), (rf_model, rf_acc), (gb_model, gb_acc)],
    key=lambda x: x[1]
)

print(f"Best model: {type(best_model).__name__} with accuracy {best_acc}")

#Save the best model
joblib.dump(best_model, "models/fake_detector.pkl")
print("Best model saved successfully!")
