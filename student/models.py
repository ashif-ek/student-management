from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    
    def __str__(self):
        return self.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year_of_admission = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Allow many-to-many with Course through Enrollment model
    courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} -> {self.course}"
