

from rest_framework import serializers
from .models import Product, Order,OrderItem, User
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # vc pode exluir alguns campos do retorno do serializer
        # exclude('password', 'user_permissions')


        fields=(
            'username',
            'email',
            'is_staff',
            'orders'
        )
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
                 'name', 
                'description',
                'price',
                'stock'
        )
 
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value
        
class OrderItemSerializer(serializers.ModelSerializer):
    # essa linha é responsável por trazer os dados do produto relacionado com essa order item
    product=ProductSerializer()

    # voce também pode pegar campos individualmente
    # product_name =serializers.CharField(source='product.name')
    # product_price =serializers.DecimalField(max_digits=10, decimal_places=2,source='product.price')
  
    class Meta:
        model=OrderItem
        # voce também pode pegar campos individualmente
        # fields = ('product_price','quantity','product_name')
        
        # subtotal é um atributo calculado no model 
        fields = ('product','quantity', 'item_subtotal')
     


# serializer específico pra criar dados 
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):  
        class Meta:
            model=OrderItem
            fields=('product','quantity')


    order_id=serializers.UUIDField(read_only=True)
    items=OrderItemCreateSerializer(many=True, required=False)
    
    def update(self, instace, validated_data):
        # cria a order sem o itens 
        orderitem_data = validated_data.pop('items')
        
        with transaction.atomic:
            # atualiza os dados de order 
            instace = super().update(instace,validated_data)

            if(orderitem_data is not None):
                # limpando itens atuais
                instace.items.all().delete()


                # cria os order itens e os relaciona com a order 
                for item in orderitem_data:
                    OrderItem.objects.create(order=instace, **item)

        return instace



    def create(self, validated_data):
        # cria a order sem o itens 
        orderitem_data = validated_data.pop('items')
        print("orderitem_data",orderitem_data)

        order = Order.objects.create(**validated_data)

        # cria os order itens e os relaciona com a order 
        for item in orderitem_data:
            OrderItem.objects.create(order=order, **item)

        return order
    class Meta:
        model=Order
 
        fields = ('order_id','user','status', 'items')
        # desta forma o campo user só é exibido no get
        extra_kwargs={
            'user':{'read_only':True}
        }

class OrderSerializer(serializers.ModelSerializer):
    # permite que o id seja ocutado ao criar uma nova order
    order_id=serializers.UUIDField(read_only=True)
    # faz o relacionamento entre o orderItems e a Order
    items=OrderItemSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField()

    def get_total_price(self,obj):
        order_items=obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model=Order
        fields = ('order_id','create_at','user','status', 'items',  'total_price')
 

class ProductInfoSerializer(serializers.Serializer):
    # get all products, count of products, max price
    products= ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
    