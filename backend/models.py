import json
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# db = SQLAlchemy()

# DB_USERNAME = os.getenv('DB_USERNAME')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')

# TEST_DB_USERNAME = os.getenv('TEST_DB_USERNAME')
# TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
# TEST_DB_HOST = os.getenv('TEST_DB_HOST')
# TEST_DB_PORT = os.getenv('TEST_DB_PORT')
# TEST_DB_NAME = os.getenv('TEST_DB_NAME')

# if not os.getenv('DATABASE_URL'):
#     database_path = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
# else:
#     database_path = os.getenv('DATABASE_URL')
#     if database_path.startswith("postgres://"):
#         database_path = database_path.replace("postgres://", "postgresql://", 1)
db = SQLAlchemy()

# def setup_db(app, database_path=database_path):
#     # if test != True:
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # else:
#     # database_path = f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
#     # app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     # migrate = Migrate(app, db)
#     # with app.app_context():
#     #     # db.drop_all()
#     #     db.create_all()

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', backref=db.backref('customer', lazy=True), lazy='joined', cascade='all, delete')

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'address': self.address}
    def __repr__(self):
        return json.dumps(self.format())


class OrderItem(db.Model):
    __tablename__ = 'OrderItem'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('order_id', 'product_id', name='unique_order_product'),
    )
    # order_haha = db.relationship('Order', back_populates='order_items', lazy=True)
    # product_haha = db.relationship('Product', back_populates='order_items', lazy=True)
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {'id': self.id, 'order_id': self.order_id, 'product_id': self.product_id, 'quantity': self.quantity}
    def __repr__(self):
        return json.dumps(self.format())


class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    unit_price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    order_items = db.relationship('OrderItem', backref=db.backref('product', lazy=True), lazy='joined', cascade='all, delete')
    orders = association_proxy('order_items', 'order')

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {'id': self.id, 'name': self.name, 'unit_price': self.unit_price, 'description': self.description}
    def __repr__(self):
        return json.dumps(self.format())

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id'), nullable=False)
    deliver_date = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String, nullable=True)
    order_items = db.relationship('OrderItem', backref=db.backref('order', lazy=True), lazy='joined', cascade='all, delete')
    products = association_proxy('order_items', 'product')

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def find_total_price(self):
        total_price = 0
        for order_item in self.order_items:
            total_price += order_item.product.unit_price * order_item.quantity
        return total_price
    def format(self):
        format_order_items_list = [{'name': order_item.product.name, 
                                'unit_price': order_item.product.unit_price, 
                                'quantity': order_item.quantity} 
                                for order_item in self.order_items]
        if isinstance(self.deliver_date, str):
            self.deliver_date = datetime.strptime(self.deliver_date, "%Y-%m-%d %H:%M:%S") # convert string to datetime
        return_order = {'id': self.id, 
                        'customer_id': self.customer_id, 
                        'deliver_date': self.deliver_date.strftime("%Y-%m-%d %H:%M:%S"), 
                        'comment': self.comment, 
                        'order_items': format_order_items_list, 
                        'total_price': self.find_total_price()}
        return return_order
    def __repr__(self):
        return json.dumps(self.format())

# the dto class for frontend to send data to backend by POST request. 
# for example, when a customer checks out an order, 
# the frontend will send a POST request to the backend with the data of the order.
# the backend will then create a CheckOutOrder object and insert the data into the database.
class CheckOutOrder():
    def __init__(self, customer_id, deliver_date, comment, order_items):
        self.customer_id = customer_id
        self.deliver_date = deliver_date
        self.comment = comment
        self.order_items = order_items
    def insert(self):
        new_order = Order(customer_id=self.customer_id, deliver_date=self.deliver_date, comment=self.comment)
        # new_order.insert()
        for each_order_item in self.order_items:
            order_item = OrderItem(order_id=new_order.id, product_id=each_order_item['product_id'], quantity=each_order_item['quantity'])
            order_item.order = new_order
            order_item.insert()
        return new_order.format()
    def format(self):
        return {'customer_id': self.customer_id, 'deliver_date': self.deliver_date, 'comment': self.comment, 'order_items': self.order_items}
    def __repr__(self):
        return json.dumps(self.format())

# class CheckOutOrderItem():
#     def __init__(self, product_id, quantity):
#         self.product_id = product_id
#         self.quantity = quantity
#     def format(self):
#         return {'product_id': self.product_id, 'quantity': self.quantity}
#     def __repr__(self):
#         return json.dumps(self.format())