from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
# Register your models here.
#admin.site.register(Collection)
#admin.site.register(Product)
#admin.site.register(Promotion)
#admin.site.register(Order)
#admin.site.register(Orderitem)
# admin.site.register(Cart)
# admin.site.register(CartItem)
# admin.site.register(Address)
# admin.site.register(Review)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title', 'products_count']
    search_fields= ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url= ((reverse('admin:store_product_changelist')+ '?' + urlencode({'collection__id': str(collection.id)})))
        return format_html('<a href="{}">{}</a>', url , collection.products_count)
    

    def get_queryset(self, request): 
        return super().get_queryset(request).annotate(
            products_count= Count('products')
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'membership', 'ordering']
    list_editable=['membership'] 
    list_select_related= ['user']
    ordering= ['user__first_name', 'user__last_name']
    list_per_page= 10
    search_fields= ['first_name__istartswith', 'last_name__istartswith']

class ProductImageInline(admin.TabularInline):
    model= models.ProductImage
    #extra= 1
    readonly_fields= ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html('<img src="{}"/>', instance.image.url)
        return ''

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields= ['collection']
    prepopulated_fields= {'slug': ['title']}
    list_display=['title', 'price', 'inventory_status', 'collection']
    list_editable=['price']
    list_per_page= 10
    list_filter= ['collection', 'last_update']
    inlines= [ProductImageInline]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory< 10:
            return 'Low'
        return 'OK'
    
class orderItemInline(admin.TabularInline):
    #autocomplete_fields= ['product']
    model= models.Orderitem
    extra= 0
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields= ['customer']
    inlines= [orderItemInline]
    list_display=['id','placed_at','customer']

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id']
   
@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['id', 'cart', 'product', 'quantity']
   