from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)

# Function to load and return a random quote
def load_random_quote():
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as file:
            quotes = json.load(file)
            if quotes:
                random_quote = random.choice(quotes)

                # Ensure characters is always treated as a list
                if "characters" in random_quote:
                    characters = random_quote["characters"]
                else:
                    characters = [random_quote["character"]]
                
                return {
                    "season": random_quote["season"],
                    "episode": random_quote["episode"],
                    "characters": ", ".join(characters),
                    "quote": random_quote["quote"]
                }
    return None

# Route for the main page
@app.route('/')
def index():
    random_quote = load_random_quote()
    return render_template('index.html', quote=random_quote)

# Route to handle adding a new quote
@app.route('/add', methods=['POST'])
def add_quote():
    season = request.form.get('season')
    episode = request.form.get('episode')
    characters = request.form.getlist('characters[]')  # Corrected to match the form name attribute
    quote = request.form.get('quote')

    new_quote = {
        "season": season,
        "episode": episode,
        "characters": characters,  # Save as a list
        "quote": quote
    }

    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as file:
            quotes = json.load(file)
    else:
        quotes = []

    quotes.append(new_quote)

    with open("quotes.json", "w") as file:
        json.dump(quotes, file, indent=4)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
