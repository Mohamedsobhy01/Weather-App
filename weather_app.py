import tkinter as tk
from tkinter import messagebox
import requests

api_key = "92987762a26afda81f75aea184711a0e"

def get_weather() :
    city = city_entry.get()
    if not city :
        messagebox.showwarning("Input Error", "Please Enter a City Name!")
        return
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200 :
            data = response.json()

            name = data["name"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            state = data["weather"][0]["description"]
            pressure = data["main"]["pressure"]

            weather_info = (f"City: {name}\n\n"
                    f"Temperature: {temp}°C\n\n"
                    f"Humidity: {humidity}%\n\n"
                    f"Wind Speed: {wind_speed} Km/h\n\n"
                    f"State: {state.capitalize()}\n\n"
                    f"Pressure: {pressure} hPa")

            
            result_label.config(text=weather_info)
        
        else :
            messagebox.showerror("Error", "City Not Found!")
            
    except:
        messagebox.showerror("Error", "Network Proplem!")


window = tk.Tk()
window.title("Weather App")
window.minsize(width=450, height=300)

search_frame = tk.Frame(window, bg="#f2f2f2")
search_frame.grid(row=0, column=0, columnspan=5, pady=20)

title_label = tk.Label(search_frame, text="Location :", font=("Arial", 12))
title_label.grid(row=0, column=0, padx=10)

city_entry = tk.Entry(search_frame, width=20, font=("Arial", 12))
city_entry.grid(row=0, column=1, padx=5)

but_search = tk.Button(search_frame, text="Search", command=get_weather, font=("Arial", 10))
but_search.grid(row=0, column=2, padx=30)

result_label = tk.Label(window, text="", justify="left", font=("Arial", 11))
result_label.grid(row=1, column=0, columnspan=3, pady=20, sticky="w", padx=80)

window.mainloop()