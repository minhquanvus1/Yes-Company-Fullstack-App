import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import db,  Customer, OrderItem, Product, Order
from auth import AuthError
from config import test_config
load_dotenv()

# TEST_DB_USERNAME = os.getenv('TEST_DB_USERNAME')
# TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
# TEST_DB_HOST = os.getenv('TEST_DB_HOST')
# TEST_DB_PORT = os.getenv('TEST_DB_PORT')
# TEST_DB_NAME = os.getenv('TEST_DB_NAME')

class YesCompanyTest(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        # self.database_path =f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
        # self.app = create_app({
        #     "SQLALCHEMY_DATABASE_URI": self.database_path,
        #     "SQLALCHEMY_TRACK_MODIFICATIONS": False}
        # )
        self.customer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRjNE5WN1pyeUppemVKdW5wblI0MyJ9.eyJpc3MiOiJodHRwczovL2Rldi10aW9pNGJuZmlzYzZiY2xpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYxOTgzMTY3OTE3MzcxMTA4NyIsImF1ZCI6Imh0dHBzOi8veWVzQ29tcGFueS9hcGkiLCJpYXQiOjE3MTA3NDg5MzksImV4cCI6MTcxMDc1NjEzOSwic2NvcGUiOiIiLCJhenAiOiJYREJEOGN5VDl1WVlnUVpqaEJHSVEzekF3UWF5Q29PSCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpvcmRlcnMiLCJkZWxldGU6cHJvZHVjdHMiLCJnZXQ6Y3VzdG9tZXJzIiwiZ2V0Om9yZGVycyIsImdldDpvcmRlcnNCeUN1c3RvbWVySWQiLCJnZXQ6b3JkZXJzLWJ5LWRhdGUiLCJnZXQ6cHJvZHVjdHMiLCJwYXRjaDpvcmRlcnMiLCJwYXRjaDpwcm9kdWN0cyIsInBvc3Q6b3JkZXJzIiwicG9zdDpwcm9kdWN0cyIsInNlYXJjaDpjdXN0b21lcnMiLCJzZWFyY2g6cHJvZHVjdHMiXX0.KescLJH9vcUI8ch4wJT_O49bN-ZFUPBfFMTOdXCxexDbnV-u6sVYj9BGyu9fjF29Ih41WbUkXiyeiyBAwcYAJdMcQmEt51v3NqDNs5sLMGHXolN_JObvmYEs2rvIyeop1h9JkahWBknBAQBoZoWyQULAq4_RTP9uM5a3mZlHMIBsfkukpqSxdz83RLWTgBKYcJrkNCeAjzN-Xsd5bs5B2G9dCykHIh2GZs6s8711VOnCEbrMxYg5rVJkJDTAlRkRPgxJhyBgxgjiwXVN3YJAl8Bgh5eCnyRYwbewqY4ke-n3msuKH2L4rnrwCMEyANWUhnlfLuOOar0MvfTaXJyMYQ'
        self.app = create_app(test_config)
        self.customer = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'subject': 'google OAuth2 | John haha'
        }
        self.product = {
            'name': 'iPhone 12',
            'unit_price': 1000,
            'description': 'Apple iPhone 12'
        }
        self.order = {
            'customer_id': 1,
            'comment': 'This is a test order',
            'deliver_date': '2024-03-17 15:30:00'
        }
        self.order_item = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 2
        }
        self.client = self.app.test_client
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(Customer(**self.customer))
            db.session.add(Product(**self.product))
            db.session.commit()
    def tearDown(self):
        """Executed after reach test"""
        # with self.app.app_context():
        #     db.session.rollback()
        #     db.session.remove()
        #     db.drop_all()
    # def tearDown(self):
    #     """Executed after reach test"""
    #     # pass
    #     with self.app.app_context():
    #         # self.db.session.remove()
    #         # self.db.drop_all()
    #         # self.db.create_all()
    #         # self.db.session.commit()
    #         # Remove the session (commit any remaining changes first)
    #         self.db.session.rollback()
    #         self.db.session.remove()
    #         # Drop all tables
    #         self.db.drop_all()
            
            
    def test_get_hello(self):
        res = self.client().get('/hello')
        data = json.loads(res.data)
        print(data)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Hello World!')
        self.assertIsInstance(data['message'], str)
        self.assertEqual(res.status_code, 200)
            
    def test_get_customers_with_expired_token(self):
        res = self.client().get('/customers', headers={'Authorization': self.customer_token})
        print(res)
        print(type(res))
        print(res.data)
        print(type(res.data))
        data = json.loads(res.data)
        print(data)
        print(type(data))
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        # self.assertTrue(data['customers'])
        # self.assertIsInstance(data['customers'], list)
        # for each_customer in data['customers']:
        #     self.assertIsInstance(each_customer, dict)
        # self.assertRaises(AuthError, self.client.get('/customers'))
    
    def test_get_products(self):
        res = self.client().get('/products')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['products'])
        self.assertIsInstance(data['products'], list)
        for each_product in data['products']:
            self.assertIsInstance(each_product, dict)

        

if __name__ == "__main__":
    unittest.main()