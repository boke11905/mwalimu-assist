from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator

class Teacher(AbstractUser):
    contact=models.CharField(max_length=15,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "



class Stream(models.Model):
    stream_name=models.CharField(max_length=60)
    grade=models.CharField(max_length=2)

    def __str__(self):
        return f"{self.stream_name} {self.grade}"

    
class Subject(models.Model):
    subject_name=models.CharField(max_length=30 ,unique=True)
    subject_code=models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    

class Student(models.Model):
    class Gender_choices(models.TextChoices):
        Male='M','Male'
        Female='F','Female'
        Other='O','other'
        rather_not_say='R','rather_not_say'
    Admission_number=models.CharField(max_length=30,unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    gender=models.CharField(max_length=1,choices=Gender_choices.choices
                            ,default=Gender_choices.rather_not_say)
    subjects=models.ManyToManyField(Subject,blank=True,related_name='learners')
    stream=models.ForeignKey(Stream,on_delete=models.SET_NULL,null=True,blank=True,related_name='students')

    def __str__(self):
        return f"{self.Admission_number} {self.first_name} {self.last_name}"


class Marks(models.Model):
    class TermChoices(models.TextChoices):
        Term1='term1','Term1'
        Term2='term2','Term2'
        Term3='term3','Term3'

    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='students')
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subjects')
    score=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    exam_term=models.CharField(max_length=20,choices=TermChoices.choices,default=TermChoices.Term1)
    date_recorded=models.DateField(auto_now_add=True)

    class Meta:
        unique_together=('student','subject','exam_term')
        verbose_name_plural='Marks'

    def __str__(self):
        return f"{self.student} {self.subject} {self.score} {self.exam_term}"


