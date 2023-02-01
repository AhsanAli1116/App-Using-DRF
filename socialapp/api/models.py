from django.db import models
from django.contrib.auth.models import User


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


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country= models.CharField(max_length=50,blank=True,null=True)
    country_code = models.CharField(max_length=10,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    is_holiday = models.BooleanField()
    holiday = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.user.username