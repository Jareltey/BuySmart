from django.shortcuts import render
from . import models, forms
from django_pivot.pivot import pivot
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template
from django.contrib.auth.decorators import login_required

# Create your views here.

def Index(request):
    return render(request,'basic_app/base.html')

class EntryList(ListView):

    model = models.Entry
    ordering = ['mall','product_category','product','shop_name','shop_address','price']

class CreateEntry(CreateView):

    model = models.Entry
    fields = ('mall','product','product_category','shop_name','shop_address','price')

class UpdateEntry(UpdateView):

    model = models.Entry
    fields = ('mall','product','product_category','shop_name','shop_address','price')

class DeleteEntry(DeleteView):

    model = models.Entry
    success_url = reverse_lazy('entry_list')

# @login_required(redirect_field_name='mall_list')
def MallList(request):
    entries = models.Entry.objects.all()

    used = []
    for entry in entries:
        if entry.mall not in used:
            used.append(entry.mall)

    all_malls_pro_cats = []

    for mall in used:
        mall_entries = models.Entry.objects.filter(mall=mall)
        mall_pro_cats = []
        for entry in mall_entries:
            if entry.product_category not in mall_pro_cats:
                mall_pro_cats.append(entry.product_category)

        all_malls_pro_cats.append(mall_pro_cats)


    return render(request,'basic_app/mall_list.html',{'used':used,'all_malls_pro_cats':all_malls_pro_cats})

def ProcatList(request,mall):
    entries = models.Entry.objects.filter(mall=mall)

    used = []
    unique = []
    for entry in entries:
        if entry.product_category not in used:
            unique.append(entry)
            used.append(entry.product_category)

    pivot_tables = []
    unique_list = []
    num_list = []
    i = 0

    shop_address_dict = {}

    for product_category in used:
        pivot_table = pivot(models.Entry.objects.filter(mall=mall,product_category=product_category),'shop_name','product','price')
        entries = models.Entry.objects.filter(mall=mall,product_category=product_category)

        unique_entries = []
        for entry in entries:
            if entry.product not in unique_entries:
                unique_entries.append(entry.product)

        for entry in entries:
            if entry.shop_name not in shop_address_dict and entry.shop_address != None:
                shop_address_dict.update({entry.shop_name:entry.shop_address})


        pivot_tables.append(pivot_table)
        unique_list.append(unique_entries)
        num_list.append(i)
        i = i+1

    return render(request,'basic_app/pro_cat_list.html',{'used':used,'unique':unique,'pivot_tables':pivot_tables,'unique_list':unique_list,'num_list':num_list,'mall':mall,'shop_address_dict':shop_address_dict})

def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('mall_list'))
            else:
                return HttpResponse('User not active')

        else:
            return HttpResponse('Invalid login credentials!')

    else:
        form = forms.UserForm()

    return render(request,'basic_app/login.html',{'form':form})

def Logout(request):

    logout(request)
    entries = models.Entry.objects.all()

    used = []
    unique = []
    for entry in entries:
        if entry.mall not in used:
            unique.append(entry)
            used.append(entry.mall)

    return HttpResponseRedirect(reverse('mall_list'))
