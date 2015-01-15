from django import forms

from finances.models import Person


class SimplePaymentForm(forms.Form):
	from_person = forms.ModelChoiceField(label = "From", queryset = Person.objects.all())
	to_person = forms.ModelChoiceField(label = "To", queryset = Person.objects.all())
	amount = forms.FloatField(label = "Amount")
	description = forms.CharField(min_length = 0, required = False)
