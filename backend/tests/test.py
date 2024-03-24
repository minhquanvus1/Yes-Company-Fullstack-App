import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import db,  Customer, OrderItem, Product, Order
from config import test_config
from sqlalchemy import text, create_engine
from sqlalchemy.orm.session import close_all_sessions
load_dotenv()

# TEST_DB_USERNAME = os.getenv('TEST_DB_USERNAME')
# TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
# TEST_DB_HOST = os.getenv('TEST_DB_HOST')
# TEST_DB_PORT = os.getenv('TEST_DB_PORT')
# TEST_DB_NAME = os.getenv('TEST_DB_NAME')

class YesCompanyTest(unittest.TestCase):
    # engine = create_engine(f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}')

    def setUp(self):
        """Define test variables and initialize app."""
        # self.database_path =f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
        # self.app = create_app({
        #     "SQLALCHEMY_DATABASE_URI": self.database_path,
        #     "SQLALCHEMY_TRACK_MODIFICATIONS": False}
        # )
        self.manager_token_expired = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRjNE5WN1pyeUppemVKdW5wblI0MyJ9.eyJpc3MiOiJodHRwczovL2Rldi10aW9pNGJuZmlzYzZiY2xpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYxOTgzMTY3OTE3MzcxMTA4NyIsImF1ZCI6Imh0dHBzOi8veWVzQ29tcGFueS9hcGkiLCJpYXQiOjE3MTA3NDg5MzksImV4cCI6MTcxMDc1NjEzOSwic2NvcGUiOiIiLCJhenAiOiJYREJEOGN5VDl1WVlnUVpqaEJHSVEzekF3UWF5Q29PSCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpvcmRlcnMiLCJkZWxldGU6cHJvZHVjdHMiLCJnZXQ6Y3VzdG9tZXJzIiwiZ2V0Om9yZGVycyIsImdldDpvcmRlcnNCeUN1c3RvbWVySWQiLCJnZXQ6b3JkZXJzLWJ5LWRhdGUiLCJnZXQ6cHJvZHVjdHMiLCJwYXRjaDpvcmRlcnMiLCJwYXRjaDpwcm9kdWN0cyIsInBvc3Q6b3JkZXJzIiwicG9zdDpwcm9kdWN0cyIsInNlYXJjaDpjdXN0b21lcnMiLCJzZWFyY2g6cHJvZHVjdHMiXX0.KescLJH9vcUI8ch4wJT_O49bN-ZFUPBfFMTOdXCxexDbnV-u6sVYj9BGyu9fjF29Ih41WbUkXiyeiyBAwcYAJdMcQmEt51v3NqDNs5sLMGHXolN_JObvmYEs2rvIyeop1h9JkahWBknBAQBoZoWyQULAq4_RTP9uM5a3mZlHMIBsfkukpqSxdz83RLWTgBKYcJrkNCeAjzN-Xsd5bs5B2G9dCykHIh2GZs6s8711VOnCEbrMxYg5rVJkJDTAlRkRPgxJhyBgxgjiwXVN3YJAl8Bgh5eCnyRYwbewqY4ke-n3msuKH2L4rnrwCMEyANWUhnlfLuOOar0MvfTaXJyMYQ'
        self.manager_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRjNE5WN1pyeUppemVKdW5wblI0MyJ9.eyJpc3MiOiJodHRwczovL2Rldi10aW9pNGJuZmlzYzZiY2xpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYxOTgzMTY3OTE3MzcxMTA4NyIsImF1ZCI6WyJodHRwczovL3llc0NvbXBhbnkvYXBpIiwiaHR0cHM6Ly9kZXYtdGlvaTRibmZpc2M2YmNsaS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzExMjkxMjU5LCJleHAiOjE3MTEzNzc2NTksInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYREJEOGN5VDl1WVlnUVpqaEJHSVEzekF3UWF5Q29PSCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpvcmRlcnMiLCJkZWxldGU6cHJvZHVjdHMiLCJnZXQ6Y3VzdG9tZXJCeUlkIiwiZ2V0OmN1c3RvbWVycyIsImdldDpvcmRlcnMiLCJnZXQ6b3JkZXJzQnlDdXN0b21lcklkIiwiZ2V0Om9yZGVycy1ieS1kYXRlIiwiZ2V0OnByb2R1Y3RCeUlkIiwiZ2V0OnByb2R1Y3RzIiwicGF0Y2g6b3JkZXJzIiwicGF0Y2g6cHJvZHVjdHMiLCJwb3N0Om9yZGVycyIsInBvc3Q6cHJvZHVjdHMiLCJzZWFyY2g6Y3VzdG9tZXJzIiwic2VhcmNoOnByb2R1Y3RzIl19.VX-et7AHNW_zYERtWomIBph9EcBxnJGzrlyeis-ez9bV4PQi51NzdbT1fD0NiQva7b-ZYTX2ehyQmLzbiIYCIbmg7abOFh7PkR-QmXpIQ8dglGVb0w-wBV_60DWuh9qanbGaJuhVYGfz4HUhJokQKprPRgnV2bv3S2p18WCmUrlyD-gNpvbJ88wk5uYVPHybDIW80w8soKk5z2bE7Vrzud8aZzI-D-IzSEg-Mq2_JPAMDUTCGssXk782Fu3xtuKIMJ6c9BoRtR6NZgbXtfvlsDT4KwrmrC4c5XGxYMsOLPA9joSpPSOFWylq_Mk3nKhpKXFgv1lFw2xxOMiN4DaBDA'
        self.customer_token_for_add_non_exist_customer = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRjNE5WN1pyeUppemVKdW5wblI0MyJ9.eyJpc3MiOiJodHRwczovL2Rldi10aW9pNGJuZmlzYzZiY2xpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWZhOGM1MmI1NDM2YzljOTI3M2JhNWUiLCJhdWQiOlsiaHR0cHM6Ly95ZXNDb21wYW55L2FwaSIsImh0dHBzOi8vZGV2LXRpb2k0Ym5maXNjNmJjbGkudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcxMTI5MTMzNSwiZXhwIjoxNzExMzc3NzM1LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoiWERCRDhjeVQ5dVlZZ1FaamhCR0lRM3pBd1FheUNvT0giLCJwZXJtaXNzaW9ucyI6WyJjaGVjazpjdXN0b21lcnMiLCJkZWxldGU6b3JkZXJzIiwiZ2V0Om9yZGVyc0J5Q3VzdG9tZXJJZCIsImdldDpwcm9kdWN0cyIsInBhdGNoOm9yZGVycyIsInBvc3Q6Y3VzdG9tZXJzIiwicG9zdDpvcmRlcnMiLCJzZWFyY2g6cHJvZHVjdHMiXX0.H73UnhwsbsgKzRV6w9t011hRyhYLeEdpcZukKVgq29A8e7eoquFmqmLF-U99RqQCkDGfx-WG-E344q6D9sIP6h4BfTUOX61LjJlNtaqTiAqxhCzEYxRDelbESXMqPmsTybtSWi0cwXrHLLQPO5kN0gcrs3zqOBBPhKFF99v9A7fz7YT3wx-Rh1Ah03u4dHZFWiZk_CO9HhQxgMU7dUVWZ_-T-OGK3o6jMRxy4KGrCygcJoxiT5qRTMaVtAvV_tAIjhGY7OLOTwdLqYRIbBwPKnQcGeuEipaFP5UM1V1q-0USww69GMP8Y_5qXiyUrgOSyn7iC4WC6j43peW3g5xjrg'
        self.customer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRjNE5WN1pyeUppemVKdW5wblI0MyJ9.eyJpc3MiOiJodHRwczovL2Rldi10aW9pNGJuZmlzYzZiY2xpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMTQ3NDYwODQ4NTc3ODk1OTE5OSIsImF1ZCI6WyJodHRwczovL3llc0NvbXBhbnkvYXBpIiwiaHR0cHM6Ly9kZXYtdGlvaTRibmZpc2M2YmNsaS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzExMjkxMjk5LCJleHAiOjE3MTEzNzc2OTksInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYREJEOGN5VDl1WVlnUVpqaEJHSVEzekF3UWF5Q29PSCIsInBlcm1pc3Npb25zIjpbImNoZWNrOmN1c3RvbWVycyIsImRlbGV0ZTpvcmRlcnMiLCJnZXQ6b3JkZXJzQnlDdXN0b21lcklkIiwiZ2V0OnByb2R1Y3RzIiwicGF0Y2g6b3JkZXJzIiwicG9zdDpjdXN0b21lcnMiLCJwb3N0Om9yZGVycyIsInNlYXJjaDpwcm9kdWN0cyJdfQ.IQPO2Fd2uBalcZba3MB_eqgVtEG6z9JvYPhO5tp9sTmiMpqMn_bYJKtUQj68cRxItKFSTn0Ch1a0XCnzdH1E6jq8YBmPHoz5B38O09uRHJYMqA4hhcFDi6pJFGrHb6OKjC5j-3xkaCfSzzdZ5-WOQhq0swbldRV64bheAZ8tXs_mu5t7dMr4y7c7wteNPJF7RrBunGU-CoWsuuElyYllr_MwBpcX9DdtulZEvC-a5lUTLNJa3JKLvs_IkDwf36L6gmZw8so1u7KvvdpOEHmQdk74JMxuw7Bwgkcwrk6IfjsiOA_hroZyLvyT0OhloUofPcRMADL4XMoAAZy_BI8sfw'
        self.app = create_app(test_config)
        self.customer = {
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "subject": "google-oauth2|111474608485778959199"
        }
        self.product = {
            "name": "iPhone 12",
            "unit_price": 1000,
            "description": "Apple iPhone 12"
        }
        self.product_1 = {
            "name": "iPhone 13",
            "unit_price": 12000,
            "description": "Apple iPhone 13"
        }
        self.order = {
            "customer_id": 1,
            "comment": "This is a test order",
            "deliver_date": "2024-03-17 15:30:00"
        }
        self.order_item = {
            "order_id": 1,
            "product_id": 1,
            "quantity": 2
        }
        #----- Objects to be added to test db tables, by API endpoint
        self.customer_add = {
            "first_name": "Donald",
            "last_name": "Trump",
            "address": "456 New York St"
        }
        self.product_add = {
            "name": "Guitar",
            "unit_price": 100,
            "description": "This is a test fingerstyle guitar"
        }
        self.order_add = {
            "customer_id": 1,
            "comment": "This is a test order to add",
            "deliver_date": "2024-03-20 15:30:00",
            "order_items": [
                {
                    "product_id": 1,
                    "quantity": 2
                },
                {
                    "product_id": 2,
                    "quantity": 3
                }
            ]
        }
        self.order_add_with_product_does_not_exist = {
            "customer_id": 1,
            "comment": "This is a test order to add",
            "deliver_date": "2024-03-20 15:30:00",
            "order_items": [
                {
                    "product_id": 1,
                    "quantity": 2
                },
                {
                    "product_id": 10,
                    "quantity": 3
                }
            ]
        }
        self.order_item_add = {
            "order_id": 1,
            "product_id": 1,
            "quantity": 5
        }
        self.client = self.app.test_client
        with self.app.app_context():
            # db.session.execute(text('truncate table "Product" cascade'))
            # db.session.execute(text('truncate table "Order" cascade'))
            # db.session.execute(text('truncate table "Customer" cascade'))
            # db.session.commit()
            # close_all_sessions()
            # db.drop_all()
            db.create_all()
            # if len(db.session.query(Customer).all()) == 0:
            #     db.session.add(Customer(**self.customer))
            # if len(db.session.query(Product).all()) == 0:
            #     db.session.add(Product(**self.product))
            #     db.session.add(Product(**self.product_1))
            # if len(db.session.query(Order).all()) == 0:
            #     db.session.add(Order(**self.order))
            # if len(db.session.query(OrderItem).all()) == 0:
            #     db.session.add(OrderItem(**self.order_item))
            # db.session.commit()
            db.session.add(Customer(**self.customer))
            db.session.add(Product(**self.product))
            db.session.add(Product(**self.product_1))
            db.session.add(Order(**self.order))
            db.session.add(OrderItem(**self.order_item))
            db.session.commit()
    def tearDown(self):
        # engine = create_engine(f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}')

        """Executed after each test"""
        print('tearDown: starting...')
        with self.app.app_context():
            print('tearDown: inside app context')
            try:
                print('tearDown: dropping all tables...')
                # db.session.execute('truncate table "Product" cascade')
                # db.session.execute('truncate table "Order" cascade')
                # db.session.execute('truncate table "Customer" cascade')
                # db.session.execute(text('truncate table "Product" cascade'))
                # db.session.execute(text('truncate table "Order" cascade'))
                # db.session.execute(text('truncate table "Customer" cascade'))
                # with engine.connect() as conn:
                #     conn.execute('truncate table "Product" cascade')
                #     conn.execute('truncate table "Order" cascade')
                #     conn.execute('truncate table "Customer" cascade')
                close_all_sessions()
                # db.session.remove()
                db.drop_all()
                print('tearDown: tables dropped successfully')
            except Exception as e:
                print('tearDown: Error dropping tables:', e)
            finally:
                print('tearDown: removing session...')
                # db.session.remove()
                print('tearDown: session removed')
        """Executed after reach test"""
        # print('teardown')
        # with self.app.app_context():
        #     print('inside teardown')
        #     # db.session.rollback()
        #     # db.session.remove()
        #     db.drop_all()

            
    def test_get_hello(self):
        res = self.client().get('/hello')
        data = json.loads(res.data)
        print(data)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Hello World!')
        self.assertIsInstance(data['message'], str)
        self.assertEqual(res.status_code, 200)
 
 # -------------------- Test for GET /customers --------------------           
    def test_get_customers_with_expired_token(self):
        res = self.client().get('/customers', headers={'Authorization': self.manager_token_expired})
        print(res)
        print(type(res)) # <class 'flask.wrappers.Response'>
        print(res.data) # b'{"code":"token_expired","description":"Token is expired."}\n's
        print(type(res.data)) # <class 'bytes'>
        data = json.loads(res.data) # {'code': 'token_expired', 'description': 'Token is expired.'}
        print(data)
        print(type(data)) # <class 'dict'>
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
    
    def test_for_successful_get_customers_with_manager_role(self):
        res = self.client().get('/customers', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['customers'])
        self.assertIsInstance(data['customers'], list)
        for each_customer in data['customers']:
            self.assertIsInstance(each_customer, dict)
    
    def test_get_customers_without_Authorization_header(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_get_customers_with_customer_role_returns_403_forbidden_error(self):
        res = self.client().get('/customers', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(data['error'] == 403)
    
#--------------------- Test for GET /products --------------------
    def test_get_products_without_Authorization_header(self):
        res = self.client().get('/products')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)

    def test_get_products_with_expired_token(self):
        res = self.client().get('/products', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_get_products_successfully_with_manager_role(self):
        res = self.client().get('/products', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['products'])
        self.assertIsInstance(data['products'], list)
        for each_product in data['products']:
            self.assertIsInstance(each_product, dict)
    
    def test_get_products_successfully_with_customer_role(self):
        res = self.client().get('/products', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['products'])
        self.assertIsInstance(data['products'], list)
        for each_product in data['products']:
            self.assertIsInstance(each_product, dict)
        
#------------------------ Test for GET /orders --------------------

    def test_get_orders_without_Authorization_header(self):
        res = self.client().get('/orders')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_get_orders_with_expired_token(self):
        res = self.client().get('/orders', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_get_all_orders_of_all_customers_successfully_with_manager_role(self):
        res = self.client().get('/orders', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])
        self.assertIsInstance(data['orders'], list)
        for each_order in data['orders']:
            self.assertIsInstance(each_order, dict)
            
    def test_get_all_orders_of_all_customers_with_customer_role_return_403_forbidden_error(self):
        res = self.client().get('/orders', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(data['error'] == 403)

#------------------------ Test for GET /orders-by-date --------------------

    def test_get_orders_by_date_without_Authorization_header(self):
        res = self.client().get('/orders-by-date')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_get_orders_by_date_with_expired_token(self):
        res = self.client().get('/orders-by-date', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_get_orders_by_date_with_not_correct_query_parameter_key(self):
        res = self.client().get('/orders-by-date?date=2024-03-17 15:30:00', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The deliver_date parameter must be provided in the request query string')
    
    def test_get_orders_by_date_with_the_date_not_in_correct_format(self):
        res = self.client().get('/orders-by-date?deliver_date=20 24 03 17 15:30:00', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The deliver_date must have the string value of a valid date and time format (YYYY-MM-DD HH:MM:SS)')
    
    def test_get_orders_by_date_successfully_with_manager_role(self):
        res = self.client().get('/orders-by-date?deliver_date=2024-03-17 15:30:00', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])
        self.assertIsInstance(data['orders'], list)
        for each_order in data['orders']:
            self.assertIsInstance(each_order, dict)
            
#------------------------ Test for POST /customers --------------------

    def test_create_customer_without_Authorization_header(self):
        res = self.client().post('/customers', json=self.customer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_create_customer_with_expired_token(self):
        res = self.client().post('/customers', json=self.customer, headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_create_customer_with_manager_role_which_does_not_have_this_permission(self):
        res = self.client().post('/customers', json=self.customer, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(data['error'] == 403)
    
    def test_create_customer_successful_with_customer_role(self):
        res = self.client().post('/customers', json=self.customer_add, headers={'Authorization': self.customer_token_for_add_non_exist_customer})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['customer'])
    
    def test_create_customer_that_already_exists(self):
        res = self.client().post('/customers', json={"first_name": "John", "last_name": "Doe", "address": "123 Main St"}, headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['message'], 'Customer already exists')
        self.assertIsInstance(data['customer'], dict)
        
#------------------------ Test for POST /products --------------------

    def test_create_product_without_Authorization_header(self):
        res = self.client().post('/products', json=self.product)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_create_product_with_expired_token(self):
        res = self.client().post('/products', json=self.product, headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_create_product_successful_with_manager_role(self):
        res = self.client().post('/products', json=self.product_add, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['product'])
    
    def test_create_a_product_that_already_exists(self):
        res = self.client().post('/products', json=self.product, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The product with the given name already exists')
        self.assertTrue(data['error'] == 409)
    
    def test_create_a_product_with_customer_role_returns_403_forbidden_error(self):
        res = self.client().post('/products', json=self.product, headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(data['error'] == 403)
    
#------------------ Test for POST /search-products --------------------

    def test_searching_for_products_without_Authorization_header(self):
        res = self.client().post('/search-products', json={'name': 'iPhone 12'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_searching_for_products_with_expired_token(self):
        res = self.client().post('/search-products', json={'name': 'iPhone 12'}, headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_searching_for_products_with_invalid_request_body(self):
        res = self.client().post('/search-products', json={'nam': '', 'age': 20}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Only 'name' is allowed in the request body")
    
    def test_searching_for_products_successful(self):
        res = self.client().post('/search-products', json={"name": "iPhone 12"}, headers={"Authorization": self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['products']) # a List with >= 1 element in it is True (bool([2]) is True) (bool([]) is False)
        self.assertIsInstance(data['products'], list)
        for each_product in data['products']:
            self.assertIsInstance(each_product, dict)
    
    def test_searching_for_product_that_does_not_exist(self):
        res = self.client().post('/search-products', json={'name': 'iPhone 14'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue('products' in data)
        # self.assertFalse(data['products']) # a List with no element in it is False (bool([]) is False)
        self.assertEqual(data['products'], [])
        self.assertEqual(data['message'], 'No product found with the given name')

#------------------- Test for GET /customers/<int:id> --------------------
    def test_for_getting_customer_by_id_without_Authorization_header(self):
        res = self.client().get('/customers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_getting_customer_by_id_with_expired_token(self):
        res = self.client().get('/customers/1', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_getting_customer_by_id_that_does_not_exist(self):
        res = self.client().get('/customers/100', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The customer with the given id is not found')
        self.assertTrue(data['error'] == 404)
    
    def test_for_getting_customer_by_id_successfully(self):
        res = self.client().get('/customers/1', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['customer'])
        self.assertIsInstance(data['customer'], dict)

#-------------------- Test for POST /search-customers --------------------

    def test_for_searching_customers_without_Authorization_header(self):
        res = self.client().post('/search-customers', json={'first_name': 'John'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_searching_customers_with_expired_token(self):
        print('inside expired')
        res = self.client().post('/search-customers', json={'first_name': 'John'}, headers={'Authorization': self.manager_token_expired})
        print('inside expired 2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
        # print('inside expired')
    
    def test_for_searching_customers_with_invalid_request_body(self):
        res = self.client().post('/search-customers', json={'firstName': 'John', 'age': 20}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Only first_name and last_name are allowed in the request body")
    
    def test_for_searching_customer_that_does_not_exist(self):
        res = self.client().post('/search-customers', json={'first_name': 'Skibidi', 'last_name': 'dum dum yes yes'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'No customer found with the given first_name and last_name')
        self.assertEqual(data['customers'], [])
        print('end test')
    
    def test_for_searching_customer_successfully_with_manager_role(self):
        res = self.client().post('/search-customers', json={"first_name": "John", "last_name": "Doe"}, headers={"Authorization": self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['customers'])
        self.assertIsInstance(data['customers'], list)
        for each_customer in data['customers']:
            self.assertIsInstance(each_customer, dict)
            
#------------------ Test for GET /products/<int:id> --------------------

    def test_for_getting_product_without_Authorization_header(self):
        res = self.client().get('/products/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_getting_product_with_expired_token(self):
        res = self.client().get('/products/1', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_getting_product_by_id_that_does_not_exist(self):
        res = self.client().get('/products/100', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The product with the given id is not found')
        self.assertTrue(data['error'] == 404)
    
    def test_for_getting_product_by_id_successfully(self):
        res = self.client().get('/products/1', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['product'])
        self.assertIsInstance(data['product'], dict)

#------------------ Test for PATCH /products/<int:id> --------------------

    def test_for_updating_product_without_Authorization_header(self):
        res = self.client().patch('/products/1', json={'name': 'iPhone 13'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_updating_product_with_expired_token(self):
        res = self.client().patch('/products/1', json={'name': 'iPhone 13'}, headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_updating_product_that_does_not_exist(self):
        res = self.client().patch('/products/100', json={'name': 'iPhone 13'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The product with the given id is not found')
        self.assertTrue(data['error'] == 404)
    
    def test_for_updating_product_with_the_name_of_an_existing_product(self):
        res = self.client().patch('/products/1', json={'name': 'iPhone 13'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The product with the given name already exists')
        self.assertTrue(data['error'] == 409)

    def test_for_updating_product_successfully(self):
        res = self.client().patch('/products/1', json={'name': 'iPhone 15'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['product'])
        self.assertEqual(data['product']['name'], 'iPhone 15')

#------------------ Test for DELETE /products/<int:id> --------------------

    def test_for_deleting_product_without_Authorization_header(self):
        res = self.client().delete('/products/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_deleting_product_with_expired_token(self):
        res = self.client().delete('/products/1', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_deleting_product_that_does_not_exist(self):
        res = self.client().delete('/products/100', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The product with the given id is not found')
        self.assertTrue(data['error'] == 404)

    def test_for_deleting_product_successfully(self):
        res = self.client().delete('/products/1', headers={'Authorization': self.manager_token})
        if not res.data:
            print('res.data is empty')
            print(res.data)
            print(type(res.data))
            self.assertEqual(res.status_code, 200)
        else:
            print('res.data is not empty')
            print(res.data)
            data = json.loads(res.data)
            self.assertTrue(data['deleted'])
            self.assertTrue(data['deleted'] == 1)
            self.assertEqual(res.status_code, 200)
        
#-------------- Test for DELETE /orders/<int:id> --------------------

    def test_for_deleting_order_without_Authorization_header(self):
        res = self.client().delete('/orders/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_deleting_order_with_expired_token(self):
        res = self.client().delete('/orders/1', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_deleting_order_that_does_not_exist(self):
        res = self.client().delete('/orders/100', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The order with the given id is not found')
        self.assertTrue(data['error'] == 404)
    
    def test_for_deleting_order_successfully(self):
        res = self.client().delete('/orders/1', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], 1)

#---------------- Test for GET /check-customer -----------------

    def test_for_check_customer_without_Authorization_header(self):
        res = self.client().get('/check-customer')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_check_customer_with_expired_token(self):
        res = self.client().get('/check-customer', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_check_customer_with_invalid_role_manager(self):
        res = self.client().get('/check-customer', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(data['error'] == 403)
    
    def test_for_check_customer_successfully(self):
        res = self.client().get('/check-customer', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['customer'])
        self.assertIsInstance(data['customer'], dict)
        
    def test_for_check_customer_that_does_not_exist_in_database(self):
        res = self.client().get('/check-customer', headers={'Authorization': self.customer_token_for_add_non_exist_customer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Customer not found, please create a customer account')
    
#---------------- Test for GET /customers/<int:id>/orders -----------------
    def test_for_getting_orders_of_customer_without_Authorization_header(self):
        res = self.client().get('/customers/1/orders')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_getting_orders_of_customer_with_expired_token(self):
        res = self.client().get('/customers/1/orders', headers={'Authorization': self.manager_token_expired})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_getting_orders_of_customer_that_has_not_made_any_order_yet(self):
        res = self.client().get('/customers/2/orders', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'This Customer with this id has no order yet')
        self.assertTrue(data['error'] == 404)
    
    def test_for_getting_orders_of_customer_successfully(self):
        res = self.client().get('/customers/1/orders', headers={'Authorization': self.customer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])
        self.assertIsInstance(data['orders'], list)
        for each_order in data['orders']:
            self.assertIsInstance(each_order, dict)

#---------------- Test for PATCH /orders/<int:id> -----------------

    def test_for_updating_order_without_Authorization_header(self):
        res = self.client().patch('/orders/1', json={'comment': 'This is a test order to update'})
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_updating_order_with_expired_token(self):
        res = self.client().patch('/orders/1', json={'comment': 'This is a test order to update'}, headers={'Authorization': self.manager_token_expired})
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_updating_customer_id_in_an_order(self):
        res = self.client().patch('/orders/1', json={'customer_id': 2}, headers={'Authorization': self.manager_token})
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The customer_id cannot be updated')
        self.assertTrue(data['error'] == 422)
    
    def test_for_updating_deliver_date_of_an_order_but_with_invalid_deliver_date_format(self):
        res = self.client().patch('/orders/1', json={'deliver_date': '2024.03.17 15-30-00'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The deliver_date must have the string value of a valid date and time format (YYYY-MM-DD HH:MM:SS)')
        self.assertTrue(data['error'] == 400)
    
    def test_for_updating_order_that_does_not_exist(self):
        res = self.client().patch('/orders/100', json={'comment': 'This is a test order to update'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The order with the given id is not found')
        self.assertTrue(data['error'] == 404)
    
    def test_for_successfully_updating_an_order(self):
        res = self.client().patch('/orders/1', json={'comment': 'This is a test order to update'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['order'])
        self.assertEqual(data['order']['comment'], 'This is a test order to update')
    
    def test_for_updating_order_with_deliver_date_in_the_past(self):
        res = self.client().patch('/orders/1', json={'deliver_date': '2020-03-17 15:30:00'}, headers={'Authorization': self.manager_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The deliver_date must be a future date and time')
        self.assertTrue(data['error'] == 422)

# -------------------- Test for POST /orders --------------------
    def test_for_creating_order_without_Authorization_header(self):
        res = self.client().post('/orders', json=self.order_add)
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_creating_order_with_expired_token(self):
        res = self.client().post('/orders', json=self.order_add, headers={'Authorization': self.manager_token_expired})
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Token is expired.')
        self.assertTrue(data['error'] == 401)
    
    def test_for_creating_order_with_invalid_request_body(self):
        res = self.client().post('/orders', json={'customer_id': 1, 'comment': 'This is a test order to add'}, headers={'Authorization': self.manager_token})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'customer_id, deliver_date, comment, order_items and quantity are required in the request body')
        self.assertTrue(data['error'] == 400)
    
    def test_for_creating_order_successfully_with_customer_role(self):
        res = self.client().post('/orders', json=self.order_add, headers={'Authorization': self.customer_token})
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertTrue(data['order'])
        print('order created: ', data['order'])
    
    def test_for_creating_order_that_has_product_does_not_exist_return_400_error(self):
        res = self.client().post('/orders', json=self.order_add_with_product_does_not_exist, headers={'Authorization': self.customer_token})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The product with the given id is not found')
        self.assertTrue(data['error'] == 400)
        
if __name__ == "__main__":
    unittest.main()