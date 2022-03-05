from django.contrib import admin
# Register your models here.
from arikeapp.models import Myuser


admin.sites.site.register(Myuser)
