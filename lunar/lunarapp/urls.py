from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('product_details/<str:name>', views.product_details, name='product_details'),
    path('course_details/ <str:name>', views.course_details, name='course_details'),
    path('register/', views.register, name='register'),
    path('BuyForm/<int:course_id>/', views.BuyForm, name='BuyForm'),
    path('payment/', views.payment ,name= 'payment'),
    path('esewaMainPage/', views.esewaMainPage, name= 'esewaMainPage'),
    
    
    #khalti url
    path('initiate/', views.initiateKhalti, name= 'initiate'),
    path('verify/', views.verifyKhalti, name= 'verify'),

    
    
    #path('login/', views.login, name='login'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)