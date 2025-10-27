# ===========================================
# 📘 FLASK APP – STUDENT SCORE PREDICTION
# ===========================================

# Importing required libraries
import pickle  # Used for model serialization (optional here)
from flask import Flask, request, render_template  # Flask modules for web app handling
import numpy as np  # Numerical operations
import pandas as pd  # Data handling

# Importing the custom pipeline and data classes
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# ===========================================
# 🔹 INITIALIZE FLASK APPLICATION
# ===========================================
application = Flask(__name__)
app = application


# ===========================================
# 🔹 HOME ROUTE (Landing Page)
# ===========================================
@app.route("/")
def index():
    """
    Displays the main landing page (index.html)
    """
    return render_template("index.html")


# ===========================================
# 🔹 PREDICTION ROUTE (Form submission)
# ===========================================
@app.route("/predictdata", methods=["GET", "POST"])
def predict_datapoint():
    """
    Handles GET (page load) and POST (form submission) requests
    for making predictions.
    """
    if request.method == "GET":
        # When user visits the page, show the input form
        return render_template("home.html")
    
    else:
        # When the user submits the form (POST request)
        # Retrieve form input values and create a CustomData object

        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )
        
        # Convert input data into DataFrame format for prediction
        pred_df = data.get_data_as_data_frame()
        print("Input DataFrame:\n", pred_df)

        # Create a prediction pipeline object
        predict_pipeline = PredictPipeline()
        
        # Get model predictions
        results = predict_pipeline.predict(pred_df)

        # Render result back to the web page
        return render_template('home.html', results=results[0])


# ===========================================
# 🔹 MAIN ENTRY POINT
# ===========================================
if __name__ == "__main__":
    # Run the Flask app on local host (accessible externally as well)
    app.run(host="0.0.0.0", debug=True)
