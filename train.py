import pandas as pd
import numpy as np
import lightgbm as lgb
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.preprocessing import label_binarize
from sklearn.feature_selection import SelectKBest, f_classif
# from scipy import interp  # This is causing issues with newer scipy versions
from itertools import cycle

print("Loading and preparing data...")

# Load the training dataset
train_data = pd.read_csv('Training.csv')
# Load the testing dataset
test_data = pd.read_csv('Testing.csv')

# Check for and remove any problematic columns in both datasets
if 'Unnamed: 133' in train_data.columns:
    train_data = train_data.drop(columns=['Unnamed: 133'])
if 'Unnamed: 133' in test_data.columns:
    test_data = test_data.drop(columns=['Unnamed: 133'])

# Print basic information about the datasets
print(f"Training dataset shape: {train_data.shape}")
print(f"Testing dataset shape: {test_data.shape}")
print(f"Number of classes in training: {train_data.iloc[:, -1].nunique()}")

# Split training data into features (X) and target (y)
X_train = train_data.iloc[:, :-1]  # All columns except the last one
y_train = train_data.iloc[:, -1]   # Last column (prognosis/disease)

# Split testing data into features (X) and target (y)
X_test = test_data.iloc[:, :-1]  # All columns except the last one
y_test = test_data.iloc[:, -1]   # Last column (prognosis/disease)

# Encode the target variables if they're categorical
print("Encoding target variables...")
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
# Use the same encoder for test data to ensure consistent labels
y_test_encoded = label_encoder.transform(y_test)

# Save the encoder for later use
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

# Save the column names for later use
with open('train_columns.pkl', 'wb') as f:
    pickle.dump(X_train.columns.tolist(), f)

print(f"Training set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

# Feature selection - using a higher number of features for better accuracy
print("\nPerforming feature selection...")
selector = SelectKBest(f_classif, k=110)  # Select more features to increase accuracy
X_train_selected = selector.fit_transform(X_train, y_train_encoded)
X_test_selected = selector.transform(X_test)

# Get indices of selected features
selected_indices = selector.get_support(indices=True)
selected_feature_names = X_train.columns[selected_indices]
print(f"Selected {len(selected_feature_names)} features out of {X_train.shape[1]}")

# Higher-accuracy model parameters (less regularization) but still with some guard rails
model_params = {
    'n_estimators': 150,         # More trees for better accuracy
    'learning_rate': 0.05,       # Higher learning rate
    'num_leaves': 31,            # More leaves
    'max_depth': 8,              # Deeper trees
    'min_data_in_leaf': 5,       # Lower minimum samples per leaf
    'lambda_l1': 0.05,           # Light L1 regularization
    'lambda_l2': 0.05,           # Light L2 regularization
    'bagging_fraction': 0.9,     # Use 90% of data for each tree
    'feature_fraction': 0.9,     # Use 90% of features for each tree
    'bagging_freq': 5,           # Perform bagging every 5 iterations
    'random_state': 42,
    'verbose': -1                # Reduce verbosity
}

# Implement cross-validation
print("\nPerforming cross-validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
model_cv = lgb.LGBMClassifier(**model_params)

try:
    cv_scores = cross_val_score(model_cv, X_train_selected, y_train_encoded, cv=cv, scoring='accuracy')
    print(f"Cross-validation accuracy: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
except Exception as e:
    print(f"Error during cross-validation: {e}")
    # Fallback to simpler model if cross-validation fails
    print("Falling back to simpler model parameters")
    model_params = {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'num_leaves': 31,
        'max_depth': 7,
        'random_state': 42,
        'verbose': -1
    }

# Train the final model
print("\nTraining high-accuracy LightGBM model...")
model = lgb.LGBMClassifier(**model_params)
try:
    model.fit(X_train_selected, y_train_encoded)
    print("Model training completed successfully.")
except Exception as e:
    print(f"Error during model training: {e}")
    # Fallback to simpler training if needed
    model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1, num_leaves=31, max_depth=7, random_state=42)
    model.fit(X_train_selected, y_train_encoded)

# Make predictions on test set
y_pred = model.predict(X_test_selected)
y_pred_proba = model.predict_proba(X_test_selected)

# Calculate accuracy
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"\n==== MODEL EVALUATION METRICS ON TESTING.CSV ====")
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# Generate and display confusion matrix
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test_encoded, y_pred)
print(cm)

