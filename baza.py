import sqlite3
import random
from faker import Faker

# Встановлення з'єднання з базою даних
conn = sqlite3.connect('mydatabase.db')

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# Створення таблиць у базі даних
cur.execute('''CREATE TABLE IF NOT EXISTS students (
               id INTEGER PRIMARY KEY,
               first_name TEXT,
               last_name TEXT,
               group_id INTEGER REFERENCES groups(id)
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS groups (
               id INTEGER PRIMARY KEY,
               name TEXT
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS teachers (
               id INTEGER PRIMARY KEY,
               first_name TEXT,
               last_name TEXT
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS subjects (
               id INTEGER PRIMARY KEY,
               name TEXT,
               teacher_id INTEGER REFERENCES teachers(id)
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS grades (
               id INTEGER PRIMARY KEY,
               student_id INTEGER REFERENCES students(id),
               subject_id INTEGER REFERENCES subjects(id),
               grade INTEGER,
               date DATE
            )''')

# Створення списку груп
groups = ["Group 1", "Group 2", "Group 3"]

# Додавання груп до таблиці groups
for group in groups:
    cur.execute("INSERT INTO groups (name) VALUES (?);", (group,))

# Створення списку викладачів
teachers = []
for i in range(5):
    first_name = Faker().first_name()
    last_name = Faker().last_name()
    teachers.append((first_name, last_name))

# Додавання викладачів до таблиці teachers
for teacher in teachers:
    cur.execute(
        "INSERT INTO teachers (first_name, last_name) VALUES (?, ?);", teacher)

# Створення списку предметів
subjects = [("Mathematics", 1), ("Physics", 2), ("Chemistry", 3),
            ("Biology", 4), ("Computer Science", 5)]

# Додавання предметів до таблиці subjects
for subject in subjects:
    cur.execute(
        "INSERT INTO subjects (name, teacher_id) VALUES (?, ?);", subject)

# Створення списку студентів
students = []
for i in range(50):
    first_name = Faker().first_name()
    last_name = Faker().last_name()
    group_id = random.randint(1, 3)
    students.append((i + 1, first_name, last_name, group_id))

# Додавання студентів до таблиці students
for student in students:
   cur.execute("SELECT id FROM students WHERE id = ?", (student[0],))
result = cur.fetchone()
if result:
    cur.execute("UPDATE students SET first_name = ?, last_name = ?, group_id = ? WHERE id = ?",
                (student[1], student[2], student[3], student[0]))
else:
    cur.execute(
        "INSERT INTO students (id, first_name, last_name, group_id) VALUES (?, ?, ?, ?);", student)

# Створення списку оцінок
grades = []
for student_id in range(1, 51):
    for subject_id in range(1, 6):
        grade = random.randint(1, 100)
        date = Faker().date_between(start_date='-3y', end_date='today')
        grades.append((student_id, subject_id, grade, date))

# Додавання оцінок до таблиці grades
for grade in grades:
    cur.execute(
        "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?);", grade)


# Підтвердження змін до бази даних
conn.commit()

# Закриття з'єднання та курсора
cur.close()
conn.close()
