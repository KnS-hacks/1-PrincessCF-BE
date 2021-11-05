from django.db import models


class Member(models.Model):
    name = models.CharField(primary_key=True, max_length=10)
    team = models.CharField(max_length=10, null=True)
    tag = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name