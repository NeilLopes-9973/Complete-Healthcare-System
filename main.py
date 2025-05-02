import os  # Make sure to import the os module
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb
import bcrypt
import hashlib
import pickle
import numpy as np
from flask_session import Session
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import traceback
import datetime
import functools
from flask_mail import Mail, Message  # Add Flask-Mail imports
from twilio.rest import Client  # Import Twilio library for SMS

# Load the symptoms directly from train_columns.pkl to ensure we have all symptoms
try:
    with open("train_columns.pkl", "rb") as f:
        symp = pickle.load(f)
    print(f"Loaded {len(symp)} symptoms from training data")
except Exception as e:
    print(f"Error loading symptoms from train_columns.pkl: {e}")
    # Fallback to a predefined list in case the file doesn't exist
    symp = [ 
        'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 
        'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 
        'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 
        'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 
        'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 
        'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 
        'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 
        'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 
        'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 
        'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 
        'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 
        'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 
        'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 
        'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 
        'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 
        'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 
        'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 
        'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 
        'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 
        'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 
        'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 
        'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 
        'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 
        'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 
        'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze',
        # Adding the missing symptoms from training data
        'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 
        'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 
        'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 
        'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 
        'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 
        'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 
        'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 
        'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 
        'loss_of_appetite', 'pain_behind_the_eyes', 'fluid_overload.1'
    ]

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

app = Flask(__name__)
app.config["DEBUG"] = True

# Set a secret key for the application
app.secret_key = 'healthcare_system_secret_key'

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = 'flask_session/'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
# Make cookies expire when browser is closed
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
Session(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # Host where MySQL is running (localhost for local setup)
app.config['MYSQL_USER'] = 'root'  # MySQL user (root is default on local setups)
app.config['MYSQL_PASSWORD'] = ''  # Password for root (empty if no password is set)
app.config['MYSQL_DB'] = 'disease_pred'  # Changed to disease_pred database (as in your SQL file)
app.config['MYSQL_PORT'] = 3306  # Default MySQL port
app.config['MYSQL_SSL_DISABLED'] = True  # Set to True to disable SSL for XAMPP
app.config['MYSQL_CUSTOM_OPTIONS'] = {'ssl_mode': 'DISABLED'}  # Explicitly disable SSL mode

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Replace with your Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Replace with your Gmail address
mail = Mail(app)

# Twilio configuration
TWILIO_ACCOUNT_SID = 'your_account_sid_here'   # Replace with your actual SID in environment variables
TWILIO_AUTH_TOKEN = 'your_auth_token_here'     # Replace with your actual token in environment variables
TWILIO_PHONE_NUMBER = 'your_twilio_number_here'  # Replace with your actual Twilio phone number

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to get a MySQL connection with SSL disabled
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT'],
        ssl_disabled=True
    )

mysql_db = MySQL(app)  # Initialize the MySQL connection for Flask - renamed to avoid conflict

# Decorator for routes that require login
def login_required(user_type=None):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if 'user_id' not in session:
                # Store the requested URL for redirecting after login
                session['next_url'] = request.url
                
                # Instead of redirecting, render the login_required template
                message = f"You need to be logged in to access this feature."
                if user_type:
                    message += f" This page requires {user_type} privileges."
                
                return render_template('login_required.html', message=message)
            
            # If a specific user type is required, check it
            if user_type and session.get('user_type') != user_type:
                message = f"This feature requires {user_type} access. Please log in with the appropriate account."
                return render_template('login_required.html', message=message)
                
            return view_func(*args, **kwargs)
        return wrapped_view
    return decorator

