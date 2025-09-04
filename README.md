# E-commerce API

This is a basic e-commerce API.

## Setup

1. Clone the repository.
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Endpoints

### Home
* `GET /` - Welcome to our E-commerce API

### Products
* `GET /products` - Get all products
* `GET /products/{id}` - Get details of a specific product

### Users
* `POST /register` - Register a new user
* `POST /login` - Log in a user

### Cart
* `POST /cart` - Add a product to a user's cart
* `GET /cart/{user_id}` - Get items in a user's cart

### Checkout
* `POST /checkout/{user_id}` - Get an order summary for a user's cart
