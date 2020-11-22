"""ProjectX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from register.views import homepage
from searchapp.views import search_page,results_page,error_page
from compareapp.views import compare_page
urlpatterns = [
	path('admin/', admin.site.urls),
	path('',homepage),
	path('search/',search_page,name='search'),
	path('results/',results_page,name='results'),
	path('error/',error_page,name='error'),
    path('compare/',compare_page,name='compare'),
]

