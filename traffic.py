import tkinter as tk
import time

class TrafficSignal:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Signal Simulation")
        self.root.geometry("300x500")
        self.root.resizable(False, False)

        # Canvas for drawing the traffic signal
        self.canvas = tk.Canvas(self.root, bg="black", height=500, width=300)
        self.canvas.pack()

        # Draw the outline of the signal box
        self.canvas.create_rectangle(80, 50, 220, 400, outline="white", width=3)

        # Create the three lights (initially gray/off)
        self.red_light = self.canvas.create_oval(100, 70, 200, 170, fill="gray")
        self.orange_light = self.canvas.create_oval(100, 190, 200, 290, fill="gray")
        self.green_light = self.canvas.create_oval(100, 310, 200, 410, fill="gray")

        # Label to show current status
        self.status_label = tk.Label(self.root, text="Status: Initializing...", font=("Arial", 14), bg="black", fg="white")
        self.status_label.place(x=60, y=450)

        # Start the signal cycle
        self.running = True
        self.signal_cycle()

    def signal_cycle(self):
        """Cycle through Red → Green → Orange lights"""
        while self.running:
            # Red light ON
            self.set_light("red")
            self.status_label.config(text="Status: STOP", fg="red")
            self.root.update()
            time.sleep(5)

            # Green light ON
            self.set_light("green")
            self.status_label.config(text="Status: GO", fg="green")
            self.root.update()
            time.sleep(5)

            # Orange light ON
            self.set_light("orange")
            self.status_label.config(text="Status: WAIT", fg="orange")
            self.root.update()
            time.sleep(2)

    def set_light(self, color):
        """Turn on the specified color and turn off others"""
        colors = {"red": "gray", "orange": "gray", "green": "gray"}
        colors[color] = color
        self.canvas.itemconfig(self.red_light, fill=colors["red"])
        self.canvas.itemconfig(self.orange_light, fill=colors["orange"])
        self.canvas.itemconfig(self.green_light, fill=colors["green"])

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficSignal(root)
    root.mainloop()
