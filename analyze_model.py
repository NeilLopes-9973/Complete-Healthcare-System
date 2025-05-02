import pickle
import numpy as np

# Load the model
print("Loading model...")
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

print(f"Model type: {type(model)}")

# Load prognosis list
prognosis = [
    'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
    'Peptic ulcer disease', 'AIDS', 'Diabetes', 'Gastroenteritis', 
    'Bronchial Asthma', 'Hypertension', 'Migraine', 'Cervical spondylosis',
    'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 
    'Dengue', 'Typhoid', 'Hepatitis A', 'Hepatitis B', 'Hepatitis C', 
    'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis',
    'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)',
    'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 
    'Hypoglycemia', 'Osteoarthritis', 'Arthritis', '(vertigo) Paroxysmal Positional Vertigo', 
    'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo'
]

# Test with all zeros (no symptoms)
print("\nTesting with no symptoms...")
input_zero = np.zeros(132)
result_zero = model.predict(input_zero.reshape(1, -1))
print(f"Raw result: {result_zero}")
prediction_idx = np.argmax(result_zero[0])
print(f"Predicted disease: {prognosis[prediction_idx]}")

# Test with all ones (all symptoms)
print("\nTesting with all symptoms...")
input_all = np.ones(132)
result_all = model.predict(input_all.reshape(1, -1))
print(f"Raw result: {result_all}")
prediction_idx = np.argmax(result_all[0])
print(f"Predicted disease: {prognosis[prediction_idx]}")

# Test with single symptoms
print("\nTesting with single symptoms...")
for i in range(min(10, 132)):  # Test first 10 symptoms only
    input_single = np.zeros(132)
    input_single[i] = 1
    result = model.predict(input_single.reshape(1, -1))
    prediction_idx = np.argmax(result[0])
    print(f"Symptom {i}: Predicted {prognosis[prediction_idx]}")

# Try to analyze model output
print("\nModel output probabilities for empty input:")
result_probs = result_zero[0]
for i, prob in enumerate(result_probs):
    if prob > 0.01:  # Only show significant probabilities
        print(f"{prognosis[i]}: {prob:.4f}")

# Check if model is predicting the same thing for all inputs
print("\nChecking if model is biased...")
test_inputs = [
    np.random.randint(0, 2, 132) for _ in range(5)  # 5 random symptom combinations
]

predictions = []
for test_input in test_inputs:
    result = model.predict(test_input.reshape(1, -1))
    pred_idx = np.argmax(result[0])
    predictions.append(pred_idx)
    print(f"Random test input resulted in: {prognosis[pred_idx]}")

if len(set(predictions)) == 1:
    print("ISSUE DETECTED: Model is predicting the same disease for all inputs!")
else:
    print(f"Model predicted {len(set(predictions))} different diseases for random inputs.") 