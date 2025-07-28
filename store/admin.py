from django.contrib import admin
from . import models
from django.db.models.aggregates import Count, Avg, Min
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price', 'inventoryStatus', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    ordering = ['inventory']
    list_select_related = ['collection']
    
    def inventoryStatus(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','productsCount', 'productsAverage', 'productUnitPrice']
    
    # OVERRIDING BASE QUERY SET TO GET ADDITIONAL DETAILS
    @admin.display(ordering='productsCount')    
    def productsCount(self, collection):
        return collection.productsCount
    
    @admin.display(ordering='productsAverage')
    def productsAverage(self, collection):
        return collection.productsAverage
    
    @admin.display(ordering='productUnitPrice')
    def productUnitPrice(self, collection):
        return collection.productUnitPrice
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            productsCount = Count('product'),
            productsAverage = Avg('product__unit_price'),
            productUnitPrice = Min('product__unit_price')
        )  
    
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership' ]
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']  

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','place_at','customer']
    

admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order, OrderAdmin)