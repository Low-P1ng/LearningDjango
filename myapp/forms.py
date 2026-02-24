from django import forms
from .models import Item

class Itemform(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name','item_desc','item_price','item_image']
        widgets = {
            "item_name":forms.TextInput(attrs={"placeholder":"Cheese Burger","required":True}),
            "item_desc":forms.TextInput(attrs={"placeholder":"Savoury and cheesy","required":True}),
            "item_price":forms.NumberInput(attrs={"placeholder":"10.99","required":True}),
            "item_imb":forms.URLInput(attrs={"placeholder":"https://something","required":False}),
        }
        
    def clean_item_price(self):
        price = self.cleaned_data["item_price"]
        if price < 0:
            raise forms.ValidationError("Price can not be negative.")
        return price
    
    def clean(self):
        cleaned = super().clean()
        name = cleaned.get("item_name")
        desc = cleaned.get("item_desc")
        if desc.lower() in name.lower():
            raise forms.ValidationError("The desc can not be just name of an item, add more info.")
        return cleaned