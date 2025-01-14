import tkinter as tk
from tkinter import filedialog, messagebox
from distance import read_data, plot_histogram, calculate_distance, add_coordinates

class DistanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Distance to Practice")
        
        # Latitude Input
        self.label_lat = tk.Label(root, text="Enter the latitude of the practice:")
        self.label_lat.pack(pady=5)
        
        self.latitude_entry = tk.Entry(root, width=30)
        self.latitude_entry.pack(pady=5)
        
        # Longitude Input
        self.label_lon = tk.Label(root, text="Enter the longitude of the practice:")
        self.label_lon.pack(pady=5)
        
        self.longitude_entry = tk.Entry(root, width=30)
        self.longitude_entry.pack(pady=5)
        
        # Upload Button
        self.upload_button = tk.Button(root, text="Upload Raw Data", command=self.upload_file)
        self.upload_button.pack(pady=20)
        
        # Calculate Distances Button
        self.calculate_button = tk.Button(root, text="Calculate Distances", command=self.calculate_distances)
        self.calculate_button.pack(pady=10)
        
        self.file_path = None

    def upload_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {self.file_path}")

    def calculate_distances(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a raw data file first.")
            return
        
        try:
            practice_lat = float(self.latitude_entry.get())
            practice_lon = float(self.longitude_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric coordinates for latitude and longitude.")
            return
        
        data = read_data(self.file_path)
        data = add_coordinates(data)
        data['distance'] = data.apply(
            lambda row: calculate_distance(practice_lat, practice_lon, row['latitude'], row['longitude']) 
            if row['latitude'] and row['longitude'] else None, axis=1
        )
        
        plot_histogram(data.dropna(subset=['distance']))

if __name__ == "__main__":
    root = tk.Tk()
    app = DistanceApp(root)
    root.mainloop()
