from flask import Flask
from routes.dashbord import dashbord_bp
from routes.booking import booking_bp
app = Flask(__name__)

app.register_blueprint(dashbord_bp)
app.register_blueprint(booking_bp)


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5050,debug=True)