# Fix the loading of model files for prediction
try:
    # Load the label encoder directly
    with open("label_encoders.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    print("Label encoder loaded successfully at startup")
    
    # Load the improved model instead of the original model
    with open("improved_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Check if model is a dictionary and extract the actual model if needed
    if isinstance(model, dict) and 'model' in model:
        model = model['model']
    print("Improved model loaded successfully at startup")
    
    # Load the training columns directly
    with open("train_columns.pkl", "rb") as f:
        train_columns = pickle.load(f)
    print(f"Loaded {len(train_columns)} features from training data at startup")
    
    # Create a global list of symptoms from train_columns for display
    model_columns = train_columns[:110] if len(train_columns) > 110 else train_columns
except Exception as e:
    print(f"Error loading prediction model files at startup: {e}")
    traceback.print_exc()

@app.route("/")
def home():
    # Make sure to display all symptoms, not just those the model can use
    global symp
    return render_template("index.html")

@app.route("/predict", methods=["POST", "GET"])
@login_required()
def predict():
    if request.method == "POST":
        # Get the selected symptoms from the form data
        selected_symptoms = request.form.getlist("symptom")
        print(f"Selected symptoms: {selected_symptoms}")

        # Check if no symptoms were selected
        if not selected_symptoms:
            # Display all symptoms
            return render_template("predict.html", error="Please select at least one symptom", symp=symp)

        try:
            # Declare global variables first
            global model, label_encoder, train_columns
            
            # Initialize expected_features to None before any conditional code
            expected_features = None
            
            # Check if model is already loaded, if not try to load it
            if 'model' not in globals():
                try:
                    # First try to load the improved model
                    with open("improved_model.pkl", "rb") as f:
                        model_data = pickle.load(f)
                    # Check if model is a dictionary and extract the actual model if needed
                    if isinstance(model_data, dict) and 'model' in model_data:
                        model = model_data['model']
                        # Check if feature count is specified
                        expected_features = model_data.get('feature_count', None)
                        print(f"Loaded improved model with {expected_features} features")
                    else:
                        model = model_data
                    print("Improved model loaded successfully")
                except FileNotFoundError:
                    # Fall back to the original model
                    with open("model.pkl", "rb") as f:
                        model = pickle.load(f)
                    # Check if model is a dictionary and extract the actual model if needed
                    if isinstance(model, dict) and 'model' in model:
                        model = model['model']
                    print("Original model loaded successfully")
            
            # Check if label_encoder is loaded, if not try to load it
            if 'label_encoder' not in globals():
                with open("label_encoders.pkl", "rb") as f:
                    label_encoder = pickle.load(f)
                print("Label encoder loaded successfully")
            
            # Check if train_columns is loaded, if not try to load it
            if 'train_columns' not in globals():
                with open("train_columns.pkl", "rb") as f:
                    train_columns = pickle.load(f)
                print(f"Train columns loaded successfully - {len(train_columns)} features")
            
            # Check if required components are loaded
            if 'model' not in globals() or 'label_encoder' not in globals() or 'train_columns' not in globals():
                return render_template("predict.html", 
                                      error="Prediction model not loaded correctly. Please contact the administrator.", 
                                      symp=symp)
            
            # Create a binary representation matching the training format
            symptoms_vector = np.zeros(len(train_columns))
            
            # Track if any symptoms were matched
            matched_count = 0
            
            for symptom in selected_symptoms:
                # Remove underscores and standardize symptom format
                clean_symptom = symptom.replace('_', ' ').lower().strip()
                
                # Try to find the matching column in training data
                found_match = False
                for i, column in enumerate(train_columns):
                    # Also clean the column name for comparison
                    clean_column = column.replace('_', ' ').lower().strip()
                    if clean_symptom == clean_column:
                        symptoms_vector[i] = 1
                        matched_count += 1
                        print(f"Matched '{symptom}' to training feature '{column}'")
                        found_match = True
                        break
                
                if not found_match:
                    print(f"Warning: Could not match symptom '{symptom}' to any training feature")
            
            print(f"Created symptom vector with {matched_count} active symptoms")
            
            # Make sure at least one symptom was matched
            if matched_count == 0:
                return render_template("predict.html", 
                                    error="None of the selected symptoms could be matched to the model features. Please try different symptoms.", 
                                    symp=symp)
            
            # Make prediction
            print("Making prediction...")
            try:
                # If we don't have expected_features from model metadata, check dynamically
                if expected_features is None:
                    # Try to determine from the model directly
                    if hasattr(model, 'n_features_in_'):
                        expected_features = model.n_features_in_
                        print(f"Detected {expected_features} features from model")
                    else:
                        # Default to the number of features in train_columns if not specified
                        expected_features = len(train_columns)
                        print(f"Using train_columns length: {expected_features} features")
                
                print(f"Model expects {expected_features} features, we have {len(symptoms_vector)}")
                
                # If our input vector doesn't match the expected size, adjust it
                if len(symptoms_vector) != expected_features:
                    print(f"Warning: Model expects {expected_features} features, but we have {len(symptoms_vector)}")
                    
                    # Use only the features the model expects
                    if len(symptoms_vector) > expected_features:
                        print("Truncating feature vector to match model expectations")
                        symptoms_vector = symptoms_vector[:expected_features]
                    else:
                        print("Padding feature vector to match model expectations")
                        symptoms_vector = np.pad(symptoms_vector, (0, expected_features - len(symptoms_vector)))
                
                # Check if the model has the predict_proba method
                if not hasattr(model, 'predict_proba'):
                    print("Model doesn't have predict_proba method, using predict instead")
                    # Use the predict method and create a dummy probability
                    result = model.predict(symptoms_vector.reshape(1, -1))[0]
                    # Create a fake probability distribution
                    adjusted_proba = np.zeros(len(prognosis))
                    disease_index = np.where(np.array(prognosis) == result)[0][0]
                    adjusted_proba[disease_index] = 0.9  # Assign high probability to the predicted disease
                    
                    # Get the main predicted disease
                    top_disease = result
                    
                    # Format the prediction results
                    prediction_results = [{
                        "disease": top_disease,
                        "probability": "90%"
                    }]
                    
                    # Generate a confidence explanation
                    confidence_level = "medium"
                    confidence_explanation = "The model has made a prediction, but confidence information is not available."
                else:
                    # Get raw prediction and probabilities
                    result_proba = model.predict_proba(symptoms_vector.reshape(1, -1))
                    print(f"Prediction probabilities shape: {result_proba.shape}")
                    
                    # Get top indices based on model prediction
                    model_top_indices = np.argsort(result_proba[0])[-5:][::-1]  # Get top 5 initially
                    
                    # Create a modified probability array that we can adjust
                    adjusted_proba = result_proba[0].copy()
                    
                    # Get top indices based on adjusted probabilities
                    top_indices = np.argsort(adjusted_proba)[-3:][::-1]  # Get top 3 for display
                    
                    # Get the main predicted disease
                    top_disease = label_encoder.inverse_transform([top_indices[0]])[0]
                    print(f"Top predicted disease: {top_disease} with adjusted probability {adjusted_proba[top_indices[0]]:.4f}")
                    
                    # Get other top candidates
                    prediction_results = []
                    
                    # Format the prediction results
                    for idx in top_indices:
                        disease = label_encoder.inverse_transform([idx])[0] 
                        probability = adjusted_proba[idx]
                        prediction_results.append({
                            "disease": disease,
                            "probability": f"{probability:.2%}"
                        })
                    
                    # Generate a confidence explanation
                    confidence_level = "low"
                    top_probability = adjusted_proba[top_indices[0]]
                    
                    if top_probability > 0.7:
                        confidence_level = "high"
                        confidence_explanation = "The model has high confidence in this prediction based on the symptoms provided."
                    elif top_probability > 0.4:
                        confidence_level = "medium"
                        confidence_explanation = "The model has moderate confidence in this prediction. Consider consulting a healthcare professional."
                    else:
                        confidence_explanation = "The model has low confidence in this prediction. Please consult a healthcare professional for proper diagnosis."
                
                # Return the predictions to the predict template
                return render_template(
                    "predict.html", 
                    result=top_disease, 
                    predictions=prediction_results,
                    selected_symptoms=selected_symptoms,
                    symp=symp,
                    confidence_explanation=confidence_explanation,
                    confidence_level=confidence_level
                )
            except Exception as e:
                print(f"Model prediction error: {e}")
                traceback.print_exc()
                flash(f"Error making prediction: {str(e)}")
                return render_template("predict.html", error=str(e), symp=symp)
                
        except Exception as e:
            print(f"General error in predict function: {e}")
            traceback.print_exc()
            flash(f"An error occurred: {str(e)}")
            return render_template("predict.html", error=str(e), symp=symp)

    # Display all symptoms
    return render_template("predict.html", symp=symp)

@app.route("/predict1")
@login_required()
def predict1():
    """Route for the alternate prediction page"""
    return render_template("predict1.html")

@app.route("/blood")  # this sets the route to this page
@login_required()
def blood():
    return render_template("blood.html")

@app.route("/ngo")  # this sets the route to this page
def ngo():
    return render_template("ngo.html")

@app.route("/add_checkups", methods=['GET', 'POST'])  # this sets the route to this page
def add_checkups():
    #ngo wrk
    if request.method == "POST":
        details = request.form
        ngo_name = details['ngo_name']
        type_check = details['type_check']
        date = details['date']
        time = details['time']
        contact = details['contact']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert event into database
            cursor.execute("INSERT INTO add_check(ngo_name, type_check, date, time, contact) VALUES (%s, %s, %s, %s, %s)",
                        (ngo_name, type_check, date, time, contact))
            conn.commit()
            
            # Get the NGO's email for the sender
            cursor.execute("SELECT email FROM ngo_users WHERE ngo_name = %s", (ngo_name,))
            ngo_data = cursor.fetchone()
            ngo_email = ngo_data[0] if ngo_data else app.config['MAIL_DEFAULT_SENDER']
            
            # Get all patient emails for notification
            cursor.execute("SELECT p_name, email FROM patient_users")
            patients = cursor.fetchall()
            
            # Send email notifications
            if patients:
                # Format date for display in email
                formatted_date = date
                try:
                    # Format date as Month day, Year if possible
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%B %d, %Y')
                except:
                    # Use as-is if formatting fails
                    pass
                
                for patient in patients:
                    patient_name = patient[0]
                    patient_email = patient[1]
                    
                    # Create email message
                    subject = f"New Healthcare Event: {type_check} by {ngo_name}"
                    html_body = f"""
                    <html>
                        <body>
                            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                                <h2 style="color: #4070f4; text-align: center;">Healthcare Event Notification</h2>
                                <p>Hello <b>{patient_name}</b>,</p>
                                <p>We're excited to inform you about an upcoming healthcare event organized by <b>{ngo_name}</b>.</p>
                                
                                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                                    <h3 style="color: #333; margin-top: 0;">{type_check}</h3>
                                    <p><b>Date:</b> {formatted_date}</p>
                                    <p><b>Time:</b> {time}</p>
                                    <p><b>Contact:</b> {contact}</p>
                                </div>
                                
                                <p>This event is a great opportunity to prioritize your health and well-being.</p>
                                <p>We hope to see you there!</p>
                                
                                <p style="margin-top: 30px;">Best regards,<br>The {ngo_name} Team</p>
                                <p><small>Contact: {ngo_email}</small></p>
                                
                                <div style="font-size: 12px; color: #777; margin-top: 30px; text-align: center; border-top: 1px solid #eee; padding-top: 10px;">
                                    <p>This is an automated message from our Healthcare Management System.</p>
                                    <p>To unsubscribe from these notifications, please contact the healthcare admin.</p>
                                </div>
                            </div>
                        </body>
                    </html>
                    """
                    
                    try:
                        msg = Message(
                            subject=subject,
                            recipients=[patient_email],
                            html=html_body,
                            sender=ngo_email
                        )
                        mail.send(msg)
                    except Exception as e:
                        print(f"Error sending email to {patient_email}: {str(e)}")
            
            cursor.close()
            conn.close()
            
            return '<script>alert("Event added successfully and notifications sent!");window.location="/ngo_server"</script>'
        
        except Exception as e:
            cursor.close()
            conn.close()
            return f'<script>alert("Error: {str(e)}");window.location="/add_checkups"</script>'

    return render_template("add_checkups.html")

@app.route('/ngo_sign_up', methods=['GET', 'POST'])
def ngo_sign_up():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        ngo_name = userDetails['ngo_name']
        pass1 = userDetails['pass1']
        type1 = userDetails['type1']
        number = userDetails['number']
        email = userDetails['email']  # Get email from form

        hashed_password = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt())

        # Initialize cursor
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # First check if we need to add the email column to ngo_users table
            try:
                cursor.execute("SHOW COLUMNS FROM ngo_users LIKE 'email'")
                if not cursor.fetchone():
                    # Email column doesn't exist, add it
                    cursor.execute("ALTER TABLE ngo_users ADD COLUMN email VARCHAR(255) NOT NULL DEFAULT 'ngo@example.com'")
                    conn.commit()
            except Exception as e:
                print(f"Error checking/adding email column: {str(e)}")
            
            # Insert user details into the table with email
            cursor.execute("INSERT INTO ngo_users(ngo_name, pass1, type1, number, email) VALUES(%s, %s, %s, %s, %s)",
                        (ngo_name, hashed_password, type1, number, email))
            conn.commit()
            cursor.close()
            conn.close()

            # Redirect to login page
            return '<script>alert("ngo registered successfully");window.location="/ngo_login"</script>'
        except Exception as e:
            return f'<script>alert("Error: {str(e)}");window.location="/ngo_sign_up"</script>'

    return render_template('ngo_sign_up.html')

@app.route('/ngo_login', methods=['POST','GET'])
def login_post():
    if request.method == 'POST':
        # Get form data
        ngo_name = request.form['ngo_name']
        pass1 = request.form['pass1']

        # Initialize cursor
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute the query to check if the user exists
        query = "SELECT * FROM ngo_users WHERE ngo_name = %s"
        cursor.execute(query, (ngo_name,))
        user = cursor.fetchone()

        # Close the cursor
        cursor.close()
        conn.close()

        # Check if the user exists and verify the password
        if user and bcrypt.checkpw(pass1.encode('utf-8'), user['pass1'].encode('utf-8')):
            # Create the session
            session['user_id'] = user['sr_no']
            session['ngo_name'] = ngo_name
            session['user_type'] = 'ngo'
            # Store email in session if it exists
            if 'email' in user:
                session['email'] = user['email']
            else:
                session['email'] = 'ngo@example.com'  # Default email

            # Check if there's a next_url in the session
            next_url = session.pop('next_url', None)
            if next_url:
                return redirect(next_url)

            # Redirect the user to a protected page
            return '<script>alert("Logged in successfully");window.location="/ngo_server"</script>'
        else:
            # If the user does not exist or password is incorrect, redirect to login page
            return '<script>alert("Invalid username or password");window.location="/ngo_login"</script>'

    return render_template("ngo_login.html")

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('home'))

