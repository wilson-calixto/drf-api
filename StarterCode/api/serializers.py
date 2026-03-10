

from rest_framework import serializers
from .models import Product, Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
                'id',
                'name', 
                'description',
                'price',
                'stock'
        )
    def validate(self, value):
        if(value<=0):
            raise serializers.ValidationError('Price must be greater than 0')
    
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
     
class OrderSerializer(serializers.ModelSerializer):
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
    