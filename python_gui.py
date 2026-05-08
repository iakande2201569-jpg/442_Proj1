import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MicroscopeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Specimen Calculator (Legacy GUI)")
        self.root.geometry("500x600")
        
        self.microscopes = {
            'Light Microscope (1000x)': 1000, 
            'Scanning Electron Microscope (100,000x)': 100000, 
            'Transmission Electron Microscope (5,000,000x)': 5000000
        }
        self.units = {'nm': 1e6, 'µm': 1000, 'mm': 1, 'cm': 0.1, 'm': 0.001}
        
        tk.Label(root, text="Username:").pack(pady=5)
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()

        tk.Label(root, text="Measured Size (mm):").pack(pady=5)
        self.size_entry = tk.Entry(root)
        self.size_entry.pack()

        tk.Label(root, text="Microscope Type:").pack(pady=5)
        self.type_var = tk.StringVar()
        self.type_cb = ttk.Combobox(root, textvariable=self.type_var, values=list(self.microscopes.keys()), state="readonly")
        self.type_cb.pack()

        tk.Label(root, text="Output Unit:").pack(pady=5)
        self.unit_var = tk.StringVar()
        self.unit_cb = ttk.Combobox(root, textvariable=self.unit_var, values=list(self.units.keys()), state="readonly")
        self.unit_cb.pack()

        self.img_path = ""
        tk.Button(root, text="Select Image", command=self.upload_image).pack(pady=10)

        tk.Button(root, text="Calculate", command=self.calculate).pack(pady=20)
        
        self.result_label = tk.Label(root, text="Result will appear here")
        self.result_label.pack(pady=10)

    def upload_image(self):
        self.img_path = filedialog.askopenfilename(title="Select Specimen Image")
        if self.img_path:
            messagebox.showinfo("Success", "Image selected successfully.")

    def calculate(self):
        try:
            measured = float(self.size_entry.get())
            mag = self.microscopes[self.type_var.get()]
            unit_mult = self.units[self.unit_var.get()]
            
            real_mm = measured / mag
            final_size = real_mm * unit_mult
            
            self.result_label.config(text=f"Actual Size: {final_size:.4f} {self.unit_var.get()}")
        except Exception as e:
            messagebox.showerror("Error", "Please check your inputs.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MicroscopeApp(root)
    root.mainloop()