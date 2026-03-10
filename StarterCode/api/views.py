from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
from api.serializers import ProductSerializer, OrderSerializer,ProductInfoSerializer
from api.models import Product,Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# @api_view(['GET'])
# def product_list(request):
#     products=Product.objects.all()
#     serializer= ProductSerializer(products, many=True)
#     return Response(serializer.data)




# jeito mais eficiente de listar e criar 

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer

# jeito mais verboso de listar e criar 
class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    # busca os dados que tem stock maior que 0
    queryset = Product.objects.filter(stock__gt=0)
    # busca os dados que tem stock menor que 0
    # queryset = Product.objects.exclude(stock__gt=0)
    serializer_class=ProductSerializer


# jeito mais verboso de listar e criar 
class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class=ProductSerializer


# @api_view(['GET'])
# def product_detail(request, pk):
#     products=get_object_or_404(Product, pk=pk)
#     serializer= ProductSerializer(products)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer



# @api_view(['GET'])
# def order_list(request):
#     # orders=Order.objects.all() não otimizado, faz uma query pra cada order 
#     orders=Order.objects.prefetch_related("items__product").all() #otimizado, faz uma query com varias orders de uma vez 
#     serializer= OrderSerializer(orders, many=True)
#     return Response(serializer.data)
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product").all()
    serializer_class=OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product").all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(user=self.request.user)
    



# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products':products,
#         'count':len(products),
#         'max_price':products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products':products,
            'count':len(products),
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
