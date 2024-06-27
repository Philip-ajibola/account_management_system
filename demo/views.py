from django.shortcuts import render, HttpResponse


# Create your views here.

def say_hello(request):
    return HttpResponse("Hello, Welcome to django")


def welcome(request, name):
    #return HttpResponse(f"welcome {name}")
    return render(request, 'index.html',{"name":name})
