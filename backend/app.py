import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Customer, Product, Order, OrderItem, CheckOutOrder
from datetime import datetime
from sqlalchemy import extract, desc
from auth import AuthError, requires_auth
from flask_migrate import Migrate
from typing import List, Dict, Optional
from config import production_config

def create_app(test_config=None):
    
  # create and configure the app
    APP = Flask(__name__)
    APP.config.from_mapping(production_config)
    CORS(APP)
    if test_config is not None:
        APP.config.from_mapping(test_config)
    db.APP = APP
    db.init_app(APP)
    with APP.app_context():
        migrate = Migrate(APP, db)
        #   db.drop_all()
        #   db.create_all()  
    APP.app_context().push()
    
    @APP.route('/hello', methods=['GET'])
    def hello():
        return jsonify({'message': 'Hello World!'})

    def check_customer_exist(payload) -> Optional[Customer]:
        subject = payload['sub']
        print(subject)
        customer = Customer.query.filter_by(subject=subject).one_or_none()
        if customer:
            return customer
        return None
        
    # ------------------ Customer ------------------

    # ---------------- endpoint for "customers" resource

    @APP.route('/check-customer', methods=['GET'])
    @requires_auth('check:customers')
    def check_customer(payload):
        customer = check_customer_exist(payload)
        if customer:
            return jsonify({'customer': customer.format()})
        return jsonify({'message': 'Customer not found, please create a customer account'}), 404

    @APP.route('/customers', methods=['POST'])
    @requires_auth('post:customers')
    def create_customer(payload):
        check_customer = check_customer_exist(payload)
        if check_customer:
            return jsonify({'message': 'Customer already exists', 'customer': check_customer.format()}), 409
        customer = request.get_json()
        if customer is None:
            abort(400, description="The request body is empty")
        first_name = customer.get('first_name', None)
        last_name = customer.get('last_name', None)
        address = customer.get('address', None)
        subject = payload.get('sub', None)
        if subject is None:
            abort(400, description="The subject is required in the payload")
        if first_name is None or last_name is None or address is None:
            abort(400, description="first_name, last_name and address are required in the request body")
        try:
            customer = Customer(**customer, subject=subject)
            customer.insert()
            return jsonify({'customer': customer.format()}), 201
        except:
            abort(422, description="The customer could not be created due to the request body is not valid or the server is not able to process the request at the moment")

    #---------- endpoint for "orders" resource
    @APP.route('/orders', methods=['POST'])
    @requires_auth('post:orders')
    def create_order(payload):
        body = request.get_json()
        customer_id = body.get('customer_id', None)
        deliver_date = body.get('deliver_date', None)
        if not 'customer_id' in body or not 'deliver_date' in body or not 'comment' in body or not 'order_items' in body:
            abort(400, description="customer_id, deliver_date, comment, order_items and quantity are required in the request body")
        if customer_id is None or deliver_date is None:
            abort(400, description="customer_id and deliver_date must have value")
        comment = body.get('comment', None)
        comment = '' if comment is None else comment
        order_items: List = body.get('order_items', None)
        for each_order_item in order_items:
            if len(each_order_item.keys()) != 2 or 'product_id' not in each_order_item.keys() or 'quantity' not in each_order_item.keys():
                abort(400, description="product_id and quantity are required in each order_item, and only these two keys are allowed")
            if each_order_item['product_id'] not in [product.id for product in Product.query.all()]:
                abort(400, description="The product with the given id is not found")
        check_out_order = CheckOutOrder(**body)
        print(check_out_order.format())
        try:
            check_out_order.insert()
            return jsonify({'order': check_out_order.format()}), 201
        except:
            abort(422, description="The order could not be created due to the request body is not valid or the server is not able to process the request at the moment")

    # -------------------Manager -------------------
    #----- endpoint for "customers" resource
    @APP.route('/customers', methods=['GET'])
    @requires_auth('get:customers')
    def get_customers(payload):
        customers = Customer.query.all()
        print(customers)
        return jsonify({'customers': [customer.format() for customer in customers]})
    
    @APP.route('/customers/<int:id>', methods=['GET'])
    @requires_auth('get:customerById')
    def get_customer_by_id(payload, id):
        customer = Customer.query.filter(Customer.id == id).one_or_none()
        if customer is None:
            abort(404, description="The customer with the given id is not found")
        return jsonify({'customer': customer.format()})

    @APP.route('/search-customers', methods=['POST'])
    @requires_auth('search:customers')
    def search_customer_by_firstName_and_lastName(payload):
        print('hello world')
        body = request.get_json()
        for each_key in body.keys():
            if each_key not in ['first_name', 'last_name']:
                abort(400, description="Only first_name and last_name are allowed in the request body")
        if len(body.keys()) > 2:
            abort(400, description="Only first_name and last_name are allowed in the request body")
        first_name = body['first_name'].strip()
        last_name = body['last_name'].strip()
        customers = []
        print(first_name)
        print(last_name)
        if first_name != '' and last_name != '':
            customers = Customer.query.filter(Customer.first_name.ilike(f'%{first_name}%'), Customer.last_name.ilike(f'%{last_name}%')).all()
        elif first_name != '':
            customers = Customer.query.filter(Customer.first_name.ilike(f'%{first_name}%')).all()
        else:
            customers = Customer.query.filter(Customer.last_name.ilike(f'%{last_name}%')).all()
        print(customers)
        if len(customers) == 0:
            return jsonify({'customers': [], 'message': 'No customer found with the given first_name and last_name'}), 404   
        return jsonify({'customers': [customer.format() for customer in customers]})

    #---------- endpoint for "products" resource
    @APP.route('/products', methods=['POST'])
    @requires_auth('post:products')
    def create_product(payload):
        body = request.get_json()
        if body is None:
            abort(400, description="The request body is empty")
        name = body.get('name', None)
        unit_price: int = body.get('unit_price', None)
        description = body.get('description', None)
        if name is None or unit_price is None or description is None:
            abort(400, description="name, unit_price and description are required in the request body")
        existing_product_list = Product.query.filter(Product.name == name).all()
        if len(existing_product_list) > 0:
            abort(409, description="The product with the given name already exists")
        try:
            product = Product(name=name, unit_price=unit_price, description=description)
            product.insert()
            return jsonify({'product': product.format()}), 201
        except:
            abort(422, description="The product could not be created due to the request body is not valid or the server is not able to process the request at the moment")

    @APP.route('/products/<int:id>', methods=['PATCH'])
    @requires_auth('patch:products')
    def update_product(payload, id):
        product = db.session.get(Product, id)
        if product is None:
            abort(404, description="The product with the given id is not found")
        body = request.get_json()
        if body is None:
            abort(400, description="The request body is empty")
        if not all(each_key in ['name', 'unit_price', 'description'] for each_key in body):
            abort(400, description="name or unit_price or description are required in the request body")
        name = body.get('name', None)
        unit_price: int = body.get('unit_price', None)
        description = body.get('description', None)
        if name is not None:
            name = name.strip()
            list_of_existing_products_apart_from_the_current_one = Product.query.filter(Product.id != id).all()
            for each_product in list_of_existing_products_apart_from_the_current_one:
                if each_product.name == name:
                    abort(409, description="The product with the given name already exists")
        if unit_price is not None:
            if not isinstance(unit_price, int):
                abort(400, description="The unit_price must be an integer")
        try:
            product.name = name if name is not None else product.name
            product.unit_price = unit_price if unit_price is not None else product.unit_price
            product.description = description.strip() if description is not None else product.description
            product.update()
            return jsonify({'product': product.format()}), 200
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
            return jsonify({'deleted': id}), 200
        except:
            abort(422, description="The product could not be deleted due to the server is not able to process the request at the moment")

    @APP.route('/products/<int:id>', methods=['GET'])
    @requires_auth('get:productById')
    def get_product_by_id(payload, id):
        product = db.session.get(Product, id)
        if product is None:
            abort(404, description="The product with the given id is not found")
        return jsonify({'product': product.format()}), 200
    # ----------- endpoint for 'orders' resource
    @APP.route('/orders', methods=['GET'])
    @requires_auth('get:orders')
    def get_orders(payload):
        sort_by: Optional[str] = request.args.get('sort_by', None)
        
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
        try:
            request_deliver_date = datetime.strptime(request_deliver_date, "%Y-%m-%d %H:%M:%S")
        except:
            abort(400, description="The deliver_date must have the string value of a valid date and time format (YYYY-MM-DD HH:MM:SS)")
        print(request_deliver_date)
        print(request_deliver_date.month)
        try:
            order_list_on_this_date = Order.query.filter(extract('month', Order.deliver_date) == request_deliver_date.month,
                                                        extract('year', Order.deliver_date) == request_deliver_date.year,
                                                        extract('day', Order.deliver_date) == request_deliver_date.day).all()
        except:
            abort(422, description="The server is not able to process the request at the moment")
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
            sort_by: Optional[str] = query_params_dict.get('sort_by', None)
            ascending: Optional[str] = query_params_dict.get('ascending', None)
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
        name = body.get('name', '').strip()
        print(name)
        products = []
        if name != '':
            products = Product.query.filter(Product.name.ilike(f'%{name}%')).all()
            if len(products) == 0:
                return jsonify({
                    'products': [],
                    'message': 'No product found with the given name'
                }), 404
        else:
            products = Product.query.all()
        print(products)
        return jsonify({'products': [product.format() for product in products]})

    #----- endpoint for "orders" resource
    @APP.route('/customers/<int:id>/orders', methods=['GET'])
    @requires_auth('get:ordersByCustomerId')
    def get_orders_by_customer(payload, id):
        orders = Order.query.filter(Order.customer_id == id).all()
        if len(orders) == 0:
            abort(404, description="This Customer with this id has no order yet")
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
            deliver_date = body.get('deliver_date', '')
            if not isinstance(deliver_date, str) or deliver_date.strip() == '':
                abort(400, description="The deliver_date must have the string value of a valid date and time format (YYYY-MM-DD HH:MM:SS)")
            try:
                deliver_date = datetime.strptime(deliver_date, "%Y-%m-%d %H:%M:%S")
            except:
                abort(400, description="The deliver_date must have the string value of a valid date and time format (YYYY-MM-DD HH:MM:SS)")
            if deliver_date < datetime.now():
                abort(422, description="The deliver_date must be a future date and time")
            print(deliver_date)
            order.deliver_date = deliver_date
        if 'comment' in body:
            comment = body.get('comment', '')
            order.comment = comment
        if 'order_items' in body:
            order_items = body.get('order_items')
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
            return jsonify({'deleted': id}), 200
        except:
            abort(422, description="The order could not be deleted due to the server is not able to process the request at the moment")

    #----- endpoint for "customers" resource

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
    return APP