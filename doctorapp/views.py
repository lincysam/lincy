from django.shortcuts import render

# Create your views here.
def login(request):
    
    return render(request,'home.html')
    #return render(request,'homepage.html')


