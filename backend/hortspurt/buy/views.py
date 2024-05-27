from django.shortcuts import render

# Create your views here.

class BuyDataView(View):
    def get(self, request):
        return render(request, 'buy_data_input1.html')

    def post(self, request):
        return render(request, 'buy_data_input1.html')