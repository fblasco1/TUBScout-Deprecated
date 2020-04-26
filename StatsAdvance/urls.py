"""StatsAdvance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from apps.usuario.views import LoginView, RegisterView
from .views import LandingPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LandingPage.as_view(),name='landingpage'), #LandingPage
    path('tfb/', include(('apps.tfb.urls','tfb'))), #urls.py tfb
    path('usuario/', include(('apps.usuario.urls','usuario'))), #urls.py usuario
    path('usuarios/', include(('apps.usuario.passwords.urls','passwords'))), #urls.py contraseñas
    path('login', LoginView.as_view(),name='login'), 
    path('logout',LogoutView.as_view(),name='logout'),
    path('registro',RegisterView.as_view(),name='registro'),
]
