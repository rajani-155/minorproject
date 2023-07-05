from django.db import models



class Student(models.Model):

    FACCHOICES=(
        ('01','Civil'),
        ('02','Computer'),
        ('03','Electrical'),
        ('04','Mechanical')
    )

    std_id=models.CharField(max_length=5,unique=True,blank=False)
    first_name=models.CharField(max_length=30,blank=False)
    middle_name=models.CharField(max_length=30,blank=True)
    last_name=models.CharField(max_length=30,blank=False)
    faculty=models.CharField(max_length=10,choices=FACCHOICES,blank=False)
    phone=models.CharField(max_length=10,blank=False)
    address=models.CharField(max_length=50,blank=False)
    email=models.CharField(max_length=100,blank=False)

    def __str__(self):
        return f"{self.std_id}"


class Attendence(models.Model):
    std_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    time=models.CharField(max_length=30,blank=False)
    date=models.CharField(max_length=30,blank=False)

    def __str__(self):
        return f"{self.std_id}"
