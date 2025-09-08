from django import forms 



class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"search your course here ..."}))