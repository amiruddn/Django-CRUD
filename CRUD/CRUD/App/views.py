from django.shortcuts import render, redirect
from App.models import Product
from django.http import HttpResponseRedirect

#home
def home(request):
    all_product = Product.objects.all().order_by('Created_date')
    return render(request, 'home.html', {"products":all_product})

#add product
def add_product(request):
    if request.method == "POST":
        if request.POST.get('product') \
            and request.POST.get('Purchase') \
            and request.POST.get('Quantity') \
            and request.POST.get('Sale') \
            and request.POST.get('Gender') \
            or request.POST.get('Note'):
            product = Product()
            product.product = request.POST.get('product')
            product.Purchase = request.POST.get('Purchase')
            product.Quantity = request.POST.get('Quantity')
            product.Sale = request.POST.get('Sale')
            product.Gender = request.POST.get('Gender')
            product.Note = request.POST.get('Note')
            product.save()
            return HttpResponseRedirect('/')
        else:
            return redirect('home')
    else:
            return render(request, 'add.html')

#view product
def product(request, product_id):
    product = Product.objects.get(id = product_id)
    if product != None:
        return render(request, 'edit.html', {'product':product})

#edit product
def edit_product(request):
    if request.method=="POST":
        product = Product.objects.get(id = request.POST.get('id'))
        if product != None:
            product.product = request.POST.get('product')
            product.Purchase = request.POST.get('Purchase')
            product.Quantity = request.POST.get('Quantity')
            product.Sale = request.POST.get('Sale')
            product.Gender = request.POST.get('Gender')
            product.Note = request.POST.get('Note')
            product.save()
            return HttpResponseRedirect('/')

#delete product
def delete_product(request, product_id):
    product = Product.objects.get(id = product_id)
    product.delete()
    return HttpResponseRedirect('/')
