from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, UpdateModelMixin
from .models import Product,ProductImage, Collection, Review, Cart,CartItem, Customer, Order, Orderitem
from .serializer import ProductSerializer,CollectionSerializer, ReviewSerializer, CartSerializer,CartItemSerializer,AddCartItemSerializer,CartItemQuantitySerializer,CustomerSerializer,OrderSerializer,CreateOrderSerializer, OrderItemSerializer,UpdateOrderSerializer, ProductImageSerializer
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from django.contrib.auth.decorators import login_required
# Create your views here.
class ProductViewset(ModelViewSet):
    queryset= Product.objects.prefetch_related('images').all()
    serializer_class= ProductSerializer 
    permission_classes=[IsAdminOrReadOnly]
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['title','description']
    ordering_fields=['price', 'last_update']
    pagination_class= PageNumberPagination

class ProductImageViewset(ModelViewSet):
    
    serializer_class= ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
   

class CollectionViewset(ModelViewSet):
    queryset= Collection.objects.all()
    serializer_class= CollectionSerializer 
    permission_classes=[IsAdminOrReadOnly]

class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, GenericViewSet, ):
    queryset= Cart.objects.prefetch_related('items__product').all()
    serializer_class= CartSerializer  


class CartItemViewset(ModelViewSet):
    http_method_names=['get','post','patch','delete']
 
    def get_serializer_class(self):
        if self.request.method== 'POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return CartItemQuantitySerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}  
    
class OrderViewset(ModelViewSet):
    # queryset= Order.objects.prefetch_related('items__product').all()
    #serializer_class= OrderSerializer
    def get_permissions(self):
        http_method_names= ['get','post','patch','delete','head','options']
        if self.request.method in ['PATCH','DELETE']:
            return  [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer= CreateOrderSerializer(data=request.data, context= {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order= serializer.save()
        serializer= OrderSerializer(order)
        return Response(serializer.data)
    def get_serializer_class(self):
        if self.request.method== 'POST':
            return CreateOrderSerializer
        elif self.request.method== 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    #permission_classes=[IsAdminUser]

    # @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    # def me(self, request):
    #     print(request.user)
    #     customer, created= Customer.objects.get_or_create(user_id=request.user.id)

    #     if request.method == 'GET':
    #         if request.user.id == None:
    #             return Response('Not logged in')
    #         orders= Order.objects.filter(customer=customer)
    #         serializer = OrderSerializer(orders, many=True)
    #         return Response(serializer.data)
           
    #     elif request.method == 'POST':
    #         serializer = OrderSerializer(data=request.data)
    #         serializer.is_valid(raise_exception='True')
    #         serializer.save(customer=customer)
    #         return Response(serializer.data)

class ReviewViewset(ModelViewSet):
    serializer_class= ReviewSerializer 

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CustomerViewset(ModelViewSet):
    queryset= Customer.objects.all()
    serializer_class= CustomerSerializer
    permission_classes=[IsAdminUser]
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        print(request.user)
        customer= Customer.objects.get(user_id=request.user.id)

        if request.method == 'GET':
            if request.user.id == None:
                return Response('Not logged in')
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
           
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception='True')
            serializer.save()
            return Response(serializer.data)


def products_page(request):
    return render(request, "products.html")

def cart_page(request):
    return render(request, "cart.html")

def product_detail_page(request, id): 
    return render(request, "product_detail.html", {"product_id": id})

#@login_required
def checkout_page(request):
    return render(request, "checkout.html")


#from .services import initiate_ecocash_payment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import Order
from .services import initiate_ecocash_payment  # your payment function

@api_view(['POST'])
def pay_order_ecocash(request, pk):
    print("----- DEBUG START -----")

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    msisdn = request.data.get("msisdn")
    print("Received MSISDN:", msisdn)
    print("Order ID:", order.id)
    print("Order Items:", order.items.all())

    if not msisdn:
        return Response({"error": "Phone number required"}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total
    total = Decimal("0.00")
    for item in order.items.all():
        total += item.quantity * item.unit_price
    print("Calculated TOTAL:", total)
    print("----- DEBUG END -----")

    if total <= 0:
        return Response({"error": "Order total must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

    # Call EcoCash API safely
    try:
        response = initiate_ecocash_payment(
            msisdn=msisdn,
            amount=float(total),
            order_id=order.id
        )
        print("EcoCash RAW RESPONSE:", response)
        print("Response content:", response.text)
    except Exception as e:
        print("EcoCash Exception:", str(e))
        return Response({"error": "Payment gateway error", "details": str(e)}, status=500)

    # Try to parse JSON only if content exists
    data = {}
    if response.text.strip():
        try:
            data = response.json()
            print("EcoCash JSON:", data)
        except Exception as e:
            print("JSON Parse Error:", str(e))
            # fallback if response not JSON
            data = {"success": True, "message": "Payment request sent (sandbox)"}  
    else:
        # empty response, assume sandbox success
        data = {"success": True, "message": "Payment request sent (sandbox)"}

    # Update order if API call succeeded
    if response.status_code == 200:
        order.payment_status = "Processing"
        order.save()

    return Response(data, status=response.status_code)
