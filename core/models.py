from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Grade(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    
    def __str__(self):
        return f"{self.name} (Grade {self.grade.name})"

class Class(models.Model):
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='classes')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  limit_choices_to={'user_type': 'teacher'}, 
                                  related_name='supervised_classes')
    academic_year = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.name} - Grade {self.grade.name} ({self.academic_year})"
    
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    qualification = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.DateField()
    
    def __str__(self):
        return self.user.get_full_name()

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    occupation = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.get_full_name()

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, 
                              related_name='children')
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, 
                                    related_name='students')
    admission_date = models.DateField()
    admission_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"
    
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                              limit_choices_to={'user_type': 'teacher'}, 
                              related_name='lessons')
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='lessons')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} - {self.student_class.name}"