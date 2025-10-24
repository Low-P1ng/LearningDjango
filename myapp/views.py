from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item
from .forms import Itemform
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

def create_item(request):
    form= Itemform(request.POST or None)
    
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
    
    #using the form here to render veiw
    context = {
        'form':form
    }
    return render(request, "myapp/item-form.html", context)

def update_item(request,id):
    item = Item.objects.get(id=id)
    form = Itemform(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('myapp:index')
        
    context ={
        'form':form
    }
    return render(request, "myapp/item-form.html", context)

def delete_item(request, id):
    item = Item.objects.get(id=id)
    if request.method=="POST":
        item.delete()
        return redirect('myapp:index')
    
    return render(request, "myapp/item-delete.html")