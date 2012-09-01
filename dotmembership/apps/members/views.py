from django.shortcuts import render

def index(request):
    """
    Index page of the member register.

    Renders a page which contains forms.
    """
    return render(request, 'index.html')

def join(request):
    """
    AJAX view for adding a new member to registry.
    """
    pass

def check_my_data(request):
    pass
