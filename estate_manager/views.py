from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'admin/index.html')

def chat(request):
    return render(request, 'admin/chat.html')