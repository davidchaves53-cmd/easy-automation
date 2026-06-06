import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# ============================================================
# ALWAYS USE THE FOLDER WHERE main.py IS LOCATED
# ============================================================

BASE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_ORDERS = os.path.join(BASE, "orders_2024.csv")
DEFAULT_LISTINGS = os.path.join(BASE, "listings_export.csv")
OUTPUT_PATH = os.path.join(BASE, "daily_output.csv")

# ============================================================
# CSV LOADER
# ============================================================

def load_csv(path, label):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{label} not found at:\n{path}")

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise Exception(f"Error loading {label}: {e}")

# ============================================================
# MERGE LOGIC
# ============================================================

def merge_orders_listings(orders, listings):
    if "SKU" not in orders.columns:
        raise ValueError("Orders CSV missing required column: SKU")
    if "SKU" not in listings.columns:
        raise ValueError("Listings CSV missing required column: SKU")

    merged = orders.merge(listings, on="SKU", how="left")
    return merged

# ============================================================
# GUI ACTION
# ============================================================

def run_merge():
    try:
        status_label.config(text="Loading CSV files...")
        progress["value"] = 10
        root.update_idletasks()

        orders = load_csv(orders_path.get(), "Orders")
        listings = load_csv(listings_path.get(), "Listings")

        status_label.config(text="Merging data...")
        progress["value"] = 50
        root.update_idletasks()

        merged = merge_orders_listings(orders, listings)

        status_label.config(text="Saving output...")
        progress["value"] = 80
        root.update_idletasks()

        merged.to_csv(OUTPUT_PATH, index=False)

        progress["value"] = 100
        status_label.config(text="Done!")

        messagebox.showinfo("Success", f"Output saved to:\n{OUTPUT_PATH}")

        # Auto-open folder
        webbrowser.open(BASE)

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Error occurred")
        progress["value"] = 0

# ============================================================
# FILE PICKERS
# ============================================================

def pick_orders():
    file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file:
        orders_path.set(file)

def pick_listings():
    file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file:
        listings_path.set(file)

# ============================================================
# GUI WINDOW
# ============================================================

root = tk.Tk()
root.title("Easy Automation — GUI Edition")
root.geometry("450x350")
root.configure(bg="#1e1e1e")

# Text variables
orders_path = tk.StringVar(value=DEFAULT_ORDERS)
listings_path = tk.StringVar(value=DEFAULT_LISTINGS)

# Title
title_label = tk.Label(root, text="Easy Automation Tool", font=("Arial", 18), fg="white", bg="#1e1e1e")
title_label.pack(pady=15)

# Orders picker
orders_frame = tk.Frame(root, bg="#1e1e1e")
orders_frame.pack(pady=5)
tk.Label(orders_frame, text="Orders CSV:", fg="white", bg="#1e1e1e").pack(side="left")
tk.Entry(orders_frame, textvariable=orders_path, width=40).pack(side="left", padx=5)
tk.Button(orders_frame, text="Browse", command=pick_orders).pack(side="left")

# Listings picker
listings_frame = tk.Frame(root, bg="#1e1e1e")
listings_frame.pack(pady=5)
tk.Label(listings_frame, text="Listings CSV:", fg="white", bg="#1e1e1e").pack(side="left")
tk.Entry(listings_frame, textvariable=listings_path, width=40).pack(side="left", padx=5)
tk.Button(listings_frame, text="Browse", command=pick_listings).pack(side="left")

# Run button
run_button = tk.Button(root, text="Run Merge", font=("Arial", 14), command=run_merge)
run_button.pack(pady=20)

# Progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

# Status label
status_label = tk.Label(root, text="Waiting...", fg="white", bg="#1e1e1e")
status_label.pack(pady=5)

root.mainloop()