@app.route("/ngo_server")
@login_required(user_type='ngo')
def ngo_server():
    return render_template("ngo_server.html")

@app.route("/patient_sign_up" ,methods=['POST','GET'])
def patient_sign_up():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        p_name = userDetails['p_name']
        email = userDetails['email']
        password1 = userDetails['password1']
        number = userDetails['number']
        address = userDetails['address']

        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())

        try:
            # Use our custom connection function
            conn = get_db_connection()
            cursor = conn.cursor(prepared=True)  # Use prepared statements
            
            # Insert user details into the table
            cursor.execute("INSERT INTO patient_users(p_name, email, password1, number, address) VALUES(%s, %s, %s, %s, %s)",
                       (p_name, email, hashed_password, number, address))
            conn.commit()
            cursor.close()
            conn.close()

            # Redirect to login page
            return '<script>alert("Registered successfully");window.location="/patient_login"</script>'
        except Exception as e:
            return f'<script>alert("Error: {str(e)}");window.location="/patient_sign_up"</script>'

    return render_template("patient_sign_up.html")

@app.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        try:
            # Use our custom connection function
            conn = get_db_connection()
            cursor = conn.cursor(prepared=True, dictionary=True)  # Get results as dictionaries

            # Execute the query to check if the user exists
            query = "SELECT * FROM patient_users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            # Close the cursor
            cursor.close()
            conn.close()

            # Check if the user exists and verify the password
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password1'].encode('utf-8')):
                # Create the session
                session['user_id'] = user['sr_no']
                session['p_name'] = user['p_name']
                session['email'] = user['email']
                session['user_type'] = 'patient'

                # Check if there's a next_url in the session
                next_url = session.pop('next_url', None)
                if next_url:
                    return redirect(next_url)

                # Redirect the user to a protected page
                return '<script>alert("Logged in successfully");window.location="/"</script>'
            else:
                # If the user does not exist or password is incorrect, redirect to login page
                return '<script>alert("Wrong username or password");window.location="/patient_login"</script>'
        except Exception as e:
            print(f"Login error: {str(e)}")
            return f'<script>alert("Error: {str(e)}");window.location="/patient_login"</script>'

    return render_template('patient_login.html')

