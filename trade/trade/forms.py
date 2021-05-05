from django import forms

class Quantity_buy(forms.Form):
    quantity_buy = forms.FloatField()

class Sell_Price(forms.Form):
    value0 = forms.CharField()
    value1 = forms.CharField()
    value2 = forms.CharField()
    value3 = forms.CharField()
    value4 = forms.CharField()
    value5 = forms.CharField()
 