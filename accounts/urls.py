from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='prod'),
    path('customers/<str:cust_id>/', customers, name='cust'),
    path('create_order/', createOrder, name="create_order") ,
    path('update_order/<str:pk>/', updateOrder, name='update_order'),   
    path('delete_order/<str:pk>/', deleteOrder, name='delete_order'),   
    path('update_customer/<str:cust_pk>/', updateCustomer, name='update_customer'),  
    path('register/', registerPage, name='register'), 
    path('login/', loginPage, name='login'), 
    path('logout/', logoutUser, name='logout'), 
    path('user/', userView , name= 'user'),
    path('account/', accountSetting, name= 'account'),
    path('reset_password' , auth_views.PasswordResetView.as_view() , name = "reset_password"),
    path('reset_password_sent' , auth_views.PasswordResetDoneView.as_view() , name = "password_reset_done"),
    path('reset/<uidb64>/<token>' , auth_views.PasswordResetConfirmView.as_view() , name= "password_reset_confirm"),
    #uidb64: users id encoded in base 64 ; token: to check that the password is valid
    path('reset_password_complete' , auth_views.PasswordResetCompleteView.as_view() , name = "password_reset_complete"),

    
]


'''Notes:
1. Submit email form                      // PasswordResetView.as_view()  
2. Email sent success form                // PasswordResetDoneView.as_view()
3. Link to password reset form in email   // PasswordResetConfirmView.as_view()
4. Password successfully changed message  // PasswordResetCompleteView.as_view()'''