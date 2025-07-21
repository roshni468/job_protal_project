from django.contrib import admin
from users_auth_app.models import CustomUserModel, PendingAcountModel

# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(PendingAcountModel)
