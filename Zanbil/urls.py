"""Zanbil URL Configuration

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

from API.Authentication import AuthentiationController
from API.Business import BusinessController
from API.Service import ServiceController,SearchController
from API.Category import CategoryController
from API.Review import ReviewController
from API.AccountPage import AccountPageController
from API.Reserve import ReserveController
from API.Uploader import ImageUploader
from API.Dashboard import DashboardController
from API.views import TEST
from API.Cancellation import CancellationController

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',AuthentiationController.as_view()),
    path('api/business/',BusinessController.as_view()),
    path('api/service/', ServiceController.as_view()),
    path('api/service/search/',SearchController.as_view()),
    path('api/category/', CategoryController.as_view()),
    path('api/service/review/',ReviewController.as_view()),
    path('api/user/',AccountPageController.as_view()),
    path('api/dashboard/',DashboardController.as_view()),
    path('api/service/reserve/',ReserveController.as_view()),
    path('api/file/picture/',ImageUploader.as_view()),
    path('api/cancellation/',CancellationController.as_view()),
    path('test/',TEST.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
