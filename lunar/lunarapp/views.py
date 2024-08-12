import base64
import hashlib
import hmac
import json
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import *
from django.contrib import messages
import requests

from decimal import Decimal

# Create your views here.

def home(request):
    product = Product.objects.filter(trending=1)
    #internship = Internship.objects.all()
    course = Course.objects.filter(trending=1)
    context = {
        'product' : product,
        'course' : course
    }
   
    return render(request, 'lunarapp/base.html', context)

def dashboard(request):
    return render(request, 'lunarapp/admin/dashboard.html', {})


def register(request):
    return render(request, 'lunarapp/register.html')        




def product_details(request, name):
    product = Product.objects.filter(name=name).first()
    if product:
        context = {
            'product': product
        }
        return render(request, 'lunarapp/product_details.html', context)
    
    else:
        messages.error('No Details of product found..')
        return redirect('home')


def course_details(request, name):
    courses = Course.objects.filter(name=name).first()
    if courses:
        context = {
            'courses': courses
        }
        return render(request, "lunarapp/course_details.html", context)
    else:
        messages.error('No Details of course found..')
        return redirect('home')




def BuyForm(request, course_id):
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        email = request.POST['email']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        country = request.POST['country']
        city = request.POST['city']
        phone = request.POST['phone']
       
        
        user, created = All_User.objects.get_or_create(
            email = email,
            defaults={ 'f_name' :f_name, 'l_name' :l_name, 'city' : city, 'country' : country, 'phone' : phone}
        )
        
        if not created:
            user.f_name = f_name
            user.l_name = l_name
            user.city = city
            user.country = country
            user.phone = phone
            user.save()
          
       
       # All_User.objects.create(email=email, f_name=f_name, l_name = l_name, city = city, country = country, phone = phone)
        
        # Redirect to the payment page with user_id and course_id as query parameters
        return redirect(reverse('payment') + f'?user_id={user.id}&course_id={course.id}')         #write this code without white spaces
    
    
                    #get_or_create:  
                    #     This method attempts to retrieve an existing All_User record from the database with the specified email.
                    # If a user with that email already exists, get_or_create retrieves that user and sets created = False.
                        
                    #     Parameters:
                    # email=email: This is the condition used to find the existing user.
                    # defaults={...}: If a new user needs to be created (i.e., the user doesn't already exist), the defaults dictionary provides the additional fields that should be used to populate the new record (f_name, l_name, city, country, phone).
    else:
        return render(request, 'lunarapp/BuyForms.html')
    
from uuid import uuid4


def payment(request):
    course_id = request.GET.get('course_id')
    user_id = request.GET.get('user_id')
    
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(All_User, id=user_id)
    
    uuid_val = uuid.uuid4()        # to create a unique value  
    
    course_price = Decimal(course.price)
    tax_rate = Decimal(0.13)
    
    tax_amount = course_price * tax_rate
    real_amount = course_price - tax_amount
    total_amount = real_amount + tax_amount
    
    
    #for esewa  {esewa}
    
    def genSha256(key, message):
        key = key.encode('utf-8')
        message = message.encode('utf-8')
        
        hmac_sha256 = hmac.new(key, message, hashlib.sha256)
        digest = hmac_sha256.digest()
        signature = base64.b64encode(digest).decode('utf-8')
        return signature

    secret_key = "8gBm/:&EnhH.1/q"
    
    data_to_sign = f"total_amount={total_amount:.2f}&transaction_uuid={uuid_val}&product_code=EPAYTEST"
    
    # Debug prints
    #print(f"Data to Sign: {data_to_sign}")
    
    signature = genSha256(secret_key, data_to_sign)
    
    #print(f"Generated Signature: {signature}")
    
    
    #{esewa}
    
    context = {
        'course': course,
        'user': user,
        'uuid_val': uuid_val,     #esewa
        'tax_amount': tax_amount,
        'real_amount': real_amount,
        'total_amount': total_amount,
        'signature': signature    #esewa
    }
    
    return render(request, 'lunarapp/payment.html', context)




def esewaMainPage(request):
    return render(request, 'lunarapp/esewa/mainPage.html')


# # Send confirmation email to the user
#  


def initiateKhalti(request):
    
    
    

    url = "https://a.khalti.com/api/v2/epayment/initiate/"    #testing phase url
    
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": name,
        "email": email,
        "phone": phone
        }
    })
    headers = {
        'Authorization': 'key 0180c8b019bd466a9df7dbec8e7a8ec7',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    new_res = json.loads(response.text)
    print(new_res)
    # print('uuid', purchase_order_id)
    # print('return_url', return_url)
    return redirect(new_res['payment_url'])

def verifyKhalti(request):
    
    url = "https://a.khalti.com/api/v2/epayment/lookup/" 
    
    
    if request.method == 'GET':
        headers = {
            'Authorization': 'key 0180c8b019bd466a9df7dbec8e7a8ec7',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
    
        payload = json.dumps({
            'pidx' : pidx
        })
    
        response = requests.request("POST", url, headers=headers, data=payload)
    
        #print(response.text)
        new_res = json.loads(response.text)
        print(new_res)
        
        if new_res['status'] == 'Completed':
            
            #Updating the values in the database of course payment
            payment = get_object_or_404(CoursePayment,pidx=pidx)  
            
            payment.status = 'COMPLETED'
            payment.payment_method = 'KHALTI'
            payment.save()
            
            
            user = payment.user    #user refers to the name inside the CoursePayment
            course = payment.course
            
            user.is_Student = True
            user.save()
            
            course.course_purchased = True
            course.save()
            print(f"Payment completed by {user.f_name} for course {course.name}")
            return render(request, 'lunarapp/esewa/dashboard.html', {'user': user, 'course': course})
            
            
            # i want to fetch the user and course for the payment applied
            
    return render(request, 'lunarapp/esewa/payment_success.html')
