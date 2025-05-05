import tkinter as tk
import weather
from location import get_location
from format import display_weather_table
import format
from save import save_favorites, load_favorites  # Import save/load functions

def get_weather(city):
    location = get_location(city)
    if location is None:
        print(f"Error: Unable to find location for city '{city}'.")
        data = None
    elif not isinstance(location.latitude, float) or not isinstance(location.longitude, float) or location.latitude is None or location.longitude is None:
        print(f"Error: Unable to find location for city '{city}'.")
        data = None
    else:
        print(f"Location: {location}")
        print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
        data = weather.get_12hr_forecast(location.latitude, location.longitude)
    return data

def app_visual():
    top = tk.Tk()
    top.title("Weather App")
    top.geometry("800x400")
    top.configure(bg="#2C2F33")

    # Load favorites
    favorites = load_favorites()

    # Title Label
    title_label = tk.Label(
        top, text="Weather App", bg="#2C2F33", fg="#FFFFFF",
        font=("Arial", 20, "bold"), pady=10
    )
    title_label.pack()

    # Main Layout
    main_frame = tk.Frame(top, bg="#2C2F33")
    main_frame.pack(fill="both", expand=True)

    # Favorites Section
    favorites_frame = tk.Frame(main_frame, bg="#23272A", width=200)
    favorites_frame.pack(side=tk.LEFT, fill="y")

    def add_to_favorites():
        city = city_entry.get()
        if not city:
            print("Error: City name cannot be empty.")
            return

        # Validate the city by checking if weather data can be fetched
        weather_data = get_weather(city)
        if weather_data is None:
            print(f"Error: Unable to fetch weather data for '{city}'. Cannot add to favorites.")
            return

        if city not in favorites:
            favorites[city] = "Saved"
            save_favorites(favorites)
            update_favorites()
            print(f"{city} added to favorites.")

    # Add to Favorites Button
    favorite_button = tk.Button(
        favorites_frame, text="Add to Favorites", command=add_to_favorites,
        bg="#43B581", fg="#FFFFFF", font=("Arial", 12), padx=10, pady=5
    )
    favorite_button.pack(fill="x", pady=5)

    # Favorites Label (ensure it's below the button)
    favorites_label = tk.Label(
        favorites_frame, text="Favorites", bg="#23272A", fg="#FFFFFF",
        font=("Arial", 14, "bold"), pady=10
    )
    favorites_label.pack()

    def update_favorites():
        for widget in favorites_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        for city in favorites.keys():
            city_frame = tk.Frame(favorites_frame, bg="#23272A")
            city_frame.pack(fill="x", pady=2)

            city_button = tk.Button(
                city_frame, text=city, bg="#7289DA", fg="#FFFFFF",
                font=("Arial", 12), padx=10, pady=5,
                command=lambda c=city: on_submit_from_favorite(c)
            )
            city_button.pack(side=tk.LEFT, fill="x", expand=True)

            remove_button = tk.Button(
                city_frame, text="X", bg="#F04747", fg="#FFFFFF",
                font=("Arial", 12), padx=5, pady=5,
                command=lambda c=city: remove_from_favorites(c)
            )
            remove_button.pack(side=tk.RIGHT)

    def remove_from_favorites(city):
        if city in favorites:
            del favorites[city]
            save_favorites(favorites)
            update_favorites()
            print(f"{city} removed from favorites.")

    update_favorites()

    # Weather Section
    weather_frame = tk.Frame(main_frame, bg="#2C2F33")
    weather_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)

    # City Input Section
    input_frame = tk.Frame(weather_frame, bg="#2C2F33", pady=10)
    input_frame.pack()

    city_label = tk.Label(
        input_frame, text="Enter city name:", bg="#2C2F33", fg="#FFFFFF",
        font=("Arial", 12)
    )
    city_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    city_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    city_entry.grid(row=0, column=1, padx=5, pady=5)

    def on_submit():
        city = city_entry.get()

        # Clear previous weather data
        for widget in weather_frame.winfo_children():
            if widget != input_frame:
                widget.destroy()

        # Fetch weather data
        weather_data = get_weather(city)
        if weather_data is None:
            error_label = tk.Label(
                weather_frame, text="Error: Unable to fetch weather data. Please try again.",
                bg="#2C2F33", fg="#FF0000", font=("Arial", 12, "bold")
            )
            error_label.pack(anchor="w", pady=5)
            return

        # Display weather data
        weather_data = display_weather_table(weather_data)

        grouped_data = {}
        for entry in weather_data:
            day = entry['Start Time'].split("T")[0]
            if day not in grouped_data:
                grouped_data[day] = []
            grouped_data[day].append(entry)

        for day, forecasts in grouped_data.items():
            day_frame = tk.Frame(weather_frame, bg="#2C2F33", padx=10)
            day_frame.pack(side=tk.LEFT, fill="y", padx=10)

            day_label = tk.Label(
                day_frame, text=f"{day}", bg="#2C2F33", fg="#FFFFFF",
                font=("Arial", 14, "bold")
            )
            day_label.pack(anchor="n", pady=5)

            for forecast in forecasts:
                forecast_frame = tk.Frame(day_frame, bg="#2C2F33", pady=5)
                forecast_frame.pack(fill="x", pady=5)

                short_forecast = tk.Label(
                    forecast_frame,
                    text="".join([format.emoji_from_forecast(x) for x in format.format_short_forecast(forecast['Short Forecast'])]),
                    bg="#2C2F33", fg="#FFFFFF", font=("Segoe UI Emoji", 24)
                )
                short_forecast.pack(anchor="w", padx=5)

                forecast_label = tk.Label(
                    forecast_frame,
                    text=f"{forecast['Name']}",
                    bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12)
                )
                forecast_label.pack(anchor="w", padx=10)

                forecast_label = tk.Label(
                    forecast_frame,
                    text=f"{forecast['Temperature']}",
                    bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12)
                )
                forecast_label.pack(anchor="w", padx=10)
                
                forecast_label = tk.Label(
                    forecast_frame,
                    text=f"{forecast['Wind']}",
                    bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12)
                )
                forecast_label.pack(anchor="w", padx=10)

    def on_submit_from_favorite(city):
        city_entry.delete(0, tk.END)  # Clear the entry field
        city_entry.insert(0, city)   # Set the entry field to the selected city
        on_submit()                  # Call the on_submit function

    submit_button = tk.Button(
        input_frame, text="Submit", command=on_submit,
        bg="#7289DA", fg="#FFFFFF", font=("Arial", 12), padx=10, pady=5
    )
    submit_button.grid(row=0, column=2, padx=5, pady=5)

    top.mainloop()

app_visual()
