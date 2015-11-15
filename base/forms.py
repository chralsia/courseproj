from django import forms


class SearchForm(forms.Form):
    word = forms.CharField(max_length=50)


class ExpressionForm(forms.Form):
    expression = forms.CharField(max_length=150)
