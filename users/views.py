from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from users.forms import UserRegisterForm

# Create your views here.
def profile(request):
    return render(request, 'registration/profile.html')

class Register(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})