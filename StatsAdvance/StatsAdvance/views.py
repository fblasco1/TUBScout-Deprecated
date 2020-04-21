from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class LandingPage(TemplateView):
    template_name = 'index.html'