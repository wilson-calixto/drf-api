from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .filters import ServidorFilter


class CargoViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializerNestedSerializer

class ServidorViewSet(ModelViewSet):
    queryset = Servidor.objects.all()
    filterset_class=ServidorFilter
    def get_queryset(self):
        return Servidor.objects.select_related('cargo', 'lotacao').prefetch_related('cursos')

    def get_serializer_class(self):
        if(self.action in ['list','retrieve']):
            return ServidorReadSerializer
        return ServidorWriteSerializer

class LotacaoViewSet(ModelViewSet):
    queryset= Lotacao.objects.all()
    serializer_class= LotacaoSerializerNestedSerializer

class CursoViewSet(ModelViewSet):
    queryset= Curso.objects.all()
    serializer_class= CursosSerializerNestedSerializer