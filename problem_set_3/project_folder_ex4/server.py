from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv("happiness_data.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    # Get user input
    country = request.form["country"].strip()
    
    # Filter dataset for matching country
    result = data[data["Country"].str.lower() == country.lower()]
    
    # Check if any matching data is found
    if not result.empty:
        # Retrieve relevant data for the specified country
        rank = result.iloc[0]["Happiness Rank"]
        score = result.iloc[0]["Happiness Score"]
        gdp = result.iloc[0]["Economy (GDP per Capita)"]
        family = result.iloc[0]["Family"]
        health = result.iloc[0]["Health (Life Expectancy)"]
        freedom = result.iloc[0]["Freedom"]
        trust = result.iloc[0]["Trust (Government Corruption)"]
        generosity = result.iloc[0]["Generosity"]
        
        return render_template(
            "result.html", country=country, rank=rank, score=score, gdp=gdp,
            family=family, health=health, freedom=freedom, trust=trust, generosity=generosity
        )
    else:
        # Show error if the country is not found
        return render_template("result.html", error="Data not found for specified country.")

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change to 5001 or other available port if needed
