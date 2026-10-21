import sqlite3
connection = sqlite3.connect("labslot.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_name TEXT NOT NULL,
    lab_name TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    purpose TEXT NOT NULL,
    student_count INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Booked'
)
""")
cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS
unique_active_booking
ON bookings (
    lab_name,
    booking_date,
    time_slot
)
WHERE status = 'Booked'
""")
connection.commit()
connection.close()
print("LabSlot database initialized successfully!")