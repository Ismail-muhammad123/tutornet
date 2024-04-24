from django.db import models

# Create your models here.


class NewsLetterList(models.Model):
    email = models.EmailField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)


class ContactMessage(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self) -> str:
        return self.subject
