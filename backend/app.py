import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Customer, Product, Order, OrderItem, CheckOutOrder

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  return app
APP = create_app()
APP.app_context().push()

@APP.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello World!'})

@APP.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify({'customers': [customer.format() for customer in customers]})

@APP.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({'products': [product.format() for product in products]})

@APP.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    date_time = orders[0].deliver_date
    print(date_time)
    print(type(date_time))
    print(date_time.strftime("%Y-%m-%d %H:%M:%S"))
    print(type(date_time.strftime("%Y-%m-%d %H:%M:%S")))
    print(date_time.isoformat())
    print(type(date_time.isoformat()))
    print(orders[0].__repr__())
    print(type(orders[0].__dict__))
    return jsonify({'orders': [order.format() for order in orders]})
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)