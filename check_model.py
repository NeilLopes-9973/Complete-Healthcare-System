import pickle
import numpy as np

print("Testing model loading and prediction...")

try:
    # Load the model
    print("Loading the model...")
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print(f"Model loaded successfully. Type: {type(model)}")
    
    # Load label encoder
    print("Loading the label encoder...")
    try:
        with open("label_encoders.pkl", "rb") as f:
            label_encoder = pickle.load(f)
        print(f"Label encoder loaded successfully. Type: {type(label_encoder)}")
    except Exception as e:
        print(f"Error loading label encoder: {e}")
        label_encoder = None
    
    # Create dummy input
    print("Creating dummy input...")
    dummy_input = np.zeros(132)  # Based on your model's expected input size
    
    # Try prediction
    print("Testing prediction...")
    result = model.predict(dummy_input.reshape(1, -1))
    print(f"Prediction result: {result}, Type: {type(result)}")
    
    # Try decoding
    if label_encoder is not None and hasattr(label_encoder, 'inverse_transform'):
        try:
            decoded = label_encoder.inverse_transform([int(result[0])])
            print(f"Decoded prediction: {decoded}")
        except Exception as e:
            print(f"Error decoding prediction: {e}")
    
    print("Model test complete!")
except Exception as e:
    print(f"Error during model test: {e}") 