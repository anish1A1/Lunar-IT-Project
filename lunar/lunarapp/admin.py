from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Course)
admin.site.register(Internship)
admin.site.register(Product)