import json

def save_favorites(favorites, file_path="preferences.txt"):
    try:
        with open(file_path, "w") as file:
            json.dump(favorites, file, indent=4)  # Save as a JSON dictionary
        print(f"Favorites saved successfully to {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving favorites: {e}")

def load_favorites(file_path="preferences.txt"):
    try:
        with open(file_path, "r") as file:
            favorites = json.load(file)  # Load as a JSON dictionary
        print(f"Favorites loaded successfully from {file_path}.")
        return favorites
    except FileNotFoundError:
        print(f"No favorites found at {file_path}.")
        return {}
    except Exception as e:
        print(f"An error occurred while loading favorites: {e}")
        return {}