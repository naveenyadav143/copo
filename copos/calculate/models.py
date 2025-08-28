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

# StudentMark removed — per-CO storage disabled. Use StudentTotal for aggregated per-student totals.
class StudentMark(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    co = models.ForeignKey(CO, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    obtained_marks = models.FloatField()
    total_marks = models.FloatField()
    attainment_level = models.IntegerField(default=1, choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')])

    def attainment_percentage(self):
        if self.total_marks == 0:
            return 0
        return round((self.obtained_marks / self.total_marks) * 100, 2)
    
    def calculate_attainment_level(self):
        """Calculate attainment level based on percentage"""
        percentage = self.attainment_percentage()
        if percentage > 70:
            return 3
        elif percentage > 50:
            return 2
        else:
            return 1

    def __str__(self):
        return f"{self.student.roll_number} - {self.co.number}: {self.obtained_marks}/{self.total_marks} (Level: {self.attainment_level})"


class StudentTotal(models.Model):
    """Stores summed CO marks for a student within a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_obtained = models.FloatField(default=0)
    total_max = models.FloatField(default=0)

    class Meta:
        unique_together = ('course', 'student')

    def attainment_percentage(self):
        if self.total_max == 0:
            return 0
        return round((self.total_obtained / self.total_max) * 100, 2)

    def __str__(self):
        return f"{self.student.roll_number} - Total: {self.total_obtained}/{self.total_max}"


class COAggregateScore(models.Model):
    """Stores the sum of scores for each CO across all students in a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    co = models.ForeignKey(CO, on_delete=models.CASCADE)
    total_obtained_marks = models.FloatField(default=0)
    total_max_marks = models.FloatField(default=0)
    student_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('course', 'co')

    def average_score(self):
        if self.student_count == 0:
            return 0
        return round(self.total_obtained_marks / self.student_count, 2)

    def attainment_percentage(self):
        if self.total_max_marks == 0:
            return 0
        return round((self.total_obtained_marks / self.total_max_marks) * 100, 2)

    def __str__(self):
        return f"{self.course.code} - {self.co.number}: {self.total_obtained_marks}/{self.total_max_marks} ({self.student_count} students)"


class POAttainment(models.Model):
    """Stores PO attainment scores for each course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    po = models.ForeignKey(PO, on_delete=models.CASCADE)
    attainment_score = models.FloatField(default=0)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'po')

    def __str__(self):
        return f"{self.course.code} - {self.po.number}: {self.attainment_score}"
