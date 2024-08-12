import datetime
import os
from uuid import uuid4
from django.db import models
from phone_field import PhoneField

def image_file_dir(instance, filename):
    original_filename = filename
    time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = time + original_filename  
    
    if isinstance(instance, Course):
        folder_name = 'courses'
    elif isinstance(instance, Internship):
        folder_name = 'internships'
        
    elif isinstance(instance, Product):
        folder_name = 'product'        
    else:
        folder_name = 'other'                
    return os.path.join(f'image_upload/{folder_name}', filename)  


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=image_file_dir)
    duration = models.IntegerField()
    category = models.CharField(max_length=100, help_text= ' Category of the course (e.g., Programming, Design)')
    instructor = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True , help_text='Whether the course is currently active')
    trending = models.BooleanField(default=False, help_text='0= default, 1= trending')
    course_purchased = models.BooleanField(default=False, help_text='If the user has made the payment of the course')
    
    
    def __str__(self):
        return self.name
    
class Internship(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField() 
    available = models.BooleanField(default=True)
    experience = models.CharField(max_length=100)
    start_date = models.DateField(blank=True)
    duration = models.IntegerField()
    type = models.CharField(max_length=50, choices=[('FT', 'Full-Time'), ('PT', 'Part-Time')])
    image = models.ImageField(upload_to=image_file_dir)
    trending = models.BooleanField(default=False, help_text='0= default, 1= trending')
    
    def __str__(self):
        return self.name    


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField( max_digits=10, decimal_places= 2)
    image = models.ImageField(upload_to=image_file_dir)
    category = models.CharField(max_length=100, help_text='Category of the product(for e.g web, app)')
    available = models.BooleanField(default=True, help_text='Whether the product is available for purchase')
    created_at = models.DateTimeField()
    trending = models.BooleanField(default=False, help_text='0= default, 1= trending')
    
    def __str__(self):
        return self.name 


class All_User(models.Model):
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    phone = PhoneField(help_text='Contact phone number')
    is_Intern = models.BooleanField(default=False, help_text="If the user is intern or not")
    is_Student = models.BooleanField(default=False, help_text="If the user is student or not")
    is_Staff = models.BooleanField(default=False, help_text="If the user is staff or not")
    
    def __str__(self):
        return self.email
    
    
class CoursePayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('FAILED', 'FAILED'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'CREDIT_CARD'),
        ('PAYPAL', 'PAYPAL'),
        ('ESEWA', 'ESEWA'),
        ('KHALTI', 'KHALTI'),
       
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(All_User, on_delete=models.CASCADE)  
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING') 
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=200, unique=True, default=uuid4)
    pidx = models.CharField(max_length=255, unique=True)
    
    
    
    def __str__(self):
        return f'{self.user.f_name} - {self.course.name} - {self.amount} ({self.status})'
    
    # def save(self, *args, **kwargs):
    #     if not self.transaction_id:
    #         self.transaction_id = generate_unique_transaction_id()
    #     super().save(*args, **kwargs)    
    

    
    


        
    
    
    
    