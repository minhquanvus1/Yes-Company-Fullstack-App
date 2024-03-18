import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Customer, Product, Order, OrderItem, CheckOutOrder
from datetime import datetime
from sqlalchemy import extract, desc

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

# ------------------ Customer ------------------

#---------- endpoint for "orders" resource
@APP.route('/orders', methods=['POST'])
def create_order():
    body = request.get_json()
    customer_id = body.get('customer_id', None)
    deliver_date = body.get('deliver_date', None)
    if not 'customer_id' in body or not 'deliver_date' in body or not 'comment' in body or not 'order_items' in body or not 'quantity' in body:
        abort(400)
    if customer_id is None or deliver_date is None:
        abort(400)
    comment = body.get('comment', None)
    comment = '' if comment is None else comment
    order_items = body.get('order_items', None)
    for each_order_item in order_items:
        if len(each_order_item.keys()) != 2 or 'product_id' not in each_order_item.keys() or 'quantity' not in each_order_item.keys():
            abort(400)
    check_out_order = CheckOutOrder(**body)
    print(check_out_order.format())
    try:
        check_out_order.insert()
        return jsonify({'order': check_out_order.format()})
    except:
        abort(422)

# -------------------Manager -------------------
#----- endpoint for "customers" resource
@APP.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify({'customers': [customer.format() for customer in customers]})

@APP.route('/search-customers', methods=['POST'])
def search_customer_by_firstName_and_lastName():
    body = request.get_json()
    for each_key in body.keys():
        if each_key not in ['first_name', 'last_name']:
            abort(400)
    if len(body.keys()) > 2:
        abort(400)
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
def create_product():
    body = request.get_json()
    name = body.get('name', None)
    unit_price = body.get('unit_price', None)
    description = body.get('description', None)

    try:
        product = Product(name=name, unit_price=unit_price, description=description)
        product.insert()
        return jsonify({'product': product.format()})
    except:
        abort(422)

@APP.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    product = db.session.get(Product, id)
    if product is None:
        abort(404)
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
        abort(422)

@APP.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    if product is None:
        abort(404)
    try:
        product.delete()
        return jsonify({'deleted': id})
    except:
        abort(422)

# ------------------Customer and Manager -------------------

#----- endpoint for "products" resource
@APP.route('/products', methods=['GET'])
def get_products():
    sort_by = request.args.get('sort_by', None)
    if sort_by is None:
        products = Product.query.all()
    elif sort_by not in ['unit_price']:
        abort(400)
    else:
        products = Product.query.order_by(Product.unit_price).all()
    return jsonify({'products': [product.format() for product in products]})

@APP.route('/search-products', methods=['POST'])
def search_by_product_name():
    body = request.get_json()
    if len(body.keys()) != 1 or 'name' not in body.keys():
        abort(400)
    name = body.get('name', None)
    products = []
    if name is not None:  
        products = Product.query.filter(Product.name.ilike(f'%{name}%')).all()
    return jsonify({'products': [product.format() for product in products]})

#----- endpoint for "orders" resource
@APP.route('/orders', methods=['GET'])
def get_orders():
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
        abort(400)
    else:
        if sort_by == 'customer_id':
            orders = Order.query.order_by(Order.customer_id, desc(Order.deliver_date)).all()
        else:
            orders = Order.query.order_by(desc(Order.deliver_date)).all()
    return jsonify({'orders': [order.format() for order in orders]})

@APP.route('/orders-by-date', methods=['GET'])
def get_orders_by_deliver_date():
    request_deliver_date = request.args.get('deliver_date', None)
    if not request_deliver_date:
        abort(400)
    # request_deliver_date.strip()
    request_deliver_date = datetime.strptime(request_deliver_date, "%Y-%m-%d %H:%M:%S")
    print(request_deliver_date)
    print(request_deliver_date.month)
    order_list_on_this_date = Order.query.filter(extract('month', Order.deliver_date) == request_deliver_date.month,
                                                 extract('year', Order.deliver_date) == request_deliver_date.year,
                                                 extract('day', Order.deliver_date) == request_deliver_date.day).all()
    return jsonify({'orders': [order.format() for order in order_list_on_this_date]})

@APP.route('/orders/<int:id>', methods=['PATCH'])
def update_order(id):
    order = Order.query.filter(Order.id == id).one_or_none()
    # print(type(order_dict))
    # print(isinstance(order_dict, Order))
    if order is None:
        abort(404)
    body = request.get_json()
    if 'customer_id' in body:
        abort(422)
    if 'deliver_date' in body:
        deliver_date = body.get('deliver_date', None)
        if deliver_date is None:
            abort(400)
        print(deliver_date)
        order.deliver_date = deliver_date
    if 'comment' in body:
        comment = body.get('comment', None)
        order.comment = comment
    if 'order_items' in body:
        order_items = body.get('order_items', None)
        if order_items is None:
            abort(400)
        print(order_items)
        list_of_order_items_objects = []
        for each_order_item in order_items:
            if len(each_order_item.keys()) != 2 or 'product_id' not in each_order_item.keys() or 'quantity' not in each_order_item.keys():
                abort(400)
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
        abort(422)

@APP.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.filter(Order.id == id).one_or_none()
    if order is None:
        abort(404)
    try:
        order.delete()
        return jsonify({'deleted': id})
    except:
        abort(422)

#----- endpoint for "customers" resource
@APP.route('/customers/<int:id>/orders', methods=['GET'])
def get_orders_by_customer(id):
    orders = Order.query.filter(Order.customer_id == id).all()
    return jsonify({'orders': [order.format() for order in orders]})

@APP.route('/customers', methods=['POST'])
def create_customer():
    customer = request.get_json()
    if customer is None:
        abort(400)
    first_name = customer.get('first_name', None)
    last_name = customer.get('last_name', None)
    address = customer.get('address', None)
    if first_name is None or last_name is None or address is None:
        abort(400)
    try:
        customer = Customer(**customer)
        customer.insert()
        return jsonify({'customer': customer.format()})
    except:
        abort(422)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)