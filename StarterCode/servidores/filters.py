import django_filters
from .models import Servidor
from django.db.models import Q, Count

class ServidorFilter(django_filters.FilterSet):
    #DjangoFilterBackend
    nome = django_filters.CharFilter(lookup_expr='icontains')
    nome_cargo = django_filters.CharFilter(field_name='cargo__nome', lookup_expr='icontains')
    cargo = django_filters.NumberFilter(field_name="cargo_id")
    lotacao = django_filters.NumberFilter(field_name="lotacao_id")


    # múltiplos cursos (?cursos=1,2,3)
    cursos = django_filters.BaseInFilter(field_name="cursos__id", lookup_expr="in")


    # busca geral
    search = django_filters.CharFilter(method="filter_search")
    
    # cursos obrigatórios (todos)
    cursos_all = django_filters.CharFilter(method="filter_cursos_all")

        # Filtros customizados
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nome__icontains=value) |
            Q(cargo__nome__icontains=value)
        )

    # curso obrigatório
    def filter_cursos_all(self, queryset, name, value):
        gt = int(value)
 
        return queryset.annotate(
            total_cursos=Count(
                "cursos",
                 distinct=True,
            )
        ).filter(
            total_cursos__gte=gt
        )

       
    class Meta:
        model=Servidor
        fields=["nome","cargo","lotacao"]