@app.route("/doc_sign_up" ,methods=['GET', 'POST'])
def doc_sign_up():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        d_name = userDetails['d_name']
        passwrd1 = userDetails['passwrd1']
        email = userDetails['email']
        special = userDetails['special']

        number = userDetails['number']
        address = userDetails['address']

        hashed_password = bcrypt.hashpw(passwrd1.encode('utf-8'), bcrypt.gensalt())

        # Initialize cursor
        # conn = mysql.connect()
        # cursor = conn.cursor()
        conn = get_db_connection()
        cursor = conn.cursor()
        # Insert user details into the table
        cursor.execute("INSERT INTO doc_user(d_name, email, passwrd1, number, address,special) VALUES(%s, %s, %s, %s, %s, %s)",
                       (d_name, email, hashed_password, number, address, special))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to login page
        return '<script>alert(" Registered successfully");window.location="/"</script>'

    return render_template("doc_sign_up.html")

@app.route("/donate", methods=['GET', 'POST'])  # this sets the route to this page blood donation
@login_required()
def donate():
        if request.method == "POST":
            details = request.form
            Name = details['name']
            age = details['age']
            blood_group = details['blood_group']
            past_illness = details['past_illness']
            mobile = details['mobile']
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO b_donation(Name, age, blood_group, past_illness, mobile) VALUES (%s, %s, %s, %s, %s)", (Name, age, blood_group, past_illness, mobile))
            conn.commit()
            cursor.close()
            conn.close()
            # return 'success'

            return '<script>alert("EVERY DROP MATTERS!! Note:you will get a call within 7 days");window.location="/blood"</script>'

        return render_template('donate.html')

