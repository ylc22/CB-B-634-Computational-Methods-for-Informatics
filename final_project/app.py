# Import necessary libraries
from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import json

# Load necessary data and models
data_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df = pd.read_csv(data_path)

# Create Flask app
app = Flask(__name__)

# Endpoint: /summary - Returns summary statistics
@app.route('/summary', methods=['GET'])
def summary():
    summary_stats = df.describe(include='all').to_dict()
    return jsonify(summary_stats)

# Endpoint: /correlation - Returns correlation matrix
@app.route('/correlation', methods=['GET'])
def correlation():
    correlation_matrix = df.corr(numeric_only=True).to_dict()
    return jsonify(correlation_matrix)

# Endpoint: /logistic_regression - Returns logistic regression predictions
@app.route('/logistic_regression', methods=['POST'])
def logistic_regression():
    # Load the trained logistic regression model
    model = joblib.load('logistic_regression_model.pkl')
    
    # Parse input data
    input_data = request.json
    input_df = pd.DataFrame(input_data)
    
    # Predict treatment likelihood
    predictions = model.predict(input_df).tolist()
    return jsonify({"predictions": predictions})

# Endpoint: /sentiment_analysis - Returns sentiment analysis results
@app.route('/sentiment_analysis', methods=['GET'])
def sentiment_analysis():
    # Load sentiment analysis results
    sentiment_counts = df['sentiment'].value_counts().to_dict()
    return jsonify(sentiment_counts)

# Endpoint: /geographical_trends - Returns country-based analysis
@app.route('/geographical_trends', methods=['GET'])
def geographical_trends():
    country_trends = df.groupby('country')['treatment'].value_counts().unstack(fill_value=0)
    country_trends['Total'] = country_trends.sum(axis=1)
    country_trends['Support Rate'] = (country_trends['Yes'] / country_trends['Total']) * 100
    return country_trends[['Support Rate']].to_dict()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def home():
    return "Welcome to the Mental Health Analysis API! Available endpoints: /summary, /correlation, /logistic_regression, /sentiment_analysis, /geographical_trends"
