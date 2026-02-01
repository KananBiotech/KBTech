from django.db import models

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    state = models.CharField(max_length=30)
    farm_type = models.CharField(max_length=50)

    class Meta:
        ordering = ["created"]

class Sessions(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.UUIDField()
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["created_at"]