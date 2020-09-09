from django.contrib import admin
from .models import User, Writing, ScrapList

admin.site.register(User)
admin.site.register(Writing)
admin.site.register(ScrapList)