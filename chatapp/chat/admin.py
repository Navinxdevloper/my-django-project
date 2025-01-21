from django.contrib import admin
from .models import YourModel
from .models import Message


admin.site.register(YourModel)
admin.site.register(Message)