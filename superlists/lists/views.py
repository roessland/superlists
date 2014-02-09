from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

def home_page(request):
    return render(request, "lists/home.html")

def view_list(request):
    items = Item.objects.all()
    return render(request, "lists/list.html", {'items': items})

def new_list(request):
    if request.method == 'POST' and request.POST.get('item-text'):
        Item.objects.create(text=request.POST.get('item-text'))
    return redirect('/lists/the-only-list-in-the-world/')
