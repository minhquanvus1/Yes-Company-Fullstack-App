import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Customer, Product, Order, OrderItem, CheckOutOrder
from datetime import datetime
from sqlalchemy import extract, desc
from auth import AuthError, requires_auth

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

def check_customer_exist(payload):
    subject = payload['sub']
    customer = Customer.query.filter_by(subject=subject).one_or_none()
    if customer:
        return customer
    return None

@APP.route('/check-customer', methods=['GET'])
@requires_auth('check:customers')
def check_customer(payload):
    customer = check_customer_exist(payload)
    if customer:
        return jsonify({'customer': customer.format()})
    return jsonify({'message': 'Customer not found, please create a customer account'}), 404
    
# ------------------ Customer ------------------

#---------- endpoint for "orders" resource
@APP.route('/orders', methods=['POST'])
@requires_auth('post:orders')
def create_order(payload):
    body = request.get_json()
    customer_id = body.get('customer_id', None)
    deliver_date = body.get('deliver_date', None)
    if not 'customer_id' in body or not 'deliver_date' in body or not 'comment' in body or not 'order_items' in body or not 'quantity' in body:
        abort(400, description="customer_id, deliver_date, comment, order_items and quantity are required in the request body")
    if customer_id is None or deliver_date is None:
        abort(400, description="customer_id and deliver_date must have value")
    comment = body.get('comment', None)
    comment = '' if comment is None else comment
    order_items = body.get('order_items', None)
    for each_order_item in order_items:
        if len(each_order_item.keys()) != 2 or 'product_id' not in each_order_item.keys() or 'quantity' not in each_order_item.keys():
            abort(400, description="product_id and quantity are required in each order_item, and only these two keys are allowed")
    check_out_order = CheckOutOrder(**body)
    print(check_out_order.format())
    try:
        check_out_order.insert()
        return jsonify({'order': check_out_order.format()})
    except:
        abort(422, description="The order could not be created due to the request body is not valid or the server is not able to process the request at the moment")

# -------------------Manager -------------------
#----- endpoint for "customers" resource
@APP.route('/customers', methods=['GET'])
@requires_auth('get:customers')
def get_customers(payload):
    customers = Customer.query.all()
    return jsonify({'customers': [customer.format() for customer in customers]})

@APP.route('/search-customers', methods=['POST'])
@requires_auth('search:customers')
def search_customer_by_firstName_and_lastName(payload):
    body = request.get_json()
    for each_key in body.keys():
        if each_key not in ['first_name', 'last_name']:
            abort(400, description="Only first_name and last_name are allowed in the request body")
    if len(body.keys()) > 2:
        abort(400, description="Only first_name and last_name are allowed in the request body")
    first_name = body.get('first_name', None)
    last_name = body.get('last_name', None)
    first_name = first_name.strip() if first_name is not None else None
    last_name = last_name.strip() if last_name is not None else None
    # if first_name is None and last_name is None:
    #     abort(400)
    customers = []
    if first_name is not None and last_name is not None:
        customers = Customer.query.filter(Customer.first_name.ilike(f'%{first_name}%'), Customer.last_name.ilike(f'%{last_name}%')).all()
    elif first_name is not None:
        customers = Customer.query.filter(Customer.first_name.ilike(f'%{first_name}%')).all()
    else:
        customers = Customer.query.filter(Customer.last_name.ilike(f'%{last_name}%')).all()    
    return jsonify({'customers': [customer.format() for customer in customers]})

#---------- endpoint for "products" resource
@APP.route('/products', methods=['POST'])
@requires_auth('post:products')
def create_product(payload):
    body = request.get_json()
    name = body.get('name', None)
    unit_price = body.get('unit_price', None)
    description = body.get('description', None)

    try:
        product = Product(name=name, unit_price=unit_price, description=description)
        product.insert()
        return jsonify({'product': product.format()})
    except:
        abort(422, description="The product could not be created due to the request body is not valid or the server is not able to process the request at the moment")

