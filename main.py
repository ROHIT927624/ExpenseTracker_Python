import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import Tk, Label, Entry, Button
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import pandas as pd
from PIL import Image, ImageTk

class ExpenseTracker:
    def __init__(self):
        self.db = self.connect_to_db()
        self.cursor = self.db.cursor()
        self.current_user_id = 1
        self.root = None
        self.login_window()

    def connect_to_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="1341",
                database="expense_tracker"
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
            exit()

    def login_window(self):
        self.window = Tk()
        self.window.title("Login - Expense Tracker")
        self.window.geometry("450x500")
        self.window.config(bg="#1F2A44")
        self.window.resizable(False, False)

        main_frame = tk.Frame(self.window, bg="#1F2A44")
        main_frame.pack(expand=True)

        image_path = "logo.png"
        try:
            img = Image.open(image_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            image_label = Label(main_frame, image=photo, bg="#1F2A44")
            image_label.image = photo
            image_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            Label(main_frame, text="Image not found", font=("Helvetica", 12), 
                  bg="#1F2A44", fg="#FF6B6B").pack(pady=20)

        Label(main_frame, text="Welcome to Xpensify", font=("Helvetica", 20, "bold"), 
              bg="#1F2A44", fg="#FFFFFF").pack(pady=10)

        login_frame = tk.Frame(main_frame, bg="#2A3F5F", padx=20, pady=20, relief=tk.RAISED, bd=2)
        login_frame.pack(pady=10)

        Label(login_frame, text="Username:", bg="#2A3F5F", fg="#A3BFFA", 
              font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky=tk.W)
        self.username_entry = Entry(login_frame, bg="#FFFFFF", fg="#1F2A44", 
                                    font=("Helvetica", 12), relief="flat", bd=2, width=25)
        self.username_entry.grid(row=0, column=1, pady=10)

        Label(login_frame, text="Password:", bg="#2A3F5F", fg="#A3BFFA", 
              font=("Helvetica", 12)).grid(row=1, column=0, pady=10, sticky=tk.W)
        self.password_entry = Entry(login_frame, show="*", bg="#FFFFFF", fg="#1F2A44",
                                    font=("Helvetica", 12), relief="flat", bd=2, width=25)
        self.password_entry.grid(row=1, column=1, pady=10)

        Button(login_frame, text="Login", command=self.login, bg="#00C4B4", fg="white",
               font=("Helvetica", 12, "bold"), relief="flat", activebackground="#00A896",
               width=10).grid(row=2, column=0, columnspan=2, pady=10)
        Button(login_frame, text="Register", command=self.register_window, bg="#FF6B6B", 
               fg="white", font=("Helvetica", 12, "bold"), relief="flat", 
               activebackground="#FF8787", width=10).grid(row=3, column=0, columnspan=2, pady=10)

        self.window.mainloop()

    def register_window(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title("Register - Expense Tracker")
        self.window.geometry("450x350")
        self.window.config(bg="#1F2A44")

        Label(self.window, text="Register for Xpensify", font=("Helvetica", 20, "bold"), 
              bg="#1F2A44", fg="#FFFFFF").pack(pady=20)
        
        reg_frame = tk.Frame(self.window, bg="#2A3F5F", padx=20, pady=20, relief=tk.RAISED, bd=2)
        reg_frame.pack(pady=10, padx=20, fill=tk.X)
        
        Label(reg_frame, text="Username:", bg="#2A3F5F", fg="#A3BFFA", 
              font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky=tk.W)
        self.reg_username_entry = Entry(reg_frame, bg="#FFFFFF", fg="#1F2A44",
                                        font=("Helvetica", 12), relief="flat", bd=2, width=25)
        self.reg_username_entry.grid(row=0, column=1, pady=10)

        Label(reg_frame, text="Password:", bg="#2A3F5F", fg="#A3BFFA", 
              font=("Helvetica", 12)).grid(row=1, column=0, pady=10, sticky=tk.W)
        self.reg_password_entry = Entry(reg_frame, show="*", bg="#FFFFFF", fg="#1F2A44",
                                        font=("Helvetica", 12), relief="flat", bd=2, width=25)
        self.reg_password_entry.grid(row=1, column=1, pady=10)

        Button(reg_frame, text="Register", command=self.register, bg="#FF6B6B", fg="white",
               font=("Helvetica", 12, "bold"), relief="flat", activebackground="#FF8787",
               width=10).grid(row=2, column=0, columnspan=2, pady=10)
        Button(reg_frame, text="Back to Login", command=self.login_window, bg="#00C4B4", 
               fg="white", font=("Helvetica", 12, "bold"), relief="flat", 
               activebackground="#00A896", width=10).grid(row=3, column=0, columnspan=2, pady=10)

        self.window.mainloop()

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if self.cursor.fetchone():
                messagebox.showwarning("Error", "Username already exists!")
                return
                
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.cursor.execute(query, (username, password))
            self.db.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.login_window()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to register: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        query = "SELECT id FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            self.current_user_id = result[0]
            messagebox.showinfo("Success", "Login Successful!")
            self.window.destroy()
            self.main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def main_window(self):
        if self.root:
            self.root.destroy()
            
        self.root = tk.Tk()
        self.root.title("Xpensify")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1F2A44")
        self.root.resizable(True, True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#1F2A44", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2A3F5F", foreground="#FFFFFF",
                       padding=[15, 8], font=('Helvetica', 14, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#00C4B4")], 
                  foreground=[("selected", "#FFFFFF")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.expense_frame = tk.Frame(self.notebook, bg="#2A3F5F")
        self.income_frame = tk.Frame(self.notebook, bg="#2A3F5F")
        self.reports_frame = tk.Frame(self.notebook, bg="#2A3F5F")

        self.notebook.add(self.expense_frame, text="Expenses")
        self.notebook.add(self.income_frame, text="Income")
        self.notebook.add(self.reports_frame, text="Reports")

        self.create_expense_section()
        self.create_income_section()
        self.create_reports_section()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def create_expense_section(self):
        input_frame = tk.Frame(self.expense_frame, bg="#2A3F5F", relief=tk.RAISED, borderwidth=2)
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        tk.Label(input_frame, text="Add New Expense", font=("Helvetica", 16, "bold"),
                bg="#2A3F5F", fg="#FFFFFF").grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Expense Name:", "Amount:", "Date:", "Category:"]
        self.expense_entries = []
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, bg="#2A3F5F", fg="#A3BFFA",
                    font=("Helvetica", 12)).grid(row=i+1, column=0, padx=10, pady=5, sticky=tk.W)
            
            if text == "Date:":
                entry = DateEntry(input_frame, date_pattern="yyyy-mm-dd", 
                                background="#1F2A44", foreground="#FFFFFF")
            elif text == "Category:":
                entry = ttk.Combobox(input_frame, values=["Food", "Transport", "Housing", 
                                                        "Entertainment", "Other"],
                                    style="Custom.TCombobox")
                ttk.Style().configure("Custom.TCombobox", fieldbackground="#2A3F5F", 
                                    background="#2A3F5F", foreground="#FFFFFF")
            else:
                entry = tk.Entry(input_frame, font=("Helvetica", 12), bg="#FFFFFF")
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky=tk.EW)
            self.expense_entries.append(entry)

        tk.Button(input_frame, text="Add Expense", command=self.add_expense,
                 bg="#FF6B6B", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).grid(row=5, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self.expense_frame, bg="#2A3F5F")
        button_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Button(button_frame, text="Import Expenses", command=lambda: self.import_file("expenses"),
                 bg="#00C4B4", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Export Expenses", command=lambda: self.export_excel("expenses"),
                 bg="#F4A261", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Edit Expense", command=self.edit_expense,
                 bg="#FFA500", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Expense", command=self.delete_expense,
                 bg="#FF4444", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        tree_frame = tk.Frame(self.expense_frame, bg="#2A3F5F")
        tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        columns = ("Sr.", "Date", "Category", "Name", "Amount")
        self.expense_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.expense_tree.heading(col, text=col, anchor=tk.CENTER)
            self.expense_tree.column(col, width=150 if col == "Sr." else 200, anchor=tk.CENTER)
        self.expense_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)

        self.load_expenses()

    def create_income_section(self):
        input_frame = tk.Frame(self.income_frame, bg="#2A3F5F", relief=tk.RAISED, borderwidth=2)
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        tk.Label(input_frame, text="Add New Income", font=("Helvetica", 16, "bold"),
                bg="#2A3F5F", fg="#FFFFFF").grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Income Source:", "Amount:", "Date:", "Category:"]
        self.income_entries = []
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, bg="#2A3F5F", fg="#A3BFFA",
                    font=("Helvetica", 12)).grid(row=i+1, column=0, padx=10, pady=5, sticky=tk.W)
            
            if text == "Date:":
                entry = DateEntry(input_frame, date_pattern="yyyy-mm-dd",
                                background="#1F2A44", foreground="#FFFFFF")
            elif text == "Category:":
                entry = ttk.Combobox(input_frame, values=["Salary", "Freelance", "Investment", "Other"],
                                    style="Custom.TCombobox")
                ttk.Style().configure("Custom.TCombobox", fieldbackground="#2A3F5F", 
                                    background="#2A3F5F", foreground="#FFFFFF")
            else:
                entry = tk.Entry(input_frame, font=("Helvetica", 12), bg="#FFFFFF")
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky=tk.EW)
            self.income_entries.append(entry)

        tk.Button(input_frame, text="Add Income", command=self.add_income,
                 bg="#00C4B4", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).grid(row=5, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self.income_frame, bg="#2A3F5F")
        button_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Button(button_frame, text="Import Income", command=lambda: self.import_file("income"),
                 bg="#00C4B4", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Export Income", command=lambda: self.export_excel("income"),
                 bg="#F4A261", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Edit Income", command=self.edit_income,
                 bg="#FFA500", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Income", command=self.delete_income,
                 bg="#FF4444", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        tree_frame = tk.Frame(self.income_frame, bg="#2A3F5F")
        tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        columns = ("Sr.", "Date", "Category", "Source", "Amount")
        self.income_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.income_tree.heading(col, text=col, anchor=tk.CENTER)
            self.income_tree.column(col, width=150 if col == "Sr." else 200, anchor=tk.CENTER)
        self.income_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.income_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.income_tree.configure(yscrollcommand=scrollbar.set)

        self.load_income()

    def create_reports_section(self):
        controls = tk.Frame(self.reports_frame, bg="#2A3F5F", relief=tk.RAISED, borderwidth=2)
        controls.pack(pady=20, fill=tk.X, padx=20)

        tk.Label(controls, text="Start Date:", bg="#2A3F5F", fg="#A3BFFA",
                 font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.start_date_entry = DateEntry(controls, date_pattern="yyyy-mm-dd",
                                         background="#1F2A44", foreground="#FFFFFF")
        # Set start date to one month ago from current date (April 2, 2025 - 1 month = March 2, 2025)
        start_date = datetime(2025, 4, 2) - timedelta(days=30)
        self.start_date_entry.set_date(start_date)
        self.start_date_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(controls, text="End Date:", bg="#2A3F5F", fg="#A3BFFA",
                 font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.end_date_entry = DateEntry(controls, date_pattern="yyyy-mm-dd",
                                       background="#1F2A44", foreground="#FFFFFF")
        # Set end date to current date (April 2, 2025)
        self.end_date_entry.set_date(datetime(2025, 4, 2))
        self.end_date_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Generate Report", command=self.generate_report,
                 bg="#00C4B4", fg="white", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        graph_frame = tk.Frame(self.reports_frame, bg="#2A3F5F")
        graph_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        tk.Button(graph_frame, text="Bar Graph", command=lambda: self.generate_report("Bar"),
                 bg="#F4A261", fg="white", font=("Helvetica", 10, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.TOP, pady=5)
        tk.Button(graph_frame, text="Pie Graph", command=lambda: self.generate_report("Pie"),
                 bg="#FF6B6B", fg="white", font=("Helvetica", 10, "bold"),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.TOP, pady=5)

        self.chart_frame = tk.Frame(self.reports_frame, bg="#2A3F5F")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def add_expense(self):
        entries = [e.get() for e in self.expense_entries]
        if not all(entries[:3]):
            messagebox.showwarning("Error", "Please fill all required fields!")
            return

        try:
            amount = float(entries[1])
            if amount <= 0:
                raise ValueError("Amount must be positive")
                
            query = """INSERT INTO expenses (user_id, expense_name, amount, date, category)
                      VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(query, (self.current_user_id, *entries))
            self.db.commit()
            self.load_expenses()
            messagebox.showinfo("Success", "Expense added successfully!")
            for entry in self.expense_entries:
                if not isinstance(entry, (DateEntry, ttk.Combobox)):
                    entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid amount: {ve}")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to add expense: {e}")

    def add_income(self):
        entries = [e.get() for e in self.income_entries]
        if not all(entries[:3]):
            messagebox.showwarning("Error", "Please fill all required fields!")
            return

        try:
            amount = float(entries[1])
            if amount <= 0:
                raise ValueError("Amount must be positive")
                
            query = """INSERT INTO income (user_id, source, amount, date, category)
                      VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(query, (self.current_user_id, *entries))
            self.db.commit()
            self.load_income()
            messagebox.showinfo("Success", "Income added successfully!")
            for entry in self.income_entries:
                if not isinstance(entry, (DateEntry, ttk.Combobox)):
                    entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid amount: {ve}")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to add income: {e}")

    def load_expenses(self):
        self.expense_tree.delete(*self.expense_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM expenses WHERE user_id=%s", (self.current_user_id,))
            rows = self.cursor.fetchall()
            for idx, row in enumerate(rows, start=1):
                self.expense_tree.insert("", tk.END, values=(idx, row[4], row[5], row[2], row[3]), tags=(row[0],))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load expenses: {e}")

    def load_income(self):
        self.income_tree.delete(*self.income_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM income WHERE user_id=%s", (self.current_user_id,))
            rows = self.cursor.fetchall()
            for idx, row in enumerate(rows, start=1):
                self.income_tree.insert("", tk.END, values=(idx, row[4], row[5], row[2], row[3]), tags=(row[0],))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load income: {e}")

    def edit_expense(self):
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to edit!")
            return

        item_id = self.expense_tree.item(selected_item, "tags")[0]
        values = self.expense_tree.item(selected_item, "values")
        current_name, current_amount, current_date, current_category = values[3], values[4], values[1], values[2]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")
        edit_window.geometry("400x300")
        edit_window.config(bg="#2A3F5F")

        labels = ["Expense Name:", "Amount:", "Date:", "Category:"]
        entries = []
        for i, text in enumerate(labels):
            tk.Label(edit_window, text=text, bg="#2A3F5F", fg="#A3BFFA",
                     font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            
            if text == "Date:":
                entry = DateEntry(edit_window, date_pattern="yyyy-mm-dd", 
                                 background="#1F2A44", foreground="#FFFFFF")
                entry.set_date(current_date)
            elif text == "Category:":
                entry = ttk.Combobox(edit_window, values=["Food", "Transport", "Housing", 
                                                         "Entertainment", "Other"],
                                     style="Custom.TCombobox")
                entry.set(current_category)
                ttk.Style().configure("Custom.TCombobox", fieldbackground="#2A3F5F", 
                                     background="#2A3F5F", foreground="#FFFFFF")
            else:
                entry = tk.Entry(edit_window, font=("Helvetica", 12), bg="#FFFFFF")
                entry.insert(0, current_name if text == "Expense Name:" else current_amount)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
            entries.append(entry)

        def save_changes():
            new_values = [e.get() for e in entries]
            if not all(new_values[:3]):
                messagebox.showwarning("Error", "Please fill all required fields!")
                return

            try:
                amount = float(new_values[1])
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                query = """UPDATE expenses 
                          SET expense_name=%s, amount=%s, date=%s, category=%s 
                          WHERE id=%s AND user_id=%s"""
                self.cursor.execute(query, (*new_values, item_id, self.current_user_id))
                self.db.commit()
                self.load_expenses()
                messagebox.showinfo("Success", "Expense updated successfully!")
                edit_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid amount: {ve}")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Failed to update expense: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes,
                 bg="#00C4B4", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_income(self):
        selected_item = self.income_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an income entry to edit!")
            return

        item_id = self.income_tree.item(selected_item, "tags")[0]
        values = self.income_tree.item(selected_item, "values")
        current_source, current_amount, current_date, current_category = values[3], values[4], values[1], values[2]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Income")
        edit_window.geometry("400x300")
        edit_window.config(bg="#2A3F5F")

        labels = ["Income Source:", "Amount:", "Date:", "Category:"]
        entries = []
        for i, text in enumerate(labels):
            tk.Label(edit_window, text=text, bg="#2A3F5F", fg="#A3BFFA",
                     font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            
            if text == "Date:":
                entry = DateEntry(edit_window, date_pattern="yyyy-mm-dd", 
                                 background="#1F2A44", foreground="#FFFFFF")
                entry.set_date(current_date)
            elif text == "Category:":
                entry = ttk.Combobox(edit_window, values=["Salary", "Freelance", "Investment", "Other"],
                                     style="Custom.TCombobox")
                entry.set(current_category)
                ttk.Style().configure("Custom.TCombobox", fieldbackground="#2A3F5F", 
                                     background="#2A3F5F", foreground="#FFFFFF")
            else:
                entry = tk.Entry(edit_window, font=("Helvetica", 12), bg="#FFFFFF")
                entry.insert(0, current_source if text == "Income Source:" else current_amount)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
            entries.append(entry)

        def save_changes():
            new_values = [e.get() for e in entries]
            if not all(new_values[:3]):
                messagebox.showwarning("Error", "Please fill all required fields!")
                return

            try:
                amount = float(new_values[1])
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                query = """UPDATE income 
                          SET source=%s, amount=%s, date=%s, category=%s 
                          WHERE id=%s AND user_id=%s"""
                self.cursor.execute(query, (*new_values, item_id, self.current_user_id))
                self.db.commit()
                self.load_income()
                messagebox.showinfo("Success", "Income updated successfully!")
                edit_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid amount: {ve}")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Failed to update income: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes,
                 bg="#00C4B4", fg="white", font=("Helvetica", 12, "bold"),
                 relief=tk.RAISED, borderwidth=2).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_expense(self):
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected expense?"):
            try:
                item_id = self.expense_tree.item(selected_item, "tags")[0]
                query = "DELETE FROM expenses WHERE id = %s AND user_id = %s"
                self.cursor.execute(query, (item_id, self.current_user_id))
                self.db.commit()
                self.load_expenses()
                messagebox.showinfo("Success", "Expense deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete expense: {e}")

    def delete_income(self):
        selected_item = self.income_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an income entry to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected income entry?"):
            try:
                item_id = self.income_tree.item(selected_item, "tags")[0]
                query = "DELETE FROM income WHERE id = %s AND user_id = %s"
                self.cursor.execute(query, (item_id, self.current_user_id))
                self.db.commit()
                self.load_income()
                messagebox.showinfo("Success", "Income entry deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete income: {e}")

    def generate_report(self, graph_type=None):
        try:
            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()

            if start_date > end_date:
                messagebox.showerror("Error", "Start date cannot be after end date!")
                return

            # Fetch expenses within the date range
            expense_query = """
                SELECT date, SUM(amount) 
                FROM expenses 
                WHERE user_id=%s AND date BETWEEN %s AND %s 
                GROUP BY date
                ORDER BY date
            """
            self.cursor.execute(expense_query, (self.current_user_id, start_date, end_date))
            expense_data = self.cursor.fetchall()

            # Fetch income within the date range
            income_query = """
                SELECT date, SUM(amount) 
                FROM income 
                WHERE user_id=%s AND date BETWEEN %s AND %s 
                GROUP BY date
                ORDER BY date
            """
            self.cursor.execute(income_query, (self.current_user_id, start_date, end_date))
            income_data = self.cursor.fetchall()

            if not expense_data and not income_data:
                messagebox.showinfo("Info", "No data available for the selected date range")
                return

            # Process data for plotting
            expense_dates = [row[0] for row in expense_data]
            expense_amounts = [row[1] for row in expense_data]
            income_dates = [row[0] for row in income_data]
            income_amounts = [row[1] for row in income_data]

            # Create a combined list of unique dates
            all_dates = sorted(set(expense_dates + income_dates))
            formatted_dates = [date.strftime("%d") for date in all_dates]

            # Align amounts with dates (fill with 0 if no data for a date)
            expense_series = {date: 0 for date in all_dates}
            for date, amount in zip(expense_dates, expense_amounts):
                expense_series[date] = amount
            expense_amounts_aligned = [expense_series[date] for date in all_dates]

            income_series = {date: 0 for date in all_dates}
            for date, amount in zip(income_dates, income_amounts):
                income_series[date] = amount
            income_amounts_aligned = [income_series[date] for date in all_dates]

            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            if graph_type == "Bar":
                # Bar graph with two columns (red for expenses, green for income)
                bar_width = 0.35
                x = range(len(all_dates))
                ax.bar([i - bar_width/2 for i in x], expense_amounts_aligned, bar_width, label="Expenses", color="red")
                ax.bar([i + bar_width/2 for i in x], income_amounts_aligned, bar_width, label="Income", color="green")
                ax.set_xlabel("Date (Day)")
                ax.set_ylabel("Amount ($)")
                ax.set_title(f"Expenses (Red) and Income (Green): {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                ax.set_xticks(x)
                ax.set_xticklabels(formatted_dates, rotation=45)
                ax.legend()
            else:  # Pie chart (showing only expenses for now, can be extended)
                total_expense = sum(expense_amounts) if expense_amounts else 0
                total_income = sum(income_amounts) if income_amounts else 0
                sizes = [total_expense, total_income]
                labels = ["Expenses", "Income"]
                colors = ["red", "green"]
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                ax.set_title(f"Expenses and Income Distribution ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate report: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def import_file(self, table):
        file_path = filedialog.askopenfilename(
            title=f"Select {table.capitalize()} File to Import",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format! Please select a CSV or Excel file.")
                return

            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

            required_columns = ['amount', 'date']
            expense_columns = ['name', 'amount', 'date', 'category']
            income_columns = ['source', 'amount', 'date', 'category']

            column_mapping = {
                'expense_name': 'name',
                'income_source': 'source',
                'amount': 'amount',
                'date': 'date',
                'category': 'category',
                'expense': 'name',
                'source': 'source',
                'amt': 'amount',
                'dt': 'date',
                'cat': 'category'
            }

            normalized_columns = {}
            for file_col in df.columns:
                for key, value in column_mapping.items():
                    if file_col == key or file_col == value:
                        normalized_columns[value] = file_col
                        break

            if table == "expenses":
                expected_columns = expense_columns
                query = """INSERT INTO expenses (user_id, expense_name, amount, date, category)
                          VALUES (%s, %s, %s, %s, %s)"""
            else:
                expected_columns = income_columns
                query = """INSERT INTO income (user_id, source, amount, date, category)
                          VALUES (%s, %s, %s, %s, %s)"""

            missing_cols = [col for col in expected_columns if col not in normalized_columns]
            if missing_cols:
                messagebox.showerror("Import Error",
                                    f"Missing required columns: {', '.join(missing_cols)}\n"
                                    f"Expected columns: {', '.join(expected_columns)}\n"
                                    f"Found columns: {', '.join(df.columns)}")
                return

            for index, row in df.iterrows():
                if not all(pd.notna(row[normalized_columns[col]]) for col in required_columns):
                    continue
                amount = float(row[normalized_columns['amount']])
                if amount <= 0:
                    continue
                date_value = row[normalized_columns['date']]
                if isinstance(date_value, pd.Timestamp):
                    date_value = date_value.strftime('%Y-%m-%d')
                elif isinstance(date_value, datetime):
                    date_value = date_value.strftime('%Y-%m-%d')
                values = (
                    self.current_user_id,
                    row[normalized_columns[expected_columns[0]]],
                    amount,
                    date_value,
                    row[normalized_columns['category']]
                )
                self.cursor.execute(query, values)

            self.db.commit()
            self.load_expenses() if table == "expenses" else self.load_income()
            messagebox.showinfo("Success", f"Data imported successfully into {table}!")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import file: {e}")

    def export_excel(self, table):
        try:
            query = f"SELECT * FROM {table} WHERE user_id=%s"
            self.cursor.execute(query, (self.current_user_id,))
            data = self.cursor.fetchall()

            if not data:
                messagebox.showinfo("Info", f"No {table} data to export!")
                return

            if table == "expenses":
                columns = ["Sr.", "Date", "Category", "Name", "Amount"]
                formatted_data = [(idx + 1, row[4], row[5], row[2], row[3]) for idx, row in enumerate(data)]
            else:
                columns = ["Sr.", "Date", "Category", "Source", "Amount"]
                formatted_data = [(idx + 1, row[4], row[5], row[2], row[3]) for idx, row in enumerate(data)]

            df = pd.DataFrame(formatted_data, columns=columns)
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                    filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"{table.capitalize()} exported successfully as Excel!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export {table} to Excel: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db.close()
            self.root.destroy()

if __name__ == "__main__":
    db = mysql.connector.connect(host="localhost", user="root", password="1341")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
    cursor.execute("USE expense_tracker")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            expense_name VARCHAR(255),
            amount DECIMAL(10,2),
            date DATE,
            category VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            source VARCHAR(255),
            amount DECIMAL(10,2),
            date DATE,
            category VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db.commit()
    db.close()
    
    ExpenseTracker()