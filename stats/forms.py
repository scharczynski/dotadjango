from django import forms

class IdForm(forms.Form):
    steam_id1 = forms.CharField(label='steam id', max_length=100)
    steam_id2 = forms.CharField(label='steam id', max_length=100)
    steam_id3 = forms.CharField(label='steam id', max_length=100)
    steam_id4 = forms.CharField(label='steam id', max_length=100)
    steam_id5 = forms.CharField(label='steam id', max_length=100)