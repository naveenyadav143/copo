from django.db import models

class PO(models.Model):
    number = models.CharField(max_length=10)  
    description = models.TextField()

    def __str__(self):
        return self.number

class Course(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

class CO(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)  # e.g., CO1
    description = models.TextField()
    max_score = models.FloatField(default=100)

    def __str__(self):
        return f"{self.course.code} - {self.number}"

class COPOMapping(models.Model):
    co = models.ForeignKey(CO, on_delete=models.CASCADE)
    po = models.ForeignKey(PO, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])

class COAttainment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    co = models.ForeignKey('CO', on_delete=models.CASCADE)
    level_avg = models.FloatField(default=0)  # Store average level (1–3)

    def __str__(self):
        return f"{self.course.code} - {self.co.number} | Level Avg: {self.level_avg}"

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

class StudentMark(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    co = models.ForeignKey(CO, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    obtained_marks = models.FloatField()
    total_marks = models.FloatField()

    def attainment_percentage(self):
        if self.total_marks == 0:
            return 0
        return round((self.obtained_marks / self.total_marks) * 100, 2)

    def __str__(self):
        return f"{self.student.roll_number} - {self.co.number}: {self.obtained_marks}/{self.total_marks}"
