from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    pass

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name
