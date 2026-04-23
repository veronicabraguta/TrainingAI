import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime
import os


class StudentExamApp:
    MAX_TICKETS = 20  # Only 20 unique exam tickets available
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Exam Ticket Manager")
        self.root.geometry("500x500")
        
        self.csv_file = "students_exam.csv"
        self.students = {}  # Dictionary to store name -> ticket number
        self.load_data()
        
        # Initialize ticket counter
        self.next_ticket = self.get_next_ticket_number()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        # Title
        title_label = tk.Label(self.root, text="Student Exam Ticket Manager", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(input_frame, text="Student Name:").pack(side="left", padx=5)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.pack(side="left", padx=5)
        self.name_entry.bind("<Return>", lambda e: self.add_student())
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        add_btn = tk.Button(button_frame, text="Add Student", 
                           command=self.add_student, bg="#4CAF50", fg="white", 
                           padx=15, pady=5)
        add_btn.pack(side="left", padx=5)
        
        save_btn = tk.Button(button_frame, text="Save to CSV", 
                            command=self.save_data, bg="#2196F3", fg="white",
                            padx=15, pady=5)
        save_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear All", 
                             command=self.clear_all, bg="#f44336", fg="white",
                             padx=15, pady=5)
        clear_btn.pack(side="left", padx=5)
        
        # List frame
        list_label = tk.Label(self.root, text="Students Registered:", 
                             font=("Arial", 10, "bold"))
        list_label.pack(pady=(15, 5), padx=10, anchor="w")
        
        # Treeview for displaying students
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Ticket"), 
                                height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Name", anchor=tk.W, width=250)
        self.tree.column("Ticket", anchor=tk.CENTER, width=150)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Name", text="Student Name", anchor=tk.W)
        self.tree.heading("Ticket", text="Ticket Number", anchor=tk.CENTER)
        
        self.tree.pack(fill="both", expand=True)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="", fg="gray")
        self.status_label.pack(pady=5)
        
        self.refresh_list()
        
    def add_student(self):
        """Add a new student"""
        name = self.name_entry.get().strip()
        
        # Validation
        if not name:
            messagebox.showwarning("Empty Input", "Please enter a student name.")
            return
        
        if name in self.students:
            messagebox.showwarning("Duplicate", 
                                  f"'{name}' is already registered with ticket #{self.students[name]:04d}.")
            return
        
        # Check if all tickets are used
        if len(self.students) >= self.MAX_TICKETS:
            messagebox.showerror("No Tickets Available", 
                               f"All {self.MAX_TICKETS} exam tickets have been assigned.\n"
                               "Cannot add more students.")
            return
        
        # Add student
        ticket = self.next_ticket
        self.students[name] = ticket
        self.next_ticket += 1
        
        self.name_entry.delete(0, tk.END)
        self.refresh_list()
        messagebox.showinfo("Success", 
                          f"'{name}' added with ticket #{ticket:04d}")
        
    def refresh_list(self):
        """Refresh the student list display"""
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add students sorted by name
        for name in sorted(self.students.keys()):
            ticket = self.students[name]
            self.tree.insert("", tk.END, values=(name, f"#{ticket:04d}"))
        
        # Update status
        remaining = self.MAX_TICKETS - len(self.students)
        self.status_label.config(text=f"Total students: {len(self.students)} | Tickets remaining: {remaining}")
        
    def save_data(self):
        """Save students to CSV file"""
        if not self.students:
            messagebox.showwarning("No Data", "No students to save.")
            return
        
        try:
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                # Header
                writer.writerow(["Student Name", "Exam Ticket"])
                # Data sorted by name
                for name in sorted(self.students.keys()):
                    ticket = self.students[name]
                    writer.writerow([name, f"#{ticket:04d}"])
            
            messagebox.showinfo("Success", 
                              f"Data saved to '{self.csv_file}'\n({len(self.students)} students)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_data(self):
        """Load students from CSV file if it exists"""
        if not os.path.exists(self.csv_file):
            return
        
        try:
            with open(self.csv_file, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        name = row[0].strip()
                        ticket_str = row[1].strip().lstrip("#")
                        try:
                            ticket = int(ticket_str)
                            self.students[name] = ticket
                        except ValueError:
                            pass
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def get_next_ticket_number(self):
        """Get the next available ticket number (1001-1020)"""
        if not self.students:
            return 1001
        max_used = max(self.students.values())
        if max_used >= 1000 + self.MAX_TICKETS:
            return None  # No more tickets available
        return max_used + 1
    
    def clear_all(self):
        """Clear all students"""
        if not self.students:
            messagebox.showinfo("Info", "No students to clear.")
            return
        
        if messagebox.askyesno("Confirm", 
                              f"Clear all {len(self.students)} students? This cannot be undone."):
            self.students.clear()
            self.next_ticket = 1001
            self.refresh_list()
            messagebox.showinfo("Cleared", "All students have been cleared.\nTickets reset to available.")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentExamApp(root)
    root.mainloop()
