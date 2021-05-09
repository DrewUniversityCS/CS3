from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class BaseUser(AbstractUser):
    first_name = CharField(null=True, blank=True, max_length=100)
    last_name = CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        if self.email == "":
            return self.username
        else:
            return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def natural_key(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
