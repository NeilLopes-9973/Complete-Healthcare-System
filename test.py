import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
import lightgbm as lgb
import joblib  # To load the model
from sklearn.preprocessing import LabelEncoder

# Load the trained model and label encoders
model = joblib.load('model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Load your test dataset
test_data = pd.read_csv('Testing.csv')

# Drop unnecessary columns
test_data = test_data.drop(columns=['Unnamed: 133'], errors='ignore')

# Separate features (X) and target (y)
X_test = test_data.iloc[:, :-1]
y_test = test_data.iloc[:, -1]

# Apply label encoding using saved encoders
for column in X_test.select_dtypes(include=['object']).columns:
    if column in label_encoders:
        X_test[column] = label_encoders[column].transform(X_test[column])

# Encode target variable if it was encoded during training
if 'target' in label_encoders:
    y_test = label_encoders['target'].transform(y_test)

# Make predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # Get probability scores

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
auc_score = roc_auc_score(y_test, y_prob, multi_class='ovr')

# Print results
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Confusion Matrix:")
print(conf_matrix)
print(f"AUC Score: {auc_score:.2f}")