"""
URL configuration for crowfunding_app_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from crowfunding import views

router = routers.DefaultRouter()
router.register(r'entrepreneur', views.EntrepreneurViewSet, basename='entrepreneur')
router.register(r'project', views.ProjectViewSet, basename='project')
router.register(r'investor', views.InvestorViewSet, basename='investor')
router.register(r'transaction', views.TransactionViesSets)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('invest/<int:project_id>/<int:investor_id>/', views.InvestInProject.as_view(), name='invest_in_project'),
]
