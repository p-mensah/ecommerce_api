# FastAPI E-Commerce
# 1. Setup
# ● Install FastAPI.
# ● Create a simple main.py with a root endpoint:
# ○ GET / → return "Welcome to our E-commerce API"

# 2. Products
# ● Create a list of sample products in Python (id, name, description, price, image).
# ● Implement routes:
# ○ GET /products → return all products.
# ○ GET /products/{id} → return details of one product (use id to search in the
# list).

# 3. Users (Basic Auth Simulation)
# ● Create a list to store users (id, username, email, password).
# ● Routes:
# ○ POST /register → accept user details and add to the list.
# ○ POST /login → check username/email + password, return "Login
# successful" or "Invalid credentials".

# 4. Cart
# ● Use a dictionary to simulate carts: {user_id: [ {product_id, quantity}, … ] }.
# ● Routes:
# ○ POST /cart → add product + quantity to a user’s cart.
# ○ GET /cart/{user_id} → return the items in that user’s cart.


# 5. Checkout
# ● Calculate the subtotal (price * quantity) for each cart item.
# ● Add them together for a total.
# ● Route:
# ○ POST /checkout/{user_id} → return an order summary (cart items + total).


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#  products
products = [
    {
        "id": 1,"name": "watch","description": "rolex","price": 1000,"image": "........",},
    {"id": 2,"name": "shirt ","description": " Gucci","price": 200,"image": ".......",},
    {"id": 3,"name": "sneakers ","description": "New Balance ","price": 139,"image": ".......",
    },
]

#  users
users = [
    {"id": 1, "username": "Peter", "email": "peter@mest.com", "password": "admin123"},
    {"id": 2, "username": "Kwame", "email": "kwame@mest.com", "password": "admin123"},
]

#  carts
carts = {}


# Define a Pydantic model for user registration
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str


# Define a Pydantic model for cart item
class CartItem(BaseModel):
    product_id: int
    quantity: int


# home endpoint
@app.get("/")
def home_page():
    return {"message": "Welcome to our E-commerce API"}


# Product endpoints
@app.get("/products")
def get_products():
    return {"products": products}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}


# User endpoints
@app.post("/register")
def register_user(user: UserRegistration):
    if any(u["username"] == user.username or u["email"] == user.email for u in users):
        return {"error": "User already exists"}
    
    new_user = {"id": len(users) + 1,"username": user.username,"email": user.email, "password": user.password,}
    users.append(new_user)
    return {"message": "User registered successfully"}


#login endpoint

@app.post("/login")
def login_user(username: str, password: str):
    # Create a new user if they don't exist
    existing_user = next((user for user in users if user["username"] == username), None)
    if existing_user is None:
        users.append(
            {"id": len(users) + 1,"username": username,"email": "","password": password,})
        return {"message": "Login successful"}
    
    # Check if the password is correct

    elif existing_user["password"] == password:
        return {"message": "Login successful"}
    else:
        return {"error": "Invalid password"}


# Cart endpoints
@app.post("/cart")
def add_to_cart(user_id: int, item: CartItem):
    if user_id not in carts:
        carts[user_id] = []
    carts[user_id].append({"product_id": item.product_id, "quantity": item.quantity})
    return {"message": "Item added to cart"}


@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    if user_id not in carts:
        return {"error": "Cart not found"}
    return {"cart": carts[user_id]}



# Checkout endpoint
@app.post("/checkout/{user_id}")
def checkout(user_id: int):
    if user_id not in carts:
        return {"error": "Cart not found"}
    cart_items = []
    subtotal = 0
    for item in carts[user_id]:
        product = next((p for p in products if p["id"] == item["product_id"]), None)
        if product:
            cart_items.append({
                "product_name": product["name"],
                "product_description": product["description"],
                "product_price": product["price"],
                "quantity": item["quantity"],
                "total": product["price"] * item["quantity"]
            })
            subtotal += product["price"] * item["quantity"]
    return {"order_summary": {"cart_items": cart_items, "total": subtotal}}

