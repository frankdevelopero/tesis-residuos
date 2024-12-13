from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import logout, authenticate, login as django_login
from users.forms import LoginForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')

        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        error_message = []
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is None:
                error_message.append("Correo electrónico o contraseña incorrecta")
            else:
                if user.is_active:
                    django_login(request, user)
                    next_url = request.GET.get('next', '')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('dashboard')
                else:
                    error_message.append("¡Oops!. El usuario está bloqueado, ponte en contacto.")

        context = {
            'errors': error_message,
            'form': form
        }
        return render(request, 'users/login.html', context)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')