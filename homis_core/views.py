from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate

from homis_core.forms import LogInForm
from homis_core.models import Person, MessageList


def index(request, messages = None):
    messages = MessageList.make(messages)

    return render(
        request,
        'homis_core/base.html',
        {
            "messages": messages,
        }
    )


def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username = data["username"],
                password = data["password"])
            if user is None:
                messages = ["Incorrect username or password.", ]
            else:
                login(request, user)
                messages = ["Logged in as " + data["username"] + ".", ]
        else:
            messages = ["Log in form invalid.", ]
    else:
        return index(request)
    return index(request, messages)


def log_out(request):
    logout(request)
    messages = ["User logged out."]
    return index(request, messages)


def people(request):
    return render(
        request,
        "homis_core/person_list.html",
        {
            'person_list': Person.objects.all(),
        }
    )
