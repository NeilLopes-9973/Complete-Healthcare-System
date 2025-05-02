import pickle
from main import symp

# Load the training columns
with open("train_columns.pkl", "rb") as f:
    train_columns = pickle.load(f)

# Find missing symptoms
missing_symptoms = set(train_columns) - set(symp)

print(f"Total symptoms in training data: {len(train_columns)}")
print(f"Total symptoms in application: {len(symp)}")
print(f"Number of missing symptoms: {len(missing_symptoms)}")
print("\nMissing symptoms:")
for symptom in sorted(missing_symptoms):
    print(f"- {symptom}")

# Print first few symptoms from both sets to verify
print("\nFirst 10 symptoms in training data:")
for symptom in train_columns[:10]:
    print(f"- {symptom}")

print("\nFirst 10 symptoms in application:")
for symptom in symp[:10]:
    print(f"- {symptom}") 