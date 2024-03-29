from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profile
from django.contrib.auth.models import User
from .forms import UserCreationForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/registration.html')
    
    def post(self, request):
        new_user_form = UserCreationForm(request.POST)
        gender = request.POST.get('gender')[0]
        print(gender)
        if new_user_form.is_valid():
            new_user = new_user_form.save()
            new_profile_form = ProfileForm({'gender':gender})
            if new_profile_form.is_valid():
                new_profile = new_profile_form.save(commit=False)
                new_profile.user = new_user
                new_profile.save()
                print("b4 authentication")
                username = new_user.username
                password = request.POST.get("password1")
                user = authenticate(request, username=username, password=password)
                print("after auth")
                print(user)
                if user is not None:
                    print('logged in')
                    login(request, user)
                    
                    return redirect("/")
            else:
                print(new_profile_form.errors)
                new_user.delete()
                return render(request, 'registration/registration.html')
        else:
            print(new_user_form.errors)
            return render(request, 'registration/registration.html')

class LandingView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "homepage.html")
        return render(request, 'index.html')

class DataView(APIView):
    def get(self, request):
        return JsonResponse({'ok':'very ok'})

    def post(self, request):
        print(request.data)
        return JsonResponse({'ok':'very ok'})