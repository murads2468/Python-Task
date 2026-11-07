
import json
import os
import uuid
import unittest


CATALOG_FILE = "catalog.json"
ORDERS_FILE = "orders.json"


# Product Class
class Product:
    def __init__(self, product_id, name, price, stock):
        if price < 0 or stock < 0:
            raise ValueError("Price and stock cannot be negative")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


# Cart Class
class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product_id, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        self.items[product_id] = self.items.get(product_id, 0) + quantity

    def calculate_total(self, inventory, discount=0):
        if not isinstance(discount, (int, float)) or not 0 <= discount <= 100:
            raise ValueError("Discount must be between 0 and 100")

        total = 0

        for product_id, quantity in self.items.items():
            if product_id not in inventory.products:
                raise ValueError(f"Product {product_id} not found")

            product = inventory.products[product_id]
            total += product.price * quantity

        return total - (total * discount / 100)


# Inventory Class
class Inventory:
    def __init__(self):
        self.products = {}

    def load_catalog(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Invalid catalog format")

        products = {}

        for item in data:
            product = Product(
                item["product_id"],
                item["name"],
                item["price"],
                item["stock"]
            )

            if product.product_id in products:
                raise ValueError("Duplicate product ID")

            products[product.product_id] = product

        self.products = products

    def save_catalog(self, file_path):
        data = [
            {
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }
            for product in self.products.values()
        ]

        temp_file = file_path + ".tmp"

        with open(temp_file, "w") as file:
            json.dump(data, file, indent=4)

        os.replace(temp_file, file_path)


# Order Class
class Order:
    def __init__(self, cart, inventory, discount=0):
        self.order_id = str(uuid.uuid4())
        self.items = cart.items.copy()
        self.discount = discount
        self.total = cart.calculate_total(inventory, discount)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "items": self.items,
            "discount": self.discount,
            "total": self.total
        }


# Order Fulfillment System
class OrderSystem:
    def __init__(self, inventory, catalog_file, orders_file):
        self.inventory = inventory
        self.catalog_file = catalog_file
        self.orders_file = orders_file

    def place_order(self, cart, discount=0):
        # Validate discount and all cart items first
        total = cart.calculate_total(self.inventory, discount)

        for product_id, quantity in cart.items.items():
            product = self.inventory.products[product_id]

            if quantity <= 0:
                raise ValueError("Invalid quantity")

            if quantity > product.stock:
                raise ValueError(f"Insufficient stock for {product_id}")

        # Create order after validation
        order = Order(cart, self.inventory, discount)

        # Read existing orders
        if os.path.exists(self.orders_file):
            with open(self.orders_file, "r") as file:
                orders = json.load(file)

            if not isinstance(orders, list):
                raise ValueError("Invalid orders file format")
        else:
            orders = []

        # Save original stock for rollback
        old_stock = {
            product_id: self.inventory.products[product_id].stock
            for product_id in cart.items
        }

        # Update inventory
        try:
            for product_id, quantity in cart.items.items():
                self.inventory.products[product_id].stock -= quantity

            # Persist updated catalog
            self.inventory.save_catalog(self.catalog_file)

            # Add order and persist orders
            orders.append(order.to_dict())

            temp_file = self.orders_file + ".tmp"

            with open(temp_file, "w") as file:
                json.dump(orders, file, indent=4)

            os.replace(temp_file, self.orders_file)

        except Exception:
            # Roll back in-memory stock
            for product_id, stock in old_stock.items():
                self.inventory.products[product_id].stock = stock

            # Restore catalog file
            self.inventory.save_catalog(self.catalog_file)

            raise

        return order


# Sample catalog
sample_catalog = [
    {
        "product_id": "P1",
        "name": "Laptop",
        "price": 100,
        "stock": 5
    },
    {
        "product_id": "P2",
        "name": "Mouse",
        "price": 50,
        "stock": 10
    },
    {
        "product_id": "P3",
        "name": "Keyboard",
        "price": 80,
        "stock": 4
    }
]

with open(CATALOG_FILE, "w") as file:
    json.dump(sample_catalog, file, indent=4)


# Load inventory
inventory = Inventory()
inventory.load_catalog(CATALOG_FILE)

# Create cart
cart = Cart()
cart.add_item("P1", 2)

# Place order
system = OrderSystem(inventory, CATALOG_FILE, ORDERS_FILE)
order = system.place_order(cart, discount=10)

print("Order ID:", order.order_id)
print("Order Total:", order.total)
print("Remaining Stock:", inventory.products["P1"].stock)


# Unit Tests
class TestOrderSystem(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

        self.inventory.products = {
            "P1": Product("P1", "Laptop", 100, 5),
            "P2": Product("P2", "Mouse", 50, 2)
        }

        self.cart = Cart()

        self.test_catalog = "test_catalog.json"
        self.test_orders = "test_orders.json"

        self.inventory.save_catalog(self.test_catalog)

        self.system = OrderSystem(
            self.inventory,
            self.test_catalog,
            self.test_orders
        )

    def tearDown(self):
        for file_path in [self.test_catalog, self.test_orders,
                          self.test_catalog + ".tmp",
                          self.test_orders + ".tmp"]:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_discount_total(self):
        self.cart.add_item("P1", 2)

        total = self.cart.calculate_total(self.inventory, 10)

        self.assertEqual(total, 180)

    def test_successful_order_updates_stock(self):
        self.cart.add_item("P1", 2)

        order = self.system.place_order(self.cart, 10)

        self.assertEqual(order.total, 180)
        self.assertEqual(self.inventory.products["P1"].stock, 3)

    def test_out_of_stock_rejected(self):
        self.cart.add_item("P2", 5)

        with self.assertRaises(ValueError):
            self.system.place_order(self.cart)

        self.assertEqual(self.inventory.products["P2"].stock, 2)


if __name__ == "__main__":
    unittest.main()
