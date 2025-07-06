"""Recommendationsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index
##from . import UserDashboard
##from . import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #index page content start
    path('index', index.index),
    path('about',index.about),
    path('user_registration',index.user_registration),
    path('submit_user_registration_details', index.submit_user_registration_details),
    path('user_login',index.user_login),
    path('submit_user_login_details',index.submit_user_login_details),
    path('admin_login',index.admin_login),
    path('submit_admin_login',index.submit_admin_login),
    #index page content end

    #user dashboard content start
    path('upload_moresignature_by_admin',index.upload_moresignature_by_admin),
    path('viewusers',index.view_users),
    path('user_dashboard',index.user_dashboard),
    path('upload_signature', index.upload_signature, name='upload_signature'),
    path('verify_signature', index.verify_signature, name='verify_signature'),
    path('user_logout', index.user_logout, name='user_logout'),
    
    #user dashboard content end

    #admin dashboard content start
    path('admin_dashboard', index.admin_dashboard, name='admin_dashboard'),
    path('upload_signature_by_admin', index.upload_signature_by_admin, name='upload_signature_by_admin'),
    path('view_signature', index.view_signature, name='view_signature'),
    path('delete_signature/<int:signature_id>/', index.delete_signature, name='delete_signature'),
    path('admin_logout', index.admin_logout,name='admin_logout'),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

