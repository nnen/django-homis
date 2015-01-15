from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import ListView

from models import Transaction, Person
from forms import SimplePaymentForm


class TransactionList(ListView):
    model = Transaction


def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    transactions = Transaction.objects.order_by('-date')
    template = loader.get_template('finances/index.html')
    context = RequestContext(request, {
        'transaction_list': transactions,
        'last_transaction': transactions[0],
        'simple_payment_form': SimplePaymentForm(),
    })
    return HttpResponse(template.render(context))

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

