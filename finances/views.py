from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import ListView

from homis_core.models import Person

from models import Transaction
from forms import SimplePaymentForm, TransactionForm, TransactionItemForm, TransactionItemFormSet


class TransactionList(ListView):
    model = Transaction


def index(request, messages = None):
    if messages is None:
        messages = []

    print "MESSAGES: %r" % (messages, )

    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    transactions = Transaction.objects.order_by('-date')
    #template = loader.get_template('finances/index.html')
    #context = RequestContext(request, {
    #    'transaction_list': transactions,
    #     'last_transaction': Transaction.get_last(),
    #     'simple_payment_form': SimplePaymentForm(),
    #     'messages': messages,
    # })
    # return HttpResponse(template.render(context))

    return render(
        request,
        'finances/index.html',
        {
            'transaction_list': transactions,
            'last_transaction': Transaction.get_last(),
            'simple_payment_form': SimplePaymentForm(),
            'messages': messages,
        }
    )

    #return HttpResponse("Hello, world. You're at the polls index.")


def add_simple_payment(request):
    messages = []

    if request.method == "POST":
        form = SimplePaymentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Transaction.create_simple_payment(
                data["from_person"],
                data["to_person"],
                data["amount"],
                request.user,
                description = data["description"])
            messages.append("Transaction added.")
        else:
            messages.append("Invalid form.")
    else:
        form = SimplePaymentForm()

    transactions = Transaction.objects.order_by('-date')

    return render(
        request,
        'finances/index.html',
        {
            "messages": messages,
            'simple_payment_form': form,
            "transaction_list": transactions,
        }
    )


def person(request, person_id = None):
    if person_id is None:
        pass
    else:
        person_id = int(person_id)
        person = Person.objects.get(pk = person_id)
        transaction = Transaction.get_last()
        debts = transaction.get_debts(person)
        return render(
            request,
            'finances/person_detail.html',
            {
                'person': person,
                'debts': debts,
            }
        )


def transactions(request, transaction_id = None):
    if transaction_id is None:
        pass
    else:
        transaction = Transaction.objects.get(pk = transaction_id)

        return render(
            request,
            'finances/transaction_detail.html',
            {
                'transaction': transaction,
            }
        )


def add_transaction(request):
    messages = []

    if request.method == "POST":
        form = TransactionForm(request.POST)
        formset = TransactionItemFormSet(request.POST)

        if form.is_valid():
            items = []

            for item_form in formset:
                if not item_form.is_valid():
                    continue

                data = item_form.cleaned_data
                person = data.get("person", None)
                amount = data.get("amount", 0.0)
                weight = data.get("weight", 1.0)

                if person is None:
                    continue

                items.append((person, amount, weight))

            if len(items) > 0:
                Transaction.create_complex(
                    items,
                    request.user,
                    description = form.cleaned_data["description"],
                    )
                messages.append("Transaction added.")
                return index(request, messages = messages)
            else:
                messages.append("No transaction items specified.")
        else:
            messages.append("Form is not valid.")
    else:
        form = TransactionForm()
        formset = TransactionItemFormSet()

    return render(
        request,
        'finances/add_transaction.html',
        {
            "messages": messages,
            'form': form,
            'formset': formset,
        }
    )
