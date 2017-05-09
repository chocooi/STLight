from django import forms

class NameForm(forms.Form):
    posX = forms.FloatField(label = 'Type Position X')
    posY = forms.FloatField(label = 'Type Position Y')
    flag = forms.CharField(label = 'Type flag')
    luminous = forms.IntegerField(label = 'Type light')
    location = forms.CharField(label = 'Type location')
    code = forms.CharField(label = 'Type code')
    ltAuto = forms.IntegerField(label = 'Type ltAuto')
    zone = forms.CharField(label = 'Type zone')
    cell = forms.CharField(label = 'Type cell')

class AddressForm(forms.Form):
    address = forms.CharField()

class SearchForm(forms.Form):
    searchZone = forms.CharField(label = 'Type zone')
    searchCell = forms.CharField(label = 'Type cell')
    searchLoc = forms.CharField(label = 'Type location')