@app.route("/receive")  # this sets the route to this page
@login_required()
def receive():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM b_donation")
    fetchdata = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("receive.html", data=fetchdata)

@app.route("/doc_list")  # this sets the route to this page
def doc_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Get results as dictionaries
        cursor.execute("SELECT * FROM doc_list")  # Fetch from doc_list table
        fetchdata = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("doc_list.html", data=fetchdata)
    except Exception as e:
        print(f"Error in doc_list: {str(e)}")
        return f"<script>alert('Error loading doctor list: {str(e)}');window.location='/'</script>"

@app.route("/ngo_list")
def ngo_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ngo_users")
        fetchdata = cursor.fetchall()
        print(f"NGO LIST DATA: {fetchdata}")
        cursor.close()
        conn.close()
        return render_template("ngo_list.html", data=fetchdata)
    except Exception as e:
        print(f"ERROR in ngo_list: {str(e)}")
        return f"<script>alert('Error loading NGO list: {str(e)}');window.location='/'</script>"

@app.route("/upcomin_check")
def upcomin_check():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM add_check")
    fetchdata = cursor.fetchall()
    cursor.close()
    conn.close()
    # patients view
    return render_template("upcomin_check.html", data=fetchdata)

@app.route('/doc_appointment')
@login_required()
def doc_appointment():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Get results as dictionaries
        cursor.execute("SELECT id, name, specialty, location FROM doc_list")  # Fetch all doctors from doc_list table
        doctors = cursor.fetchall()  # Get all doctor records
        cursor.close()
        conn.close()
        
        # Pass today's date for the date input minimum value
        today = datetime.date.today().strftime('%Y-%m-%d')
        return render_template('doc_appointment.html', doctors=doctors, today=today)
    except Exception as e:
        print(f"Error in doc_appointment: {str(e)}")
        return f"<script>alert('Error loading doctor list: {str(e)}');window.location='/'</script>"

