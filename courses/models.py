from distutils.command.upload import upload
from pydoc import describe
from queue import Empty
from turtle import title
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    cover_photo = models.ImageField(upload_to="course_categories")
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    slug = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(default="")
    tutor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses",  limit_choices_to={"tutor": True})
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='courses')
    cover_photo = models.ImageField(upload_to="courses")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules")
    added_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class SupportDocument(models.Model):
    type = models.CharField(max_length=200)
    file = models.FileField(upload_to="course_support_docs")
    added_at = models.DateTimeField(auto_now_add=True)


class Enrolement(models.Model):
    enroled_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrolements")
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enrolements")


class Certifications(models.Model):
    pass
