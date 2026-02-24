from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item
from .forms import Itemform
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)
#@login_required
# @cache_page(60 * 10)
def index(request):
   #getting items from database
   logger.info("Fethcing all items from the database.")
   item_list = Item.objects.all()
   logger.debug(f"There are {item_list.count()} items.")
   paginator = Paginator(item_list, 5)
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)
   #creating context
   context={
       'page_obj':page_obj
   }
  # passing the context object to the render method along the template
   return render(request,"myapp/index.html",context)

def detail(request,id):
    
   #created a detailed veiw for each item
    logger.info(f"Fetching an item with id:{id}")
    logger.info(f"User {request.user} requested item from {request.META.get('REMOTE_ADDR')}")
    try:
        item = get_object_or_404(Item, pk=id)
        logger.debug(f"Item found {item.item_name}")
    except Exception as e:
        logger.error("Error whiule fetching item with %s: %s",id,e)
        raise

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
    return render(request, "myapp/item_form.html", context)

# def update_item(request,id):
#     item = Item.objects.get(id=id)
#     form = Itemform(request.POST or None, instance=item)
#     if form.is_valid():
#         form.save()
#         return redirect('myapp:index')
    # context ={
    #     'form':form
    # }
    # return render(request, "myapp/item-form.html", context)
    
# def delete_item(request, id):
#     item = Item.objects.get(id=id)
#     if request.method=="POST":
#         item.delete()
#         return redirect('myapp:index')
    
#     return render(request, "myapp/item-delete.html")

# class IndexClassView(ListView):
#     model=Item
#     template_name="myapp/index.html"
#     context_object_name="item_list"
    

# class FoodDetail(DetailView):
#     model=Item
#     template_name="myapp/detail.html"
#     context_object_name="item"

# class ItemCreateView(CreateView):
#     #item_form.html
#     model=Item
#     fields=['item_name', 'item_desc', 'item_price', 'item_image']
#     def form_valid(self, form):
#         form.instance.user_name = self.request.user
#         return super().form_valid(form)
    

class ItemUpdateView(UpdateView):
    model=Item
    fields=['item_name', 'item_desc', 'item_price', 'item_image']
    template_name_suffix='_update_form'
    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)
    
    
class DeleteItemView(DeleteView):
    model=Item
    success_url=reverse_lazy('myapp:index')


