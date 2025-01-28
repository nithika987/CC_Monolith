import json
import products
from cart import dao
from products import Product

class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    # Fetch cart details from DAO
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    # Safely parse contents using json.loads
    all_product_ids = set()
    for cart_detail in cart_details:
        try:
            product_ids = json.loads(cart_detail['contents'])  # Parse JSON safely
            all_product_ids.update(product_ids)  # Add unique product IDs to the set
        except json.JSONDecodeError:
            continue  # Ignore invalid data
    
    # Fetch all product details in a single batch query
    product_list = products.get_products_by_ids(all_product_ids)  # Bulk query
    return product_list


(starting replacement of cart)