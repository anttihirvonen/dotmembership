from django.shortcuts import render

from .forms import MemberForm


def index(request):
    """
    Index page of the member register.

    Renders a page which contains forms.
    """
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MemberForm()

    return render(request, 'index.html', {'member_form': form})


def join(request):
    """
    AJAX view for adding a new member to registry.
    """
    pass


def check_my_data(request):
    pass
