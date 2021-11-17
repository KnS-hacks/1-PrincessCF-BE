from django.db import models


class HashTag(models.Model):
    name = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.name


class MBTI(models.Model):
    name = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.name


class Participate(models.Model):
    name = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.name


class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    school = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=10)
    introduce = models.CharField(null=True, blank=True, max_length=1000)
    motto = models.CharField(null=True, blank=True, max_length=1000)
    team = models.IntegerField(null=True)
    participate = models.ManyToManyField(Participate, blank=True)
    interest = models.ManyToManyField(Interest, blank=True)
    mbti = models.ManyToManyField(MBTI, blank=True)
    hashtag = models.ManyToManyField(HashTag, blank=True)
    github = models.URLField(blank=True, null=True, max_length=100)
    instagram = models.URLField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['team']