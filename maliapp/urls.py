from django.urls import path,include

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('api/profile',ProfileViewSet)
router.register('api/user', UserViewSet)
router.register('api/post', PostViewSet)


urlpatterns = [
    path('users/', RegistrationAPIView.as_view(),name='RegistrationAPIView'),
    path('users/login/', LoginAPIView.as_view(),name='LoginAPIView'),
    path('User/', UserRetrieveUpdateAPIView.as_view(),name='UserRetrieveUpdateAPIView'),
    path('',include(router.urls))
    
]
