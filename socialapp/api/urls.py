from . import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # path("",views.hello,name='hello'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts', views.AllPosts.as_view()),
    path('posts/<str:id>', views.AllPosts.as_view()),

]
