import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import pytz

# ============= CONFIG ==================
TASKS_FILE = "tasks.txt"
CITY = "Karachi"
TIMEZONE = pytz.timezone("Asia/Karachi")

# Simple static prayer times for Karachi (approx daily average)
PRAYER_TIMES = {
    "Fajr": "05:15",
    "Dhuhr": "12:30",
    "Asr": "15:45",
    "Maghrib": "17:50",
    "Isha": "19:30"
}
# =======================================


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do + Prayer Time App (Karachi)")
        self.root.geometry("450x600")
        self.root.config(bg="#f7f7f7")

        # ---------- Header ----------
        tk.Label(
            root, text="🕌 To-Do + Prayer Timings",
            font=("Helvetica", 16, "bold"), bg="#f7f7f7", fg="#333"
        ).pack(pady=10)

        # ---------- Prayer Frame ----------
        self.prayer_frame = tk.Frame(root, bg="#fff", bd=1, relief="solid")
        self.prayer_frame.pack(pady=10, padx=15, fill="x")

        tk.Label(
            self.prayer_frame, text=f"City: {CITY}", font=("Helvetica", 12, "bold"),
            bg="#fff"
        ).pack(pady=(5, 0))

        self.prayer_label = tk.Label(
            self.prayer_frame, text="", font=("Helvetica", 12), bg="#fff", fg="#444"
        )
        self.prayer_label.pack(pady=5)

        self.next_label = tk.Label(
            self.prayer_frame, text="", font=("Helvetica", 11, "italic"), bg="#fff", fg="#00796B"
        )
        self.next_label.pack(pady=(0, 5))

        # ---------- Task Input ----------
        entry_frame = tk.Frame(root, bg="#f7f7f7")
        entry_frame.pack(pady=10)

        self.task_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.task_var, font=("Helvetica", 13), width=26)
        self.entry.grid(row=0, column=0, padx=5)

        tk.Button(
            entry_frame, text="Add", command=self.add_task,
            font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", padx=10
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            entry_frame, text="Update", command=self.update_task,
            font=("Helvetica", 12), bg="#FFA000", fg="white", relief="flat", padx=10
        ).grid(row=0, column=2, padx=5)

        # ---------- Listbox ----------
        self.listbox = tk.Listbox(
            root, width=45, height=15, font=("Helvetica", 12),
            bg="#fff", activestyle="none", selectmode=tk.SINGLE
        )
        self.listbox.pack(pady=10)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(root, bg="#f7f7f7")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Mark Done", command=self.mark_done,
            font=("Helvetica", 12), bg="#0288D1", fg="white", relief="flat", padx=10
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame, text="Delete", command=self.delete_task,
            font=("Helvetica", 12), bg="#E53935", fg="white", relief="flat", padx=10
        ).grid(row=0, column=1, padx=5)

        # ---------- Load Saved Tasks ----------
        self.load_tasks()

        # ---------- Events ----------
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start live prayer updates
        self.update_prayer_time()

    # ----------------- TASK FUNCTIONS -----------------

    def add_task(self):
        task = self.task_var.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Enter a task first!")
            return
        self.listbox.insert(tk.END, task)
        self.task_var.set("")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            task = self.listbox.get(index)
            if task.startswith("✔ "):
                task = task[2:]
            else:
                task = "✔ " + task
            self.listbox.delete(index)
            self.listbox.insert(index, task)
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to mark done.")

    def update_task(self):
        try:
            index = self.listbox.curselection()[0]
            updated_text = self.task_var.get().strip()
            if updated_text:
                self.listbox.delete(index)
                self.listbox.insert(index, updated_text)
                self.task_var.set("")
            else:
                messagebox.showwarning("Warning", "Enter new text to update.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to update.")

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                for line in file:
                    self.listbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            pass

    def on_close(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            for i in range(self.listbox.size()):
                file.write(self.listbox.get(i) + "\n")
        self.root.destroy()

    # ----------------- PRAYER FUNCTIONS -----------------

    def update_prayer_time(self):
        now = datetime.now(TIMEZONE)
        current_time = now.strftime("%H:%M")

        upcoming = None
        for name, time_str in PRAYER_TIMES.items():
            prayer_time = datetime.strptime(time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            prayer_time = TIMEZONE.localize(prayer_time)
            if prayer_time > now:
                upcoming = (name, prayer_time)
                break

        if not upcoming:  # If day ended, next prayer is tomorrow's Fajr
            next_day = now + timedelta(days=1)
            prayer_time = datetime.strptime(PRAYER_TIMES["Fajr"], "%H:%M").replace(
                year=next_day.year, month=next_day.month, day=next_day.day
            )
            prayer_time = TIMEZONE.localize(prayer_time)
            upcoming = ("Fajr", prayer_time)

        next_name, next_time = upcoming
        time_diff = next_time - now
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes = remainder // 60

        self.prayer_label.config(text=f"Next Prayer: {next_name} at {next_time.strftime('%I:%M %p')}")
        self.next_label.config(text=f"Time left: {hours}h {minutes}m")

        self.root.after(60000, self.update_prayer_time)  # refresh every 60 sec


# ----------------- RUN APP -----------------
if __name__ == "__main__":
    try:
        import pytz
    except ImportError:
        messagebox.showerror("Error", "Please install pytz: pip install pytz")

    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
