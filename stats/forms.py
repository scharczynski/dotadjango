from django import forms

class IdForm(forms.Form):
    steam_id = forms.CharField(label='steam id', max_length=100)