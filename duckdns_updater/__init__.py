import tkinter as tk
import requests
import pystray
import time
import threading
from tkinter import messagebox
from PIL import Image
from os import linesep, path
from sys import exit

class DuckDNSUpdater:
    def __init__(self):
        self.config = {"subdomain": "", "token": ""}
        self.config_file = "duckupdatercfg.txt"
        self.window = tk.Tk()
        self.icon = None
        self.window.title("DuckDNS IP Updater")
        self.window.resizable(False, False)
        self.txtdomain = tk.StringVar()
        self.txttoken = tk.StringVar()
        self.create_ui()
        self.load_config()

    def create_ui(self):
        title_label = tk.Label(self.window, text="DuckDNS IP Updater", font=("Arial", 20))
        subdomain_label = tk.Label(self.window, text="DuckDNS Subdomain:")
        self.subdomain_entry = tk.Entry(self.window, width=30, textvariable=self.txtdomain)
        token_label = tk.Label(self.window, text="DuckDNS Token:")
        self.token_entry = tk.Entry(self.window, width=30, textvariable=self.txttoken)
        update_button = tk.Button(self.window, text="Update IP now", width=20, command=self.update_duckdns)
        save_button = tk.Button(self.window, text="Save Config", width=20, command=self.save_config)
        load_button = tk.Button(self.window, text="Load Config", width=20, command=self.load_config)
        self.result_label = tk.Label(self.window, text="", font=("Arial", 14))

        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        subdomain_label.grid(row=1, column=0, sticky="E", padx=10, pady=5)
        self.subdomain_entry.grid(row=1, column=1, padx=10, pady=5)
        token_label.grid(row=2, column=0, sticky="E", padx=10, pady=5)
        self.token_entry.grid(row=2, column=1, padx=10, pady=5)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)
        save_button.grid(row=4, column=0, columnspan=2, pady=5)
        load_button.grid(row=5, column=0, columnspan=2, pady=5)
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)
        # Create a thread to update DuckDNS every 30 minutes
        update_thread = threading.Thread(target=self.update_periodically)
        update_thread.daemon = True
        update_thread.start()
        # Create a system tray icon        
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        _script_dir = path.dirname(path.abspath(__file__))
        _icon_path = path.join(_script_dir, 'icon.ico')
        icon_image = Image.open(_icon_path)  # ICO file
        menu = (
            pystray.MenuItem("Show", self.on_display),
            pystray.MenuItem("Update IP", self.update_duckdns),
            pystray.MenuItem("Exit program", self.exit_program)
        )
        self.icon = pystray.Icon("DuckDNS Updater", icon_image, menu=menu)
        systray_thread = threading.Thread(target=self.run_systray)
        systray_thread.daemon = True
        systray_thread.start()
        # Start the tkinter main loop
        self.window.mainloop()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    self.config[key] = value
            if not self.config['subdomain'] or not self.config['token']:
                self.result_label.config(text="Empty subdomain or token.", fg="red")
            else:
                self.txtdomain.set(self.config['subdomain'])
                self.txttoken.set(self.config['token'])
                self.result_label.config(text="Config loaded", fg="green")
        except FileNotFoundError:
            messagebox.showinfo("Alert", "Configuration file not found. You must create one.")

    def save_config(self):
        self.config["subdomain"] = self.subdomain_entry.get().strip()
        self.config["token"] = self.token_entry.get().strip()
        try:
            with open(self.config_file, "wb") as f:
                f.write(f"subdomain={self.config['subdomain']}{linesep}".encode())
                f.write(f"token={self.config['token']}".encode())
            messagebox.showinfo("Info", "Saved the configuration to disk!")
        except Exception:
            messagebox.showinfo("Alert", "Error saving configuration to disk!")

    def update_duckdns(self):
        self.load_config()
        subdomain = self.config["subdomain"]
        token = self.config["token"]
        if not subdomain or not token:
            self.result_label.config(text="Need a subdomain and token.", fg="red")
            return

        try:
            response = requests.get(f"https://www.duckdns.org/update?domains={subdomain}&token={token}&ip=")
            if response.status_code == 200 and response.text == "OK":
                self.result_label.config(text="IP updated in DuckDNS.org!", fg="green")
            else:
                messagebox.showinfo("Error", "Verify subdomain and token.")
                self.result_label.config(text=f"Error updating IP. Status code: {response.status_code}", fg="red")
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"Error: {str(e)}")

    def update_periodically(self):
        while True:
            self.update_duckdns()
            time.sleep(1800)  # Sleep for 30 minutes (30 * 60 seconds)

    def run_systray(self):
        self.icon.run()

    def on_display(self):
        self.window.deiconify()
        self.window.lift()

    def on_exit(self):
        self.window.withdraw()

    def exit_program(self):
        self.window.destroy()  # Close the main window and terminate the program
        exit()

def main():
    app = DuckDNSUpdater()
    self.run_systray()
    self.window.mainloop()

if __name__ == "__main__":
    main()    
