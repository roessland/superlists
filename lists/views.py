from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request, "lists/home.html")

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, "lists/list.html", {'list': list_})

def new_list(request):
    if request.method == 'POST' and request.POST.get('item-text'):
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get('item-text'), list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item-text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))