from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profile
from django.contrib.auth.models import User
from .forms import UserCreationForm, ProfileForm, RegisterForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.views.generic.edit import UpdateView 
from transactions.models import AddMoneyTransaction
from buy.models import BuyAirtimeData
from django.db.models import Q
from itertools import chain
# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/registration.html')
    
    def post(self, request):
        new_user_form = RegisterForm(request.POST)

        if new_user_form.is_valid():
            gender = request.POST.get('gender')[0]
            new_profile_form = ProfileForm({'gender':gender})
            if new_profile_form.is_valid():
                new_user = new_user_form.save()
                new_profile = new_profile_form.save(commit=False)
                new_profile.user = new_user
                new_profile.save()
                username = new_user.username
                password = request.POST.get("password1")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    return render(request, 'registration/registration.html')
            else:
                print(new_profile_form.errors)
                return render(request, 'registration/registration.html')
        else:
            print(new_user_form.errors)
            return render(request, 'registration/registration.html')

class LandingView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "homepage.html")
        return render(request, 'index.html')

class DataView(LoginRequiredMixin, APIView):
    def get(self, request):
        return JsonResponse({'ok':'very ok'})

    def post(self, request):
        print(request.data)
        return JsonResponse({'ok':'very ok'})

class ComingSoonView(View):
    def get(self, request):
        return render(request, 'error404.html')

class ShoutOutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shoutout.html')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'editProfile.html')
    
    def post(self, request):
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/my-profile/')
        else:
            print(form.errors)
            return render(request, 'editProfile.html')


class SupportView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'let_us_know.html')
    
    def post(self, request):
        return render(request, 'we_know.html')

class HistoryView(LoginRequiredMixin, View):
    def get(self, request):
        # Combine transactions into a single queryset
        add_moneytr = AddMoneyTransaction.objects.filter(user=request.user)
        airtime_datatr = BuyAirtimeData.objects.filter(Q(buyer=request.user) | Q(receiver=request.user))
        if add_moneytr or airtime_datatr:
            transactions = sorted(chain(add_moneytr, airtime_datatr), key=lambda feedobj: feedobj.updated_at, reverse=True)
        else:
            transactions = []
        transactions_by_date = {}
        for transaction in transactions:
            transaction_date = transaction.updated_at.date()  # Extract date from updated_at
            if transaction_date not in transactions_by_date:
                transactions_by_date[transaction_date] = []
            transactions_by_date[transaction_date].append(transaction)

        ctx = {'transactions': transactions_by_date}
        print(ctx)
        return render(request, 'history.html', ctx)


class TransactionDetailView(LoginRequiredMixin, View):
    def get(self, request, trid):
        category =  trid[:3]
        transaction_id = trid[3:]
        print(category, transaction_id)
        if (category == 'ADM'):
            tr_obj = AddMoneyTransaction.objects.get(id=transaction_id)
            if not tr_obj:
                return render(request, 'error404.html')
            if tr_obj.user != request.user:
                msg = 'You do not have access to this resource'
                return HttpResponse(msg, status=403, content_type="text/html")

        elif (category == 'ADT'):
            tr_obj = BuyAirtimeData.objects.get(id=transaction_id)
            if not tr_obj:
                return render(request, 'error404.html')
            if tr_obj.buyer != request.user and tr_obj.receiver != request.user:
                msg = 'You do not have access to this resource'
                return HttpResponse(msg, status=403, content_type="text/html")

        ctx = {'transaction': tr_obj}
        return render(request, 'transaction_detail.html', ctx)
