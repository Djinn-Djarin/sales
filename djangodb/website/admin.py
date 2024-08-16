from django.contrib import admin
from .models import Member, Audit
# Register your models here.
admin.site.register(Member)
admin.site.register(Audit)