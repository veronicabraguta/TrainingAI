import pytest
import tkinter as tk
import csv
import os
from student_exam_app import StudentExamApp


@pytest.fixture
def root():
    """Create a Tkinter root window for testing"""
    root = tk.Tk()
    yield root
    root.destroy()


@pytest.fixture
def app(root):
    """Create an app instance for testing"""
    app = StudentExamApp(root)
    yield app
    # Cleanup
    if os.path.exists(app.csv_file):
        os.remove(app.csv_file)


def test_app_initialization(app):
    """Test app initializes with correct values"""
    assert app.MAX_TICKETS == 20
    assert app.next_ticket == 1001
    assert len(app.students) == 0


def test_add_single_student(app):
    """Test adding a single student"""
    app.name_entry.insert(0, "John Doe")
    app.add_student()
    
    assert "John Doe" in app.students
    assert app.students["John Doe"] == 1001
    assert app.next_ticket == 1002


def test_add_multiple_students(app):
    """Test adding multiple students with sequential ticket numbers"""
    names = ["Alice", "Bob", "Charlie"]
    
    for i, name in enumerate(names):
        app.name_entry.insert(0, name)
        app.add_student()
        assert app.students[name] == 1001 + i
    
    assert len(app.students) == 3


def test_reject_empty_input(app):
    """Test that empty input is rejected"""
    app.name_entry.insert(0, "")
    app.add_student()
    
    assert len(app.students) == 0


def test_reject_whitespace_only_input(app):
    """Test that whitespace-only input is rejected"""
    app.name_entry.insert(0, "   ")
    app.add_student()
    
    assert len(app.students) == 0


def test_reject_duplicate_student(app):
    """Test that duplicate student names are rejected"""
    app.name_entry.insert(0, "John")
    app.add_student()
    
    app.name_entry.insert(0, "John")
    app.add_student()
    
    assert len(app.students) == 1
    assert app.students["John"] == 1001


def test_max_tickets_limit(app):
    """Test that only 20 tickets can be assigned"""
    for i in range(20):
        app.name_entry.insert(0, f"Student{i}")
        app.add_student()
    
    assert len(app.students) == 20
    
    # Try to add 21st student
    app.name_entry.insert(0, "Student20")
    app.add_student()
    
    assert len(app.students) == 20


def test_save_to_csv(app, tmp_path):
    """Test saving students to CSV file"""
    app.students = {"Alice": 1001, "Bob": 1002}
    app.csv_file = str(tmp_path / "test_students.csv")
    
    app.save_data()
    
    assert os.path.exists(app.csv_file)
    
    with open(app.csv_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert rows[0] == ["Student Name", "Exam Ticket"]
    assert rows[1] == ["Alice", "#1001"]
    assert rows[2] == ["Bob", "#1002"]


def test_load_from_csv(tmp_path):
    """Test loading students from CSV file"""
    csv_file = str(tmp_path / "test_load.csv")
    
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Student Name", "Exam Ticket"])
        writer.writerow(["Alice", "#1001"])
        writer.writerow(["Bob", "#1002"])
    
    root = tk.Tk()
    app = StudentExamApp(root)
    app.csv_file = csv_file
    app.load_data()
    
    assert "Alice" in app.students
    assert "Bob" in app.students
    assert app.students["Alice"] == 1001
    assert app.students["Bob"] == 1002
    
    root.destroy()


def test_clear_all(app):
    """Test clearing all students"""
    app.students = {"Alice": 1001, "Bob": 1002}
    app.clear_all()
    
    assert len(app.students) == 0
    assert app.next_ticket == 1001


def test_get_next_ticket_number(app):
    """Test ticket number generation with existing data"""
    # Add students through normal flow to populate next_ticket
    app.name_entry.insert(0, "Alice")
    app.add_student()
    app.name_entry.insert(0, "Bob")
    app.add_student()
    app.name_entry.insert(0, "Charlie")
    app.add_student()
    
    # next_ticket should be incremented to 1004
    assert app.next_ticket == 1004
    next_ticket = app.get_next_ticket_number()
    assert next_ticket == 1004


def test_refresh_list(app):
    """Test that student list updates correctly"""
    app.students = {"Charlie": 1003, "Alice": 1001, "Bob": 1002}
    app.refresh_list()
    
    tree_items = app.tree.get_children()
    assert len(tree_items) == 3
    
    # Check sorting is alphabetical
    assert app.tree.item(tree_items[0])["values"][0] == "Alice"
    assert app.tree.item(tree_items[1])["values"][0] == "Bob"
    assert app.tree.item(tree_items[2])["values"][0] == "Charlie"


def test_ticket_format(app):
    """Test that tickets are formatted correctly"""
    app.name_entry.insert(0, "John")
    app.add_student()
    
    assert app.students["John"] == 1001