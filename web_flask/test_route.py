from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

database = "mysampledb"
username = "alchemy"
host = "localhost"


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
    username, "password", host, database
)

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employees'

    name = db.Column(db.String(15), primary_key=True)
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(15))

@app.route('/employees', strict_slashes=False)
def employees():
    emps = Employee.query.all()
    return jsonify([emp.name for emp in emps])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
