from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()
router.register('add', views.planesviewset)
router.register('addfeaters', views.plansfeatersviewset)
router.register('buy', views.bookingplansviewset)

urlpatterns = [
    path('', include(router.urls))
]