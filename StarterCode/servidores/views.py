from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Sum,Value,Max,Min
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .filters import ServidorFilter
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import filters


class MateriaViewSet(ModelViewSet):
    queryset=Materia.objects.all()
    serializer_class= MateriaSerializer

class CargoViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializerNestedSerializer
    # responsavel por trazer um campo extra que resume um dado 
    # contar (COUNT)
    # somar (SUM)
    # média (AVG)
    # máximo/mínimo (MAX, MIN)

    
    @action(
        detail=False,
            methods=['get'],
            url_path='servidores_por_cargo',
     )
    def servidores_por_cargo(self,request):
        cargos=Cargo.objects.annotate(total_servidores=Count("servidores",distinct=True))
        serializer = self.get_serializer(cargos,many=True)
        return Response(serializer.data)


    
    @action(
        detail=False,
            methods=['get'],
            url_path='media_de_carga_horaria_de_cursos_por_cargo',
     )
    def media_de_carga_horaria_de_cursos_por_cargo(self,request):
        cargos=Cargo.objects.annotate(media_de_horas=Avg("servidores__cursos__carga_horaria"))
        serializer = self.get_serializer(cargos,many=True)
        return Response(serializer.data)





class ServidorViewSet(ModelViewSet):
    queryset = Servidor.objects.all()
    filterset_class=ServidorFilter
    # Busca em todos os campos do modelo
    filter_backends=[
        DjangoFilterBackend,#filtro do filterset_class 
        filters.SearchFilter,#search_fields
        filters.OrderingFilter,#ordering_fields
     ]
    
    #  search filter
    search_fields = ["nome", "cargo__nome"]#search_fields
    ordering_fields = ["nome"]

    def get_queryset(self):
        return Servidor.objects.select_related('cargo', 'lotacao').prefetch_related('cursos')
        # queryset = queryset.filter(cursos__id=1).distinct()
        
     
    # Adiciona uma rota extra à view
    @action(
            detail=False,
            methods=['get'],
            url_path='servidores-lotados-l1',
     )
    def servidores_lotados_l1(self,request):
                
        servidores=Servidor.objects.select_related('cargo', 'lotacao').prefetch_related('cursos').filter(
    Q(cargo__nome="c1") | Q(lotacao_id=1)
)       
        serializer = self.get_serializer(servidores,many=True)
        return Response(serializer.data)

    @action(
            detail=False,
            methods=['get'],
            url_path='servidores-aggregate',
     )
    def servidores_aggregate(self,request):
                
        servidores=Servidor.objects.aggregate(total_cursos=Count("id"))
        print(  'ser',servidores)
        return Response(servidores)
        serializer = self.get_serializer(servidores,many=True)
        return Response(serializer.data)

    @action(
            detail=False,
            methods=['get'],
            url_path='servidores-por-lotacao',
     )
    def servidores_por_lotacao(self,request):
                
        servidores=Servidor.objects.values('lotacao').annotate(total=Count("id"))
        return Response(servidores)
 

 

    @action(
            detail=False,
            methods=['get'],
            url_path='servidores-acima-media-cursos',
     )
    def servidores_acima_media_cursos(self,request):
        media=Servidor.objects.annotate(total_cursos=Count("cursos")).aggregate(media=Avg("total_cursos"))
        
        servidores=Servidor.objects.annotate(total_cursos=Count('cursos')).filter(total_cursos__gt=media['media'])
        serializer = self.get_serializer(servidores,many=True)
        
        return Response(serializer.data)
 

    # Total de horas de curso por servidor
    @action(
            detail=False,
            methods=['get'],
            url_path='horas_de_curso_por_servidor',
     )
    def horas_de_curso_por_servidor(self,request):
        # todo fazer funcionar 
                
        servidores=Servidor.objects.annotate(total_horas=Sum("cursos__carga_horaria"))
        serializer = self.get_serializer(servidores,many=True)
        
        return Response(serializer.data)
 
    # 
    # 
    @action(
            detail=False,
            methods=['get'],
            url_path='horas_de_curso_especifico_por_servidor',
     )
    def horas_de_curso_especifico_por_servidor(self,request):
        # todo fazer funcionar 
                
        servidores=Servidor.objects.annotate(horas_especificas=Sum("cursos__carga_horaria", filter=Q(cursos__nome__icontains="c2w")))
        serializer = self.get_serializer(servidores,many=True)
        
        return Response(serializer.data)
 


# Média de horas de curso por servidor
    @action(
            detail=False,
            methods=['get'],
            url_path='media_de_horas_de_curso_por_servidor',
     )
    def media_de_horas_de_curso_por_servidor(self,request):
                 
        servidores=Servidor.objects.annotate(media_horas=Coalesce(Avg("cursos__carga_horaria"),Value(0)))
        
        serializer = self.get_serializer(servidores,many=True)
        
        return Response(serializer.data)



    # @action(
    #         detail=False,
    #         methods=['get'],
    #         url_path='servidores-por-cargo',
    #  )
    # def servidores_por_cargo(self,request):
       
    #     servidores=Servidor.objects.values('cargo').annotate(total=Count("id"))
    #     return Response(servidores)
 

     
    @action(
        detail=False,
            methods=['get'],
            url_path='maior_carga_horaria_por_servidor',
     )
    def maior_carga_horaria_por_servidor(self,request):
        servidores=Servidor.objects.annotate(maior_curso=Max("cursos__carga_horaria"))
        serializer = self.get_serializer(servidores,many=True)
        return Response(serializer.data)


    @action(
        detail=False,
            methods=['get'],
            url_path='menor_carga_horaria_por_servidor',
     )
    def menor_carga_horaria_por_servidor(self,request):
        servidores=Servidor.objects.annotate(menor_curso=Min("cursos__carga_horaria"))
        serializer = self.get_serializer(servidores,many=True)
        return Response(serializer.data)


 

    def get_serializer_class(self):
        if(self.action in ['list','retrieve'] or  self.request.method =='GET'):
            return ServidorReadSerializer
        return ServidorWriteSerializer

class LotacaoViewSet(ModelViewSet):
    queryset= Lotacao.objects.all()
    serializer_class= LotacaoSerializerNestedSerializer

    @action(
            detail=False,
            methods=['get'],
            url_path='max_cursos_por_lotacao',
     )
    def max_cursos_por_lotacao(self,request):
    #     Exemplo 2 — Maior número de cursos em uma lotação
        lotacao=Lotacao.objects.annotate(max_cursos=Max("servidores__cursos__id"))

        serializer = self.get_serializer(lotacao,many=True)
        return Response(serializer.data)  

 
class CursoViewSet(ModelViewSet):
    queryset= Curso.objects.all()
 
 

    def get_serializer_class(self):
        if(self.action in ['list','retrieve'] or  self.request.method =='GET'):
            return CursosReadSerializerNestedSerializer
        return CursosWriteSerializerNestedSerializer

    @action(
            detail=False,
            methods=['get'],
            url_path='servidores_por_cursos',
     )
    def servidores_por_curso(self,request):
       
        servidores=Curso.objects.annotate(total_servidores=Count("servidores"))

        serializer = self.get_serializer(servidores,many=True)
        return Response(serializer.data)  

 