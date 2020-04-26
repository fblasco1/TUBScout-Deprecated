from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from .mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm, RegisterForm,ReactivateEmailForm, UserDetailChangeForm
from .models import EmailActivation
from .signals import user_logged_in

class HomeView(LoginRequiredMixin, DetailView):
    template_name = 'tfb/home.html'
    def get_object(self):
        return self.request.usuario

class AccountEmailActivateView(FormMixin, View):
    success_url = reverse_lazy('login')
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmacion()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Su email ha sido confirmado. Por favor inicie sesión")
                return redirect('usuario/login.html')
            else:
                activated_qs = qs.filter(activado=True)
                if activated_qs.exists():
                    reset_link = reverse_lazy('passwords:password_reset')
                    msg = """Su email ya ha sido confirmado
                    usted necesita  <a href="{link}">restaurar su contraseña</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('login') 
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/error_activación_email.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """El link de activación ha sido enviado. Por favor revise su correo"""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        usuario = obj.usuario 
        new_activation = EmailActivation.objects.create(usuario, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/error_activación_email.html', context)

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = 'tfb/'
    template_name = 'usuario/login.html'
    default_next = 'tfb/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'usuario/registro.html'

    def get_success_url(self):
        return reverse_lazy('login')
    

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'usuario/actualizar_usuario.html'

    def get_object(self):
        return self.request.usuario

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Actualizar Usuario'
        return context

    def get_success_url(self):
        return reverse_lazy("tfb")
