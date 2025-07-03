import time
import threading
import tkinter as tk
from tkinter import ttk
from db_handler import DBHandler
from net_utils import get_current_ip, check_internet, get_wifi_strength
from tray_icon import run_tray
from plyer import notification

class NetworkMonitorApp:
    def __init__(self):
        self.db = DBHandler()
        self.last_status = None
        self.root = tk.Tk()
        self.root.title("Network Monitoring Application")
        self.root.geometry("400x300")
        self.tree = ttk.Treeview(self.root, columns=('Time', 'IP', 'Signal', 'Status'), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.running = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        self.refresh_history()

        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        threading.Thread(target=run_tray, args=(self.show_window, self.stop), daemon=True).start()
        self.root.mainloop()

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()
        self.refresh_history()

    def stop(self):
        self.running = False
        self.root.quit()

    def refresh_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in self.db.fetch_all():
            self.tree.insert('', 'end', values=entry)

    def monitor_loop(self):
        while self.running:
            ip = get_current_ip()
            status = 'Connected' if check_internet() else 'Disconnected'
            signal = get_wifi_strength() or 0
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            self.db.insert(timestamp, ip, signal, status)

            if status != self.last_status:
                msg = f"Network {status.lower()}"
                notification.notify(title="Network Monitoring Application", message=msg, timeout=3)
                self.last_status = status

            time.sleep(0.5)

if __name__ == "__main__":
    NetworkMonitorApp()