@app.route('/filter', methods=['POST'])
def filter():
    try:
        location = request.form.get('filter_location')
        specialty = request.form.get('filter_specialty')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Get results as dictionaries
        
        # Build query based on which filters are provided
        query = "SELECT id, name, specialty, location FROM doc_list WHERE 1=1"
        params = []
        
        if location and location.strip():
            query += " AND location LIKE %s"
            params.append(f"%{location}%")
            
        if specialty and specialty.strip():
            query += " AND specialty = %s"
            params.append(specialty)
            
        cursor.execute(query, params)  # Run the filtered query
        filtered_doctors = cursor.fetchall()  # Fetch results
        cursor.close()
        conn.close()
        
        # Pass today's date for the date input minimum value
        today = datetime.date.today().strftime('%Y-%m-%d')
        return render_template('doc_appointment.html', doctors=filtered_doctors, today=today)
    except Exception as e:
        print(f"Error in filter: {str(e)}")
        return f"<script>alert('Error filtering doctors: {str(e)}');window.location='/doc_appointment'</script>"

@app.route('/book_appointment', methods=['POST'])
@login_required()
def book_appointment():
    try:
        # Use the logged-in patient's name if available
        if 'p_name' in session:
            patient_name = session['p_name']
        else:
            patient_name = request.form['patient_name']
            
        appointment_date = request.form['appointment_date']
        doctor_id = int(request.form['doctor_id'])  # Get the doctor ID from the form
        appointment_time = request.form.get('appointment_time', '10:00:00')  # Default time if not provided

        # First get the doctor name
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # First get the doctor name from doc_list
        cursor.execute("SELECT name FROM doc_list WHERE id = %s", (doctor_id,))
        doctor_data = cursor.fetchone()
        
        if not doctor_data:
            cursor.close()
            conn.close()
            return f"<script>alert('Doctor not found with ID {doctor_id}');window.location='/doc_appointment'</script>"
            
        doctor_name = doctor_data['name']
        
        # Then find the corresponding sr_no in doc_user table by matching d_name
        cursor.execute("SELECT sr_no FROM doc_user WHERE d_name = %s", (doctor_name,))
        doc_user = cursor.fetchone()
        
        if not doc_user:
            # Doctor doesn't exist in doc_user table, create a temporary record for them
            hashed_password = bcrypt.hashpw("temporary".encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO doc_user (d_name, email, passwrd1, number, address, special) VALUES (%s, %s, %s, %s, %s, %s)",
                (doctor_name, f"{doctor_name.lower().replace(' ', '')}@example.com", 
                 hashed_password, "0000000000", "Address not provided", "General")
            )
            conn.commit()
            
            # Get the ID of the newly inserted doctor
            doc_user_id = cursor.lastrowid
        else:
            doc_user_id = doc_user['sr_no']
        
        # Insert appointment using the sr_no from doc_user as doctor_id and include user_id
        cursor.execute(
            "INSERT INTO appointments (doctor_id, doctor_name, patient_name, appointment_date, appointment_time, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (doc_user_id, doctor_name, patient_name, appointment_date, appointment_time, session['user_id'])
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('appointment_success'))  # Redirect to success page
    except Exception as e:
        print(f"Error in book_appointment: {str(e)}")
        return f"<script>alert('Error booking appointment: {str(e)}');window.location='/doc_appointment'</script>"

