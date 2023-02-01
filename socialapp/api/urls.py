from . import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # path("",views.hello,name='hello'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts', views.PostsApi.as_view()),
    path('posts/<str:id>', views.PostsApi.as_view()),
    path('registration',views.RegistrationApi.as_view()),
]
