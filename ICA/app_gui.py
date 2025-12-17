import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import phase_1
import phase_2
import phase_3

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()
    def flush(self): pass

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenMeteo Weather System")
        self.root.geometry("650x600")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        tk.Label(root, text="Historical Weather Data System", font=("Arial", 16, "bold"), bg="#333", fg="white", pady=10).pack(fill="x")

        # Main Container
        paned = ttk.PanedWindow(root, orient=tk.VERTICAL)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        controls = tk.Frame(paned)
        paned.add(controls, weight=1)

        # --- SECTION 1: Data (Phase 3) ---
        tk.Label(controls, text="Phase 3: Data Pipeline", font=("Arial", 11, "bold"), fg="blue").pack(anchor="w", pady=(0,5))
        ttk.Button(controls, text="Fetch & Update Data (Abuja, NYC, Tokyo, etc)", command=self.run_update).pack(fill="x", pady=5)
        
        ttk.Separator(controls, orient="horizontal").pack(fill="x", pady=10)

        # --- SECTION 2: Visualization (Phase 2) ---
        tk.Label(controls, text="Phase 2: Visualizations", font=("Arial", 11, "bold"), fg="blue").pack(anchor="w", pady=(0,5))
        
        # ID Input
        f_id = tk.Frame(controls)
        f_id.pack(fill="x", pady=5)
        tk.Label(f_id, text="City ID:").pack(side="left")
        self.ent_id = tk.Entry(f_id, width=5)
        self.ent_id.insert(0, "1")
        self.ent_id.pack(side="left", padx=5)
        
        # Buttons
        f_btns = tk.Frame(controls)
        f_btns.pack(fill="x")
        ttk.Button(f_btns, text="Precipitation (Bar)", command=lambda: self.plot(1)).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(f_btns, text="Temp Stats (Group)", command=lambda: self.plot(2)).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(f_btns, text="Trends (Line)", command=lambda: self.plot(3)).grid(row=1, column=0, sticky="ew", padx=2)
        ttk.Button(f_btns, text="Scatter Plot", command=lambda: self.plot(4)).grid(row=1, column=1, sticky="ew", padx=2)
        f_btns.columnconfigure(0, weight=1)
        f_btns.columnconfigure(1, weight=1)

        ttk.Separator(controls, orient="horizontal").pack(fill="x", pady=10)

        # --- SECTION 3: Reports (Phase 1) ---
        tk.Label(controls, text="Phase 1: Database Reports", font=("Arial", 11, "bold"), fg="blue").pack(anchor="w", pady=(0,5))
        ttk.Button(controls, text="Run Text Reports", command=self.run_reports).pack(fill="x")

        # --- Log Window ---
        log_frame = tk.Frame(paned)
        paned.add(log_frame, weight=3)
        tk.Label(log_frame, text="System Log:", font=("Arial", 9, "bold")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True)

        # Redirect Print
        sys.stdout = ConsoleRedirector(self.log_area)
        print("System Ready.")

    def run_update(self):
        def task():
            try: phase_3.main()
            except Exception as e: print(e)
        threading.Thread(target=task).start()

    def plot(self, type_):
        try:
            cid = int(self.ent_id.get())
            print(f"Plotting Chart {type_} for City {cid}...")
            if type_ == 1: phase_2.plot_precipitation_bar_chart(cid, "2020-01-01")
            elif type_ == 2: phase_2.plot_temp_stats_grouped_bar(cid, "2020-01-01")
            elif type_ == 3: phase_2.plot_multi_line_temp(cid, "2020")
            elif type_ == 4: phase_2.plot_temp_vs_rain_scatter(cid)
        except ValueError: print("Invalid City ID")

    def run_reports(self):
        print("\n--- Running Phase 1 Reports ---")
        conn = phase_1.sqlite3.connect("CIS4044-N-SDI-OPENMETEO-PARTIAL.db")
        phase_1.select_all_countries(conn)
        phase_1.select_all_cities(conn)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()