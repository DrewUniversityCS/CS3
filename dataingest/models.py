from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True)
    phone = models.CharField(max_length=150,unique=True)
    profile = models.TextField()
    message = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'