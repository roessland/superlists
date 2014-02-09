from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

def home_page(request):
    if request.method == 'POST' and request.POST.get('item-text'):
        Item.objects.create(text=request.POST.get('item-text'))
        return redirect('/')

    return render(request, "lists/home.html", {
        'items': Item.objects.all()    
    })
