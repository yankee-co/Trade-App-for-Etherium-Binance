from django.db import models

class UserData(models.Model):
    nickname = models.CharField(max_length=66)
    api_key = models.CharField(max_length=66)
    secret_key = models.CharField(max_length=66)

    def __str__(self) -> str:
        return self.nickname
