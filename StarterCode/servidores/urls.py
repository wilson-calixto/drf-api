 

 
# from django.urls import path
# from . import views

# from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     # path("products", views.product_list),
#     path("cargos", views.CargoViewSet.as_view()),
 
#      path("servidores", views.ServidorViewSet.as_view(),name='servidor-detail'),
 
 

# ]


# router = DefaultRouter()

# urlpatterns+=router.urls


from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'cargos', CargoViewSet, basename='cargos')
router.register(r'lotacoes', LotacaoViewSet, basename='lotacoes')
router.register(r'cursos', CursoViewSet, basename='cursos')
router.register(r'servidores', ServidorViewSet, basename='servidor')
urlpatterns = router.urls