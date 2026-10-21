# LabSlot – Computer Lab Booking System

LabSlot is a simple web-based Computer Lab Booking System developed using Python Flask and SQLite.

The system allows faculty members to book computer labs, view existing bookings, filter bookings, and cancel bookings.

## Features

- Book a computer lab
- View all lab bookings
- Filter bookings by lab and date
- Cancel bookings
- Prevent duplicate active bookings
- Prevent booking for past dates
- Cancelled bookings automatically free the selected slot
- Simple and responsive user interface

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| HTML | Frontend structure |
| CSS | Frontend styling |
| Jinja2 | Template rendering |

## Project Structure

```text
labslot/
│
├── app.py
├── database.py
├── init_db.py
├── README.md
├── .gitignore
│
├── routes/
│   ├── __init__.py
│   ├── booking.py
│   └── dashboard.py
│
├── templates/
│   ├── booking.html
│   ├── bookings.html
│   └── dashboard.html
│
└── static/
    └── css/
        └── style.css
```

## Database

The application uses SQLite.

Database table:

### bookings

| Field | Description |
|---|---|
| booking_id | Unique booking ID |
| faculty_name | Name of faculty member |
| lab_name | Selected computer lab |
| booking_date | Date of booking |
| time_slot | Selected time slot |
| purpose | Purpose of lab usage |
| student_count | Number of students |
| status | Booked or Cancelled |

## Business Rules

1. A faculty member must provide a name.
2. A lab must be selected.
3. Past dates cannot be selected.
4. A valid time slot must be selected.
5. Purpose must contain between 5 and 100 characters.
6. Student count must be between 1 and 60.
7. The same lab cannot be booked twice for the same date and time slot.
8. Cancelled bookings do not occupy the slot.
9. Cancelled bookings are retained in the database for history.

## Available Labs

- Lab 1
- Lab 2
- Lab 3
- Lab 4

## Available Time Slots

- 9:00 AM – 11:00 AM
- 11:00 AM – 1:00 PM
- 2:00 PM – 4:00 PM
- 4:00 PM – 6:00 PM

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Udaylandge/MCA-33_LabSlot.git
```

### 2. Open the project

```bash
cd MCA-33_LabSlot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

### 5. Install Flask

```bash
pip install Flask
```

### 6. Initialize the database

```bash
python init_db.py
```

### 7. Run the application

```bash
python app.py
```

### 8. Open in browser

```text
http://127.0.0.1:5050
```

## Application Pages

| URL | Purpose |
|---|---|
| `/` | Dashboard |
| `/book` | Book a lab |
| `/bookings` | View all bookings |
| `/bookings/cancel/<id>` | Cancel a booking |

## Booking Flow

```text
Faculty
   ↓
Select Lab
   ↓
Select Date
   ↓
Select Time Slot
   ↓
Enter Purpose
   ↓
Enter Student Count
   ↓
Submit Booking
   ↓
Validate Business Rules
   ↓
Check Slot Availability
   ↓
Save Booking in SQLite
```

## Duplicate Booking Prevention

LabSlot checks whether an active booking already exists for the selected:

- Lab
- Date
- Time Slot

If the combination already exists, the new booking is rejected.

A unique SQLite index is also used to enforce this rule at the database level.

## Cancellation

When a booking is cancelled, its status changes from:

```text
Booked
```

to:

```text
Cancelled
```

The record is not deleted, which allows booking history to be preserved.
