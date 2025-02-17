import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x400")

        # Set initial theme
        self.dark_theme = False  

        # Widgets
        tk.Label(root, text="User:").grid(row=0, column=0)
        self.user_text = tk.Text(root, height=2, width=30, bg="lightgray")  
        self.user_text.grid(row=0, column=1)

        tk.Label(root, text="Task Description:").grid(row=1, column=0)
        self.description_text = tk.Text(root, height=4, width=30, bg="lightgray")  
        self.description_text.grid(row=1, column=1)

        self.start_btn = tk.Button(root, text="Start Task", command=self.start_task)
        self.start_btn.grid(row=2, column=0)

        self.end_btn = tk.Button(root, text="End Task", command=self.end_task)
        self.end_btn.grid(row=2, column=1)

        self.theme_btn = tk.Button(root, text="Dark Mode", command=self.change_theme)
        self.theme_btn.grid(row=3, column=1)

        # Table
        self.tree = ttk.Treeview(root, columns=("ID", "User", "Description", "Start", "End"), show="headings")
        for col in ("ID", "User", "Description", "Start", "End"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=4, column=0, columnspan=2)

        # Load existing tasks
        self.load_tasks()

        # Set theme after widgets are created
        self.set_theme()

    def set_theme(self):
        """Set dark or light theme"""
        if self.dark_theme:
            background_color = "#2E2E2E"
            text_color = "white"
            button_color = "#555"
            button_text_color = "white"
            self.theme_btn.config(text="Light Mode")
        else:
            background_color = "white"
            text_color = "black"
            button_color = "#ccc"
            button_text_color = "black"
            self.theme_btn.config(text="Dark Mode")

        self.root.configure(bg=background_color)

        # Change modes
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=background_color, fg=text_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg=button_color, fg=button_text_color)

    def change_theme(self):
        """Toggle between light and dark mode"""
        self.dark_theme = not self.dark_theme
        self.set_theme()

    def load_tasks(self):
        """Load tasks from database"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor.execute("SELECT * FROM tasks")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def start_task(self):
        """Start a task and save to database"""
        user = self.user_text.get("1.0", tk.END).strip()  # Get text from Text Box
        description = self.description_text.get("1.0", tk.END).strip()  # Get text from Text Box
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not user or not description:
            messagebox.showerror("Error", "Please, fill in all fields!")
            return

        cursor.execute("INSERT INTO tasks (user, description, start, end) VALUES (?, ?, ?, ?)",
                    (user, description, start_time, None))
        conn.commit()
        self.load_tasks()
        messagebox.showinfo("Success", "Task started successfully!")

    def end_task(self):
        """End a selected task"""
        try:
            selected_item = self.tree.selection()[0]
            task_id = self.tree.item(selected_item, "values")[0]
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("UPDATE tasks SET end = ? WHERE id = ?", (end_time, task_id))
            conn.commit()
            self.load_tasks()
            messagebox.showinfo("Success", "Task ended successfully!")
        except IndexError:
            messagebox.showerror("Error", "No task selected!")

# Database connection
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    description TEXT,
    start TEXT,
    end TEXT
)
""")
conn.commit()

# Create interface
root = tk.Tk()
app = TaskManager(root)
root.mainloop()
