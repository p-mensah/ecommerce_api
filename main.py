from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

# Create a FastAPI application
app = FastAPI()

# Define the MongoDB connection string
connection_string = (
    "mongodb+srv://ecommerce_api:ecommerce_api@grow-cohort6.safmckr.mongodb.net/"
)

# Create a MongoDB client
client = MongoClient(connection_string)

# Select the database
db = client["ecommerce"]


# Define the user model
class User(BaseModel):
    name: str
    email: str
    password: str


# Define the product model
class Product(BaseModel):
    name: str
    description: str
    price: float
    stock: int


# Define the cart item model
class CartItem(BaseModel):
    product_id: str
    quantity: int


# User Flow
@app.get("/", tags=["Home"])
def home_page():
    return {"message": "Welcome to our E-commerce API"}


@app.post("/register")
def register_user(user: User):
    users_collection = db["users"]
    users_collection.insert_one(user.dict())
    user_id = str(users_collection.find_one({"email": user.email})["_id"])
    return {"message": "User registered successfully", "user_id": user_id}


@app.post("/login")
def login_user(user: User):
    users_collection = db["users"]
    user_doc = users_collection.find_one(
        {"email": user.email, "password": user.password}
    )
    if user_doc:
        user_id = str(user_doc["_id"])
        return {"message": "User logged in successfully", "user_id": user_id}
    raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/products")
def fetch_all_available_products():
    """Fetch all available products"""
    products_collection = db["products"]
    products = list(products_collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return {"products": products}


@app.get("/products/{product_id}")
def get_product(product_id: str):
    """Fetch product by ID"""
    products_collection = db["products"]
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
        return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/cart/{user_id}")
def add_to_cart(user_id: str, item: CartItem):
    carts_collection = db["carts"]
    user_obj_id = ObjectId(user_id)
    cart = carts_collection.find_one({"user_id": user_obj_id})
    if not cart:
        carts_collection.insert_one({"user_id": user_obj_id, "items": []})
    carts_collection.update_one(
        {"user_id": user_obj_id}, {"$push": {"items": item.dict()}}
    )
    return {"message": "Item added to cart"}


@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    from bson import ObjectId

    carts_collection = db["carts"]
    cart = carts_collection.find_one({"user_id": ObjectId(user_id)})
    if not cart:
        return {"cart": {"products": []}}

    products = []
    for item in cart.get("items", []):
        product = db["products"].find_one({"_id": ObjectId(item["product_id"])})
        if product:
            subtotal = product["price"] * item["quantity"]
            products.append(
                {
                    "product_id": str(product["_id"]),
                    "name": product["name"],
                    "description": product["description"],
                    "quantity": item["quantity"],
                    "unit_price": product["price"],
                    "subtotal": subtotal,
                }
            )
    return {"cart": {"products": products}}


@app.post("/checkout/{user_id}")
def checkout(user_id: str):
    carts_collection = db["carts"]
    cart = carts_collection.find_one({"user_id": ObjectId(user_id)})
    if cart:
        if "items" in cart:
            orders_collection = db["orders"]
            order = {"user_id": ObjectId(user_id), "products": [], "total": 0}
            for item in cart["items"]:
                product_collection = db["products"]
                product = product_collection.find_one(
                    {"_id": ObjectId(item["product_id"])}
                )
                if product:
                    order["products"].append(
                        {"product_id": item["product_id"], "quantity": item["quantity"]}
                    )
                    order["total"] += product["price"] * item["quantity"]
            order_id = orders_collection.insert_one(order).inserted_id
            return {
                "message": "Order placed successfully",
                "order_id": str(order_id),
                "total ₵": order["total"],
            }
        else:
            return {"message": "Cart is empty"}
    return {"message": "Cart not found"}


# Admin Flow
@app.post("/add_product", tags=["Admin"])
def add_product(product: Product):
    products_collection = db["products"]
    products_collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


@app.put("/products/{product_id}", tags=["Admin"])
def update_product(product_id: str, product: Product):
    products_collection = db["products"]
    products_collection.update_one(
        {"_id": ObjectId(product_id)}, {"$set": product.dict()}
    )
    return {"message": "Product updated successfully"}


@app.delete("/products/{product_id}", tags=["Admin"])
def delete_product(product_id: str):
    products_collection = db["products"]
    products_collection.delete_one({"_id": ObjectId(product_id)})
    return {"message": "Product deleted successfully"}
