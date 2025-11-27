import csv
from datetime import datetime
from pathlib import Path

# File paths
BASE_DIR = Path.cwd()
STUDENTS_FILE = BASE_DIR / "students.csv"
GRADES_FILE = BASE_DIR / "grades.csv"
ATTENDANCE_FILE = BASE_DIR / "attendance.csv"

# Ensure files exist
for file in [STUDENTS_FILE, GRADES_FILE, ATTENDANCE_FILE]:
    if not file.exists():
        file.touch()

# Safe input to handle Ctrl+C / EOF
def safe_input(prompt):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError) as e:
        print(f"\nInput cancelled ({type(e).__name__}). Returning to menu...")
        return None

# Add a student
def add_student():
    student_id = safe_input("Enter student ID: ")
    if student_id is None:
        return
    name = safe_input("Enter student name: ")
    if name is None:
        return
    with open(STUDENTS_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([student_id, name])
    print(f"Student {name} added successfully!\n")

# Record a grade
def record_grade():
    student_id = safe_input("Enter student ID: ")
    if student_id is None:
        return
    subject = safe_input("Enter subject: ")
    if subject is None:
        return
    grade = safe_input("Enter grade: ")
    if grade is None:
        return
    with open(GRADES_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([student_id, subject, grade])
    print(f"Grade recorded successfully!\n")

# Record attendance
def record_attendance():
    student_id = safe_input("Enter student ID: ")
    if student_id is None:
        return
    status = safe_input("Enter attendance (Present/Absent): ")
    if status is None:
        return
    date = datetime.now().strftime("%Y-%m-%d")
    with open(ATTENDANCE_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([student_id, date, status])
    print(f"Attendance recorded successfully!\n")

# View students
def view_students():
    print("\n--- Students ---")
    with open(STUDENTS_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
            print(f"ID: {row[0]}, Name: {row[1]}")
    print("")

# View grades
def view_grades():
    print("\n--- Grades ---")
    with open(GRADES_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            print(f"ID: {row[0]}, Subject: {row[1]}, Grade: {row[2]}")
    print("")

# View attendance
def view_attendance():
    print("\n--- Attendance ---")
    with open(ATTENDANCE_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            print(f"ID: {row[0]}, Date: {row[1]}, Status: {row[2]}")
    print("")

# Average grades per student and overall
def average_grades():
    grades_by_student = {}
    total_sum = 0.0
    total_count = 0
    with open(GRADES_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            sid = row[0].strip()
            try:
                val = float(row[2])
            except ValueError:
                # skip non-numeric grades
                continue
            grades_by_student.setdefault(sid, []).append(val)
            total_sum += val
            total_count += 1

    print("\n--- Average Grades ---")
    if not grades_by_student:
        print("No numeric grades recorded yet.\n")
        return

    # load student names for display
    names = {}
    with open(STUDENTS_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and len(row) >= 2:
                names[row[0].strip()] = row[1].strip()

    for sid, vals in grades_by_student.items():
        avg = sum(vals) / len(vals)
        display_name = names.get(sid, "<unknown>")
        print(f"ID: {sid}, Name: {display_name}, Average: {avg:.2f} ({len(vals)} grades)")

    overall = total_sum / total_count if total_count else 0.0
    print(f"\nOverall average: {overall:.2f}\n")

# Attendance percentage per student and overall
def attendance_percentage():
    counts = {}  # sid -> (present_count, total_count)
    with open(ATTENDANCE_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            sid = row[0].strip()
            status = row[2].strip().lower()
            present = status.startswith('p')  # accepts "Present", "present", "p", etc.
            present_count, total_count = counts.get(sid, (0, 0))
            counts[sid] = (present_count + (1 if present else 0), total_count + 1)

    print("\n--- Attendance Percentage ---")
    if not counts:
        print("No attendance records yet.\n")
        return

    # load student names for display
    names = {}
    with open(STUDENTS_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and len(row) >= 2:
                names[row[0].strip()] = row[1].strip()

    overall_present = 0
    overall_total = 0
    for sid, (present_count, total_count) in counts.items():
        pct = (present_count / total_count) * 100 if total_count else 0.0
        display_name = names.get(sid, "<unknown>")
        print(f"ID: {sid}, Name: {display_name}, Attendance: {present_count}/{total_count} ({pct:.2f}%)")
        overall_present += present_count
        overall_total += total_count

    overall_pct = (overall_present / overall_total) * 100 if overall_total else 0.0
    print(f"\nOverall attendance percentage: {overall_pct:.2f}%\n")

# Reset all data (students, grades, attendance)
def reset_all_data():
    print("\n--- Reset All Data ---")
    confirm = safe_input("Type 'RESET' to permanently delete all data (Enter to cancel): ")
    if confirm is None or confirm != "RESET":
        print("Reset cancelled.\n")
        return
    for file in [STUDENTS_FILE, GRADES_FILE, ATTENDANCE_FILE]:
        # open in write mode to truncate the file
        with open(file, mode='w', newline='') as f:
            pass
    print("All data reset successfully.\n")

# Main menu
def main():
    while True:
        print("1. Add Student")
        print("2. Record Grade")
        print("3. Record Attendance")
        print("4. View Students")
        print("5. View Grades")
        print("6. View Attendance")
        print("7. Average Grades")
        print("8. Average Attendance Percentage")
        print("9. Reset All Data")
        print("10.Exit")
        choice = safe_input("Select an option: ")
        if choice is None:
            # don't exit the whole program; go back to the menu
            continue

        if choice == "1":
            add_student()
        elif choice == "2":
            record_grade()
        elif choice == "3":
            record_attendance()
        elif choice == "4":
            view_students()
        elif choice == "5":
            view_grades()
        elif choice == "6":
            view_attendance()
        elif choice == "7":
            average_grades()
        elif choice == "8":
            attendance_percentage()
        elif choice == "9":
            reset_all_data()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()