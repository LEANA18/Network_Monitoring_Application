import time
import threading
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
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

        
        graph_button = tk.Button(self.root, text="Show Signal Graph", command=self.show_graph)
        graph_button.pack(pady=5)

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
            connected,dns_server=check_internet()
            status = 'Connected' if connected else 'Disconnected'
            if connected:
                print(f"Internet is connected via DNS: {dns_server}")
            else:
                print(f"Internet is not reachable via any DNS.")
            signal = get_wifi_strength() or 0
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            self.db.insert(timestamp, ip, signal, status)
            self.root.title(f"Network Monitoring Application - {status}")

            if status != self.last_status:
                msg = f"Network {status.lower()}"
                notification.notify(title="Network Monitoring Application", message=msg, timeout=3)
                self.last_status = status

            time.sleep(0.5)
            
    def show_graph(self):
        data = self.db.fetch_all()
        if not data:
            return

        timestamps = [row[0] for row in reversed(data)]
        signals = [row[2] for row in reversed(data)]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(timestamps, signals, marker='o', linestyle='-', color='blue')
        ax.set_title("Wi-Fi Signal Strength Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Signal Strength (%)")

    # Rotate and format x-axis
        ax.tick_params(axis='x', labelrotation=60)

    # Optionally reduce number of labels shown
        if len(timestamps) > 15:
            step = len(timestamps) // 15
            ax.set_xticks(timestamps[::step])

        plt.tight_layout()  # Adjust layout to fit labels

        graph_window = tk.Toplevel(self.root)
        graph_window.title("Signal History")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    NetworkMonitorApp()