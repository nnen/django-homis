from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import ListView

from models import Transaction


class TransactionList(ListView):
    model = Transaction


def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    transactions = Transaction.objects.order_by('-date')
    template = loader.get_template('finances/index.html')
    context = RequestContext(request, {
        'transaction_list': transactions,
        'last_transaction': transactions[0],
    })
    return HttpResponse(template.render(context))

    #return HttpResponse("Hello, world. You're at the polls index.")

