from . import views
from django.urls import path



urlpatterns = [
    path('posts', views.PostsApi.as_view(),name='posts'),
    path('user/<str:id>',views.UserDetails.as_view(),name='userdetail'),

]
