from django.shortcuts import render
from . import models, forms
from django_pivot.pivot import pivot
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template
from django.contrib.auth.decorators import login_required
from funky_sheets.formsets import HotView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def Index(request):
    return render(request,'basic_app/base.html')

class EntryList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Entry
    ordering = ['mall','product_category','product','shop_name','shop_address','price']

class CreateEntryView(LoginRequiredMixin,HotView):
    login_url = '/login/'
    model = models.Entry
    template_name = 'basic_app/create_form.html'
    prefix = 'table'
    success_url = reverse_lazy('update')
    fields = ('mall','product_category','product','shop_name','shop_address','price')
    hot_settings = {
    'contextMenu':'true',
    'autoWrapRow':'true',
    'rowHeaders':'true',
    'contextMenu':'true',
    'search':'true',
    'licenseKey':'non-commercial-and-evaluation',
    }
    ordering = ['mall','product_category','product','shop_name','shop_address','price']

class UpdateEntryView(CreateEntryView):
    template_name = 'basic_app/update_form.html'
    action = 'update'
    button_text = 'Update'

# class CreateEntry(CreateView):
#
#     model = models.Entry
#     fields = ('mall','product','product_category','shop_name','shop_address','price')
#
# class UpdateEntry(UpdateView):
#
#     model = models.Entry
#     fields = ('mall','product','product_category','shop_name','shop_address','price')
#

class DeleteEntry(LoginRequiredMixin,DeleteView):

    login_url = '/login/'
    model = models.Entry
    success_url = reverse_lazy('entry_list')

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

    entry_dates = []
    for entry in entries:
        entry_dates.append(entry.created_at)
        entry_dates.append(entry.updated_at)

    latest_update = max(entry_dates)
    print(latest_update)

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
                unique_entries.sort()

        for entry in entries:
            if entry.shop_name not in shop_address_dict and entry.shop_address != None:
                shop_address_dict.update({entry.shop_name:entry.shop_address})


        pivot_tables.append(pivot_table)
        unique_list.append(unique_entries)
        num_list.append(i)
        i = i+1

    return render(request,'basic_app/pro_cat_list.html',{'used':used,'unique':unique,'pivot_tables':pivot_tables,'unique_list':unique_list,'num_list':num_list,'mall':mall,'shop_address_dict':shop_address_dict,'latest_update':latest_update})

def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                try:
                    if request.GET['next'] == '/create/':
                        return HttpResponseRedirect(reverse('create'))
                    elif request.GET['next'] == '/update/':
                        return HttpResponseRedirect(reverse('update'))
                    elif request.GET['next'] == '/entry_list/':
                        return HttpResponseRedirect(reverse('entry_list'))
                    elif request.GET['next'].split('/')[1] == 'delete':
                        return HttpResponseRedirect(reverse('delete',kwargs={'pk':request.GET['next'].split('/')[2]}))
                except:
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
