from rest_framework import serializers
from .models import *
from .service import ServidorService

class ServidorSerializerPrimaryKeyRelatedField(serializers.ModelSerializer):
    class Meta:
        model = Servidor
        fields = "__all__"

class ServidorSerializerStringRelatedField(serializers.ModelSerializer):
    cargo= serializers.StringRelatedField()
    lotacao= serializers.StringRelatedField()

    class Meta:
        model=Servidor
        fields='__all__'

class ServidorSerializerSlugRelatedField(serializers.ModelSerializer):
    cargo = serializers.SlugRelatedField(
        slug_field="nome",
        queryset=Cargo.objects.all()
    )

    class Meta:
        model=Servidor
        fields='__all__'


class CursosSerializerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Curso
        fields=["id","nome"]
        
class LotacaoSerializerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lotacao
        fields=["id","nome"]

class CargoSerializerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cargo
        fields=["id","nome"]

class ServidorSerializerNestedSerializer(serializers.ModelSerializer):
    cargo=CargoSerializerNestedSerializer()
    lotacao=LotacaoSerializerNestedSerializer()

    class Meta:
        model=Servidor
        field="__all__"



class ServidorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servidor
        fields = "__all__"

    def update(self, instance, validated_data):
        return ServidorService.update(instance,validated_data)
 

class ServidorReadSerializer(serializers.ModelSerializer):
    cargo=CargoSerializerNestedSerializer()
    lotacao=LotacaoSerializerNestedSerializer()
    cursos=CursosSerializerNestedSerializer(many=True)


    class Meta:
        model = Servidor
        fields = "__all__"        