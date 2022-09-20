from django import forms
from management.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'})
        }
        
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name','category','image']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'})
        }     

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','subcategory','brand','unitMeasurement','stock','image','description']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'subcategory':forms.Select(attrs={'class':'form-control'}),
            'brand':forms.Select(attrs={'class':'form-control'}),
            'unitMeasurement':forms.Select(attrs={'class':'form-control'}),
            'stock':forms.NumberInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'})            
        }

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name','phone','email']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }
        
class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields =['provider','payment']
        widgets = {
            'user':forms.Select(attrs={'class':'form-control'}),
            'payment':forms.Select(attrs={'class':'form-control'})
        }
        
class DetailBuyForm(forms.ModelForm):
    class Meta:
        model = DetailBuy
        fields = ['product','amount']
        widgets = {
            'product':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'})
        }
    
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields=['user','typeSale','payment','client','nDocument','address']
        widgets = {
            'user':forms.Select(attrs={'class':'form-control'}),
            'typeSale':forms.Select(attrs={'class':'form-control'}),
            'payment':forms.Select(attrs={'class':'form-control'}),
            'client':forms.TextInput(attrs={'class':'form-control'}),
            'nDocument':forms.NumberInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'})
        }
        
class DetailSaleForm(forms.ModelForm):
    class Meta:
        model = DetailSale
        fields =['product','amount']
        widgets = {
            'product':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'})
        }
     
class BackupForm(forms.ModelForm):
    class Meta:
        model = Backup
        fields = ['name','file']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'file':forms.FileInput(attrs={'class':'form-control'})
        }