@APP.route('/products/<int:id>', methods=['PATCH'])
@requires_auth('patch:products')
def update_product(payload, id):
    product = db.session.get(Product, id)
    if product is None:
        abort(404, description="The product with the given id is not found")
    body = request.get_json()
    name = body.get('name', None)
    unit_price = body.get('unit_price', None)
    description = body.get('description', None)

    try:
        if name is not None:
            product.name = name
        if unit_price is not None:
            product.unit_price = unit_price
        if description is not None:
            product.description = description
        product.update()
        return jsonify({'product': product.format()})
    except:
        abort(422, description="The product could not be updated due to the request body is not valid or the server is not able to process the request at the moment")

@APP.route('/products/<int:id>', methods=['DELETE'])
@requires_auth('delete:products')
def delete_product(payload, id):
    product = db.session.get(Product, id)
    if product is None:
        abort(404, description="The product with the given id is not found")
    try:
        product.delete()
        return jsonify({'deleted': id})
    except:
        abort(422, description="The product could not be deleted due to the server is not able to process the request at the moment")

# ----------- endpoint for 'orders' resource
@APP.route('/orders', methods=['GET'])
@requires_auth('get:orders')
def get_orders(payload):
    sort_by = request.args.get('sort_by', None)
    
    if sort_by is None:
        orders = Order.query.all()
        # date_time = orders[0].deliver_date
        # print(date_time)
        # print(type(date_time))
        # print(date_time.strftime("%Y-%m-%d %H:%M:%S"))
        # print(type(date_time.strftime("%Y-%m-%d %H:%M:%S")))
        # print(date_time.isoformat())
        # print(type(date_time.isoformat()))
        # print(orders[0].__repr__())
        # print(type(orders[0].__dict__))
    elif sort_by not in ['customer_id', 'deliver_date']:
        abort(400, description="The sort_by parameter must be 'customer_id' or 'deliver_date' if it is provided in the request query string")
    else:
        if sort_by == 'customer_id':
            orders = Order.query.order_by(Order.customer_id, desc(Order.deliver_date)).all()
        else:
            orders = Order.query.order_by(desc(Order.deliver_date)).all()
    return jsonify({'orders': [order.format() for order in orders]})

@APP.route('/orders-by-date', methods=['GET'])
@requires_auth('get:orders-by-date')
def get_orders_by_deliver_date(payload):
    request_deliver_date = request.args.get('deliver_date', None)
    if not request_deliver_date:
        abort(400, description="The deliver_date parameter must be provided in the request query string")
    # request_deliver_date.strip()
    request_deliver_date = datetime.strptime(request_deliver_date, "%Y-%m-%d %H:%M:%S")
    print(request_deliver_date)
    print(request_deliver_date.month)
    order_list_on_this_date = Order.query.filter(extract('month', Order.deliver_date) == request_deliver_date.month,
                                                 extract('year', Order.deliver_date) == request_deliver_date.year,
                                                 extract('day', Order.deliver_date) == request_deliver_date.day).all()
    return jsonify({'orders': [order.format() for order in order_list_on_this_date]})

# ------------------Customer and Manager -------------------

#----- endpoint for "products" resource
@APP.route('/products', methods=['GET'])
@requires_auth('get:products')
def get_products(payload):
    query_params_dict = request.args.to_dict() # convert the ImmutableMultiDict to a dictionary
    if len(query_params_dict.keys()) == 0:
        products = Product.query.all()
    else:
        if len(query_params_dict.keys()) > 2 or not all([each_key in ['sort_by', 'ascending'] for each_key in query_params_dict.keys()]):
            abort(400, description="The sort_by and ascending are the only allowed query parameters")
        sort_by = query_params_dict.get('sort_by', None)
        ascending = query_params_dict.get('ascending', None)
        if ascending is not None and sort_by is None:
            abort(400, description="The sort_by parameter must be provided if the ascending parameter is provided in the request query string")
        elif sort_by is not None and sort_by in ['unit_price']:
            if ascending is None:
                products = Product.query.order_by(Product.unit_price).all()
            elif ascending.lower() not in ['true', 'false']:
                abort(400, description="The sort_by parameter must be 'unit_price' and the ascending parameter must be 'true' or 'false' if they are provided in the request query string")
            elif ascending.lower() == 'true':
                products = Product.query.order_by(Product.unit_price).all()
            else:
                products = Product.query.order_by(Product.unit_price.desc()).all()
        else:
            abort(400, description="The sort_by parameter must be 'unit_price' if it is provided in the request query string")
    return jsonify({'products': [product.format() for product in products]})

