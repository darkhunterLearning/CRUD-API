# import lib
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost/customers'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create table customers
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Customer %r>" % self.customer_name

    def __init__(self, customer_name, customer_phone, customer_address):
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_address = customer_address

db.create_all()

# Run app
@cross_origin()
@app.route('/')
def index():
    return jsonify({"message":"Hello World"})

# Get all customer
@cross_origin()
@app.route('/getcustomers', methods=['GET'])
def getcustomers():
     all_customers = []
     customers = Customer.query.all()
     for customer in customers:
          results = {
                    "customer_id":customer.id,
                    "customer_name":customer.customer_name,
                    "customer_phone":customer.customer_age,
                    "customer_address":customer.customer_type }
          all_customers.append(results)

     return jsonify(
            {
                "success": True,
                "customers": all_customers,
                "total_customers": len(customers),
            }
        )
if __name__ == '__main__':
  app.run(debug=True)