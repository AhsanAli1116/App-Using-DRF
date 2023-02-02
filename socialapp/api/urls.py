from . import views
from django.urls import path



urlpatterns = [
    path('posts', views.PostsApi.as_view(),name='posts'),
    path('user',views.UserDetails.as_view(),name='userdetail'),

]
