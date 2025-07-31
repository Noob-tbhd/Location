import tkinter as tk
from tkinter import messagebox
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import webbrowser

# ✅ Your OpenCage API Key
OPENCAGE_API_KEY = "c882e23e2fe54537b2b155339790a742"

def track_number():
    number = entry.get()
    try:
        parsed_number = phonenumbers.parse(number)
        location = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")

        # Use OpenCage to geocode the location
        geocoder_api = OpenCageGeocode(OPENCAGE_API_KEY)
        query = str(location)
        results = geocoder_api.geocode(query)

        if results and len(results):
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']

            # Display results in the GUI
            result_label.config(
                text=f"Location: {location}\nCarrier: {service_provider}\nLatitude: {lat}\nLongitude: {lng}"
            )

            # Create and save a map
            map_location = folium.Map(location=[lat, lng], zoom_start=10)
            folium.Marker([lat, lng], popup=location).add_to(map_location)
            map_location.save("location.html")

            # Open the map in browser
            webbrowser.open("location.html")
        else:
            messagebox.showerror("Error", "Location not found. Try a different number.")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid number or API issue:\n{e}")

# GUI Setup
app = tk.Tk()
app.title("Phone Number Tracker")
app.geometry("400x300")
app.configure(bg="#f0f0f0")

tk.Label(app, text="Enter Phone Number (+880...):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
entry = tk.Entry(app, width=30, font=("Arial", 12))
entry.pack()

tk.Button(app, text="Track", command=track_number, font=("Arial", 12), bg="#4caf50", fg="white").pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 11), bg="#f0f0f0", justify="left")
result_label.pack(pady=20)

app.mainloop()
