from pydoc import describe
from turtle import title
from django.db import models



class Topic(models.Model):
    name = models.CharField(max_length=200)
    cover_photo = models.ImageField()


class Course(models.Model):
    title = models.CharField(max_length=100)
    tutor = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name="courses")
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='courses')
    cover_photo = models.ImageField()


class Modules(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Enrolement(models.Model):
    pass
