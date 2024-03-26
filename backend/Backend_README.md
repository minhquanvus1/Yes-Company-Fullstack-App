# YES-Company App (Backend)

- This is the fantastic app for YES Company, which is a company that sells products, especially the Bottles of Drinking Water.

- Before the advent of this app, the Manager of this company has to manually keep track, and try to remember all of the orders (including: all the order items in 1 Order and their corresponding quantity, total price, and on what date, at what time the customer requires the order to be delivered...) of all the customers, who make the orders by phone call. This is a very time-consuming and error-prone process, because the company is expanding at a very fast pace, and the number of customers is increasing day by day, so are their orders. Therefore, memorizing all the orders of all the customers is not quite a small task at all. On top of that, listening to phone calls continuously in a day is quite a headache for the Manager. Because of this, the Manager is not able to focus on other important tasks, which are also important for the company's growth.

- To solve this problem, the Manager wants to have an app that can handle these tasks automatically. So at the end of every day, the Manager just needs to check the app, and he will get all the details of all the orders of all the customers, who made the orders on the next day. This will save a lot of time for the Manager, and he can focus on other important tasks, which are also important for the company's growth.

- With the advent of this app, this app can help the Manager to get out of all this headache. This app allows users to register to be the company's customer, and make their order online, keep track of all their orders, total price, and deliver date. And Manager can see the Customer details (including their delivering address) and see all of the orders, with the quantity of each order item so that he knows how many bottles of drinking water he needs to deliver to the customers on the next day, as well as manage the orders.

- For the Backend, the app uses: Python Flask, SQLAlchemy, and PostgreSQL for the database.

All the backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisite and Local Development

