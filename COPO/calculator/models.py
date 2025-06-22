from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Cos(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class Pos(models.Model):
    name = models.CharField(max_length=100)
    cos = models.ForeignKey(Cos, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class CO(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)  # e.g. "CO1"
    description = models.TextField()

    def __str__(self):
        return f"{self.course.course_code} {self.number}: {self.description[:30]}"

class PO(models.Model):
    number = models.CharField(max_length=10, unique=True)  # e.g. "PO1"
    description = models.TextField()

    def __str__(self):
        return f"{self.number}: {self.description[:30]}"

class COPOMapping(models.Model):
    co = models.ForeignKey(CO, on_delete=models.CASCADE)
    po = models.ForeignKey(PO, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])

    def __str__(self):
        return f"{self.co} → {self.po} (Level {self.level})"

class COAttainment(models.Model):
    co = models.OneToOneField(CO, on_delete=models.CASCADE)
    attainment_percentage = models.FloatField()

    def __str__(self):
        return f"{self.co}: {self.attainment_percentage}%"