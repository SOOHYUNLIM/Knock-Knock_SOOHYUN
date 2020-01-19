"""kk_admin URL Configuration

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
from django.urls import path
import kk.views as rest

urlpatterns = [
    path('', rest.index),
    path('charts', rest.charts),
    path('members', rest.members),

    # REST API
    path('visitant', rest.visitant),
    path('member', rest.member),
    path('pick', rest.pick),
    path('specialPrice', rest.specialPrice),
    path('category', rest.category),
    path('traffic', rest.traffic),
]
