from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()
router.register('list', views.USERViewset)
urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path("change_password/", views.ChangePasswordViewset.as_view(), name="changePassword"),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]