@app.route('/appointment_success')
@login_required()  # Add login requirement
def appointment_success():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Get results as dictionaries
        
        # Only fetch appointments for the current user
        cursor.execute(
            "SELECT * FROM appointments WHERE patient_name = %s ORDER BY created_at DESC",
            (session['p_name'],)
        )
        
        appointments = cursor.fetchall()  # Get all results
        cursor.close()
        conn.close()
        
        # Format dates and times to avoid strftime errors
        for appointment in appointments:
            # Convert datetime objects to strings
            if isinstance(appointment['created_at'], datetime.datetime):
                appointment['created_at'] = appointment['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(appointment['appointment_date'], datetime.date):
                appointment['appointment_date'] = appointment['appointment_date'].strftime('%Y-%m-%d')
            if isinstance(appointment['appointment_time'], datetime.timedelta):
                # Convert timedelta to string (HH:MM:SS format)
                total_seconds = int(appointment['appointment_time'].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                appointment['appointment_time'] = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        return render_template('appointment_success.html', appointments=appointments)
    except Exception as e:
        print(f"Error in appointment_success: {str(e)}")
        return f"<script>alert('Error loading appointments: {str(e)}');window.location='/'</script>"

# Email settings routes
@app.route("/email_settings")
@login_required(user_type='ngo')  # Only NGOs can access email settings
def email_settings():
    # Get current email settings
    settings = {
        'mail_server': app.config.get('MAIL_SERVER', ''),
        'mail_port': app.config.get('MAIL_PORT', 587),
        'mail_use_tls': app.config.get('MAIL_USE_TLS', True),
        'mail_use_ssl': app.config.get('MAIL_USE_SSL', False),
        'mail_username': app.config.get('MAIL_USERNAME', ''),
        'mail_password': '', # Don't send actual password to template for security
        'mail_default_sender': app.config.get('MAIL_DEFAULT_SENDER', '')
    }
    
    # Pre-fill with NGO's email if available in session
    if 'email' in session:
        settings['mail_username'] = session['email']
        settings['mail_default_sender'] = session['email']
    
    return render_template('email_settings.html', settings=settings)

@app.route("/save_email_settings", methods=['POST'])
@login_required(user_type='ngo')  # Only NGOs can save email settings
def save_email_settings():
    try:
        # Update application email settings
        app.config['MAIL_SERVER'] = request.form.get('mail_server')
        app.config['MAIL_PORT'] = int(request.form.get('mail_port', 587))
        app.config['MAIL_USE_TLS'] = 'mail_use_tls' in request.form
        app.config['MAIL_USE_SSL'] = 'mail_use_ssl' in request.form
        app.config['MAIL_USERNAME'] = request.form.get('mail_username')
        
        # Only update password if provided
        if request.form.get('mail_password'):
            app.config['MAIL_PASSWORD'] = request.form.get('mail_password')
            
        app.config['MAIL_DEFAULT_SENDER'] = request.form.get('mail_default_sender')
        
        # Recreate Mail instance with new settings
        global mail
        mail = Mail(app)
        
        # Save settings to database so they persist across app restarts
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if settings table exists, create if not
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mail_server VARCHAR(255),
                mail_port INT,
                mail_use_tls BOOLEAN,
                mail_use_ssl BOOLEAN,
                mail_username VARCHAR(255),
                mail_password VARCHAR(255),
                mail_default_sender VARCHAR(255),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        # Check if we need to insert or update
        cursor.execute("SELECT COUNT(*) FROM email_settings")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert new settings
            cursor.execute("""
                INSERT INTO email_settings (
                    mail_server, mail_port, mail_use_tls, mail_use_ssl, 
                    mail_username, mail_password, mail_default_sender
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                app.config['MAIL_SERVER'],
                app.config['MAIL_PORT'],
                app.config['MAIL_USE_TLS'],
                app.config['MAIL_USE_SSL'],
                app.config['MAIL_USERNAME'],
                app.config['MAIL_PASSWORD'],
                app.config['MAIL_DEFAULT_SENDER']
            ))
        else:
            # Update existing settings
            if request.form.get('mail_password'):
                # If password was provided, update it
                cursor.execute("""
                    UPDATE email_settings SET
                        mail_server = %s,
                        mail_port = %s,
                        mail_use_tls = %s,
                        mail_use_ssl = %s,
                        mail_username = %s,
                        mail_password = %s,
                        mail_default_sender = %s
                    WHERE id = 1
                """, (
                    app.config['MAIL_SERVER'],
                    app.config['MAIL_PORT'],
                    app.config['MAIL_USE_TLS'],
                    app.config['MAIL_USE_SSL'],
                    app.config['MAIL_USERNAME'],
                    app.config['MAIL_PASSWORD'],
                    app.config['MAIL_DEFAULT_SENDER']
                ))
            else:
                # If no password, don't update it
                cursor.execute("""
                    UPDATE email_settings SET
                        mail_server = %s,
                        mail_port = %s,
                        mail_use_tls = %s,
                        mail_use_ssl = %s,
                        mail_username = %s,
                        mail_default_sender = %s
                    WHERE id = 1
                """, (
                    app.config['MAIL_SERVER'],
                    app.config['MAIL_PORT'],
                    app.config['MAIL_USE_TLS'],
                    app.config['MAIL_USE_SSL'],
                    app.config['MAIL_USERNAME'],
                    app.config['MAIL_DEFAULT_SENDER']
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Email settings saved successfully!', 'success')
        return redirect(url_for('email_settings'))
        
    except Exception as e:
        flash(f'Error saving email settings: {str(e)}', 'danger')
        return redirect(url_for('email_settings'))

@app.route("/test_email", methods=['POST'])
@login_required(user_type='ngo')
def test_email():
    try:
        test_email = request.form.get('test_email')
        
        if not test_email:
            flash('Please provide an email address for testing.', 'warning')
            return redirect(url_for('email_settings'))
        
        # Create a test email
        subject = "Test Email from Healthcare System"
        html_body = """
        <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #4070f4; text-align: center;">Healthcare System Test Email</h2>
                    <p>This is a test email to verify that your email configuration is working correctly.</p>
                    <p>If you received this email, your email settings are configured properly!</p>
                    <p style="margin-top: 30px;">Best regards,<br>The Healthcare System Team</p>
                </div>
            </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[test_email],
            html=html_body
        )
        
        mail.send(msg)
        flash('Test email sent successfully!', 'success')
        
    except Exception as e:
        flash(f'Error sending test email: {str(e)}', 'danger')
    
    return redirect(url_for('email_settings'))

# Load email settings from database on startup
def init_app(app):
    # Load email settings from database
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'email_settings'")
        if cursor.fetchone():
            # Get settings
            cursor.execute("SELECT * FROM email_settings WHERE id = 1")
            settings = cursor.fetchone()
            
            if settings:
                app.config['MAIL_SERVER'] = settings['mail_server']
                app.config['MAIL_PORT'] = settings['mail_port']
                app.config['MAIL_USE_TLS'] = settings['mail_use_tls']
                app.config['MAIL_USE_SSL'] = settings['mail_use_ssl']
                app.config['MAIL_USERNAME'] = settings['mail_username']
                app.config['MAIL_PASSWORD'] = settings['mail_password']
                app.config['MAIL_DEFAULT_SENDER'] = settings['mail_default_sender']
                
                # Recreate Mail instance with new settings
                global mail
                mail = Mail(app)
                
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error loading email settings: {str(e)}")

# Add new route for donor notifications via email instead of SMS
@app.route('/send_donor_notification', methods=['POST'])
def send_donor_notification():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'})
    
    data = request.json
    donor_name = data.get('donor_name')
    blood_type = data.get('blood_type')
    receiver_name = data.get('receiver_name', 'A patient')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT mobile FROM b_donation WHERE Name = %s", (donor_name,))
        donor = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not donor or not donor['mobile']:
            return jsonify({'success': False, 'error': 'Donor phone number not found'})
        
        phone_number = donor['mobile']
        if not phone_number.startswith('+'):
            phone_number = '+91' + phone_number
        
        message_body = f"URGENT: Blood Donation Request\n\nHello {donor_name},\n\n{receiver_name} is looking for {blood_type} blood type and would like to connect with you.\n\nPlease respond if you're available to donate.\n\nThank you,\nHealthcare System Team"
        
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        return jsonify({
            'success': True,
            'message': 'SMS notification sent successfully',
            'twilio_message_id': message.sid
        })
        
    except Exception as e:
        app.logger.error(f"Error sending SMS: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    # Call the initialization function before running the app
    init_app(app)
    app.run(debug=True)

    # things which r done
    #
