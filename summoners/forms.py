from django import forms


class SearchForm(forms.Form):
    # region = forms.CharField(label='Region')
    name = forms.CharField(label='Summoner', max_length=24)
    region = forms.ChoiceField(label='Region', choices=(
        ('BR', 'BR'),
        ('EUNE', 'EUNE'),
        ('EUW', 'EUW'),
        ('KR', 'KR'),
        ('LAN', 'LAN'),
        ('LAS', 'LAS'),
        ('NA', 'NA'),
        ('OCE', 'OCE'),
        ('RU', 'RU'),
        ('TR', 'TR'),
    ))
