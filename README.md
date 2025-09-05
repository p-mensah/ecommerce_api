# E-commerce API

This is a FastAPI-based E-commerce API that provides functionalities for user management, product browsing, shopping cart operations, and order processing. It also includes administrative endpoints for managing products.

## Features

*   **User Authentication:** Register and log in users.
*   **Product Management:** View all products, view a single product by ID.
*   **Shopping Cart:** Add items to a user's cart, view cart contents.
*   **Checkout:** Process orders from the shopping cart.
*   **Admin Panel:** Add, update, and delete products (requires authentication, not explicitly implemented in provided code but implied by routes).

## Technologies Used

*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Pydantic:** Used for data validation and settings management.
*   **PyMongo:** A Python distribution containing tools for working with MongoDB.
*   **MongoDB Atlas:** Cloud-hosted NoSQL database for storing application data.
*   **python-dotenv:** For loading environment variables from a `.env` file.

## Setup and Installation

### Prerequisites

*   Python 3.7+
*   MongoDB Atlas account (or a local MongoDB instance)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p-mensah/ecommerce_api.git
    cd ecommerce_api
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project and add your MongoDB Atlas connection string:
    ```
    MONGO_URI="mongodb+srv://ecommerce_api:ecommerce_api@grow-cohort6.********.mongodb.net/"
    ```
    *Replace the connection string with your actual MongoDB Atlas connection string.*

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.
    You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Home

*   `GET /` - Welcome message.

### User Flow

*   `POST /register` - Register a new user.
*   `POST /login` - Log in a user.
*   `GET /products` - Fetch all available products.
*   `GET /products/{product_id}` - Fetch a single product by ID.
*   `POST /cart/{user_id}` - Add an item to the user's cart.
*   `GET /cart/{user_id}` - Get the contents of the user's cart.
*   `POST /checkout/{user_id}` - Process the checkout for a user's cart.

### Admin Flow

*   `POST /add_product` - Add a new product (Admin).
*   `PUT /products/{product_id}` - Update an existing product (Admin).
*   `DELETE /products/{product_id}` - Delete a product (Admin).

## Models

### User

*   `name`: `str`
*   `email`: `str`
*   `password`: `str`

### Product

*   `name`: `str`
*   `description`: `str`
*   `price`: `float`
*   `stock`: `int`

### CartItem

*   `product_id`: `str`
*   `quantity`: `int`
t
