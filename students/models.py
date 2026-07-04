from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    email = models.EmailField()

    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name