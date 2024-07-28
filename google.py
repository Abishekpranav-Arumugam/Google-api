from flask import Flask, request, render_template, jsonify
import pandas as pd
from fuzzywuzzy import process
import re

app = Flask(__name__)

# Load the CSV file
df = pd.read_csv('UGC Universities.csv')

# Preprocess the Data
df['Address'] = df['Address'].str.strip()

# Define Function for Details Retrieval
def find_details(identifier):
    # Try matching with email addresses
    matched_rows = df[df['Email'] == identifier]
    if not matched_rows.empty:
        return matched_rows.iloc[0].to_dict()

    # Try matching with websites
    matched_rows = df[df['Website'] == identifier]
    if not matched_rows.empty:
        return matched_rows.iloc[0].to_dict()

    # Fuzzy matching for college names
    matches = process.extract(identifier, df['Name'], limit=1)
    closest_match = matches[0][0]
    if matches[0][1] < 80:  # Set a threshold for similarity score
        return None  # If similarity score is too low, return None
    matched_rows = df[df['Name'] == closest_match]
    if not matched_rows.empty:
        return matched_rows.iloc[0].to_dict()

    return None

# Define Flask Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.lower() == 'exit':
            return "Exiting the program."
        else:
            details = find_details(user_input)
            if details:
                result = "Details:\n"
                for key, value in details.items():
                    result += f"{key}: {value}\n"
                return result
            else:
                return "No matching records found for the provided input."
    else:
        return render_template('sam1.html')

# Route to handle AJAX request from the HTML page
@app.route('/get_details', methods=['POST'])
def get_details():
    user_input = request.form['user_input']
    details = find_details(user_input)
    if details:
        result = "<center><p><b>Details:</b></p></center>"
        for key, value in details.items():
            result += f"<p>{key}: {value}</p>"
        return result
    else:
        return "No matching records found for the provided input."

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
