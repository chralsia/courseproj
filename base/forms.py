from django import forms


class SearchForm(forms.Form):
    word = forms.CharField(max_length=50)


class ExpressionForm(forms.Form):
    expression = forms.CharField(max_length=150)
    from_ = forms.IntegerField(min_value=-100, max_value=100, required=False)
    to_ = forms.IntegerField(min_value=-100, max_value=100, required=False)
