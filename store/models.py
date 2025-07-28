from django.db import models

# PROMOTION - PRODUCTS (MANY-TO-MANY)
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #products

# Create your models here.
class Collection(models.Model): 
    title = models.CharField(max_length=255)
    #onetoone
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') # related_name='+' means no reverse relation will be created

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2) #999999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    #onetomany each product belongs to a collection and a collection can have many products
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT) # PROTECT means we cannot delete collection until  products are within it        

    # CHANGE TITLE IN ADMIN PANEL
    def __str__(self):
        return self.title
    # SORT IN ASCENDING ORDER IN ADMIN PANEL
    class Meta:
        ordering = ['title']
 
    promotions = models.ManyToManyField(Promotion)

    
class Customer(models.Model):
    # Choices for membership levels 1 character
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,"Bronze"),
        (MEMBERSHIP_SILVER,"Silver"),
        (MEMBERSHIP_GOLD,"Gold"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering=['first_name','last_name']

    # class Meta:
    #     db_table = 'store_customers'
    #     indexes = [ #indexing to make searching faster
    #         models.Index(fields=['last_name','first_name'])
    #     ]


class Order(models.Model):
    place_at = models.DateTimeField(auto_now_add=True)
    # Choices for order status
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"

    PAYMENT_CHOICES = [
        (PAYMENT_STATUS_PENDING,"Pending"),
        (PAYMENT_STATUS_COMPLETE,"Complete"),
        (PAYMENT_STATUS_FAILED,"Failed"),
    ]

    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_STATUS_PENDING)
    # customer can have multiple orders
    # You CANNOT delete a customer if they have one or more related orders.
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    # we cannot delete a order if ordeitem is linekd to it and we cannot delete a product if its ordered
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)  # Price at the time of order



# Each customer will have only one address and one address can belong to only one customer
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    # specify the parent(customer) of this class, CASCADE means if the customer is deleted, the address will also be deleted
    # one customer can have one address due to primary key = True
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, primary_key=True)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    # cart can have multiple products & a product can be in multiplt carts
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveSmallIntegerField()