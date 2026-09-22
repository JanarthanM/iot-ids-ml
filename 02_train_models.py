import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Load synthetic dataset
df = pd.read_csv('synthetic_iot_traffic.csv')
X = df.drop('label', axis=1)
y = df['label']

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Initialize and train Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate model performance
preds = clf.predict(X_test)
print("--- Classification Report ---")
print(classification_report(y_test, preds))

# Serialize and save trained model
joblib.dump(clf, 'ids_model.pkl')
print("✅ Model trained and saved as ids_model.pkl!")