- Developers should already have Python 3, pip and node installed on their local machines.
- For database, we use PostgreSQL. You can download it from [here](https://www.postgresql.org/download/).

#### Backend

To follow the best practice when working on a Python project, we will create a virtual environment for our project. This will keep your dependencies for this project separate from other projects.

```bash
# Windows users
cd backend
python -m venv venv
env\Scripts\activate
```

After creating the virtual environment, we need to change the Python Interpreter to the virtual environment that we just created, by clicking on the Python Interpreter at the bottom left corner of the VS Code, and select the virtual environment that we just created (by entering the PATH to the venv/ folder we have just created).

- **Install Dependencies**

```bash
pip install -r requirements.txt
```

- For the local database setup, this app uses 2 separate databases, 1 for Development, and the other one for Testing.
- The credentials of these 2 databases are stored in .env file (which is not included in the repository for security reasons), and load into the app in the config.py file. You can create your own .env file and store the credentials of your own databases (you can create 2 separate local databases yourself), and add their credentials to a .env file in this format:

```bash
# production database credentials
DB_USERNAME=YOUR_DB_USERNAME
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=localhost
DB_NAME=YOUR_DB_NAME
DB_PORT=YOUR_DB_PORT


# test database credentials
TEST_DB_USERNAME = YOUR_TEST_DB_USERNAME
TEST_DB_PASSWORD = YOUR_TEST_DB_PASSWORD
TEST_DB_HOST = localhost
TEST_DB_PORT = YOUR_TEST_DB_PORT
TEST_DB_NAME = YOUR_TEST_DB_NAME
```

- Then, after creating the local databases, and add their credentials to the .env file, you need to use flask-migrate to create the tables in the databases. You can do this by running the following commands:

```bash
cd backend
flask db migrate
flask db upgrade
```

- So after creating the virtualenv, install the dependencies into this virtualenv, and create the local databases, you can run the app by running the following command:

```bash
cd backend
export FLASK_APP=app
flask run --port=8080 --reload
```

The backend Flask application will run on `http://127.0.0.1:8080/` by default and is a proxy in the frontend configuration.

----- That is all for setting up the Backend to run the Backend of the app

## Testing

- For Testing, this app uses the unittest library in Python.
- All of these tests are run against the Testing database, which will automatically clean up after each test
- All of these tests require the JWT of the Manager, Customer to be able to run successfully (which I have already added in it).
- To run the tests, you can run the following command:

```bash
cd backend
python -m unittest -v tests/test.py
```

## Backend Folder Structure

- The Backend Flask has the following structure:

  - `backend/` folder: Contains all the source code of the Backend Flask.
    - `auth.py` file: Contains all the authentication and authorization functionalities of the Backend Flask.
    - `models.py` file: Contains all the models of the Backend Flask.
    - `tests/` folder: Contains all the tests of the Backend Flask.
    - `config.py` file: Contains the database credentials (loaded from .env file) for Development, and Testing
    - `app.py` file: Contains the creation of the Flask app, and the configuration of the Flask app.
  - `migrations/` folder: Contains all the migrations of the Backend Flask.
  - `venv/` folder: Contains the virtual environment of the Backend Flask.
  - `.env` file: Contains the credentials of the local databases.
  - `requirements.txt` file: Contains all the dependencies of the Backend Flask.
  - `production_schema.sql` file: Contains the schema of the Production/Development/Testing database.

## API Reference

### Introduction

- This app has 2 types of users: Manager and Customer, each of them has their own Role, and their own permissions to be able to access resources of certain endpoints, as for Role-based access control (RBAC)
- The JWT access token is required for all endpoints, and we will get this JWT after we log in successfully in the Frontend
  React

### Error Handling

- Errors are returned in JSON format as follows:

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found" // Notice that: there can be Custom Messages for each error
}
```

There are three types of errors:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity
- 409: Conflict
- 500: Internal Server Error

### Endpoints

- I will demonstrate the endpoints for each Role, which are: Customer and Manager

#### Customer

1. GET /check-customer:

   - General:
     - Check if the Authenticated Customer is already registered as a Customer in backend database or not
   - Request Arguments:
     - None
   - Returns:
     - if found: return the custom Customer Dictionary
     - if not found: return 404 error with custom message
   - Sample request:
     - `curl GET http://localhost:8080/check-customer -H "Authorization: Bearer <JWT_of_authenticated_but_not_a_Customer_in_backend database>"`
   - Sample response:
     ```json
     {
       "customer": {
         "address": "Canada",
         "first_name": "Amy",
         "id": 2,
         "last_name": "Nguyen"
       }
     }
     ```

2. POST /customers:
   - General:
     - Register as a Customer in the backend database
   - Request Arguments:
     - first_name: string
     - last_name: string
     - address: string
   - Returns:
     - return the custom Customer Dictionary
   - Sample request:
     - `curl POST http://localhost:8080/customers -H "Authorization: Bearer <JWT_of_authenticated_but_not_a_Customer_in_backend database>" -d '{"first_name": "Amy", "last_name": "Nguyen", "address": "Canada"}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "customer": {
         "address": "Canada",
         "first_name": "Amy",
         "id": 2,
         "last_name": "Nguyen"
       }
     }
     ```
3. POST /orders:
   - General:
     - Make an order
   - Request Arguments:
     - order_items: list of dictionaries, each dictionary contains:
       - product_id: int
       - quantity: int
   - Returns:
     - return the custom Order Dictionary
   - Sample request:
     - `curl POST http://localhost:8080/orders -H "Authorization: Bearer <JWT_of_authenticated_Customer_in_backend database>" -d '{"order_items": [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 3}]}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "order": {
         "customer_id": 2,
         "deliver_date": "2021-09-01 09:00:00",
         "id": 1,
         "order_items": [
           {
             "id": 1,
             "product_id": 1,
             "quantity": 2
           },
           {
             "id": 2,
             "product_id": 2,
             "quantity": 3
           }
         ],
         "total_price": 15.0
       }
     }
     ```

#### Manager

