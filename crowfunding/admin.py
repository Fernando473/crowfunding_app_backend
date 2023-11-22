from django.contrib import admin
from .models import Entrepreneur, Project, Investor, Transaction

# Register your models here.

admin.site.register(Entrepreneur)
admin.site.register(Project)
admin.site.register(Investor)
admin.site.register(Transaction)
