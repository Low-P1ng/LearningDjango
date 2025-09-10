from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

# Create your views here.
def index(request):
    #getting items from database
    item_list = Item.objects.all()
    #creating context
    context={
        'item_list':item_list
    }
    # passing the context object to the render method along the template
    return render(request,"myapp/index.html",context)


def detail(request,id):
    #created a detailed veiw for each item
    item=Item.objects.get(id=id)
    context={
        'item':item
    }
    return render(request,"myapp/detail.html",context)