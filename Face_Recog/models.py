from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    face_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length = 40)
    phone = models.CharField(max_length =  10)
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    balance = models.IntegerField(default=1000)
    customerLocation = models.BooleanField(default=False)

    @staticmethod
    def getUserByID(ids):
        return UserProfile.objects.filter(face_id=ids)
    
    @staticmethod
    def getAllUsers():
        return UserProfile.objects.all()

    def __str__(self):
        return self.name