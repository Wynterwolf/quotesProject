import tkinter as tk
from tkinter import ttk
import json
import os
import random

# Create the main window
root = tk.Tk()
root.title("Supernatural Quotes Manager")
root.geometry("400x300")

# Season dropdown
season_label = ttk.Label(root, text="Season:")
season_label.pack(pady=10)
season_var = tk.StringVar()
season_dropdown = ttk.Combobox(root, textvariable=season_var)
season_dropdown['values'] = [f"Season {i}" for i in range(1, 16)]  # Assuming 15 seasons
season_dropdown.pack()

# Episode dropdown
episode_label = ttk.Label(root, text="Episode:")
episode_label.pack(pady=10)
episode_var = tk.StringVar()
episode_dropdown = ttk.Combobox(root, textvariable=episode_var)
episode_dropdown['values'] = [f"Episode {i}" for i in range(1, 23)]  # Assuming 22 episodes per season
episode_dropdown.pack()

# Character dropdown (now a multi-select Listbox)
character_label = ttk.Label(root, text="Character(s):")
character_label.pack(pady=10)

character_listbox = tk.Listbox(root, selectmode="multiple", height=6)
character_listbox.insert(1, "Dean Winchester")
character_listbox.insert(2, "Sam Winchester")
character_listbox.insert(3, "Castiel")
character_listbox.insert(4, "Bobby Singer")
# Add more characters as needed
character_listbox.pack()

# Entering Quotes
quote_label = ttk.Label(root, text="Quote:")
quote_label.pack(pady=10)
quote_entry = tk.Text(root, height=4, width=40)
quote_entry.pack()

# Label to display the random quote
display_quote_label = tk.Label(root, text="", wraplength=350)
display_quote_label.pack(pady=20)

# Function to load and display a random quote
def load_random_quote():
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as file:
            quotes = json.load(file)
            if quotes:
                random_quote = random.choice(quotes)
                display_quote_label.config(
                    text=f"Season: {random_quote['season']}, Episode: {random_quote['episode']}, Characters: {', '.join(random_quote['characters'])}\n\n{random_quote['quote']}"
                )
            else:
                display_quote_label.config(text="No quotes available.")
    else:
        display_quote_label.config(text="No quotes found.")

# Submit button
def submit_quote():
    season = season_var.get()
    episode = episode_var.get()
    selected_characters = character_listbox.curselection()
    characters = [character_listbox.get(i) for i in selected_characters]
    quote = quote_entry.get("1.0", "end-1c")  # Get text from text widget
    
    new_quote = {
        "season": season,
        "episode": episode,
        "characters": characters,  # Use list of selected characters
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

    season_var.set('')
    episode_var.set('')
    character_listbox.selection_clear(0, 'end')  # Clear all selections
    quote_entry.delete("1.0", "end")
    load_random_quote()  # Update the displayed quote after adding a new one


# Add quote button
submit_button = ttk.Button(root, text="Add Quote", command=submit_quote)
submit_button.pack(pady=20)

# Load a random quote when the program starts
load_random_quote()

# Start the main loop
root.mainloop()