1. GET /customers:
   - General:
     - Get all Customers
   - Request Arguments:
     - None
   - Returns:
     - return the custom Customers Dictionary
   - Sample request:
     - `curl GET http://localhost:8080/customers -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "customers": [
         {
           "address": "Canada",
           "first_name": "Amy",
           "id": 2,
           "last_name": "Nguyen"
         }
       ]
     }
     ```
2. GET /customers/<int:id>
   - General:
     - Get a Customer by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - return the custom Customer Dictionary
   - Sample request:
     - `curl GET http://localhost:8080/customers/2 -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "customer": {
         "address": "Canada",
         "first_name": "Amy",
         "id": 2,
         "last_name": "Nguyen"
       }
     }
     ```
3. POST /search-customers:
   - General:
     - Search for Customers by their first name and/or last name
   - Request Arguments:
     - None
   - Returns:
     - if found: return the custom Customers Dictionary
     - if not found: return 404 error with custom message, and the empty list of Customers
   - Sample request:
     - `curl POST http://localhost:8080/search-customers -H "Authorization: Bearer <JWT_of_authenticated_Manager>" -d '{"first_name": "Amy"}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "customers": [
         {
           "address": "Canada",
           "first_name": "Amy",
           "id": 2,
           "last_name": "Nguyen"
         }
       ]
     }
     ```
4. POST /products
   - General:
     - Add a new Product
   - Request Arguments:
     - None
   - Returns:
     - if the to-be-created Product's name does not exist in the database yet: return the custom Product Dictionary
     - if the to-be-created Product's name already exists in the database: return 409 Conflict error with custom message
   - Sample request:
     - `curl POST http://localhost:8080/products -H "Authorization: Bearer <JWT_of_authenticated_Manager>" -d '{"name": "Crystal Bottle of Drinking Water", "unit_price": 5.0, "description": "Crystal is good for your health"}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "product": {
         "id": 1,
         "name": "Crystal Bottle of Drinking Water",
         "unit_price": 5.0
       }
     }
     ```
5. PATCH /products/<int:id>
   - General:
     - Partially update a Product by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - if found: return the custom Product Dictionary
     - if not found: return 404 error with custom message
   - Sample request:
     - `curl PATCH http://localhost:8080/products/1 -H "Authorization: Bearer <JWT_of_authenticated_Manager>" -d '{"unit_price": 6.0}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "product": {
         "id": 1,
         "name": "Crystal Bottle of Drinking Water",
         "unit_price": 6.0
       }
     }
     ```
6. DELETE /products/<int:id>
   - General:
     - Delete a Product by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - if found: return the deleted Product ID
     - if not found: return 404 error with custom message
   - Sample request:
     - `curl DELETE http://localhost:8080/products/1 -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "deleted": {
         "id": 1
       }
     }
     ```
7. GET /products/<int:id>:
   - General:
     - Get a Product by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - if found: return the custom Product Dictionary
     - if not found: return 404 error with custom message
   - Sample request:
     - `curl GET http://localhost:8080/products/1 -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "product": {
         "id": 1,
         "name": "Crystal Bottle of Drinking Water",
         "unit_price": 6.0
       }
     }
     ```
8. GET /orders:
   - General:
     - Get all Orders
   - Request Arguments:
     - None
   - Returns:
     - return the custom Orders Dictionary
   - Sample request:
     - `curl GET http://localhost:8080/orders -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "orders": [
         {
           "customer_id": 2,
           "deliver_date": "2021-09-01 09:00:00",
           "id": 1,
           "order_items": [
             {
               "id": 1,
               "product_id": 1,
               "quantity": 2
             },
             {
               "id": 2,
               "product_id": 2,
               "quantity": 3
             }
           ],
           "total_price": 15.0
         }
       ]
     }
     ```
