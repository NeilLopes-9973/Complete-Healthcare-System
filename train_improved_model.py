import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import lightgbm as lgb
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import class_weight

print("Loading and preparing data...")

# Load both datasets
training_data = pd.read_csv('Training.csv')
testing_data = pd.read_csv('Testing.csv')

# Combine the datasets
combined_data = pd.concat([training_data, testing_data], ignore_index=True)

# Check for and remove any problematic columns
if 'Unnamed: 133' in combined_data.columns:
    combined_data = combined_data.drop(columns=['Unnamed: 133'])

# Print basic information about the dataset
print(f"Combined dataset shape: {combined_data.shape}")
print(f"Number of features: {combined_data.shape[1] - 1}")  # All columns except prognosis
print(f"Number of classes: {combined_data.iloc[:, -1].nunique()}")
print(f"Classes: {combined_data.iloc[:, -1].unique()}")

# Split into features (X) and target (y)
X = combined_data.iloc[:, :-1]  # All columns except the last one
y = combined_data.iloc[:, -1]   # Last column (prognosis/disease)

# Encode the target variable
print("Encoding target variable...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save the label encoder for later use
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

# Save the column names for later use - critical for feature matching
with open('train_columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

print(f"Saved {len(X.columns)} feature names to train_columns.pkl")

# Print class distribution
print("\nClass distribution before balancing:")
class_counts = pd.Series(y_encoded).value_counts().sort_index()
for class_idx, count in class_counts.items():
    class_name = label_encoder.inverse_transform([class_idx])[0]
    print(f"{class_name}: {count} samples")

# Calculate class weights for balanced training
class_weights = class_weight.compute_class_weight(
    'balanced',
    classes=np.unique(y_encoded),
    y=y_encoded
)
class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"\nTraining set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

# Create and train the LightGBM model with class balancing and improved parameters
print("\nTraining LightGBM model with class weights and optimized parameters...")
model = lgb.LGBMClassifier(
    n_estimators=300,             # More trees for better performance
    learning_rate=0.03,           # Slower learning rate for better generalization
    num_leaves=31,
    max_depth=15,
    class_weight=class_weight_dict,  # Use class weights for balanced training
    boosting_type='gbdt',
    objective='multiclass',
    random_state=42,
    reg_alpha=0.1,                # L1 regularization
    reg_lambda=0.1,               # L2 regularization
    min_child_samples=20,         # Minimum number of samples in a leaf
    feature_fraction=0.8,         # Use 80% of features in each iteration
    bagging_fraction=0.8,         # Use 80% of data in each iteration
    bagging_freq=5                # Perform bagging every 5 iterations
)

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
target_names = label_encoder.classes_
print(classification_report(y_test, y_pred, target_names=target_names))

# Perform cross-validation for a more robust evaluation
cv_scores = cross_val_score(model, X, y_encoded, cv=5, scoring='accuracy')
print(f"\nCross-validation accuracy: {cv_scores.mean() * 100:.2f}% ± {cv_scores.std() * 100:.2f}%")

# Feature importance analysis
feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)[::-1][:20]  # Top 20 features

plt.figure(figsize=(12, 10))
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
plt.yticks(range(len(sorted_idx)), X.columns[sorted_idx])
plt.title('Top 20 Most Important Symptoms')
plt.tight_layout()
plt.savefig('Feature_Importance_Improved.png')

# Test model predictions for a few cases
print("\nTesting model prediction diversity...")
test_cases = [
    np.zeros(X.shape[1]),  # No symptoms
    np.ones(X.shape[1]),   # All symptoms
    np.random.randint(0, 2, X.shape[1]),  # Random symptoms
]

for i, test_case in enumerate(test_cases):
    pred = model.predict([test_case])[0]
    pred_prob = model.predict_proba([test_case])[0]
    top_3_idx = pred_prob.argsort()[-3:][::-1]
    
    disease = label_encoder.inverse_transform([pred])[0]
    print(f"\nTest case {i+1}:")
    print(f"Predicted disease: {disease}")
    print("Top 3 probabilities:")
    for idx in top_3_idx:
        print(f"  {label_encoder.inverse_transform([idx])[0]}: {pred_prob[idx]:.4f}")

# Save the improved model with metadata
print("\nSaving improved model to disk...")
model_package = {
    'model': model,
    'features': X.columns.tolist(),
    'feature_count': len(X.columns),
    'target_classes': label_encoder.classes_.tolist(),
    'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    'model_version': '2.0'
}

with open('improved_model.pkl', 'wb') as f:
    pickle.dump(model_package, f)

print("Training complete and improved model saved successfully.")
print(f"The model uses all {len(X.columns)} features from the dataset.")
print("You can now use this model in your application with the updated feature set.") 