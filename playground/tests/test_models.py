from django.test import TestCase
from store.models import Product, Collection, Customer, Promotion, Order, OrderItem, Cart, CartItem, Address

class ModelTestCase(TestCase):
    def test_create_collection_and_product(self):
        collection = Collection.objects.create(title="Electronics")
        product = Product.objects.create(
            title="Laptop",
            slug="laptop",
            description="Gaming Laptop",
            unit_price=1500.00,
            inventory=5,
            collection=collection
        )
        self.assertEqual(str(product), "Laptop")
        self.assertEqual(product.collection.title, "Electronics")

    def test_customer_str(self):
        customer = Customer.objects.create(
            first_name="John", last_name="Doe",
            email="john@example.com", phone="1234567890"
        )
        self.assertEqual(str(customer), "John Doe")

    def test_order_creation(self):
        customer = Customer.objects.create(first_name="Jane", last_name="Smith", email="jane@example.com", phone="0987654321")
        order = Order.objects.create(customer=customer)
        self.assertEqual(order.payment_status, "P")

    def test_address_linked_to_customer(self):
        customer = Customer.objects.create(first_name="Alice", last_name="Wonder", email="alice@example.com", phone="0001112222")
        address = Address.objects.create(customer=customer, street="123 Main", city="Wonderland", zip="00000")
        self.assertEqual(address.customer.email, "alice@example.com")
