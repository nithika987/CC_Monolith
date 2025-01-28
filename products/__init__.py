from products import dao

class Product:
    def _init_(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        """Load a Product object from a dictionary."""
        return Product(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            cost=data.get('cost'),
            qty=data.get('qty', 0)
        )

def list_products() -> list[Product]:
    """Retrieve all products from the DAO and return them as Product objects."""
    products = dao.list_products()
    
    # Use list comprehension for better readability and performance
    return [Product.load(product) for product in products]

def get_product(product_id: int) -> Product:
    """Retrieve a single product by its ID."""
    product_data = dao.get_product(product_id)
    
    # Validate if product exists before attempting to load it
    if not product_data:
        raise ValueError(f"Product with ID {product_id} does not exist.")
    
    return Product.load(product_data)

def add_product(product: dict):
    """Add a new product to the inventory."""
    required_fields = {'id', 'name', 'description', 'cost', 'qty'}
    
    # Ensure the provided product dictionary has all the required fields
    if not required_fields.issubset(product.keys()):
        raise ValueError(f"Product data must include the fields: {required_fields}")
    
    dao.add_product(product)

def update_qty(product_id: int, qty: int):
    """Update the quantity of a product."""
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    
    # Validate if the product exists before attempting to update quantity
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Cannot update quantity: Product with ID {product_id} does not exist.")
    
    dao.update_qty(product_id, qty)