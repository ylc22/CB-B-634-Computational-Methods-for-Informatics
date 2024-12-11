from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os

# Load necessary data
data_path = 'preprocessed_survey.csv'
df = pd.read_csv(data_path)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Home route to render index.html
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint: /summary - Returns summary statistics as JSON
@app.route('/summary', methods=['GET'])
def summary():
    try:
        summary_stats = df.describe(include='all').fillna('N/A').to_dict()
        return jsonify(summary_stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: /correlation - Returns correlation matrix as JSON
@app.route('/correlation', methods=['GET'])
def correlation():
    try:
        correlation_matrix = df.corr(numeric_only=True).fillna(0).to_dict()
        return jsonify(correlation_matrix)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: /sentiment_analysis - Returns sentiment analysis image
@app.route('/sentiment_analysis', methods=['GET'])
def sentiment_analysis():
    return send_from_directory('static', 'sentiment_analysis.png')

# Endpoint: /geographical_trends - Returns geographical trends image
@app.route('/geographical_trends', methods=['GET'])
def geographical_trends():
    return send_from_directory('static', 'geographical_trends.png')

# Endpoint: /logistic_regression - Returns logistic regression predictions and metrics
@app.route('/logistic_regression', methods=['POST'])
def logistic_regression():
    try:
        # Features and target
        features = ['age', 'stigma_score', 'employer_support_score']
        target = 'treatment'
        X = df[features].dropna()
        y = df.loc[X.index, target].map({'Yes': 1, 'No': 0})

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Logistic Regression Model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Metrics
        report = classification_report(y_test, y_pred, output_dict=True)
        confusion = confusion_matrix(y_test, y_pred).tolist()

        return jsonify({
            "classification_report": report,
            "confusion_matrix": confusion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
