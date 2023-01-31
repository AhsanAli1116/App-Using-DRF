from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()


# Create your models here.
class Posts(models.Model): 
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50,null=False,blank=True)
    body = models.CharField(max_length=500,null=True,blank=True)
    date_published=models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blogpost_like',blank=True)

    def __str__(self):
        return self.title


class UserGeoDetail(models.Model):
    pass