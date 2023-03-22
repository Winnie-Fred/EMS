from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'estate-manager/index.html')

def chat(request):
    return render(request, 'estate-manager/chat.html')