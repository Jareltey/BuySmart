"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from basic_app import views

urlpatterns = [
    path('',views.MallList,name='mall_list'),
    path('mall/<mall>/',views.ProcatList,name='pro_cat_list'),
    path('entry_list/',views.EntryList.as_view(),name='entry_list'),
    # path('create/',views.CreateEntry.as_view(),name='create'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('admin/',admin.site.urls),
    path('basic_app/',include('basic_app.urls')),
    # path('mall_list/<mall>/<product_category>',views.PriceListing,name='price_listing'),
    # path('entry_update/<int:pk>/',views.UpdateEntry.as_view(),name='update'),
    path('delete/<int:pk>/',views.DeleteEntry.as_view(),name='delete'),
    path('create/',views.CreateEntryView.as_view(),name='create'),
    path('update/',views.UpdateEntryView.as_view(),name='update'),
]
