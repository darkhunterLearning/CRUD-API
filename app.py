# import lib
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jwt:123456@localhost/customers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Customer %r>" % self.customer_name

db.create_all()

@app.route('/')
def index():
    return jsonify({"message":"Hello World"})

if __name__ == '__main__':
  app.run(debug=True)