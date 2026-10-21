from flask import Blueprint, render_template
from database import get_db_connection
from datetime import date

dashbord_bp = Blueprint("dashbord", __name__)


@dashbord_bp.route("/")
def dashbord():

    connection = get_db_connection()

    today = date.today().isoformat()

    total_bookings = connection.execute("""
        SELECT COUNT(*) AS count
        FROM bookings
        WHERE status = 'Booked'
    """).fetchone()["count"]

    today_bookings = connection.execute("""
        SELECT COUNT(*) AS count
        FROM bookings
        WHERE booking_date = ?
        AND status = 'Booked'
    """, (today,)).fetchone()["count"]

    lab_counts = connection.execute("""
        SELECT lab_name, COUNT(*) AS count
        FROM bookings
        WHERE status = 'Booked'
        GROUP BY lab_name
        ORDER BY lab_name
    """).fetchall()

    connection.close()

    return render_template(
        "dashbord.html",
        total_bookings=total_bookings,
        today_bookings=today_bookings,
        lab_counts=lab_counts
    )