@APP.route('/search-products', methods=['POST'])
@requires_auth('search:products')
def search_by_product_name(payload):
    body = request.get_json()
    if len(body.keys()) != 1 or 'name' not in body.keys():
        abort(400, description="Only 'name' is allowed in the request body")
    name = body.get('name', None)
    products = []
    if name is not None:  
        products = Product.query.filter(Product.name.ilike(f'%{name}%')).all()
    return jsonify({'products': [product.format() for product in products]})

#----- endpoint for "orders" resource
@APP.route('/customers/<int:id>/orders', methods=['GET'])
@requires_auth('get:ordersByCustomerId')
def get_orders_by_customer(payload, id):
    orders = Order.query.filter(Order.customer_id == id).all()
    return jsonify({'orders': [order.format() for order in orders]})

@APP.route('/orders/<int:id>', methods=['PATCH'])
@requires_auth('patch:orders')
def update_order(payload, id):
    order = Order.query.filter(Order.id == id).one_or_none()
    # print(type(order_dict))
    # print(isinstance(order_dict, Order))
    if order is None:
        abort(404, description="The order with the given id is not found")
    body = request.get_json()
    if 'customer_id' in body:
        abort(422, description="The customer_id cannot be updated")
    if 'deliver_date' in body:
        deliver_date = body.get('deliver_date', None)
        if not isinstance(deliver_date, str) or deliver_date.strip() == '':
            abort(400, description="The deliver_date must have the string value of a valid date and time format (YYYY-MM-DD HH:MM:SS)")
        print(deliver_date)
        order.deliver_date = deliver_date
    if 'comment' in body:
        comment = body.get('comment', None)
        order.comment = comment
    if 'order_items' in body:
        order_items = body.get('order_items', None)
        if not isinstance(order_items, list) and len(order_items) <= 0:
            abort(400, description="The order_items must be a list of order_item objects and it cannot be empty")
        print(order_items)
        list_of_order_items_objects = []
        for each_order_item in order_items:
            if len(each_order_item.keys()) != 2 or 'product_id' not in each_order_item.keys() or 'quantity' not in each_order_item.keys():
                abort(400, description="product_id and quantity are required in each order_item, and only these two keys are allowed")
            print(isinstance(each_order_item, dict))
            each_order_item_object = OrderItem(**each_order_item, order_id=id)
            print(each_order_item_object.format())
            list_of_order_items_objects.append(each_order_item_object)
        print(order_items)
        print(list_of_order_items_objects)
        order.order_items = list_of_order_items_objects
    try:
        order.update()
        return jsonify({'order': order.format()})
    except:
        abort(422, description="The order could not be updated due to the request body is not valid or the server is not able to process the request at the moment")

@APP.route('/orders/<int:id>', methods=['DELETE'])
@requires_auth('delete:orders')
def delete_order(payload, id):
    order = Order.query.filter(Order.id == id).one_or_none()
    if order is None:
        abort(404, description="The order with the given id is not found")
    try:
        order.delete()
        return jsonify({'deleted': id})
    except:
        abort(422, description="The order could not be deleted due to the server is not able to process the request at the moment")

#----- endpoint for "customers" resource

@APP.route('/customers', methods=['POST'])
@requires_auth('post:customers')
def create_customer(payload):
    check_customer = check_customer_exist(payload)
    if check_customer:
        return jsonify({'message': 'Customer already exists'}), 409
    customer = request.get_json()
    if customer is None:
        abort(400, description="The request body is empty")
    first_name = customer.get('first_name', None)
    last_name = customer.get('last_name', None)
    address = customer.get('address', None)
    if first_name is None or last_name is None or address is None:
        abort(400, description="first_name, last_name and address are required in the request body")
    try:
        customer = Customer(**customer)
        customer.insert()
        return jsonify({'customer': customer.format()})
    except:
        abort(422, description="The customer could not be created due to the request body is not valid or the server is not able to process the request at the moment")

# ---------------- Error Handling -------------------

@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400

@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404

@APP.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description
    }), 422

@APP.errorhandler(409)
def conflict(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": error.description
    }), 409

@APP.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500

@APP.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)