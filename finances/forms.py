from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

from finances.models import Person, Transaction, TransactionItem


class SimplePaymentForm(forms.Form):
	from_person = forms.ModelChoiceField(label = "From", queryset = Person.objects.all())
	to_person = forms.ModelChoiceField(label = "To", queryset = Person.objects.all())
	amount = forms.FloatField(label = "Amount")
	description = forms.CharField(min_length = 0, required = False)


class TransactionItemForm(forms.Form):
    person = forms.ModelChoiceField(
        label = "Person",
        queryset = Person.objects.all(),
        required = True)
    amount = forms.FloatField(label = "Amount", initial = 0.0)
    weight = forms.FloatField(label = "Weight", initial = 1.0)


TransactionItemFormSet = formset_factory(
    TransactionItemForm,
    extra = 10)


class TransactionForm(forms.Form):
    description = forms.CharField(min_length = 0, required = False, widget = forms.Textarea)

