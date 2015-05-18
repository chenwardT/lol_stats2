from django import forms


class SearchForm(forms.Form):
    # region = forms.CharField(label='Region')
    name = forms.CharField(label='Summoner', max_length=24)