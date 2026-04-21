from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),  # default page
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
]