from flask import Blueprint, render_template, request
from database import get_db_connection
from datetime import date

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/book", methods=["GET", "POST"])
def book_lab():

    if request.method == "POST":

        faculty_name = request.form.get("faculty_name", "").strip()
        lab_name = request.form.get("lab_name", "").strip()
        booking_date = request.form.get("booking_date", "").strip()
        time_slot = request.form.get("time_slot", "").strip()
        purpose = request.form.get("purpose", "").strip()
        student_count_raw = request.form.get(
            "student_count", ""
        ).strip()

        if not faculty_name:
            return "Faculty name is required."

        if not lab_name:
            return "Lab is required."

        if not booking_date:
            return "Booking date is required."

        if not time_slot:
            return "Time slot is required."

        if not purpose:
            return "Purpose is required."

        if len(purpose) < 5 or len(purpose) > 100:
            return "Purpose must be between 5 and 100 characters."

        if not student_count_raw.isdigit():
            return "Student count must be a number."

        student_count = int(student_count_raw)

        if student_count < 1 or student_count > 60:
            return "Student count must be between 1 and 60."

        selected_date = date.fromisoformat(booking_date)

        if selected_date < date.today():
            return "Past dates are not allowed."

        connection = get_db_connection()

        existing_booking = connection.execute(
            """
            SELECT booking_id
            FROM bookings
            WHERE lab_name = ?
              AND booking_date = ?
              AND time_slot = ?
              AND status = 'Booked'
            """,
            (
                lab_name,
                booking_date,
                time_slot
            )
        ).fetchone()

        if existing_booking:

            connection.close()

            return (
                "This lab is already booked "
                "for the selected date and time."
            )

        connection.execute(
            """
            INSERT INTO bookings (
                faculty_name,
                lab_name,
                booking_date,
                time_slot,
                purpose,
                student_count
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                faculty_name,
                lab_name,
                booking_date,
                time_slot,
                purpose,
                student_count
            )
        )

        connection.commit()
        connection.close()

        return "Lab booked successfully!"

    return render_template("booking.html")


@booking_bp.route("/bookings")
def view_bookings():

    lab = request.args.get("lab", "").strip()
    booking_date = request.args.get("date", "").strip()

    connection = get_db_connection()

    query = """
        SELECT *
        FROM bookings
        WHERE 1 = 1
    """

    parameters = []

    if lab:
        query += " AND lab_name = ?"
        parameters.append(lab)

    if booking_date:
        query += " AND booking_date = ?"
        parameters.append(booking_date)

    query += """
        ORDER BY booking_date ASC, time_slot ASC
    """

    bookings = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "bookings.html",
        bookings=bookings,
        selected_lab=lab,
        selected_date=booking_date
    )
@booking_bp.route("/bookings/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):

    connection = get_db_connection()

    booking = connection.execute(
        """
        SELECT booking_id, status
        FROM bookings
        WHERE booking_id = ?
        """,
        (booking_id,)
    ).fetchone()

    if booking is None:

        connection.close()

        return "Booking not found.", 404

    if booking["status"] == "Cancelled":

        connection.close()

        return "Booking is already cancelled."

    connection.execute(
        """
        UPDATE bookings
        SET status = 'Cancelled'
        WHERE booking_id = ?
        """,
        (booking_id,)
    )

    connection.commit()
    connection.close()

    return "Booking cancelled successfully!"
