from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('product', views.productViewSet)
router.register('buy', views.buyproductViewSet)
urlpatterns = [
    path('', include(router.urls))
]