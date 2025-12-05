import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

API_KEY = "92987762a26afda81f75aea184711a0e"
API_URL = "https://api.openweathermap.org/data/2.5/weather"
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"

def fetch_weather(city: str):
    """Fetch weather data from OpenWeather API."""
    try:
        r = requests.get(API_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        return None

def update_ui(data: dict):
    """Update labels and icon with fetched weather data."""
    if not data:
        messagebox.showerror("Error", "Network problem or invalid city!")
        return
    try:
        info = (
            f"📍 {data['name']}\n\n"
            f"🌡 {data['main']['temp']}°C\n"
            f"💧 {data['main']['humidity']}%\n"
            f"🌬 {data['wind']['speed']} km/h\n"
            f"☁ {data['weather'][0]['description'].capitalize()}\n"
            f"🔽 {data['main']['pressure']} hPa"
        )
        result_lbl.config(text=info)

        # Load icon
        icon_code = data["weather"][0]["icon"]
        icon_data = requests.get(ICON_URL.format(icon_code)).content
        img = ImageTk.PhotoImage(Image.open(BytesIO(icon_data)))
        icon_lbl.config(image=img)
        icon_lbl.image = img
    except KeyError:
        messagebox.showerror("Error", "Invalid data format received.")

def get_weather(event=None):
    city = city_entry.get().strip()
    if not city:
        return messagebox.showwarning("Input Error", "Please enter a city name!")
    update_ui(fetch_weather(city))

# --- UI Setup ---
root = tk.Tk()
root.title("🌤 Weather App")
root.geometry("400x420")
root.configure(bg="#e6f0ff")

frame = tk.Frame(root, bg="#e6f0ff")
frame.pack(pady=20)

tk.Label(frame, text="City:", font=("Arial", 12, "bold"), bg="#e6f0ff").grid(row=0, column=0, padx=6)
city_entry = tk.Entry(frame, font=("Arial", 12), width=18)
city_entry.grid(row=0, column=1, padx=4)
tk.Button(frame, text="Search 🔍", font=("Arial", 10, "bold"), bg="#4da6ff", fg="white",
          cursor="hand2", command=get_weather).grid(row=0, column=2, padx=8)
root.bind("<Return>", get_weather)

icon_lbl = tk.Label(root, bg="#e6f0ff")
icon_lbl.pack(pady=5)

result_lbl = tk.Label(root, text="", font=("Arial", 11), justify="left", bg="#e6f0ff", fg="#333")
result_lbl.pack(pady=10)

tk.Label(root, text="Powered by OpenWeatherMap", font=("Arial", 9, "italic"),
         bg="#e6f0ff", fg="#666").pack(side="bottom", pady=5)

city_entry.focus()
root.mainloop()