# Print classification report
print("\nClassification Report:")
report = classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_, zero_division=0)
print(report)

# Plot confusion matrix as a heatmap
plt.figure(figsize=(14, 12))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(len(label_encoder.classes_))
plt.xticks(tick_marks, label_encoder.classes_, rotation=90)
plt.yticks(tick_marks, label_encoder.classes_)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.savefig('confusion_matrix.png', bbox_inches='tight')
print("Confusion matrix plot saved.")

# Compute ROC curve and ROC area for each class
n_classes = len(label_encoder.classes_)
# Binarize the output for ROC calculation
y_test_bin = label_binarize(y_test_encoded, classes=range(n_classes))

# Calculate ROC AUC
try:
    # Compute macro-average ROC curve and ROC area
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_pred_proba[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test_bin.ravel(), y_pred_proba.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    # Compute macro-average ROC curve and ROC area
    # First aggregate all false positive rates
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
    
    # Then interpolate all ROC curves at these points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
    
    # Finally average it and compute AUC
    mean_tpr /= n_classes
    
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    
    # Plot ROC curves
    plt.figure(figsize=(12, 8))
    
    # Plot micro-average ROC curve
    plt.plot(fpr["micro"], tpr["micro"],
             label=f'micro-average ROC curve (area = {roc_auc["micro"]:.2f})',
             color='deeppink', linestyle=':', linewidth=4)
    
    # Plot macro-average ROC curve
    plt.plot(fpr["macro"], tpr["macro"],
             label=f'macro-average ROC curve (area = {roc_auc["macro"]:.2f})',
             color='navy', linestyle=':', linewidth=4)
    
    # Plot a subset of ROC curves for individual classes (to avoid overcrowding)
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'green', 'red', 'purple', 'brown', 'pink'])
    
    # Plot ROC curves for a subset of classes
    for i, color in zip(range(min(10, n_classes)), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label=f'ROC curve of class {label_encoder.classes_[i]} (area = {roc_auc[i]:.2f})')
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Multi-class ROC Curves')
    plt.legend(loc="lower right")
    plt.savefig('roc_curve.png')
    print("ROC curve plot saved.")
    
    # Print overall AUC scores
    print("\nROC AUC Scores:")
    print(f"Micro-average AUC: {roc_auc['micro']:.4f}")
    print(f"Macro-average AUC: {roc_auc['macro']:.4f}")
    
    # Compare CV accuracy with test accuracy
    try:
        cv_test_diff = abs(cv_scores.mean() - accuracy)
        print(f"\nDifference between CV ({cv_scores.mean():.4f}) and test accuracy ({accuracy:.4f}): {cv_test_diff:.4f}")
        
        if cv_test_diff > 0.1:
            print("\n===== ACCURACY DIFFERENCE WARNING =====")
            print(f"Large difference between cross-validation ({cv_scores.mean():.4f}) and test accuracy ({accuracy:.4f})")
            print("This suggests the model may not generalize well to new data.")
    except Exception as e:
        print(f"Could not compare CV and test accuracy: {e}")
    
    if roc_auc['micro'] > 0.95:
        print("\n===== HIGH AUC NOTICE =====")
        print(f"The AUC score is high ({roc_auc['micro']:.4f}), which indicates excellent class separation")
    
except Exception as e:
    print(f"Error calculating ROC curves: {e}")

# Feature importance
feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)[::-1]
selected_feature_names_list = selected_feature_names.tolist()

plt.figure(figsize=(10, 6))
top_n = min(20, len(feature_importance))  # Use top 20 features
plt.barh(range(top_n), feature_importance[sorted_idx][:top_n])
plt.yticks(range(top_n), [selected_feature_names_list[i] for i in sorted_idx[:top_n]])
plt.title('Top 20 Feature Importance')
plt.savefig('Feature_Importance.png')
print("Feature importance plot saved.")

print("\nSaving high-accuracy model to disk...")
# Save the model along with feature selector for future use
with open('model.pkl', 'wb') as f:
    pickle.dump({'model': model, 'feature_selector': selector}, f)

print("\nFinal model parameters:")
for param, value in model.get_params().items():
    print(f"  {param}: {value}")

print("\nEvaluation on Testing.csv completed successfully.")
