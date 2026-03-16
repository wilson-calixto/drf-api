from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
from api.serializers import ProductSerializer, OrderSerializer,ProductInfoSerializer,OrderCreateSerializer
from api.models import Product,Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from api.filters import ProductFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import InStockFilterBackend, OrderFilter
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from api.pagination import CustomPagination
from rest_framework import viewsets
from rest_framework.decorators import action



# @api_view(['GET'])
# def product_list(request):
#     products=Product.objects.all()
#     serializer= ProductSerializer(products, many=True)
#     return Response(serializer.data)




# jeito mais eficiente de listar e criar Product

class ProductListCreateAPIView(generics.ListCreateAPIView):
    # sempre que usar paginação adicione uma ordenação default
    queryset = Product.objects.order_by('-pk')
    serializer_class=ProductSerializer
    filterset_class=ProductFilter
    # search filter, busca a substring em todos os campos de search_fields 
    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,#search_fields
        filters.OrderingFilter,#ordering_fields
        InStockFilterBackend,#custom filter 
        ]
    # =name busca a correspondencia exata
    # ^name busca o que começa com a pesquisa

    search_fields=['=name','description']
    ordering_fields=['name','price','stock']

    # vc pode sobrescrever o pagination
    pagination_class= CustomPagination

    # vc pode usar o offset pra scroll infinito pois ele pula a q uanti
    # quantidade de tuplas do offset e retorna a quantidade de tuplas do limit

    # pagination_class= LimitOffsetPagination



    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if(self.request.method=='POST'):
            self.permission_classes=[IsAdminUser]
            
        return super().get_permissions()

# jeito mais verboso de listar e criar Product
class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    # busca os dados que tem stock maior que 0
    queryset = Product.objects.filter(stock__gt=0)
    # busca os dados que tem stock menor que 0
    # queryset = Product.objects.exclude(stock__gt=0)
    serializer_class=ProductSerializer


# jeito mais verboso de listar e criar Product
class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class=ProductSerializer


# @api_view(['GET'])
# def product_detail(request, pk):
#     products=get_object_or_404(Product, pk=pk)
#     serializer= ProductSerializer(products)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'
    
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if(self.request.method in ['PUT','PATCH','DELETE']):
            self.permission_classes=[IsAdminUser]
            
        return super().get_permissions()


# @api_view(['GET'])
# def order_list(request):
#     # orders=Order.objects.all() não otimizado, faz uma query pra cada order 
#     orders=Order.objects.prefetch_related("items__product").all() #otimizado, faz uma query com varias orders de uma vez 
#     serializer= OrderSerializer(orders, many=True)
#     return Response(serializer.data)







# crud completo de Order
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").all().order_by('-pk')
    serializer_class=OrderSerializer
    # permission_classes=[AllowAny]
    permission_classes=[IsAuthenticated]
    # remove a paginação
    pagination_class=None
    filterset_class=OrderFilter
    filter_backends=[DjangoFilterBackend]

    # adiciona novos parametros no save do serializer 
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # sobrescrever a classe de serializer dependendo do metodo que esta sendo usado
    def get_serializer_class(self):
        if(self.action=='create'): # ou self.request.method =='POST'
            return OrderCreateSerializer
        return super().get_serializer_class()
    

    # modifica o comportamento dos dados buscados dependendo do tipo de usuário
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user=self.request.user)
        return qs



    # Adiciona uma rota extra à view
    @action(
            detail=False,
            methods=['get'],
            url_path='user-orders',
            permission_classes=[IsAuthenticated]
    )
    def user_orders(self,request):
        orders=self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders,many=True)
        return Response(serializer.data)






# tem somente o get de Order
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
