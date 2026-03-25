# from django.urls import path
# from . import views

# from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     # path("products", views.product_list),
#     path("products", views.ProductListCreateAPIView.as_view()),
#     # path("products/create/", views.ProductCreateAPIView.as_view()),
#     # path("products/info/", views.product_info),
#     path("products/info/", views.ProductInfoAPIView.as_view()),
    

    
    

#     # path("products/<int:pk>/", views.product_detail),
#     path("products/<int:product_id>/", views.ProductDetailAPIView.as_view(),name='product-detail'),
#     # path("orders", views.order_list),
#     # path("orders", views.OrderListAPIView.as_view()),
#     path("user-orders", views.UserOrderListAPIView.as_view(),name='user-orders'),
    
#     path("users/", views.UserListView.as_view()),

# ]


# router = DefaultRouter()
# router.register('orders', views.OrderViewSet)
# urlpatterns+=router.urls

from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('orders', views.OrderViewSet)

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view()),
    path("products/info/", views.ProductInfoAPIView.as_view()),
    path("products/<int:product_id>/", views.ProductDetailAPIView.as_view(), name='product-detail'),
    path("user-orders/", views.UserOrderListAPIView.as_view(), name='user-orders'),
    path("users/", views.UserListView.as_view()),
]

urlpatterns += router.urls