from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def items(request):
    return HttpResponse("This is items page you're seeing")