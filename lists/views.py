from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Item, List
from .forms import ItemForm

def home_page(request):
    return render(request, "lists/home.html", {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, "lists/list.html", {'list': list_, 'error': error, 'form': ItemForm()})

def new_list(request):
    list_ = List.objects.create()
    try:
        Item.objects.create(text=request.POST.get('text'), list=list_)
    except ValidationError:
        error_text = "You can't have an empty list item"
        return render(request, "lists/home.html", {'error': error_text, 'form': ItemForm()})
    return redirect(list_)