9. GET /orders-by-date
   - General:
     - Get all Orders by Deliver Date
   - Request Arguments:
     - None
   - Returns:
     - return the custom Orders Dictionary
   - Sample request:
     - `curl GET http://localhost:8080/orders-by-date -H "Authorization: Bearer <JWT_of_authenticated_Manager> -d '{"deliver_date": "2021-09-01 09:00:00"}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "orders": [
         {
           "customer_id": 2,
           "deliver_date": "2021-09-01 09:00:00",
           "id": 1,
           "order_items": [
             {
               "id": 1,
               "product_id": 1,
               "quantity": 2
             },
             {
               "id": 2,
               "product_id": 2,
               "quantity": 3
             }
           ],
           "total_price": 15.0
         }
       ]
     }
     ```

#### Endpoints for Both Customer and Manager

1. GET /products:
   - General:
     - Get all Products
   - Request Arguments:
     - None
   - Returns:
     - return the custom Products Dictionary
   - Sample request:
     - `curl GET http://localhost:8080/products -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "products": [
         {
           "id": 1,
           "name": "Crystal Bottle of Drinking Water",
           "unit_price": 6.0
         }
       ]
     }
     ```
2. POST /search-products
   - General:
     - Search for Products by their name
   - Request Arguments:
     - None
   - Returns:
     - if found: return the custom Products Dictionary
     - if not found: return 404 error with custom message, and the empty list of Products
   - Sample request:
     - `curl POST http://localhost:8080/search-products -H "Authorization: Bearer <JWT_of_authenticated_Manager>" -d '{"name": "Crystal"}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "products": [
         {
           "id": 1,
           "name": "Crystal Bottle of Drinking Water",
           "unit_price": 6.0
         }
       ]
     }
     ```
3. GET /customers/<int:id>/orders
   - General:
     - Get all Orders of a Customer by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - return the custom Orders Dictionary
   - Sample request:
     - `curl GET http://localhost:8080/customers/2/orders -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "orders": [
         {
           "customer_id": 2,
           "deliver_date": "2021-09-01 09:00:00",
           "id": 1,
           "order_items": [
             {
               "id": 1,
               "product_id": 1,
               "quantity": 2
             },
             {
               "id": 2,
               "product_id": 2,
               "quantity": 3
             }
           ],
           "total_price": 15.0
         }
       ]
     }
     ```
4. PATCH /orders/<int:id>
   - General:
     - Partially update an Order by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - if found: return the custom Order Dictionary
     - if not found: return 404 error with custom message
   - Sample request:
     - `curl PATCH http://localhost:8080/orders/1 -H "Authorization: Bearer <JWT_of_authenticated_Manager>" -d '{"deliver_date": "2021-09-01 10:00:00"}' -H "Content-Type: application/json"`
   - Sample response:
     ```json
     {
       "order": {
         "customer_id": 2,
         "deliver_date": "2021-09-01 10:00:00",
         "comment": "Change the deliver date to 10:00:00",
         "id": 1,
         "order_items": [
           {
             "id": 1,
             "product_id": 1,
             "quantity": 2
           },
           {
             "id": 2,
             "product_id": 2,
             "quantity": 3
           }
         ],
         "total_price": 15.0
       }
     }
     ```
5. DELETE /orders/<int:id>
   - General:
     - Delete an Order by ID
   - Request Arguments:
     - None
   - Path Parameters:
     - id: int
   - Returns:
     - if found: return the deleted Order ID
     - if not found: return 404 error with custom message
   - Sample request:
     - `curl DELETE http://localhost:8080/orders/1 -H "Authorization: Bearer <JWT_of_authenticated_Manager>"`
   - Sample response:
     ```json
     {
       "deleted": {
         "id": 1
       }
     }
     ```

## Deployment

- The Backend of the app has been deployed on Render. You can access it by clicking on this link: [YES-Company App (Backend)](https://yes-company.onrender.com/)
- This Backend API URL is also integrated with the Frontend of the app, which is also hosted on Render, so that the Frontend can interact with the Backend API.

## Author:

Quan Tran

## Acknowledgements

Thanks to the fantastic team at Udacity for their excellent Full Stack Web Development Nanodegree Program that provides me the necessary knowledge to implement this app Full Stack.
