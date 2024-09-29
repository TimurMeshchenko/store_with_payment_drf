"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from store_app.views import CatalogView, BasketView, get_product, \
    get_products_by_search, get_products_page

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('basket', BasketView.as_view(), name='basket'),
    path('api/get_products_page', get_products_page, name='get_products_page'),
    path('api/get_product', get_product, name='get_product'),
    path('api/get_products_by_search', get_products_by_search, name='get_products_by_search'),
]
