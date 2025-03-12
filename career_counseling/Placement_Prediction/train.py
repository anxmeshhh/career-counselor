# train.py

# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# ✅ Load the fixed dataset
file_path = 'cleaned_dataset_fixed.csv'
df = pd.read_csv(file_path)

# ✅ Encode categorical variables
le_gender = LabelEncoder()
le_stream = LabelEncoder()

df['Gender'] = le_gender.fit_transform(df['Gender'])
df['Stream'] = le_stream.fit_transform(df['Stream'])

# ✅ Split into features and target
X = df.drop('PlacedOrNot', axis=1)
y = df['PlacedOrNot']

# ✅ Split into training and testing sets (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

# ✅ Predict on test set
y_pred = rf_model.predict(X_test)

# ✅ Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)

# ✅ Display Results
print(f"\n🔥 Model Accuracy: {accuracy * 100:.2f}%\n")
print("📊 Classification Report:\n", report)
print("🎯 Confusion Matrix:\n", confusion)

# ✅ Save the model
with open('placement_model.pkl', 'wb') as model_file:
    pickle.dump(rf_model, model_file)

print("\n✅ Model saved as 'placement_model.pkl'")
