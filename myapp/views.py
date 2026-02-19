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


#@login_required
# @cache_page(60 * 10)
def index(request):
   #getting items from database
   item_list = Item.objects.all()
   paginator = Paginator(item_list, 5)
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)
   #creating context
   context={
       'page_obj':page_obj
   }
  # passing the context object to the render method along the template
   return render(request,"myapp/index.html",context)

#def detail(request,id):
#    #created a detailed veiw for each item
#    item=Item.objects.get(id=id)
#    context={
#        'item':item
#    }
#    return render(request,"myapp/detail.html",context)

# def create_item(request):
#     form= Itemform(request.POST or None)
    
#     if request.method=="POST":
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:index')
    
#     #using the form here to render veiw
#     context = {
#         'form':form
#     }
#     return render(request, "myapp/item-form.html", context)

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
    

class FoodDetail(DetailView):
    model=Item
    template_name="myapp/detail.html"
    context_object_name="item"

class ItemCreateView(CreateView):
    #item_form.html
    model=Item
    fields=['item_name', 'item_desc', 'item_price', 'item_image']
    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)
    

class ItemUpdateView(UpdateView):
    model=Item
    fields=['item_name', 'item_desc', 'item_price', 'item_image']
    template_name_suffix='_update_form'
    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)
    
    
class DeleteItemView(DeleteView):
    model=Item
    success_url=reverse_lazy('myapp:index')


