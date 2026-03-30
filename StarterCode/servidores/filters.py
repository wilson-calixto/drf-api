import django_filters
from .models import Servidor

class ServidorFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    cargo = django_filters.NumberFilter(field_name="cargo_id")
    lotacao = django_filters.NumberFilter(field_name="lotacao_id")

    class Meta:
        model=Servidor
        fields=["nome","cargo","lotacao"]