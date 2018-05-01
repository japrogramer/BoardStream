from django.contrib import admin
from .models import Panel, Comments



class PanelAdmin(admin.ModelAdmin):
    pass


class CommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Panel, PanelAdmin)
admin.site.register(Comments, CommentsAdmin)
