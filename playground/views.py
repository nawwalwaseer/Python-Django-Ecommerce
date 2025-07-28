from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order, Customer, Collection
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat, Upper, Length, ExtractYear, Now
from django.db.models.aggregates import Count, Max, Min, Avg
from .forms import ContactForm
from django.contrib.contenttypes.models import ContentType
from tags.models import TagItem
from datetime import datetime
from django.db import transaction, connection



# Create your views here.
# views are functions that take a request and return a response
# its a request handler known as VIEW

# # greeting view function
# def greeting(request):
#     return HttpResponse("Hello,World! How are you doing?")

# # saying full name function
# def fullName(request):
#     return HttpResponse("My name is Nawwal Waseer")

# # debugger check!
# def calculate():
#     x=1
#     y=2
#     return x

# def sumNumbers(request, a, b):
#     return HttpResponse(f"The sum of {a} and {b} is {a + b}")

# def multiplyNumbers(request, a, b, c):
#     return HttpResponse(f"the product of {a}, {b} & {c} is {a*b*c}")



# template name -> hello.html

def sayHello(request):
    # try:
        # keywords
        # unit_price__range=(10.00,30.00)
        # unit_price__gt=10.00
        # title__icontains='coffee'
        # title__iendswith
        # last_update__year=2021
        # description__icontains='eco'

        # inventory < 10 OR unit_price < 20
        product = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

        # inventory < 10 AND unit_price < 20
        product = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))

        # inventory < 10 AND NOT unit_price < 20
        product = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))

        # where inventory = collection_id
        product = Product.objects.filter(inventory=F('collection_id'))

        product = Product.objects.order_by('-title', 'unit_price').reverse()

        # limiting page size
        product = Product.objects.all()[5:500]

        # getting desired fields -> value_list to get data in tuple, value to get data in dictionary
        product = Product.objects.values_list('id','title','collection__title')

        # select product_id from orderitem table and show as order
        # product = OrderItem.objects.values('product_id')
        # get that products which were ordered and not show duplication
        product = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

        # only and defer avoid multiple single queries
        product = Product.objects.only('title','unit_price')
        product = Product.objects.defer('description')

        # get product as well as collection which is related to product. we use select_related becasue .all() will only list objects of product not collection
        product = Product.objects.select_related('collection').all()

        product = Product.objects.prefetch_related('promotions').all()

        # get last 5 orders with customer and items(including products)
        order = Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by('-place_at')[:5]

        # Aggreagting objects
        result_dict = Product.objects.aggregate(Count('id'), min_unit_price=Min('unit_price'), max_unit_price=Max('unit_price'), avg_collection_id=Avg('collection_id'))

        # annotating a new boolean field in product
        product = Product.objects.annotate(is_new=Value(True))
        
        # annotating existing id with products
        product = Product.objects.annotate(new_id=F('id')+1)

        product = Product.objects.annotate(is_expensive=F('unit_price') * 2)


        customer = Customer.objects.annotate(
             fullName = Func(F('first_name'), Value(' ') , F('last_name'), function='CONCAT')
        )

        # database concat function
        customer = Customer.objects.annotate(
             fullname = Concat('first_name', Value(' '), 'last_name')
        )
        # upper & lower
        customer = Customer.objects.annotate(
             fullname = Upper('first_name')
        )
        # length
        customer = Customer.objects.annotate(
             nameLength = Length('first_name')
        )
        #Extract Year
        order = Order.objects.annotate(
             placedYear = ExtractYear('place_at')
        )
        #Now to check placed date and time & present date and time
        order = Order.objects.annotate(
             placedYear = Now('place_at')
        )

        # which customer has placed how many orders
        customer = Customer.objects.annotate(
             orders_count= Count('order')
        )

        # used expression wrapper for complex computations involving different data types
        discountedPrice = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
        product = Product.objects.annotate(
             discounted_price = discountedPrice
        )
        
        # custom manager to tag a specific item of any model that is refered
        TagItem.objects.get_tags_for(Product,1)

        # query caching (optimized)
        query_set = Product.objects.all()  
        list(query_set)
     #    query_set[0]



        # creating & updating new objects, inserting manually from code
     #    new_collection = Collection.objects.create(title='Video Games', featured_product_id=1001)
     #    collection_update = Collection.objects.filter(id=1).update(title='Nawwal Aftab Wasser', featured_product_id=1001)
        # updating & delete product table row with specific id
     #    update_product = Product.objects.filter(id=2).update(title='Salmom Smoked', description='asdf', inventory=10, last_update= datetime(2025,2,17,0,0,0), collection_id=272)
     #    delete_product = Product.objects.filter(id=1001).delete()
     
     # IF BOTH OPERATION SSUCCEED TRANSACTION IS RUN AND IF ONE FAILS TRANSACTION IS ROLLLBACKED
     #    with transaction.atomic():
     #                 order = Order()
     #    order.customer_id=1
     #    order.save()

     #    item = OrderItem()
     #    item.order = order
     #    item.product_id = 3
     #    item.quantity = 1
     #    item.unit_price = 10.00
     #    item.save()

        query_set = Product.objects.raw('SELECT id, title FROM store_product')

        # Django specified way of executing Raw Sql queries
        cursor_RAW_Queries = connection.cursor()
        cursor_RAW_Queries.execute('SELECT * FROM store_product')
        cursor_RAW_Queries.close()


        return render(request, "hello.html", {"name":"Nawwal Aftab Waseer" , 'result': list(query_set)})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            gender = form.cleaned_data['gender']
            country = form.cleaned_data['country']
            address = form.cleaned_data['address']
            return render(request, 'thankyou.html', {'name': name})
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
