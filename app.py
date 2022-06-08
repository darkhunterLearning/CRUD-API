# import lib
from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__)
jwt = JWTManager(app)


app.config['SECRET_KEY'] = 'secretkey'
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
    password = db.Column(db.String(100))

db.create_all()


# Run app
@app.route('/')
def index():
    return jsonify({"message":"Hello World!"})

# Get all customer
@app.route('/getcustomers', methods=['GET'])
@jwt_required()
def getcustomers():
     all_customers = []
     customers = Customer.query.all()
     for customer in customers:
          results = {
                    "customer_id":customer.id,
                    "customer_name":customer.customer_name,
                    "customer_phone":customer.customer_phone,
                    "customer_address":customer.customer_address,
                    "password":customer.password}
          all_customers.append(results)

     return jsonify(
            {
                "success": True,
                "customers": all_customers,
                "total_customers": len(customers),
            }
        )

# Create new customer
@app.route('/customers', methods = ['POST'])
def create_customer():
    customer_phone = request.form["customer_phone"]
    test = Customer.query.filter_by(customer_phone=customer_phone).first()
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        customer_name = request.form["customer_name"]
        customer_phone = request.form["customer_phone"]
        customer_address = request.form["customer_address"]
        password = request.form["password"]
        customer = Customer(customer_name=customer_name, customer_phone=customer_phone, customer_address=customer_address, password=password)
        db.session.add(customer)
        db.session.commit()
        return jsonify(message="User added sucessfully"), 201

# Log-in to get JWT
# route for logging user in
@app.route('/login', methods =['POST'])
def login_user():
   # creates dictionary of form data
    auth = request.form
  
    if not auth or not auth.get('customer_phone') or not auth.get('password'):
        # returns 401 if any customer_phone or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = Customer.query\
        .filter_by(customer_phone=auth.get('customer_phone'))\
        .first()
  
    if user:
        access_token = create_access_token(identity=auth.get('customer_phone'))
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Invalid!"), 401

# Get single customer by Id
@app.route('/customers/<id>', methods=['GET'])
@jwt_required()
def get_customer(id):
  customer = Customer.query.get(id)

  return jsonify(
                {
                    "customer_id":customer.id,
                    "customer_name":customer.customer_name,
                    "customer_phone":customer.customer_phone,
                    "customer_address":customer.customer_address
                }
            )

# Update Customer's Information ---- Only update phone & address
@app.route('/customers/<id>', methods=['PATCH'])
@jwt_required()
def update_customer(id):
  customer = Customer.query.get(id)
  customer_phone = request.json['customer_phone']
  customer_address = request.json['customer_address']

  if customer is None:
      abort(404)

  else:
      customer.customer_phone = customer_phone
      customer.customer_address = customer_address
      db.session.add(customer)
      db.session.commit()
      return jsonify({"success": True, "reponse": "Customer's Infomation Updated"})

# Delete Customer by Id
@app.route('/customers/<id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
  db.session.query(Customer).filter_by(id=id).delete()
  db.session.commit()
  return jsonify({"success": True, "reponse": "Customer deleted"})
    

if __name__ == '__main__':
  app.run(debug=True)