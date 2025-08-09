from django import forms 
from .models import ProductModel, OrdersModel

# class product for admin only
class ProductForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter the products name'}))
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=ProductModel.ProductStatus.choices)
    quantity = forms.IntegerField()
    price = forms.IntegerField()
    class Meta:
        model = ProductModel
        fields = [
            'name',
            'status',
            'quantity',
            'price',
        ]
        
    
    
    
# orders form for worker

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrdersModel
        fields = ['product_name', 'quantity']
        widgets = {
            'product_name': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    
    
    
    
     