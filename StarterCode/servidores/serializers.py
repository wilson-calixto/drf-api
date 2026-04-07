from rest_framework import serializers
from .models import *
from .service import ServidorService


class MateriaSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Materia
        fields = "__all__"
    
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



class CursosReadSerializerNestedSerializer(serializers.ModelSerializer):
    total_servidores=serializers.IntegerField(read_only=True)
    materias=MateriaSerializer(many=True)

    class Meta:
        model=Curso
        fields=["id","nome","carga_horaria","total_servidores","materias"]
        
class CursosWriteSerializerNestedSerializer(serializers.ModelSerializer):
    total_servidores=serializers.IntegerField(read_only=True)

    class Meta:
        model=Curso
        fields=["id","nome","carga_horaria","total_servidores","materias"]
        
class LotacaoSerializerNestedSerializer(serializers.ModelSerializer):
    max_cursos=serializers.FloatField(read_only=True)
    class Meta:
        model=Lotacao
        fields=["id","nome","max_cursos"]

class CargoSerializerNestedSerializer(serializers.ModelSerializer):
    total_servidores=serializers.IntegerField(read_only=True)
    media_de_horas=serializers.FloatField(read_only=True)
    class Meta:
        model=Cargo
        fields=["id","nome","total_servidores","media_de_horas"]

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
    cursos=CursosReadSerializerNestedSerializer(many=True)
    total_cursos=serializers.IntegerField(read_only=True)
    media_horas = serializers.FloatField(read_only=True)
    maior_curso= serializers.FloatField(read_only=True)
    menor_curso= serializers.FloatField(read_only=True)
    class Meta:
        model = Servidor
        fields = "__all__"        

