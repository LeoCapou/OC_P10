from django.contrib import admin
from ManageAPI.models import Contributors, Projects, Comments , Issues

admin.site.register(Contributors)
admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Comments)