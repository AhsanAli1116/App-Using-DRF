from . import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts', views.PostsApi.as_view(),name='posts'),
    path('posts/<str:id>', views.PostsApi.as_view(),name='posts'),
    path('registration',views.RegistrationApi.as_view(),name='registration'),
    path('user/<str:id>',views.UserDetails.as_view(),name='userdetail'),

]
