from django.urls import path, re_path

from .views import (
        HomeView, 
        AccountEmailActivateView,
        UserDetailUpdateView
        )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('act_usuario', UserDetailUpdateView.as_view(), name='act_usuario'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', 
            AccountEmailActivateView.as_view(), 
            name='email-activate'),
    path('email/resend-activation/', 
            AccountEmailActivateView.as_view(), 
            name='resend-activation'),
]